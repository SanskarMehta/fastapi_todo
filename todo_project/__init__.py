from starlette.responses import JSONResponse

import config
from fastapi import FastAPI, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from todo_project import exceptions
from todo_project import constants


@AuthJWT.load_config
def get_config():
    return config.Settings()


def create_app():
    """
    Basically core construction of application is done here.
    Created an app as an object of FastAPI app and Routers are registered here for separate apps.
    """
    app = FastAPI(title="todoapp", description=constants.DESCRIPTION, version="1.0.1", exception_handlers={
        AuthJWTException: exceptions.authjwt_exception_handler}, )

    from todo_project.tasks.views import todo_router as task_router
    from todo_project.users import user_router

    app.include_router(task_router)
    app.include_router(user_router)
    return app


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
