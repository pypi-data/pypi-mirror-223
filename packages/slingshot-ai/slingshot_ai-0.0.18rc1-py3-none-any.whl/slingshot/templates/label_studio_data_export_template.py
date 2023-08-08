from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from typing import Optional

import label_studio_sdk
from dateutil import parser
from pydantic import BaseModel, Field

from slingshot.schemas import Annotation, ExampleModification, Result, Upsert
from slingshot.sdk import SlingshotSDK

LS_API_KEY = os.environ.get('LABEL_STUDIO_API_KEY')
LS_URL = os.environ.get('LABEL_STUDIO_URL')

# If you are performing classification, modify the list of classes here to match your use case
ALL_CLASSES: list[str] = []

# This is the tag of your existing Slingshot dataset that you want to upsert annotations into
DATASET_TAG = 'dataset'
UPSERT_FILENAME = 'dataset.jsonl'


# This is an example annotation object from Label Studio where the task type is classification and
# the classification result is stored in the `classification` field. You should modify this class
# to match the annotation object that you are exporting from your own use case.
class LabelStudioAnnotation(BaseModel):
    created_at: str
    updated_at: str
    classification: Optional[str] = None  # Missing if skipped
    image: Optional[str] = None
    text: Optional[str] = None
    example_id: str = Field(..., alias='exampleId')
    annotator: int


def get_label_studio_annotations(ls_client: label_studio_sdk.Client) -> dict[str, list[Annotation]]:
    users = ls_client.get_users()
    user_id_to_email = {user.id: user.email for user in users}

    project = ls_client.get_project(id=1)
    res = project.export_tasks(export_type='JSON_MIN')
    ls_annotations = [LabelStudioAnnotation.model_validate(annotation_obj) for annotation_obj in res]

    example_to_annotations: defaultdict[str, list[Annotation]] = defaultdict(list)
    for annotation in ls_annotations:
        if annotation.classification not in ALL_CLASSES:
            raise ValueError(f"Unknown class {annotation.classification}")
        new_annotation = Annotation(
            result=[
                Result(
                    task_type="classification",
                    value={**{c: False for c in ALL_CLASSES}, annotation.classification: True},
                )
            ],
            created_at=parser.parse(annotation.created_at),
            updated_at=parser.parse(annotation.created_at),
            annotator=user_id_to_email[annotation.annotator],
        )
        example_to_annotations[annotation.example_id].append(new_annotation)
    return example_to_annotations


def create_upsert_from_annotations(example_to_annotations: dict[str, list[Annotation]]) -> Upsert:
    modified_examples = []
    for example_id, new_annotations in example_to_annotations.items():
        modified_examples.append(ExampleModification(example_id=example_id, new_annotations=new_annotations))
    return Upsert(modified_examples=modified_examples)


async def main() -> None:
    """
    This script will export all annotations from Label Studio and upsert them into a Slingshot dataset artifact with the
    tag specified under `DATASET_TAG`.
    """
    ls_client = label_studio_sdk.Client(url=LS_URL, api_key=LS_API_KEY)
    ls_annotations = get_label_studio_annotations(ls_client)
    print(f"Found {len(ls_annotations)} examples with annotations in Label Studio")

    upsert = create_upsert_from_annotations(ls_annotations)
    print(f"Created upsert with {len(upsert.modified_examples)} modified examples")

    sdk = SlingshotSDK()
    await sdk.setup()
    await sdk.upsert_dataset_artifact(upsert, dataset_tag=DATASET_TAG)


if __name__ == "__main__":
    asyncio.run(main())
