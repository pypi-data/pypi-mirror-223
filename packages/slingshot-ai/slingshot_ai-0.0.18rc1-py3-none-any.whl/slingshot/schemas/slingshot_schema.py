from __future__ import annotations

import json
from abc import ABC
from pathlib import Path
from typing import Any, Literal, Optional, Union

import deepdiff
import pydantic
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from rich.console import Console
from typing_extensions import Annotated

from slingshot import schemas
from slingshot.sdk.errors import SlingshotDeprecationException, SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.shared.utils import (
    get_default_num_gpu,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

REPO = "https://github.com/slingshot-ai/slingshot"
PATH_TO_FILE = "slingshot_client/src/slingshot/schemas"
FILENAME = "slingshot-schema.config.json"
FILE_LOCATION = "/".join([REPO, "blob/main", PATH_TO_FILE, FILENAME])
PATH_FIELD = Field(..., title="Path", description="The path to mount into the environment.", pattern=r'/mnt/\w+')
MODE_FIELD = Field(..., title="Mode", description="The mode to use for the mount.")
ALPHANUMERIC_UNDERSCORE_HYPHEN_RE = "^[A-Za-z][A-Za-z0-9_-]*$"  # This should match the regex on the backend

console: Console = Console()  # TODO is this okay to use here?


class BaseMountSpec(BaseModel):
    mode: str = Field(..., title="Mode", description="The mode to use for the mount.")
    path: str = Field(..., title="Path", description="The path to mount into the environment.", pattern=r'/mnt/\w+')

    def diff(self, other: BaseMountSpec) -> list[str]:
        what_changed = []
        if self.mode != other.mode:
            what_changed.append(f"mode: {other.mode} → {self.mode}")
        if self.path != other.path:
            what_changed.append(f"path: {other.path} → {self.path}")
        return what_changed


class DownloadByNameMountSpec(BaseMountSpec):
    mode: Literal["DOWNLOAD"] = Field("DOWNLOAD", title="Mode", description="The mode to use for the mount.")
    name: str = Field(
        ..., title="Name", description="The name of the asset to mount. Either name or tag should be set, but not both."
    )

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, DownloadByNameMountSpec) and self.name != other.name:
            d.append(f"name: {other.name} → {self.name}")
        elif isinstance(other, DownloadByTagMountSpec):
            d.append(f"replaced tag='{other.tag}' → name='{self.name}'")
        return d


class DownloadByTagMountSpec(BaseMountSpec):
    mode: Literal["DOWNLOAD"] = Field("DOWNLOAD", title="Mode", description="The mode to use for the mount.")
    tag: str = Field(
        ...,
        title="Tag",
        description="The artifact selector. If multiple matching artifacts contain the tag, the "
        "latest one will be used.  Either name or tag should be set, but not both.",
    )

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, DownloadByTagMountSpec) and self.tag != other.tag:
            d.append(f"tag: {other.tag} → {self.tag}")
        elif isinstance(other, DownloadByNameMountSpec):
            d.append(f"replaced name='{other.name}' → tag='{self.tag}'")
        return d


