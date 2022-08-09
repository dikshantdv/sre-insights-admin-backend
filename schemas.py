from pydantic import BaseModel
from typing import List

# Schema for the task creation request body


class TaskBase(BaseModel):
    job_environment_id: str

# Schema for lookup data


class LookUpData(BaseModel):
    jobs: List
    tasks: List

# Schema for environment list data


class EnvironmentListData(BaseModel):
    environments: List

# Schema for lookup data


class TaskData(BaseModel):
    currentTask: List
    tasks: List
