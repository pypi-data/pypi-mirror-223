#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.rounds.round_2.process.candidate_blocks_hashes.candidate_blocks_hashes_main import \
    process_candidate_blocks_hashes
from naruno.consensus.rounds.round_2.process.rescue.rescue_main import \
    rescue_main
from naruno.consensus.rounds.round_2.process.validate.validate_main import \
    validate_main
from naruno.lib.log import get_logger
from naruno.node.client.client import client
from naruno.node.server.server import server

logger = get_logger("CONSENSUS_SECOND_ROUND")


def round_process(
    block: Block,
    candidate_class: candidate_block,
    unl_nodes: dict,
    custom_server: server = None,
    custom_unl: client = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
) -> bool:
    logger.info("Processing of round 2 is started")
    logger.debug(f"First block: {block.dump_json()}")
    candidate_block_hash = process_candidate_blocks_hashes(
        block, candidate_class, unl_nodes)
    logger.debug(f"candidate_block_hash: {candidate_block_hash}")
    result = None
    if (block.hash == candidate_block_hash["hash"]["hash"] or block.hash
            == candidate_block_hash["previous_hash"]["previous_hash"]):
        validate_main(block)
        result = True
    else:
        if not candidate_block_hash["hash"]["hash"] == False:
            rescue_main(
                block,
                candidate_block_hash,
                custom_server=custom_server,
                custom_unl=custom_unl,
            )
            result = False

    SaveBlock(
        block,
        custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
    )
    logger.debug(f"End block: {block.dump_json()}")
    logger.info(f"Round 2 process result is: {result}")
    return result
