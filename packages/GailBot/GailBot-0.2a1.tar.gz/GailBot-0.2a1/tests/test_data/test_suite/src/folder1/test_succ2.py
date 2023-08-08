from gailbot import Plugin, GBPluginMethods, UttObj
import logging

class TestSucc2(Plugin):
    """ 
    The plugin itself does not fail, but since it depends on test_fail2, 
    it also will never be run, and should fail
    """
    def __init__(self) -> None:
        super().__init__()

    def apply(
        self, dependency_outputs, methods: GBPluginMethods
    ):
        print("test succ2")
        logging.info("running test_succ1")
        self.successful = True
        return True