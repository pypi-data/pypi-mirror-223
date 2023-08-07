#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
import copy
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.get_block import GetBlock
from naruno.lib.settings_system import save_settings
from naruno.lib.settings_system import the_settings
from naruno.node.unl import Unl
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction


def Status(
    custom_TEMP_BLOCK_PATH: str = None,
    custom_UNL_NODES_PATH: str = None,
    custom_first_block: Block = None,
    custom_new_block: Block = None,
    custom_connections: list = None,
    custom_transactions: list = None,
    no_cache: bool = False,
    cache_time: int = 300,
    wait_time=None,
) -> dict:
    """
    Returns the status of the network.
    """
    a_settings = the_settings()
    currently_time = time.time()
    the_wait_time = wait_time if wait_time is not None else Block("status").block_time*3

    if (no_cache or a_settings["status_cache_time"] + cache_time <=
            currently_time) and (not a_settings["status_working"]
                                 or a_settings["status_cache_time"] +
                                 the_wait_time + 2 <= currently_time):
        a_settings["status_working"] = True
        if not no_cache:
            a_settings["status_cache_time"] = time.time()
        save_settings(a_settings)
        first_block = copy.copy((GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
                       if custom_first_block is None else custom_first_block))

        
        time.sleep(the_wait_time)
        new_block = (GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
                     if custom_new_block is None else custom_new_block)

        connections = (Unl.get_as_node_type(
            Unl.get_unl_nodes(custom_UNL_NODES_PATH=custom_UNL_NODES_PATH))
                       if custom_connections is None else custom_connections)
        connected_nodes = [
            str(f"{the_connections.host}:{the_connections.port}")
            for the_connections in connections
        ]

        transactions = (GetMyTransaction() if custom_transactions is None else
                        custom_transactions)


        last_transaction_of_block = (
            str(new_block.validating_list[-1].dump_json())
            if len(new_block.validating_list) > 0 else "")

        status_json = {
            "status": "",
            "first_block": str(first_block.dump_json()),
            "new_block": str(new_block.dump_json()),
            "last_transaction_of_block": last_transaction_of_block,
            "connected_nodes": connected_nodes,
        }

        status_json["status"] = ("Not working" if
                                 (first_block.sequence_number +
                                  first_block.empty_block_number)
                                 == (new_block.sequence_number +
                                     new_block.empty_block_number) else
                                 "Working")

        if not no_cache:
            a_settings["status_cache"] = status_json
            a_settings["status_cache_time"] = time.time()

        a_settings["status_working"] = False
        save_settings(a_settings)
        return status_json

    else:
        return a_settings["status_cache"]
