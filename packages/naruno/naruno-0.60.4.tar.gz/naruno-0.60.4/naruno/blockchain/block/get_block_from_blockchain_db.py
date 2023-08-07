#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.accounts.get_accounts import GetAccounts
from naruno.blockchain.block.blocks_hash import GetBlockshash
from naruno.blockchain.block.blocks_hash import GetBlockshash_part
from naruno.blockchain.block.get_block import GetBlock
from naruno.config import BLOCKS_PATH


def GetBlockstoBlockchainDB(
    sequence_number,
    custom_BLOCKS_PATH=None,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_TEMP_BLOCKSHASH_PATH=None,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
    dont_clean=False,
):
    """
    Gets the block from the blockchain database
    """
    try:
        the_BLOCKS_PATH = (BLOCKS_PATH if custom_BLOCKS_PATH is None else
                           custom_BLOCKS_PATH)

        the_block = GetBlock(
            (the_BLOCKS_PATH + str(sequence_number) + ".block.json"),
            dont_clean=dont_clean, reset=True,
        )
        the_accounts = GetAccounts(
            (the_BLOCKS_PATH + str(sequence_number) + ".accounts.db"))
        the_blockshash = GetBlockshash(the_BLOCKS_PATH + str(sequence_number) +
                                       ".blockshash.json")
        the_blockshashpart = GetBlockshash_part(the_BLOCKS_PATH +
                                                str(sequence_number) +
                                                ".blockshashpart.json")
        result = [the_block, the_accounts, the_blockshash, the_blockshashpart]

        return result

    except TypeError:
        return False
