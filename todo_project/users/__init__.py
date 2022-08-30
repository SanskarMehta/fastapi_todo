from fastapi import APIRouter
from fastapi import status
from todo_project.users import views
from todo_project.users.schemas import UserRegistrationResponse

user_router = APIRouter(
    tags=["users"],
)

user_router.add_api_route("/test_server", views.server_check, methods=["GET"], status_code=status.HTTP_200_OK,
                          )
user_router.add_api_route("/api/v1/auth/register", views.create_user, methods=["POST"],
                          status_code=status.HTTP_201_CREATED)
user_router.add_api_route("/api/v1/auth/login", views.login, methods=["POST"], status_code=status.HTTP_200_OK)
user_router.add_api_route("/api/v1/auth/refresh", views.refresh_token, methods=["POST"],
                          status_code=status.HTTP_201_CREATED)
user_router.add_api_route("/api/v1/auth/change-password", views.change_password, methods=["PUT"],
                          status_code=status.HTTP_200_OK)
user_router.add_api_route("/api/v1/auth/password-reset-confirm", views.password_reset_confirm, methods=["PATCH"],
                          status_code=status.HTTP_200_OK)
user_router.add_api_route("/api/v1/auth/forgot-password", views.forgot_password, methods=['POST'],
                          status_code=status.HTTP_200_OK)
