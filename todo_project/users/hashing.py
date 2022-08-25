from passlib.context import CryptContext


class Hasher:
    """
    Password hashing with Bcrypt.
    https://www.fastapitutorial.com/blog/password-hashing-fastapi/
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        This method verify the plain password and hashed password.
        :param plain_password: plain password
        :param hashed_password: hashed password
        :return: True if verify else False
        """
        return Hasher.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        This method is used to create the hashed password.
        :param password: password
        :return: hashed password
        """
        return Hasher.pwd_context.hash(password)
