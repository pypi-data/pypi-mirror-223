#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import threading
import traceback

from naruno.transactions.check.check_transaction import \
    CheckTransaction
from naruno.transactions.pending.save_pending import SavePending



def GetTransaction(
    block,
    the_transaction,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
    custom_account_list=None,
    except_client=None,
    custom_server=None,
):
    if CheckTransaction(
            block,
            the_transaction,
            custom_current_time,
            custom_sequence_number,
            custom_balance,
            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
            custom_account_list=custom_account_list,
    ):
        SavePending(
            the_transaction,
            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
        )
        return True
    else:
        return False
