# coding: utf-8
import logging
import config


class WebElementsExtended(object):
    """
    Класс расширяющий Appium WebElement.
    Модуль обеспечивает работу с элементами внутри элемента
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = None
        self.driver = args[0]
        self.logger = logging.getLogger(config.APPIUM_LOG_NAME)




