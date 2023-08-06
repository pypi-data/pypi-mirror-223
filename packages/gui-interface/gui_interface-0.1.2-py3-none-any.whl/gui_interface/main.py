# -*- coding: utf-8 -*-
import re
import sys
from gui_interface import MainWindow, SingleInstanceApp
if __name__ == '__main__':
    app = SingleInstanceApp([])
    window = MainWindow(app)
    window.show()
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(app.exec())
