class AppExceptions(Exception):
    pass


class UserNotExist(AppExceptions):
    pass


class UserAlreadyExist(AppExceptions):
    pass


class ProjectAlreadyExist(AppExceptions):
    pass


class TokenNotExist(AppExceptions):
    pass
