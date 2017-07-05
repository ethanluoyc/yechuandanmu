import os
import time


class BaseConfig:
    YEAR = time.strftime("%Y", time.localtime())  # Try to automatically config the year
    SECRET_KEY = os.environ.get('DANMU_SECRET', 'cldds_safeword')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:@localhost:5432/yechuan')
