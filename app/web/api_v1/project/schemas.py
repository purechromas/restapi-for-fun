from pydantic import BaseModel


class ProjectCreateIn(BaseModel):
    name: str
    description: str | None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "project_name",
                "description": "project_description",
            }
        }


class ProjectCreateOut(ProjectCreateIn):
    id: int
