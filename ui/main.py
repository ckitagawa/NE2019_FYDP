#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.
"""Main"""

import signal
import serial_reader


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def process_packet(packet):
    # TODO(drousso): do requisite processing on the packet
    # TODO(dparmar): implement display
    # Feel free to use classes or threads but this is the "hook" that supplies
    # fresh data periodically.
    pass


def main():
    gk = GracefulKiller()
    device = serial_reader.select_device()
    sdc = serial_reader.SerialDataSource(device)
    sdc.start()
    while True:
        if gk.kill_now:
            break
        packet = sdc.get_packet()
        if not packet:
            print("No Packet")
            continue
        process_packet(packet)
    sdc.stop()


if __name__ == '__main__':
    main()
