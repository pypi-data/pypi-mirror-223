#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.accounts.get_accounts import GetAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import GetBlockshash
from naruno.blockchain.block.blocks_hash import GetBlockshash_part
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.rounds.round_1.process.transactions.transactions_main import \
    transactions_main
from naruno.lib.log import get_logger
from naruno.transactions.process_the_transaction import ProccesstheTransaction

logger = get_logger("CONSENSUS_FIRST_ROUND")


def round_process(
    block: Block,
    candidate_class: candidate_block,
    unl_nodes: dict,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
    custom_shares=None,
    custom_fee_address=None,
    clean=True,
) -> Block:
    logger.info("Processing for round 1 is started")
    logger.debug(f"First block: {block.dump_json()}")
    transactions_main(block,
                      candidate_class=candidate_class,
                      unl_nodes=unl_nodes,
                      clean=clean)

    block.round_1 = True
    block.round_2_starting_time = block.start_time + block.round_1_time

    account_list = GetAccounts(
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH)
    resukt_of_proccesstransaction = ProccesstheTransaction(
        block,
        account_list,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_shares=custom_shares,
        custom_fee_address=custom_fee_address,
    )
    block = resukt_of_proccesstransaction[0]
    account_list = resukt_of_proccesstransaction[1]

    part_of_blocks_hash = GetBlockshash_part(
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
    the_blocks_hash = GetBlockshash(
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)

    block.hash = CalculateHash(block, part_of_blocks_hash, the_blocks_hash,
                               account_list)



    SaveBlock(
        block,
        custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        delete_old_validating_list=True,
    )
    logger.debug(f"End block: {block.dump_json()}")
    return block
