from fastapi import APIRouter, Depends
from schemas import TaskBase, TaskData
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks

# Create a FastAPI subrouter
router = APIRouter(
    prefix='/data',
    tags=['Create task']
)

# To handle task creation post request
@router.post('/', response_model=TaskData,status_code=201,summary="Create task",description="This api url is called to create new task. This endpoint accepts job environment Id as a url parameter.",response_description="This url endpoint returns a dictions with two keys (currentTask and tasks). Where currentTask's value is the task just created and tasks value is a list of all tasks.")
def create_task(request: TaskBase, db: Session = Depends(get_db)):
    return db_tasks.create_task(db, request)
