from datetime import timedelta
from todo_project import language as common_language
from http import HTTPStatus
from todo_project.users.models import User
from todo_project import constants
from todo_project.users.hashing import Hasher
from todo_project.users import language
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from todo_project.users.schemas import UserRegistrationResponse
from todo_project.users.authentication import JWTAuthentication, DecodeToken
from todo_project.utils import Mail
from config import Settings
from config import MailConfig
from todo_project.users import domain


class Authentication:
    def __init__(self, request_data, ):
        """
        Form this method set the schema request data.
        :param request_data: schema request data
        """
        self.request_data = request_data

    async def register_user(self):
        """
        From this request get the required params data.
        :return: Json formed response
         """
        req_data = self.get_json_data()
        email = req_data.get("email")
        user_name = req_data.get("username")
        password = req_data.get("hashed_password")
        if not await User.check_is_email_exists(email):
            if not await User.check_is_username_exists(user_name):
                hash_password = Hasher.get_password_hash(password)
                req_data["password"] = hash_password
                if not (user := await User.save_user(req_data)):
                    return self.send_error_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                    message=constants.ERR_SQL_ALCHEMY_ERROR)
                data = language.convert_response_data_according_to_response_models(user, UserRegistrationResponse)
                return self.send_success_response(status_code=HTTPStatus.CREATED,
                                                  message=constants.MSG_REGISTER_USER_SUCCESSFULLY.format(
                                                      user.username),
                                                  data=data)
            else:
                err_msg = constants.ERR_USER_NAME_ALREADY_TAKEN.format(user_name)
                return self.send_error_response(status_code=HTTPStatus.BAD_REQUEST,
                                                message=err_msg)
        else:
            err_msg = constants.ERR_EMAIL_ALREADY_TAKEN.format(email)
            return self.send_error_response(status_code=HTTPStatus.BAD_REQUEST,
                                            message=err_msg)

    async def user_login(self, authorize: AuthJWT = Depends()):
        """
        From this request get the required params data.
        :return: Json formed response
        """
        req_data = self.get_json_data()
        user_name = req_data.get("user_name")
        password = req_data.get("password")
        user = await User.check_is_username_exists(user_name)
        if not user:
            err_msg = constants.ERR_USER_WITH_USER_NAME_NOT_EXISTS.format(user_name)
            return self.send_error_response(status_code=HTTPStatus.FORBIDDEN, message=err_msg)
        if not Hasher.verify_password(password, user.password):
            err_msg = constants.ERR_PASSWORD_INCORRECT
            return self.send_error_response(status_code=HTTPStatus.FORBIDDEN, message=err_msg)

        jwt = JWTAuthentication(user_name, authorize)
        tokens = jwt.get_tokens_for_user()
        data = language.convert_response_data_according_to_response_models(user, UserRegistrationResponse).dict()
        data.update(tokens)

        return self.send_success_response(status_code=HTTPStatus.OK, message=constants.MSG_LOG_IN_SUCCESSFULLY,
                                          data=data,
                                          )

    async def password_change(self, authorize: AuthJWT = Depends()):
        """
        This method is used to change the user password.
        :param authorize: authorize
        :return: Json success and error response
        """
        current_user = authorize.get_jwt_subject()
        req_data = self.get_json_data()
        current_password = req_data.get("current_password")
        new_password = req_data.get("new_password")
        confirm_new_password = req_data.get("confirm_new_password")
        user = await User.get_user(current_user)
        print(user.password)
        if not Hasher.verify_password(current_password, user.password):
            err_msg = constants.ERR_PASSWORD_INCORRECT
            return self.send_error_response(status_code=HTTPStatus.FORBIDDEN, message=err_msg)
        if new_password != confirm_new_password:
            err_msg = constants.ERR_PASSWORD_NOT_MATCH
            return self.send_error_response(status_code=HTTPStatus.FORBIDDEN, message=err_msg)
        hash_password = Hasher.get_password_hash(new_password)
        if not (await User.update_password(current_user, hash_password)):
            return self.send_error_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                                            message=constants.ERR_SQL_ALCHEMY_ERROR)
        return self.send_success_response(status_code=HTTPStatus.OK, message=constants.MSG_UPDATE_PASSWORD)

    async def forgot_password(self, authorize: AuthJWT = Depends()):
        """
        Forgot password and send forgot password link.
        :param authorize: authorize
        :return:send success response.
        """
        if not (user := await User.check_is_email_exists(self.request_data.email)):
            err_msg = constants.ERR_EMAIL_IS_NOT_EXISTS.format(self.request_data.email)
            return self.send_success_response(status_code=HTTPStatus.BAD_REQUEST,
                                              message=err_msg)

        # create reset token.
        jwt = JWTAuthentication(user.username, authorize, expires=timedelta(minutes=5))
        reset_token = jwt.create_access_token()
        content = {'username': user.username, "token": reset_token, "host_url": Settings().LOCAL_HOST_URL}
        message_schema = domain.Message.generate_msg_schema(constants.PASSWORD_RESET_SUBJECT, [self.request_data.email],
                                                            content)
        mail_conf = MailConfig.connection_config()
        await Mail.send_mail(message_schema, mail_conf, "forgot-password.html")

        return self.send_success_response(status_code=HTTPStatus.OK, message=constants.PASSWORD_RESET_MAIL_MSG)

    def reset_password_confirm(self):
        """
        Password Reset Confirm Method.
        """
        sub_id = DecodeToken(self.request_data.reset_token).decode_token()

        if self.request_data.new_password != self.request_data.confirm_new_password:
            err_msg = constants.ERR_PASSWORD_NOT_MATCH
            return common_language.Response(status_code=HTTPStatus.FORBIDDEN, message=err_msg).send_error_response()
        hash_password = Hasher.get_password_hash(self.request_data.new_password)
        if not (User.update_password(sub_id, hash_password)):
            return self.send_error_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                                            message=constants.ERR_SQL_ALCHEMY_ERROR)
        return self.send_success_response(status_code=HTTPStatus.OK, message=constants.MSG_PASSWORD_RESET)

    def get_json_data(self):
        """
        This method convert data into Json
        :return: Json data.
        """
        return language.convert_data_into_json(self.request_data)

    @staticmethod
    def set_response(status_code, message, data=None):
        """
        From this method we can set the response object.
        :param status_code: status code
        :param message: response message
        :param data: json data
        :return: response object.
        """
        return common_language.Response(status_code=status_code,
                                        message=message,
                                        data=data)

    def send_error_response(self, status_code, message, data=None):
        """
        From this method set the error response.
        :param status_code: status code
        :param message: response message
        :param data: json data
        :return: send error response.
        """
        response = self.set_response(status_code, message, data=data)
        return response.send_error_response()

    def send_success_response(self, status_code, message, data=None):
        """
        From this method set the success response.
        :param status_code: status code
        :param message: response message
        :param data: json data
        :return: send success response.
        """
        response = self.set_response(status_code, message, data=data)
        return response.send_success_response()


def create_refresh_token(authorize: AuthJWT = Depends()):
    """
    Create new access token form the refresh token.
    :param authorize:
    :return: Json formed response
    """
    current_user = authorize.get_jwt_subject()
    jwt = JWTAuthentication(current_user, authorize)
    new_access_token = jwt.create_access_token()
    response = Authentication.set_response(status_code=HTTPStatus.OK, message=constants.MSG_CREATE_ACCESS_TOKEN,
                                           data=new_access_token, )
    return response.send_success_response()
