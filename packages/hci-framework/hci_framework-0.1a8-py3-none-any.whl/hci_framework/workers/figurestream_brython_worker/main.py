from hci_framework.radiant.server import FrameworkAPI, FigureStream
from hci_framework.radiant.utils import environ

import os
import json
from browser import document, html
import material_3 as md


########################################################################
class BareMinimumWorker(FrameworkAPI):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        green_button = md.text_button('Green')
        orange_button = md.text_button('Orange')
        green_button.bind('click', self.set_green)
        orange_button.bind('click', self.set_orange)

        self.body <= green_button
        self.body <= orange_button

        self.figurestream = FigureStream()
        self.body <= self.figurestream.container

    # ----------------------------------------------------------------------
    def set_green(self, evt):
        """"""
        print('Green')
        self.figurestream.set('color', 'C2')
        self.figurestream.update()

    # ----------------------------------------------------------------------
    def set_orange(self, evt):
        """"""
        print('Orange')
        self.figurestream.set('color', 'C1')
        self.figurestream.update()


if __name__ == '__main__':

    scripts = (
        ('/app/worker/stream.py', environ('STREAM', '5001')),
        ('stream.py', environ('STREAM', '5001')),
    )

    BareMinimumWorker(scripts=scripts)
