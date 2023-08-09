from typing import List

from pydantic import BaseModel, FilePath, Field

from datazone.utils.types import PydanticObjectId


class Pipeline(BaseModel):
    id: PydanticObjectId
    path: FilePath


class Config(BaseModel):
    project_name: str
    project_id: PydanticObjectId
    pipelines: List[Pipeline] = Field(default_factory=list)
