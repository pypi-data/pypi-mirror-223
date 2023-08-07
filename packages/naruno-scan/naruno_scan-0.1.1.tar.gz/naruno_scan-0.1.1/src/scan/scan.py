#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from threading import Thread
import time
from kot import KOT
import requests
import traceback


from naruno.lib.perpetualtimer import perpetualTimer

the_block_db = KOT("blocks_db", folder=os.path.join(os.path.dirname(__file__)))
the_statatus_db = KOT("status_db", folder=os.path.join(os.path.dirname(__file__)))


class SCAN:
    @staticmethod
    def gui():
        from .gui import GUI
        GUI()


    @staticmethod
    def web(host=None, port=0):
        from .gui import WEB
        WEB(host, port)


    @staticmethod
    def bacground_proccess_1(network, port, ):
            try:
                response = requests.get(f"http://{network}:{port}/export/block/json", timeout=5)
                if response.status_code == 200:
                    for old_key in the_block_db.get_all():
                        the_block_db.delete(old_key)
                    the_block_db.set(str(int(time.time())), response.json())

            except:
                pass

    @staticmethod
    def bacground_proccess_2(network, port, ):

            try:
                response = requests.get(f"http://{network}:{port}/status", timeout=130)
                if response.status_code == 200:

                    the_statatus_db.set("status", response.json())
            except:
                pass

    @staticmethod
    def background(network_1, port_1, network_2=None, port_2=None,interval_1=1,interval_2=100):
        if network_2 == None:
            network_2 = network_1
        if port_2 == None:
            port_2 = port_1
        perpetualTimer(interval_1 ,SCAN.bacground_proccess_1, [network_1, port_1,])
        perpetualTimer(interval_2 ,SCAN.bacground_proccess_2, [network_1, port_1,])


def main():
    import fire

    fire.Fire(SCAN)
