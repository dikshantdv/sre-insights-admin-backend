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


@router.get('/', response_model=LookUpData,status_code=200,tags=["Get lookup data"])
def get_tasks(db: Session = Depends(get_db)):
    return db_tasks.get_all_tasks(db)

# To handle environment list get request


@router.get('/{jobid}/environments', response_model=EnvironmentListData,status_code=200,tags=["Get environment list"])
def get_environment(jobid: str, db: Session = Depends(get_db)):
    return db_tasks.get_environment_list(db, jobid)
