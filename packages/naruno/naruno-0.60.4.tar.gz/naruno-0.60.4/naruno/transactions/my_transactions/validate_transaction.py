#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.lib.notification import notification
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from naruno.transactions.transaction import Transaction
from naruno.lib.log import get_logger

logger = get_logger("TRANSACTIONS")


def ValidateTransaction(tx: Transaction,
                        custom_currently_list: list = None, force_notify:bool=False) -> list:
    """
    Validates the transaction.
    Parameters:
        tx: The transaction that is going to be validated.
    Returns:
        The list of the my transactions.
    """

    custom_currently_list = (GetMyTransaction() if custom_currently_list
                             is None else custom_currently_list)
    save_list = []
    for i in custom_currently_list:
        first_signature = None
        if isinstance(i,str):
            first_signature = i
        else:
            first_signature = i[0].signature

        if first_signature == tx.signature:
           
            if not i[1] or force_notify:
                notification("Validated TX",
                             f"{tx.data}:{tx.amount} to {tx.toUser}")
            i[1] = True
            save_list.append(i)
    SaveMyTransaction(save_list)
    return custom_currently_list
