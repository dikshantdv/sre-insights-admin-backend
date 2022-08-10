from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from router import tasks_get, tasks_post
from config.exceptions import UUIDException

# Create a FastAPI application
app = FastAPI()

# Add CORS middleware
origins = ['http://localhost:13000', 'http://127.0.0.1:13000']
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

@app.get("/")
def read_info():
    return {
        "version":"4.0.0",
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
