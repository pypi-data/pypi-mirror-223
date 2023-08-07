from gailbot import Plugin, GBPluginMethods, UttObj
import logging

class TestFail2(Plugin):
    """ 
    The plugin itself does not fail, but since it depends on test_fail2, 
    it also will never be run, and should fail
    """
    def __init__(self) -> None:
        super().__init__()

    def apply(
        self, dependency_outputs, methods: GBPluginMethods
    ):
        print("test fail 2")
        logging.error("this line will never be logged")
        self.successful = True
        return True