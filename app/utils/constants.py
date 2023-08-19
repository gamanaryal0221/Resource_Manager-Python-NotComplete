class Template():
    HOME = "home.html"
    LOGIN = "login.html"

class Environment():
    KEY = "environment"
    DEVELOPMENT = "dev"
    QC = "qc"
    PROD = "prod"

class Config():
    MYSQL_DATA_SOURCES = 'data_sources'


class Mysql():
    RESOURCE_MANAGER = 'resource_manager'

    HOSTNAME = 'hostname'
    DATABASE = 'database'
    USER = 'user'
    PASSWORD = 'password'

class Key():
    STATUS_CODE = "status_code"
    TITLE = "title"
    MESSAGE = "message"
    REDIRECT_URL = "redirect_url"
    REDIRECT_TEXT = "redirect_text"

    SECRET_COOKIE_KEY = "cookie_secret"

    TOKEN = "token"

    SALT_VALUE = "salt_value"
    HASHED_PASSWORD = "hashed_password"

    USER_ID = "user_id"
    FULLNAME = "fullname"

    HOST_URL = "host_url"


class Token():
    PRIVATE_KEY = "private_key"
    EXPIRE_DURATION = "expire_duration"
    ALGORITHM = "algorithm"

    DEFAULT_EXPIRE_DURATION = 8
    DEFAULT_ALGORITHM = 'HS256'

class Url():
    CAS_LOGIN_URL = "http://login.ENVIRONMENT.vcp.com/login?host_url=HOST_URL"