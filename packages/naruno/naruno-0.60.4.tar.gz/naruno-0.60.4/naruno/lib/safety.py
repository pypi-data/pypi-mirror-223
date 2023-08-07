#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings

logger = get_logger("Safety")


def safety_check(
    interface=None,
    timeout=None,
    exit_on_error=True,
    custom_pywall=None,
    custom_debug_mode=None,
):
    """

    :param interface: Default value = None)
    :param timeout: Default value = None)
    :param exit_on_error: Default value = True)
    :param custom_pywall: Default value = None)
    :param custom_debug_mode: Default value = None)

    """
    logger.debug("Checking safety")
    try:
        the_import_string = "from pywall import pywall"
        pywall_class = (exec(the_import_string)
                        if custom_pywall is None else custom_pywall)
        the_pywall = pywall() if custom_pywall is None else custom_pywall()
        the_pywall.iface = the_pywall.iface if interface is None else interface
        the_pywall.timeout = the_pywall.timeout if timeout is None else timeout

        control = the_pywall.control()

        debug_mode = (the_settings()["debug_mode"]
                      if custom_debug_mode is None else custom_debug_mode)

        if control is not None:
            if control:
                logger.error("NOT Safe")
                exit() if exit_on_error else None
                return False
            else:
                logger.debug("Safe")
                return True
        elif debug_mode:
            logger.debug(
                "Control check is none but passing because of debug mode")
            return None
        else:
            logger.debug("NOT Safe (Control check is None)")
            exit() if exit_on_error else None
            return False
    except ImportError:
        logger.debug("Passing safety check (no pywall)")
        return None
