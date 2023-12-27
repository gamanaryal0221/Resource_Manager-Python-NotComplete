import tornado.web
import json

from app import settings
from .database import Sql
from app.utils.constants import Key, Environment, Token
from app.utils.common import fetch_data


# for url mappings
import re
from app.handlers.home_handler import HomeHandler
from app.handlers.login_success import LoginSuccessHandler
from app.handlers.user_handler import UserHandler


class Application():

    def initialize(self, environment):
        app = tornado.web.Application(
            UrlMapping().get_all(),
            debug=(True if environment == Environment.DEVELOPMENT else False)
        )
        app.environment = environment

        config = self.read_configuration()
        app.mysql_connections = Sql().initialize(config)
        app.token_detail = self.get_token_detail(config)

        if Key.SECRET_COOKIE_KEY in config:
            app.settings[Key.SECRET_COOKIE_KEY] = config[Key.SECRET_COOKIE_KEY]
            print(f'\nCoookie secret key has been set successfully')
        else:
            raise ValueError(f"Missing configuration for '{Key.SECRET_COOKIE_KEY}'")

        app.settings[settings.TEMPLATE_PATH_KEY] = settings.TEMPLATE_PATH
        print(f"\nTemplate path: {settings.TEMPLATE_PATH}")
        print(f"Static path: {settings.STATIC_PATH}")

        port = fetch_data(config, Key.PORT, -1)
        if port is not -1:
            print(f"\nListening to port:{port}")
            app.listen(port)

        return app
    
    
    def read_configuration(self):
        config_file = settings.CONFIG_PATH+'\\'+settings.CONFIG_FILE_NAME
        print(f'\nReading configuration from {config_file} ...')

        with open(config_file, 'r') as file:
            data = json.load(file)

        return data
    
    
    def get_token_detail(self, config):
        print('\n---------- Getting token details ----------')
        token = fetch_data(config, Key.TOKEN) 
        if token:
            return {
                Token.PRIVATE_KEY: fetch_data(token, Token.PRIVATE_KEY),
                Token.EXPIRE_DURATION: fetch_data(token, Token.EXPIRE_DURATION, Token.DEFAULT_EXPIRE_DURATION),
                Token.ALGORITHM: fetch_data(token, Token.ALGORITHM, Token.DEFAULT_ALGORITHM),
            }
        else:
            raise ConnectionError(f'Null received for token detail')
    
    
class UrlMapping():
    def get_all(self):
        print('\n---------- Initializing url -> handlers ----------')

        handlers = [
            (fr"/", HomeHandler),
            (fr"{settings.STATIC_URL}", tornado.web.StaticFileHandler, {"path": settings.STATIC_PATH}),
            (fr"/login/success", LoginSuccessHandler),

            (fr"/user/(?P<action>list|add|profile|logout)", UserHandler),
        ]

        for i, handler in enumerate(handlers):
            print(f'{i+1}. {handler[0]} -> {self.get_handler_name(handler[1])}')

        return handlers

    def get_handler_name(self, _class):
        class_name = re.search(r"'(.*?)'", str(_class)).group(1)
        return str(class_name)

