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
PyScribus

High-level interface to Scribus file module.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

import re
import functools

from typing import Union, Optional, NoReturn, Literal
from pathlib import Path

import lxml.etree as ET

import pyscribus.file.exceptions as pyfe

from pyscribus.file.ui import UI
from pyscribus.file.colors import Colors
from pyscribus.file.stories import Stories
from pyscribus.file.document import Metadatas, Pages
from pyscribus.file.pageobjects import PageObjects
from pyscribus.file.hyphenation import Hyphenation

# TODO Implement those
# from pyscribus.file.document import Fonts, Layers

from pyscribus.model.sla import SLA
from pyscribus.model.common.math import PicaConverter

# Global variables / annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

StringOrPath = Union[str, Path]

UnitString = Literal[
    "points",
    "pt",
    "millimeters",
    "mm",
    "inches",
    "in",
    "picas",
    "p",
    "centimeters",
    "cm",
    "ciceros",
    "c",
]

CodingUnitString = Literal[
    "millimeters",
    "mm",
    "inches",
    "in",
    "ciceros",
    "c",
]

# Classes ===============================================================#


class ScribusFile:
    """
    High-level interface to Scribus file.

    :type filepath: str
    :param filepath: Scribus file path
    :type version: str
    :param version: Scribus version (ex. '1.5.1')
    :type kwargs: dict
    :param kwargs: kwargs

    **Kwargs options :**

    +-----------------------+----------------------------+---------------+
    | Kwarg key             | Use                        | Default value |
    +=======================+============================+===============+
    | templating            | Use templating ?           | ``False``     |
    +-----------------------+----------------------------+---------------+
    | templatingInsensitive | Should in-text templating  | ``False``     |
    |                       | be case insensitive ?      |               |
    +-----------------------+----------------------------+---------------+
    | templatingPattern     | compiled regex to find     | ``\^%\w+%$``  |
    |                       | templated elements         |               |
    |                       | (ex: %TITLE%)              |               |
    +-----------------------+----------------------------+---------------+
    | units                 | Units used in the document | ``"points"``  |
    +-----------------------+----------------------------+---------------+
    """

    def __init__(
        self, version: str, load: Optional[StringOrPath] = None, **kwargs
    ):
        # “Low-level” representation of Scribus format
        self.model = None

        self.settings = {
            "coding_unit": None,
        }

        self.pica_converter = PicaConverter()

        # Templating --------------------------------------------------------

        self.templating = {
            "active": False,
            # In text templating sequences are like %Title%
            # "intext-pattern": re.compile("^%\w+%$"),
            "intext-pattern": re.compile("(%\w+%)+"),
            # %Title% = %title% = %TITLE% ?
            "intext-insensitive": False,
            # Page object attribute templating names are like %Title%
            "attribute-pattern": re.compile("(%\w+%)+"),
            # dict for evaluating an item attribute value as python boolean
            "attribute-eval-bool-keywords": {"true": "True", "false": "False"},
            # Insensitive item attribute value evaluation as boolean ?
            "attribute-eval-bool-insensive": False,
        }

        for argname, argvalue in kwargs.items():
            if argname == "templating" and argvalue:
                self.templating["active"] = True

            if argname == "templatingInsensitive" and argvalue:
                self.templating["intext-insensitive"] = True

            if argname == "templatingPattern":
                try:
                    pattern = re.compile(argvalue)
                    self.templating["intext-pattern"] = pattern

                except TypeError as not_re_pattern:
                    raise TypeError(
                        "templating-pattern must be a re pattern string."
                    ) from not_re_pattern

        # -------------------------------------------------------------------

        if load is None:
            self.model = SLA(filepath=None, version=version)
        else:
            self.load(load, version)

        # -------------------------------------------------------------------

        ensure_model = kwargs.get("ensure_model")

        if ensure_model is None:
            ensure_model = True
        else:
            ensure_model = bool(ensure_model)

        if self.model is None and ensure_model:
            raise pyfe.NoModelError(
                "No underlying model found in this ScribusFile."
            )

        # if self.model:
        # self.model.templating = self.templating

        # Handling other arguments in kwargs --------------------------------

        if kwargs:
            self._quick_setup(kwargs)

    # Initialisation methods ---------------------------------------------

    def _quick_setup(self, settings: dict) -> NoReturn:
        for setting_name, setting_value in settings.items():
            # Document units ----------------------------------------------

            if setting_name == "unit":
                self.set_units(setting_value)

            # Settings unit -----------------------------------------------

            if setting_name == "coding_unit":
                self.set_coding_unit(setting_value)

    @pyfe.has_model
    def fromdefault(self) -> bool:
        return self.model.fromdefault()

    def load(self, sla_path: StringOrPath, version: str) -> Union[SLA, bool]:
        """
        Load a SLA file from its path ``sla_path``.

        :type sla_path: StringOrPath
        :param sla_path: Path of the SLA file.
        :type version: str
        :param version: Scribus version
        :rtype: Union[SLA, bool]
        :returns: SLA model or ``False``.
        """

        model = SLA(filepath=None, version=version)
        loaded = model.parse(sla_path)

        if loaded:
            self.model = model

            return model

        return False

    # --------------------------------------------------------------------

    @pyfe.has_model
    def set_units(self, unit: UnitString) -> bool:
        """
        Set the unit used in the document.

        +--------------+------------------------------+
        | Unit         | Short form | Long form       |
        +==============+============+=================+
        | Centimeters  | ``cm``     | ``centimeters`` |
        +--------------+------------+-----------------+
        | Ciceros      | ``c``      | ``ciceros``     |
        +--------------+------------+-----------------+
        | Inches       | ``in``     | ``inches``      |
        +--------------+------------+-----------------+
        | Millimeters  | ``mm``     | ``millimeters`` |
        +--------------+------------+-----------------+
        | Picas        | ``p``      | ``millimeters`` |
        +--------------+------------+-----------------+
        | Points       | ``pt``     | ``points``      |
        +--------------+------------+-----------------+

        :rtype: bool
        :returns: Success.
        """
        for model, abrev in [
            ["points", "pt"],
            ["millimeters", "mm"],
            ["inches", "in"],
            ["picas", "p"],
            ["centimeters", "cm"],
            ["ciceros", "c"],
        ]:
            if unit == abrev:
                self.model.document.units = model
                return True

            if unit == model:
                self.model.document.units = model
                return True

        return False

    @pyfe.has_model
    def set_font(self, **kwargs) -> bool:
        """
        .. warning:: Not implemented.

        """
        # """
        # Définit la fonte pour le fichier, le style, l’élément de Story désigné.
        # """
        raise NotImplementedError()

    # XML properties -----------------------------------------------------

    @property
    def xml_loaded(self) -> Union[None, ET.Element]:
        """
        XML node of the source XML file, if it exists.
        """
        return self.model.xml_copy

    @property
    def xml_output(self) -> ET.Element:
        """
        XML node of the document produced by the underlying model.
        """
        return self.model.toxml()

    # Properties ---------------------------------------------------------

    @property
    @pyfe.has_model
    def colors(self):
        """
        Interface to the colors of the document.

        .. seealso:: :class:`pyscribus.file.colors.Colors`
        """
        return Colors(self.model)

    @property
    @pyfe.has_model
    def fonts(self):
        """
        .. warning:: Not implemented.

        Interface to the fonts of the document.
        """
        raise NotImplementedError()

    @property
    @pyfe.has_model
    def hyphenation(self):
        """
        Interface to the hyphenation settings of the document.

        .. seealso:: :class:`pyscribus.file.hyphenation.Hyphenation`
        """
        return Hyphenation(self.model)

    @property
    @pyfe.has_model
    def layers(self):
        """
        .. warning:: Not implemented.

        Interface to the layers of the document.
        """
        raise NotImplementedError()

    @property
    @pyfe.has_model
    def metadatas(self):
        """
        Interface to the metadatas of the document.

        .. seealso:: :class:`pyscribus.file.document.Metadatas`
        """
        return Metadatas(self.model)

    @property
    @pyfe.has_model
    def pageobjects(self) -> list:
        """
        Interface to the page objects of the document.

        .. seealso:: :class:`pyscribus.file.document.PageObjects`
        """
        # return self.model.document.pageobjects(object_type, templatable)
        return PageObjects(self)

    @property
    @pyfe.has_model
    def pages(self):
        """
        Interface to the pages of the document.

        .. seealso:: :class:`pyscribus.file.document.Pages`
        """
        return Pages(self.model)

    @property
    @pyfe.has_model
    def ui(self):
        """
        Interface to the document's settings related to Scribus UI.

        .. seealso:: :class:`pyscribus.file.ui.UI`
        """
        return UI(self)

    # Properties related to stories --------------------------------------

    @property
    @pyfe.has_model
    def stories(self) -> list:
        """
        Interface to all the stories of the document.

        .. seealso:: :class:`pyscribus.file.stories.Stories`
        """
        return Stories(self)

    @property
    @pyfe.has_model
    def templatable_stories(self) -> list:
        """
        Interface to the templatable stories of the document.

        .. seealso:: :class:`pyscribus.file.stories.Stories`
        """
        return Stories(self, templatable=True)

    # PyScribus settings -------------------------------------------------

    def set_coding_unit(self, unit: CodingUnitString) -> NoReturn:
        """
        Set the unit used in programming.

        (You might want to use inches in a document configured for millimeters.)

        +--------------+------------------------------+
        | Unit         | Short form | Long form       |
        +==============+============+=================+
        | Ciceros      | ``c``      | ``ciceros``     |
        +--------------+------------+-----------------+
        | Inches       | ``in``     | ``inches``      |
        +--------------+------------+-----------------+
        | Millimeters  | ``mm``     | ``millimeters`` |
        +--------------+------------+-----------------+
        """
        self.settings["coding_unit"] = self.pica_converter.set_unit(unit)

    # --------------------------------------------------------------------

    @pyfe.has_model
    def save(self, filepath: StringOrPath) -> bool:
        """
        Save the file.

        :type filepath: StringOrPath
        :param filepath: SLA file path
        :rtype: boolean
        :returns: ``True`` if successfull
        """
        return self.model.save(filepath)


# vim:set shiftwidth=4 softtabstop=4 spl=en:
