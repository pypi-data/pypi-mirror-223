#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from hashlib import sha256

from naruno.config import PENDING_TRANSACTIONS_PATH
from naruno.lib.config_system import get_config
from naruno.transactions.pending.save_pending import pendingtransactions_db
from naruno.lib.kot import KOT

def DeletePending(tx, custom_PENDING_TRANSACTIONS_PATH=None):
    if custom_PENDING_TRANSACTIONS_PATH == PENDING_TRANSACTIONS_PATH:
        custom_PENDING_TRANSACTIONS_PATH = None    
    file_name = sha256((tx.signature).encode("utf-8")).hexdigest()
    pendingtransactions_db.delete(file_name)  if custom_PENDING_TRANSACTIONS_PATH is None else KOT("pendingtransactions"+custom_PENDING_TRANSACTIONS_PATH, folder=get_config()["main_folder"] + "/db").delete(file_name)
