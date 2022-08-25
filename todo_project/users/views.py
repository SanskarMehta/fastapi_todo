# from database import init_db
from todo_project.users.schemas import UserRegistrationRequest, UserLoginRequest, PasswordChangeSchema, \
    ForgotPasswordSchema, ForgotPasswordSetSchema
from todo_project.users import services
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

router = APIRouter(
    tags=["users"],
)


# @router.on_event("startup")
# async def start_db():
#     await init_db()


# @router.get("/test_server", status_code=status.HTTP_200_OK)
def server_check():
    """
    A Simple function to check if server is working state or not
    :return: str: Simple message
    """
    return "Server is working"


# @router.post("/api/v1/auth/register/", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserRegistrationRequest):
    """
    This is call when request method is post.
    :param request: schema request data
    :return:
    """
    service_object = services.Authentication(request)
    return await service_object.register_user()


# @router.post("/api/v1/auth/login/", status_code=status.HTTP_200_OK)
async def login(request: UserLoginRequest, authorize: AuthJWT = Depends()):
    """
    This is call when request method is post.
    :param request: schema request data
    :param authorize:
    :return:
    """
    service_object = services.Authentication(request)
    return await service_object.user_login(authorize)


# @router.post('/api/v1/auth/refresh/', status_code=status.HTTP_201_CREATED)
def refresh_token(authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()
    return services.create_refresh_token(authorize)


# @router.put("/api/v1/auth/change-password/", status_code=status.HTTP_200_OK)
async def change_password(request: PasswordChangeSchema, authorize: AuthJWT = Depends()):
    """
    This is called when method is put.
    :return:
    """
    authorize.jwt_required()
    service_object = services.Authentication(request)
    return await service_object.password_change(authorize)


# @router.post("/api/v1/auth/forgot-password/", status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPasswordSchema, authorize: AuthJWT = Depends()):
    """
    forgot  password api.
    :param request: schema request data.
    :param authorize:
    :return:
    """
    service_object = services.Authentication(request)
    return await (service_object.forgot_password(authorize))


# @router.patch("/api/v1/auth/password-reset-confirm/",)
def password_reset_confirm(request: ForgotPasswordSetSchema, ):
    """
    password reset confirm api.
    :param request:schema request data.
    :return:
    """
    service_object = services.Authentication(request)
    return service_object.reset_password_confirm()
