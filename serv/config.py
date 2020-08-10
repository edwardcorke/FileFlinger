import os
import pathlib


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = str(pathlib.Path(__file__).parent.absolute()) + '\\static\\uploads\\'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2GB upload limit

    permissionLevels = dict()
    permissionLevels['suspended'] = 0
    permissionLevels['user'] = 1
    permissionLevels['admin'] = 2
    permissionLevels['manager'] = 3
    permissionLevels['owner'] = 4
