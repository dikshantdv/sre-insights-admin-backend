from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from schemas import LookUpData, EnvironmentListData

# Create a FastAPI subrouter
router = APIRouter(
    prefix='/data',
)

# To handle lookup get request


@router.get('/', response_model=LookUpData,status_code=200,tags=["Lookup data"],summary="Get lookup data",description="This api url is called to get initial data of tasks and jobs list.",response_description="This url endpoint returns a dictionary with two keys(Tasks and Jobs) whose values are in the form of list.")
def get_lookup_data(db: Session = Depends(get_db)):
    return db_tasks.get_all_tasks(db)

# To handle environment list get request


@router.get('/{jobid}/environments', response_model=EnvironmentListData,status_code=200,tags=["Environment list"],summary="Get environment list",description="This api url is called to get list of environments which are related to a particular job. This endpoint accepts job Id as a url parameter.",response_description="This url endpoint returns a dictions with one key (environments) whose value is a list containing all the related environments.")
def get_environment_list(jobid: str, db: Session = Depends(get_db)):
    return db_tasks.get_environment_list(db, jobid)
