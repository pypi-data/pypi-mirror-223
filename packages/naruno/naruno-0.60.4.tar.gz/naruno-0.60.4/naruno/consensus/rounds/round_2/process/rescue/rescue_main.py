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
import random

from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger
from naruno.node.client.client import client
from naruno.node.server.server import server
from naruno.node.unl import Unl

logger = get_logger("CONSENSUS_SECOND_ROUND")


def rescue_main(
    block: Block,
    candidate_block_hash: dict,
    custom_server: server = None,
    custom_unl: client = None,
) -> Block:
    logger.info("Rescue operation is started")
    logger.debug(f"First block: {block}")
    sender = candidate_block_hash["hash"]["sender"]
    logger.debug(
        f"Our block is not valid, the system will try to get true block from naruno.node {sender}"
    )
    block.dowload_true_block = sender
    unl_list = Unl.get_as_node_type([sender], c_type=2)
    the_server = server.Server if custom_server is None else custom_server
    the_unl_node = random.choice(
        unl_list) if custom_unl is None else custom_unl
    logger.info(f"True block requested from {the_unl_node}")
    the_server.send_client(the_unl_node, {"action": "sendmefullblock"})
    logger.debug(f"End block: {block}")
    return block
