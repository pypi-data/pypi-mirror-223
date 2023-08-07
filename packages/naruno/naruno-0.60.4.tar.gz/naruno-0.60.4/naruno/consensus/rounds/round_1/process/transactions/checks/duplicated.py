#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger

logger = get_logger("TRANSACTIONS")


def Remove_Duplicates(block: Block):
    """
    Remove duplicate transactions
    """
    logger.info("Removing dublicated transaction is started")
    logger.debug(f"First block.validatin_list: {block.validating_list}")

    new_validating_list = []
    for tx in block.validating_list:
        if tx.signature == "NARUNO" or not any(tx.signature == tx2.signature
                   for tx2 in new_validating_list):
            new_validating_list.append(tx)
        else:
            logger.debug(
                f"tx: {tx} will be removed because its added more than one")
    block.validating_list = new_validating_list
    logger.debug(f"End block.validatin_list: {block.validating_list}")
    return block
