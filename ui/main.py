#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.
"""Main"""

import random
import os
import serial_reader
import fiber_reading
import pickle
from statistics import median, mean


def fix_bits(packet):
    # Correct leading bit weirdness
    min_d = min(packet.data)
    for i, d in enumerate(packet.data):
        diff = len(bin(abs(d))) - len(bin(abs(min_d)))
        packet.data[i] >>= diff
    return packet


def process_packets(sdc):
    ardata = [0.0] * 100
    linedata = [0.0] * 100
    flush = False
    cnt = 0
    while True:
        if cnt == 0:
            ardata = [0.0] * 100

        packet = sdc.get_packet()
        if not packet:
            continue
        packet = fix_bits(packet)

        # TODO(drousso): do requisite processing on the packet and write data
        # to ardata and linedata 10x10 array represented as a 100 element array.
        # to flush to the gui set flush = True after processing the packet.
        x = mean(packet.data)
        if packet.calibration_value != 0:
            x /= packet.calibration_value
        if packet.axis == fiber_reading.Axis.X_AXIS:
            for i in range(0, 10):
                ardata[10 * packet.index + i] += x
        elif packet.axis == fiber_reading.Axis.Y_AXIS:
            for i in range(0, 10):
                ardata[i * 10 + packet.index] += x

        cnt = (cnt + 1) % 20
        if cnt == 0:
            flush = True

        if flush:
            with open('tmp_ardata.pkl', 'wb') as output:
                pickle.dump(ardata, output, pickle.HIGHEST_PROTOCOL)
            os.rename('tmp_ardata.pkl', 'ardata.pkl')

            with open('tmp_linedata.pkl', 'wb') as output:
                pickle.dump(linedata, output, pickle.HIGHEST_PROTOCOL)
            os.rename('tmp_linedata.pkl', 'linedata.pkl')
            flush = False


def main():
    device = serial_reader.select_device()
    sdc = serial_reader.SerialDataSource(device.device)
    sdc.start()
    while True:
        process_packets(sdc)
    sdc.stop()


if __name__ == '__main__':
    main()
