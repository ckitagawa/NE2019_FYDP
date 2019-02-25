#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.

import logging
import threading
import queue
import serial
import serial.tools.list_ports
import fiber_reading


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
        self.q = queue.Queue()
        self.ser = serial.Serial(device, 115200)
        self.running = False
        self.stop_event = threading.Event()
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
        self.stop_event.set()
        self.t.join()
        self.t = None
        self.stop_event.clear()

    def get_packet(self):
        try:
            return self.q.get(block=False, timeout=1)
        except queue.Empty:
            return None

    def packet_service(self):
        while not self.stop_event.is_set():
            line = self.readline()
            if not line:
                continue
            l = len(line)
            if l < 6:
                continue
            logging.info('{}'.format(line))

            axis_char = line[0:1]
            axis = fiber_reading.Axis.UNKNOWN
            if (axis_char == 'x'):
                axis = fiber_reading.Axis.X_AXIS
            elif (axis_char == 'y'):
                axis = fiber_reading.Axis.Y_AXIS

            index = int.from_bytes(line[1:2], 'little')
            callib = int.from_bytes(line[2:6], 'little')

            reading = fiber_reading.FiberReading(axis, index, callib)
            for i in range(6, l, 4):
                reading.AddData(int.from_bytes(line[i:i + 4], 'little'))
            self.q.put(reading)

    def readline(self, eol=b'\n'):
        """Readline with arbitrary EOL delimiter
        Args:
            ser: Serial device to read
            eol: Bytes to use a EOL delimiter
        Returns:
            All data read from the device until the EOL delimiter was found.
        """
        leneol = len(eol)
        line = bytearray()
        while True:
            read_char = self.ser.read(1)
            if read_char:
                line += read_char
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)
