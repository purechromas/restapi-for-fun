from .abc_exception import AppError


class ProjectExistError(AppError):
    pass


class UserNotExistError(AppError):
    pass


class UserExistError(AppError):
    pass