class UploadMountSpec(BaseMountSpec):
    mode: Literal["UPLOAD"] = Field("UPLOAD", title="Mode", description="The mode to use for the mount.")
    tag: Optional[str] = Field(None, title="Tag", description="Optional tag to attach to the written asset.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, UploadMountSpec) and self.tag != other.tag:
            d.append(f"tag: {other.tag} → {self.tag}")
        return d


class VolumeMountSpec(BaseMountSpec):
    mode: Literal["VOLUME"] = Field("VOLUME", title="Mode", description="The mode to use for the mount.")
    name: str = Field(..., title="Name", description="The name of the volume to mount.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, VolumeMountSpec) and self.name != other.name:
            d.append(f"name: {other.name} → {self.name}")
        return d


MountSpecUnion = Union[DownloadByNameMountSpec, DownloadByTagMountSpec, UploadMountSpec, VolumeMountSpec]


def mount_spec_from_remote(mount_spec: fragments.MountSpec) -> MountSpecUnion:
    return TypeAdapter(MountSpecUnion).validate_python(mount_spec.model_dump())


def diff_mount_spec(new: MountSpecUnion, existing: fragments.MountSpec) -> list[str]:
    """Returns a list of differences between a local and a remote mount spec."""
    return new.diff(mount_spec_from_remote(existing))


class EnvironmentSpec(BaseModel):
    python_version: Union[
        Literal["3.10"],
        Annotated[
            float,
            Field(
                # Literal 3.10
                ge=3.10,
                le=3.10,
            ),
        ],
    ] = Field("3.10", title="Python version")
    python_packages: list[str] = Field(
        default_factory=list,
        title="Python packages",
        description=f"List of Python packages to install in the environment.",
    )
    post_install_command: str = Field(
        "",
        title="Post-install command",
        description="Custom command to run after all packages have been installed. Skipped if not specified.",
    )
    apt_packages: list[str] = Field(
        default_factory=list, title="APT packages", description=f"List of APT packages to install"
    )
    model_config = ConfigDict(
        title="Environment",
        json_schema_extra={
            "example": {"python_version": "3.10", "python_packages": ["numpy", "pandas", "torch==2.0.1"]}
        },
    )

    # All python packages can be converted to RequestedRequirement
    @classmethod
    @field_validator("python_packages")
    def convert_python_packages(cls, v: list[str]) -> list[str]:
        for i in v:
            try:
                schemas.RequestedRequirement.from_str(i)
            except ValueError as e:
                raise ValueError(f"Error occurred while trying to parse python packages") from e
        return v

    def diff(self, existing: fragments.ExecutionEnvironmentSpec) -> list[str]:
        """Returns a list of differences between this and another environment spec."""
        diff = []
        current_python_packages = [schemas.RequestedRequirement.from_str(pkg) for pkg in self.python_packages]
        current_apt_packages = [schemas.RequestedAptPackage(name=pkg) for pkg in self.apt_packages]
        assert existing.environment_instances, "Environment spec has no instances"
        existing_env_instance = existing.environment_instances[0]
        existing_python_packages = TypeAdapter(list[schemas.RequestedRequirement]).validate_python(
            existing_env_instance.requested_python_requirements
        )
        existing_apt_packages = TypeAdapter(list[schemas.RequestedAptPackage]).validate_python(
            existing_env_instance.requested_apt_packages
        )
        existing_post_install_command = existing_env_instance.post_install_command

        if existing_post_install_command != self.post_install_command:
            existing_post_install_command_repr = existing_post_install_command.replace("\n", "\\n")
            new_post_install_command_repr = self.post_install_command.replace("\n", "\\n")
            diff.append(f"Post-install command: {existing_post_install_command_repr} → {new_post_install_command_repr}")

        python_package_diffs = self._diff_python_requirements(current_python_packages, existing_python_packages)
        if python_package_diffs:
            diff.append(f"Python packages changed")
            diff.extend(python_package_diffs)

        apt_package_diffs = self._diff_apt_packages(current_apt_packages, existing_apt_packages)
        if apt_package_diffs:
            diff.append(f"APT packages changed")
            diff.extend(apt_package_diffs)

        return diff

    @staticmethod
    def _diff_python_requirements(
        current: list[schemas.RequestedRequirement], existing: list[schemas.RequestedRequirement]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {str(req)}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {str(req)}")
        return diff

    @staticmethod
    def _diff_apt_packages(
        current: list[schemas.RequestedAptPackage], existing: list[schemas.RequestedAptPackage]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {req.name}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {req.name}")
        return diff


class SlingshotAbstractAppSpec(BaseModel, ABC):
    name: str = Field(..., title="Name", description="The name of the app.", pattern=ALPHANUMERIC_UNDERSCORE_HYPHEN_RE)
    environment: str = Field(..., title="Environment", description="The name of the execution environment.")
    machine_type: schemas.MachineType = Field(
        schemas.MachineType.CPU_SMALL, title="Machine size", description="The machine size to be used."
    )
    num_gpu: int = Field(0, title="Number of GPUs", description="The number of GPUs to use.")
    config_variables: dict[str, Any] = Field(
        default_factory=dict, title="Arguments", description="Optional user defined arguments to pass to the app."
    )

    mounts: list[MountSpecUnion] = Field(default_factory=list, title="Mounts", description="The mounts to be attached.")
    attach_project_credentials: bool = Field(
        True,
        title="Attach project credentials",
        description=(
            "If true, will make an API key available to instances under the `SLINGSHOT_API_KEY` environment"
            "variable so that they can make requests using the Slingshot SDK for this project"
        ),
    )
    model_config = ConfigDict(
        title="App", json_schema_extra={"example": {"cmd": "python app.py", "environment": "slackbot"}}
    )

    @classmethod
    @field_validator("mounts")
    def validate_mount_paths_unique(cls, v: list[MountSpecUnion]) -> list[MountSpecUnion]:
        """
        Verify that all download mount paths are unique, and all upload mount paths are unique.
        However, it should be possible for download and upload mounts to share the same mount path.
        """
        download_paths = [str(spec.path) for spec in v if spec.mode == "DOWNLOAD"]
        if len(download_paths) != len(set(download_paths)):
            raise ValueError("All download mount paths must be unique.")

        upload_paths = [str(spec.path) for spec in v if spec.mode == "UPLOAD"]
        if len(upload_paths) != len(set(upload_paths)):
            raise ValueError("All upload mount paths must be unique.")

        return v

    @classmethod
    @field_validator("num_gpu", mode="after")
    def validate_num_gpu(cls, v: int | None, info: FieldValidationInfo) -> int:
        """Validate that the number of GPUs is valid based on machine_type."""
        machine_type: schemas.MachineType = info.data["machine_type"]
        v = v or get_default_num_gpu(machine_type)
        try:
            machine_type_gpu_count_to_machine_size(gpu_count=v, machine_type=machine_type)
        except ValueError as e:
            raise ValueError(f"Invalid number of GPUs ({v}) for machine type {machine_type}") from e
        return v

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        diff = []
        name = existing.app_spec_name
        environment = existing.execution_environment_spec.execution_environment_spec_name
        config_variables = json.loads(existing.config_variables) if existing.config_variables else {}

        existing_machine_type, existing_num_gpu = machine_size_to_machine_type_gpu_count(existing.machine_size)
        self_machine_type = self.machine_type
        self_num_gpu = self.num_gpu

        if self.name != name:
            diff.append(f"Name changed from '{name}' → '{self.name}'")
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if deepdiff.DeepDiff(config_variables, self.config_variables, ignore_order=True):
            diff.append(f'Config variables changed from {config_variables} → {self.config_variables}')
        if self_machine_type != existing_machine_type:
            diff.append(f"Machine type changed from '{existing_machine_type}' → '{self_machine_type}'")
        if self_num_gpu != existing_num_gpu:
            diff.append(f"Number of GPUs changed from '{existing_num_gpu}' → '{self_num_gpu}'")
        if self.attach_project_credentials and not existing.service_account:
            diff.append(f"Project credentials added")
        elif not self.attach_project_credentials and existing.service_account:
            diff.append(f"Project credentials removed")

        my_mount_path = {f"{i.mode}: {i.path}": i for i in self.mounts}
        existing_mounts = {f"{i.mode}: {i.path}": i for i in existing.mount_specs}
        added_keys = set(my_mount_path.keys()) - set(existing_mounts.keys())
        for i in added_keys:
            diff.append(f"Added mount '{i}'")
        removed_keys = set(existing_mounts.keys()) - set(my_mount_path.keys())
        for i in removed_keys:
            diff.append(f"Removed mount '{i}'")
        same_path = set(existing_mounts.keys()) & set(my_mount_path.keys())
        for i in same_path:
            existing = existing_mounts[i]
            new = my_mount_path[i]
            d = ",".join(diff_mount_spec(new, existing))
            if d:
                diff.append(f"Changed mount '{i}': {d}")

        return diff


class SlingshotCustomAppSpec(SlingshotAbstractAppSpec):
    port: Optional[int] = Field(None, title="Port", description="The port to expose.")
    cmd: str = Field(..., title="Command", description="The command to run.")

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.CUSTOM:
            raise ValueError(f"Cannot diff an app against a non-app.")
        diff = super().diff(existing)
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class SessionAppSpec(SlingshotAbstractAppSpec):
    using: Literal["session"] = Field(
        ...,
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    @property
    def port(self) -> int:
        return 8080

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.SESSION:
            raise ValueError(f"Cannot diff session app against a non-session.")
        diff = super().diff(existing)
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class RedisAppSpec(SlingshotAbstractAppSpec):
    using: Literal["redis"] = Field(
        ...,
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    @property
    def port(self) -> int:
        return 6379

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.REDIS:
            raise ValueError(f"Cannot diff redis app against a non-redis one.")
        diff = super().diff(existing)
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class RunSpec(SlingshotAbstractAppSpec):
    name: str = Field("run", title="Name", description="The name of the run.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    model_config = ConfigDict(
        title="Run", json_schema_extra={"example": {"cmd": "python train.py", "environment": "training"}}
    )

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.RUN:
            raise ValueError(f"Cannot diff a run against a non-run.")
        diff = super().diff(existing)
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        return diff


class DeploymentSpec(SlingshotAbstractAppSpec):
    name: str = Field("deployment", title="Name", description="The name of the deployment.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    model_config = ConfigDict(title="Deployment", json_schema_extra={"example": {"environment": "deployment"}})

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.DEPLOYMENT:
            raise ValueError(f"Cannot diff a run against a non-deployment.")
        diff = super().diff(existing)
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        return diff


class SlingshotValidationResult(BaseModel):
    warning: Optional[str] = Field(None, title="Warning", description="A warning message.")
    error: Optional[str] = Field(None, title="Error", description="An error message.")

    @classmethod
    def of_invalid_machine_type(cls, machine_type: str) -> "SlingshotValidationResult":
        return cls(
            error=(
                f"Machine type '{machine_type}' is not supported in slingshot.yaml (since version '0.0.10'). Hint: Use "
                "'slingshot machines' for machine options."
            )
        )

    def warning_or_raise(self) -> str:
        if self.error:
            raise SlingshotDeprecationException(self.error)

        assert self.warning, "No warning or error message found."
        return self.warning


class ProjectManifest(BaseModel):
    environments: dict[str, EnvironmentSpec] = Field(
        default_factory=dict, title="Environments", description="The environments to use for the job."
    )
    apps: list[Union[SlingshotCustomAppSpec, SessionAppSpec, RedisAppSpec]] = Field(
        default_factory=list, title=SlingshotAbstractAppSpec.model_config["title"]
    )
    runs: list[RunSpec] = Field(default_factory=list, title=RunSpec.model_config["title"])
    deployments: list[DeploymentSpec] = Field(default_factory=list, title=DeploymentSpec.model_config["title"])
    model_config = ConfigDict(
        title="Slingshot Config Spec",
        json_schema_extra={"$schema": "http://json-schema.org/draft/2020-12/schema", "$id": FILE_LOCATION},
    )

    @staticmethod
    def check_deprecations(v: dict[str, Any]) -> list[SlingshotValidationResult]:
        deprecations = []

        all_apps_runs_deployments = []
        all_apps_runs_deployments.extend(v.get("apps", []))
        all_apps_runs_deployments.extend(v.get("runs", []))
        all_apps_runs_deployments.extend(v.get("deployments", []))

        # Check old GPUs
        for app_run_deployment in all_apps_runs_deployments:
            app_run_deployment = (
                app_run_deployment.model_dump() if isinstance(app_run_deployment, BaseModel) else app_run_deployment
            )
            machine_type = ('machine_type' in app_run_deployment and app_run_deployment['machine_type']) or ""
            if machine_type in {"GPU", "GPU_A100"}:
                deprecations.append(SlingshotValidationResult.of_invalid_machine_type(machine_type))

        return deprecations

    # TODO: add typing for values and return type, split deprecation checks into a separate validator
    @classmethod
    @pydantic.model_validator(mode="before")
    def validate_environment_names(cls, info: FieldValidationInfo) -> dict[str, Any]:
        if deprecations := cls.check_deprecations(info.data):
            warnings = [deprecation.warning_or_raise() for deprecation in deprecations]
            warnings_fmt = "\n".join(warnings)
            console.print(f"[yellow]⚠️ Detected deprecated slingshot.yaml fields[/yellow]:\n{warnings_fmt}")

        # Validate that jupyter is in all session environments:
        sessions = [app for app in info.data.get("apps", []) if isinstance(app, SessionAppSpec)]
        envs: dict[str, EnvironmentSpec] = info.data.get("environments", {})

        if not isinstance(envs, dict):
            raise SlingshotException(f"'environments' must be a YAML mapping (was: {type(envs)})")

        session_envs = {
            env_name: env
            for env_name, env in envs.items()
            if any(session.environment == env_name for session in sessions)
        }
        for session_env_name, session_env in session_envs.items():
            requested_python_requirements = session_env.python_packages
            if not any("jupyterlab" in requirement for requirement in requested_python_requirements):
                raise SlingshotException(
                    f"'jupyterlab' was not found in the '{session_env_name}' environment. Please add it and try again."
                )

        # Validate that all referenced environments are in the environments list:
        for app_or_run_or_deployment in [
            *info.data.get("apps", []),
            *info.data.get("runs", []),
            *info.data.get("deployments", []),
        ]:
            app_ = (
                app_or_run_or_deployment.model_dump()
                if not isinstance(app_or_run_or_deployment, dict)
                else app_or_run_or_deployment
            )
            env = app_.get("environment", '')
            if env not in envs:
                raise SlingshotException(f"Environment '{env}' not found in 'environments' {list(envs.keys())}")
        return info.data


if __name__ == "__main__":
    with open(Path(PATH_TO_FILE) / FILENAME, "w") as f:
        json.dump(ProjectManifest.model_json_schema(), f, indent=2)
