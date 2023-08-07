#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import shutil
import sys
import time
from typing import Union

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from naruno.config import BACKUPS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger

logger = get_logger("LIB")


def naruno_export() -> Union[str, None]:
    """
    Create a ZIP archive of the `db` folder in the main directory of the application.

    Returns:
        The path of the created ZIP file, or None if the ZIP file could not be created.
    """
    logger.info("Export system is started")
    main_folder = get_config()["main_folder"]
    zip_dir = f"{main_folder}/db/"
    result_file = f"{main_folder}/{BACKUPS_PATH}{int(time.time())}"
    logger.debug(f"zip_dir: {zip_dir}")
    logger.debug(f"result_file: {result_file}.zip")
    shutil.make_archive(result_file, "zip", zip_dir)
    logger.info("Export complated")

    return f"{result_file}.zip"


if __name__ == "__main__":
    naruno_export()
