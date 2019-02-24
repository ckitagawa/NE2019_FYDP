#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
#
# Distributed under terms of the MIT license.
"""Fiber Reading Data Object"""

import enum


class Axis(enum.Enum):
    X_AXIS = 0
    Y_AXIS = 1


class FiberReading(object):
    """Object for storing Fiber Readings"""

    def __init__(self, axis, index, calibration_value):
        """
        Args:
        axis: an instance of Axis
        index: an index for the fiber [0..9]
        calibration_value: a baseline reading on an unstressed fiber
        """
        self.axis = axis
        self.index = index
        self.calibration_value = calibration_value
        self.data = []

    def AddData(self, datum):
        """
        Args:
        datum: a reading from the fiber.
        """
        self.data.append(datum)
