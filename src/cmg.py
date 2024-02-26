from src.logging import logger
import yaml


class Cmg:
    def __init__(self):
        self._prompt = '*A:QUE260974'
        self._context = []  # ['show', 'router']
        # Intro - Message to be output when cmdloop() is called.
        self.__config_file_name = './config/cmg.yaml'
        self.__config_file = self.__read_config_file(self.__config_file_name)
        print(self.__config_file['show_router_9999_bfd_session'])
        self._intro = """Fake OS Software\r
Copyright (c) Ing. Bernhard Wagesreiter 2024.  All Rights Reserved.\n\r"""

    def get_config_file(self):
        return self.__config_file['show_router_9999_bfd_session']

    def get_prompt(self):
        return self._prompt

    def get_intro(self):
        return self._intro

    def set_context(self, context):
        # self._context.append(context)
        self._context = context

    def get_context(self):
        return self._context

    def get_context_as_string(self):
        context_string = ''
        for i in self._context:
            new_string = '>' + context_string + i
            context_string = new_string

        # return '>show>router'
        return context_string

    def __read_config_file(self, config_file_name):
        try:
            with open(config_file_name, 'r') as f:
                config_file = yaml.safe_load(f)
        except Exception as error:
            logger.error(error)
            # Todo: change error code
            exit(1)

        return config_file