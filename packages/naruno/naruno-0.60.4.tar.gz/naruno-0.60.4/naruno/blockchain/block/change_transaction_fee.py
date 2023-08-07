#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.lib.log import get_logger
from naruno.transactions.pending.get_pending import GetPendingLen
from decimal import Decimal


logger = get_logger("BLOCKCHAIN")


def ChangeTransactionFee(
    block,
    custom_pending_transaction_len=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
):
    """
    Increase transaction fee by 0.01 naruno coin for each block.default_optimum_transaction_number argument
    """
    logger.info("Calculating the transaction fee")
    logger.debug(f"Start fee is: {block.transaction_fee}")
    pending_transactions = (GetPendingLen(
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)
                            if custom_pending_transaction_len is None else
                            custom_pending_transaction_len)
    validating_list_len = 0
    for tx in block.validating_list:
        if tx.signature != "NARUNO":
            validating_list_len += 1
    total_len = validating_list_len + pending_transactions
    logger.debug(f"total_len: {total_len}")
    logger.debug(
        f"block.default_optimum_transaction_number {block.default_optimum_transaction_number}"
    )
    logger.debug(
        f"block.default_increase_of_fee {block.default_increase_of_fee}")
    if (total_len // block.default_optimum_transaction_number) != 0:
        increase = (total_len // block.default_optimum_transaction_number
                    ) * block.default_increase_of_fee
        decimal_amount = Decimal(str(block.transaction_fee)) + Decimal(str(increase))
        block.transaction_fee = float(decimal_amount)
        logger.debug("Transaction fee will be increased")

    else:
        logger.debug("Transaction fee is not changed")
        block.transaction_fee = block.default_transaction_fee
    logger.debug(f"New transaction fee is : {block.transaction_fee} ")
