from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from router import tasks_get, tasks_post
from config.exceptions import UUIDException

tags_metadata = [
    {
        "name": "Lookup data",
        "description": "This api url can be used to get initial lookup data(Tasks and Jobs).",
    },
    {
        "name": "Environment list",
        "description": "This api url can be used to retrive the list of environment related to a particular job.",
    },
    {
        "name": "Create task",
        "description": "This api url can be used to create new task.",
    },
    {
        "name": "Health check",
        "description": "This api url can be used to get health status of our api.",
    }
]

# Create a FastAPI application
app = FastAPI(title="SRE Insights Admin", description="SRE Insights Admin can be used to track all the schedules tasks and there status of prgress with added and last modified dates.",version="1.5.0",openapi_tags=tags_metadata)

# Add CORS middleware
origins = ['http://app.sre-admin.sreinsights.com']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )

#  Add the routers
app.include_router(tasks_get.router)
app.include_router(tasks_post.router)

# health check

@app.get("/",tags=["Health check"])
def read_info():
    return {
        "version":"1.6.0",
        "port":"18000",
        "health":"green",
        "name":"sre-intern-sre-insights-admin-backend"
    }

# Add Exceptions


@app.exception_handler(UUIDException)
def uuid_exception_handler(request: Request, exc: UUIDException):
    return JSONResponse(status_code=422, content={"detail": exc.name})


@app.exception_handler(HTTPException)
def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
