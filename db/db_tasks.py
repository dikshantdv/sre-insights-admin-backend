from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import OperationalError
from schemas import TaskBase
from config.exceptions import is_valid_uuid, UUIDException

# Function to get all tasks


def get_all_tasks(db: Session):
    try:
        jobs = db.execute('select * from get_admin_job()').all()
        tasks = db.execute("select * from get_admin_task()").all()
    except OperationalError:
        raise HTTPException(status_code=500, detail='Database refused to connect')
    if not (jobs or tasks):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='failed to fetch lookup data')
    jobs = [{
        "value": data["name"],
        "label": data["name"],
        "key": data['job_id']
    } for data in jobs]
    return {"detail":"Data fetched successfully","jobs": jobs, "tasks": tasks}

# Function to get all environments for a job
def get_environment_list(db: Session, request: str):
    if not is_valid_uuid(request):
        raise UUIDException('Invalid UUID provided')
    try:
        environments = db.execute(
            f"select * from get_admin_environment('{request}')").all()
    except OperationalError:
        raise HTTPException(status_code=409, detail='Database refused to connect')
    if not environments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No environments linked with Job ID {request} found')
    environments = [{
        "value": data["name"],
        "label": data["name"],
        "key":data["job_environment_id"]
    } for data in environments]
    return {"environments": environments}

# Function to create a task


def create_task(db: Session, request: TaskBase):
    if not is_valid_uuid(request.job_environment_id):
        raise UUIDException('Invalid UUID provided')
    try:
        current_task = db.execute(
            f"select * from create_admin_task('{request.job_environment_id}')").all()
        db.commit()
        tasks = db.execute("select * from get_admin_task()").all()
    except OperationalError:
        raise HTTPException(
            status_code=409, detail='Database refused to connect')
    if not current_task:
        raise HTTPException(status_code=400, detail='Task creation failed')
    return {"detail":"Task created successfully" ,"currentTask": current_task, "tasks": tasks}
