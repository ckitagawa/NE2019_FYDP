#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.

import logging
import threading
import serial
import serial.tools.list_ports
import fiber_reading

from collections import deque


def select_device():
    """User-provided serial device selector.
    Args:
        None
    Returns:
        The selected serial device as ListPortInfo.
    """
    while True:
        print('Pick the serial device:')
        ports = serial.tools.list_ports.comports()
        for i, port in enumerate(ports):
            print('{}: {}'.format(i, port))

        try:
            chosen_port = ports[int(input())]
            print('Selected {}'.format(chosen_port))
            return chosen_port
        except IndexError:
            print('Invalid device!')
            continue


class SerialDataSource(object):
    """A datasource that reads from a bound serial port interface."""

    def __init__(self, device):
        self.q = deque()
        self.ser = serial.Serial(device, 115200)
        self.running = False
        self.t = None

    def start(self):
        """Starts the packet_service."""
        if self.running:
            return
        self.running = True
        self.t = threading.Thread(target=self.packet_service)
        self.t.start()

    def stop(self):
        self.running = False
        self.t.join()
        self.t = None

    def get_packet(self):
        if self.q:
            return self.q.popleft()

    def packet_service(self):
        # Discard the first packet
        self.ser.readline().decode('ascii')
        while True:
            line = self.ser.readline().decode('ascii')
            if not line:
                continue
            ints = line.split(',')
            l = len(ints)
            if l < 3:
                print(line)
                continue

            axis_char = int(ints[0])
            axis = fiber_reading.Axis.UNKNOWN
            if (axis_char == 0):
                axis = fiber_reading.Axis.X_AXIS
            elif (axis_char == 1):
                axis = fiber_reading.Axis.Y_AXIS

            index = int(ints[1])
            callib = int(ints[2])

            reading = fiber_reading.FiberReading(axis, index, callib)
            for i in range(3, l):
                reading.AddData(int(ints[i]))
            self.q.append(reading)
