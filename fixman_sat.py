# -*- coding: utf-8 -*-
import os

from LibTools.filesystem import Carpeta
from slaves import Fixman

import settings

if __name__ == '__main__':

    abspath = os.path.join(settings.project_path, "media", "comprobantes")

    carpeta = Carpeta(abspath)
    Fixman.reload_Files_v3(carpeta)
