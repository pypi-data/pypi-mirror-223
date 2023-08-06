#!/usr/bin/python3
# -*- coding:Utf-8 -*-

# PyScribus, python library for Scribus SLA
# Copyright (C) 2020-2023 Étienne Nadji
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Mathematics related values, functions and enumerations.
"""

# Imports ===============================================================#

import enum
import math

from typing import Union, Literal, Optional

# Global variables / annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# 1 pica point = 25,4/72 milimeters
PICA_TO_MM = 25.4 / 72

# 1 inch = 25,4 milimeters
INCH_TO_MM = 25.4

# 1 cicero = 1.066 picas
CICERO_TO_PICA = 1.066

ConvertableToPicas = Literal["mm", "in", "c"]

# Classes ===============================================================#

class FloatEnum(enum.Enum):
    """
    Enum class usable with float() function / method.
    """

    def __float__(self):
        if isinstance(self.value, float):
            return self.value

        return float(self.value)

# Fonctions =============================================================#


def truncate(number, digits) -> float:
    """
    Truncate value `number` to X `digits` digits.

    From Stack Overflow.

    <https://stackoverflow.com/questions/8595973/truncate-to-three-decimals-in-python>

    :type number: float
    :type digits: int
    :rtype: float
    """

    dec_number = len(str(number).split('.')[1])

    if dec_number <= digits:
        return number

    stepper = 10.0 ** digits

    return math.trunc(stepper * number) / stepper


def necessary_float(f: float) -> Union[float, int]:
    """
    Return **integer** if float f has no decimals, else returns **float**.

    :type f: float
    :param f: Float value
    :rtype: int,float
    :returns: Integer if float f has no decimals, else float.
    """

    if float(f) == int(f):
        return int(f)

    return float(f)


def pica(value: float, unit: ConvertableToPicas) -> float:
    """
    Return value ``value`` in original unit ``unit`` in pica points.

    :rtype: float
    """

    value = float(value)

    if unit == "in":
        return inch(value)
    if unit == "mm":
        return mm(value)
    if unit == "c":
        return cicero(value)

    raise ValueError(f"Unit {unit} not known by pica conversion function.")


def cicero(ciceros: Union[int, float]) -> float:
    """
    Returns ciceros in pica points.

    :type inches: int,float
    :param ciceros: Ciceros
    :rtype: float
    """
    if isinstance(ciceros, int):
        ciceros = float(ciceros)

    return ciceros / CICERO_TO_PICA


def inch(inches: Union[int, float]) -> float:
    """
    Returns inches in pica points.

    :type inches: int,float
    :param inches: Inches
    :rtype: float
    """
    if isinstance(inches, int):
        inches = float(inches)

    return mm(inches / INCH_TO_MM)


def mm(milimeters: Union[int, float]) -> float:
    """
    Returns milimeters in pica points.

    :type milimeters: int,float
    :param milimeters: Milimeters
    :rtype: float
    """
    if isinstance(milimeters, int):
        milimeters = float(milimeters)

    return milimeters / PICA_TO_MM


# Converter classes =====================================================#

class PicaConverter:
    """
    Converter into picas class.

    Define a original units, output picas.
    """

    convertable_units = {
        "millimeters": "mm",
        "inches": "in",
        "ciceros": "c",
    }

    def __init__(self, original_unit: Optional[str] = None):
        self.original_unit = original_unit

    def set_unit(self, original_unit: Optional[str] = None) -> bool:
        for long, short in PicaConverter.convertable_units.items():

            if original_unit == short:
                self.original_unit = long
                break

            if original_unit == long:
                self.original_unit = long
                break

        if self.original_unit is None:
            self.original_unit = None
            return None

        return self.original_unit

    def picas(self, value: Union[int, float]) -> float:
        """
        Return value ``value`` in pica points.

        :rtype: float
        """

        if self.original_unit is None:
            return value

        return pica(value, PicaConverter.convertable_units[self.original_unit])

# vim:set shiftwidth=4 softtabstop=4:
