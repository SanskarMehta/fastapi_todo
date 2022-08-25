EMAIL_REGEX = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,12}$"
USER_NAME_REGEX = r"^[A-Za-z\d@$!_#%*?&]{3,50}$"

PASSWORD_RESET_SUBJECT = "Password Reset"
BLOG_CREATE_SUBJECT = "Blog Create"
PASSWORD_RESET_MAIL_LINK_MSG = "click on the link below to reset your password."
PASSWORD_RESET_MAIL_MSG = "Mail is send on your email. kindly look into it."
MSG_PASSWORD_RESET = "Successfully password reset."
ERR_USERNAME_WRONG = "Please enter valid username!"
ERR_PASSWORD_WRONG = "Please enter valid password!"
ERR_EMAIL_WRONG = "Please enter valid email!"
ERR_SQL_ALCHEMY_ERROR = "Error in storing database."
MSG_REGISTER_USER_SUCCESSFULLY = "Hey {} you registered successfully."
ERR_USER_NAME_ALREADY_TAKEN = "The user name {} is already taken."
ERR_EMAIL_ALREADY_TAKEN = "The Email {} is already taken."
ERR_PASSWORD_INCORRECT = "The password is incorrect"
MSG_UPDATE_PASSWORD = "Successfully password change"
ERR_PASSWORD_NOT_MATCH = "The new password and confirm new password is not same."
ERR_EMAIL_IS_NOT_EXISTS = "The Email {} is not exists."
ERR_USER_WITH_USER_NAME_NOT_EXISTS = "There is no user with user_name {}"
MSG_LOG_IN_SUCCESSFULLY = "Successfully Logged in."
MSG_FOR_ACCESS_TOKEN_REFRESH = "Your access token is successfully refresh."
MSG_LOG_OUT_SUCCESSFULLY = "Successfully Logged out."
MSG_CREATE_ACCESS_TOKEN = "Successfully create access token."
MSG_REGISTER_BLOG_SUCCESSFULLY = "Hey {} your blog post created successfully."
ERR_BLOG_NOT_EXISTS = "User with blog_id {} does not exists."
MSG_RETRIEVE_BLOG = "Successfully retrieved blog."
MSG_RETRIEVE_BLOGS = "Successfully retrieved blogs."
ERR_NO_DATA_IN_BLOG = "There is no blog available in database."
MSG_DELETED_BLOG = "Blog deleted successfully."
ERR_BLOG_ID_NOT_PROVIDE = "Blog id not provide."
MSG_UPDATE_BLOG = "Successfully updated blog."
LATEST_BLOG_SEND_SUBJECT = "Latest blogs."
MSG_SCOPE_INVALID_TOKEN = "Scope for the token is invalid."
MSG_TOKEN_EXPIRE = "Token expired."
MSG_TOKEN_INVALID = "Invalid token"
DESCRIPTION = "FAST-API BEST PRACTICE PROJECT STRUCTURE"
