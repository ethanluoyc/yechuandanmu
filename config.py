import os


class BaseConfig:
    YEAR = 2016  # Change the year here for all site's year to take effect
    SECRET_KEY = os.environ.get('DANMU_SECRET', 'cldds_safeword')


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:@localhost:5432/yechuan')
