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
        self._intro = """Fake SR OS Software\r
Copyright (c) Ing. Bernhard Wagesreiter 2024.  All Rights Reserved.\r
\r
Trademarks\r
\r
Nokia and the Nokia logo are registered trademarks of Nokia. All other\r
trademarks are the property of their respective owners.\r
\r
IMPORTANT: READ CAREFULLY\r
\r
The SR OS Software (the "Software") is proprietary to Nokia and is subject\r
to and governed by the terms and conditions of the End User License\r
Agreement accompanying the product, made available at the time of your order,\r
or posted on the Nokia website (collectively, the "EULA").  As set forth\r
more fully in the EULA, use of the Software is strictly limited to your\r
internal use.  Downloading, installing, or using the Software constitutes\r
acceptance of the EULA and you are binding yourself and the business entity\r
that you represent to the EULA.  If you do not agree to all of the terms of\r
the EULA, then Nokia is unwilling to license the Software to you and (a) you\r
may not download, install or use the Software, and (b) you may return the\r
Software as more fully set forth in the EULA.\r
\r
This product contains cryptographic features and is subject to United States\r
and local country laws governing import, export, transfer and use. Delivery\r
of Nokia cryptographic products does not imply third-party authority to\r
import, export, distribute or use encryption.\r
\r
If you require further assistance please contact us by sending an email\r
to support@nokia.com.\n\r"""

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