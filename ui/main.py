#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.
"""Main"""

import serial_reader
import fiber_reading
from statistics import median


def process_packet(packet):
    # TODO(drousso): do requisite processing on the packet
    # TODO(dparmar): implement display
    # Feel free to use classes or threads but this is the "hook" that supplies
    # fresh data periodically.
    if packet.axis == fiber_reading.Axis.X_AXIS:
        print(packet.axis, packet.index, min(packet.data))


def main():
    device = serial_reader.select_device()
    sdc = serial_reader.SerialDataSource(device.device)
    sdc.start()
    while True:
        packet = sdc.get_packet()
        if not packet:
            continue
        process_packet(packet)
    sdc.stop()


if __name__ == '__main__':
    main()
