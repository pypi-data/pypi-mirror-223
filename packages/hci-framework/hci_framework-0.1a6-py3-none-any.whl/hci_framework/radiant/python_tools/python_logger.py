from radiant.framework.server import PythonHandler
from hci_framework.utils import kafkalogs
import logging as logging_orig


########################################################################
class logging(PythonHandler):
    """"""

    # ----------------------------------------------------------------------
    def __getattribute__(self, attribute):
        """"""
        def inset(*args, **kwargs):
            """"""
            return getattr(logging_orig, attribute)(*args, **kwargs)
        return inset

    # # ----------------------------------------------------------------------
    # def warning(self, msg):
        # """"""
        # return logging_orig.warning(msg)
