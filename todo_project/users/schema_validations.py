import re
from todo_project import constants
from fastapi import HTTPException, status


def username_validation(username):
    """
    This method validate the username
    :param username: username
    :return: validate username
    """
    regex = constants.USER_NAME_REGEX
    if re.fullmatch(regex, username):
        return username
    else:
        raise HTTPException(detail=constants.ERR_USERNAME_WRONG, status_code=status.HTTP_400_BAD_REQUEST)


def email_validation(email):
    """
    This method validate the user email.
    :param email: user email
    :return: validate email
    """
    regex = constants.EMAIL_REGEX

    if not re.fullmatch(regex, email):
        raise HTTPException(detail=constants.ERR_EMAIL_WRONG, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return email


def password_validation(password):
    """
    This method validate the user password according to the regx pattern.
    :param password: user password
    :return: validate password
    """
    regex = constants.PASSWORD_REGEX

    if re.fullmatch(regex, password):
        return password
    else:
        raise HTTPException(detail=constants.ERR_PASSWORD_WRONG, status_code=status.HTTP_400_BAD_REQUEST)
