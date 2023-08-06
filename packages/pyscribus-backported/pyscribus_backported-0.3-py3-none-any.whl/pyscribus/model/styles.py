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
PyScribus classes for styles manipulation.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, Optional, NoReturn, Literal
from enum import IntEnum
from pathlib import Path

import lxml
import lxml.etree as ET

import pyscribus.model.common.xml as xmlc
import pyscribus.model.common.math as mathc
import pyscribus.model.logs as logs
import pyscribus.model.exceptions as exceptions
import pyscribus.model.dimensions as dimensions

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

StringOrPath = Union[str, Path]
BoolOrElement = Union[bool, ET.Element]

LeadingMode = Literal["fixed", "automatic", "grid"]

# Classes ===============================================================#


class TextDirection(IntEnum):
    """
    Enum for (paragraph) STYLE/@DIRECTION values.
    """

    LTR = 0
    RTL = 1


class NoteStyle(xmlc.PyScribusElement):
    """SLA notes style (notesStyle)"""

    range_type_xml = {
        "document": "0",
        "section": "1",
        "story": "2",
        "page": "3",
        "form": "4",
    }

    def __init__(self, default: bool = False):
        super().__init__()

        if default:
            self.fromdefault()
        else:
            self.name = ""
            self.set_type("footnote")
            self.num_start = 1
            self.num_type = "decimal"
            self.affixes = {"prefix": "", "suffix": ""}
            self.auto_dims = {"width": True, "height": True}
            self.auto_remove = True
            self.auto_link = True
            self.superscript = {"note": True, "mark": True}
            self.styles = {"mark": "", "note": ""}
            self.range = "document"

    def set_numtype(self, numtype: str) -> bool:
        # if numtype.lower() in NoteStyle.keys():
        if numtype.lower() in xmlc.num_type_xml.keys():
            self.num_type = numtype.lower()
            return True

        return False

    def set_type(self, note_type: str = "footnote") -> NoReturn:
        if note_type.lower() == "footnote":
            self.is_endnotes = False
            self.is_footnotes = True
        else:
            self.is_endnotes = True
            self.is_footnotes = False

    def toxml(self) -> ET.Element:
        xml = ET.Element("notesStyle")

        xml.attrib["Name"] = self.name
        xml.attrib["Start"] = str(self.num_start)
        xml.attrib["Endnotes"] = xmlc.bool_to_num(self.is_endnotes)
        # xml.attrib["Type"] = NoteStyle.num_type_xml[self.num_type]
        xml.attrib["Type"] = xmlc.num_type_xml[self.num_type]
        xml.attrib["Range"] = NoteStyle.range_type_xml[self.range]
        xml.attrib["Prefix"] = self.affixes["prefix"]
        xml.attrib["Suffix"] = self.affixes["suffix"]
        xml.attrib["AutoHeight"] = xmlc.bool_to_num(self.auto_dims["height"])
        xml.attrib["AutoWidth"] = xmlc.bool_to_num(self.auto_dims["width"])
        xml.attrib["AutoRemove"] = xmlc.bool_to_num(self.auto_remove)
        xml.attrib["AutoWeld"] = xmlc.bool_to_num(self.auto_link)
        xml.attrib["SuperNote"] = xmlc.bool_to_num(self.superscript["note"])
        xml.attrib["SuperMaster"] = xmlc.bool_to_num(self.superscript["mark"])
        xml.attrib["MarksStyle"] = self.styles["mark"]
        xml.attrib["NotesStyle"] = self.styles["note"]

        return xml

    def fromxml(self, xml) -> bool:
        self.num_start = int(xml.get("Start"))
        self.name = xml.get("Name")
        self.affixes["prefix"] = xml.get("Prefix")
        self.affixes["suffix"] = xml.get("Suffix")
        self.auto_link = xmlc.num_to_bool(xml.get("AutoWeld"))
        self.auto_remove = xmlc.num_to_bool(xml.get("AutoRemove"))
        self.auto_dims["width"] = xml.get("AutoWidth")
        self.auto_dims["height"] = xml.get("AutoHeight")
        self.superscript["note"] = xmlc.num_to_bool(xml.get("SuperNote"))
        self.superscript["mark"] = xmlc.num_to_bool(xml.get("SuperMaster"))
        self.styles["note"] = xml.get("NotesStyle")
        self.styles["mark"] = xml.get("MarksStyle")

        nt = xml.get("Type")

        # for h,x in NoteStyle.num_type_xml.items():
        for h, x in xmlc.num_type_xml.items():
            if nt == x:
                self.num_type = h
                break

        rg = xml.get("Range")

        for h, x in NoteStyle.range_type_xml.items():
            if rg == x:
                self.range = h
                break

        return True

    def fromdefault(self) -> NoReturn:
        self.name = "Default"
        self.set_type("footnote")
        self.num_start = 1
        self.num_type = "decimal"
        self.affixes = {"prefix": "", "suffix": ")"}
        self.auto_dims = {"width": True, "height": True}
        self.auto_remove = True
        self.auto_link = True
        self.superscript = {"note": True, "mark": True}
        self.styles = {"mark": "", "note": ""}
        self.range = "document"

        return True


# FIXME This is a giant class.
# When styles attributes list will be stable, we will need to :
#   - move the type-specific (to|from)xml code and class attributes to
#     inherited classes. StyleAbstract.toxml() already returns xml Element.
#   - move the type-specific functions to inherited classes


class StyleAbstract(xmlc.PyScribusElement):
    """
    Abstract class for paragraph, character, table, cell styles in SLA.

    :type style_type: str
    :param style_type: Style type. Must be "paragraph", "character",
        "table", "cell".
    :type default: boolean
    :param default: Use default settings (False by default)
    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs tables of inherited classes)
    """

    # TODO Reste des attributs

    type_xml = {
        "paragraph": "STYLE",
        "character": "CHARSTYLE",
        "table": "TableStyle",
        "cell": "CellStyle",
    }

    name_xml = {"NAME": ["paragraph", "table", "cell"], "CNAME": ["character"]}

    shortcut_xml = {"PSHORTCUT": ["paragraph"], "SHORTCUT": ["character"]}

    parent_xml = {"PARENT": ["paragraph"], "CPARENT": ["character"]}

    fshade_xml = {
        "FillShade": ["table", "cell"],
        "FSHADE": ["character", "paragraph"],
    }

    fcolor_xml = {
        "FillColor": ["table", "cell"],
        "FCOLOR": ["character", "paragraph"],
    }

    default_name = {
        "paragraph": "Default Paragraph Style",
        "character": "Default Character Style",
        "table": "Default Table Style",
        "cell": "Default Cell Style",
    }

    bg_color_xml = {"BCOLOR": ["paragraph"], "BGCOLOR": ["character"]}
    bg_shade_xml = {"BSHADE": ["paragraph"], "BGSHADE": ["character"]}

    default_font = {
        "name": "Arial Regular",
        "size": 12,
        "features": [],
        "color": "Black",
        "alignment": "left",
    }

    def __init__(self, style_type, doc_parent, default=False, **kwargs):
        super().__init__()

        self.doc_parent = doc_parent

        if not style_type.lower() in StyleAbstract.type_xml.keys():
            raise ValueError("Unknown style type for StyleAbstract")

        self.style_type = style_type.lower()

        self.name = ""
        self.parent = None

        self.is_default = False

        if self.style_type in ["paragraph", "character"]:
            # TODO FIXME Handle font features as a dict instead
            # of a list, like in other styles
            # Features: -clig, inherit

            self.font = {
                "name": "",
                "size": dimensions.Dim(0, unit="pt"),
                "features": [],
                "color": "",
                "alignment": "left",
                "strike": {"width": None, "offset": None},
                "underline": {"width": None, "offset": None},
                "shadow": {"hoffset": None, "voffset": None},
                # NOTE There is no offset setting for outline, obviously
                "outline": {"width": None},
                "kerning": None,
            }

            # NOTE Weird, but FONTFEATURES is not the same as FEATURES
            # even if it has obviously an effect on fonts...
            self.features = {}

            self.lang = None
            self.shortcut = None

            self.background = {
                "color": "None",
                "shade": dimensions.Dim(100, unit="pc", integer=True),
            }

        if self.style_type in ["table", "cell", "character", "paragraph"]:
            self.fill = {"color": None, "shade": None}

        if self.style_type in ["table", "cell"]:
            self.borders = []

        if self.style_type == "cell":
            self.padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

        if self.style_type == "paragraph":
            self.tabs = []
            self.character_parent = ""

            self.space = {
                "after": None,
                "before": None,
            }

            self.leading = {"mode": "fixed", "value": dimensions.Dim(0)}

        if default:
            self.fromdefault()

        if kwargs:
            self._quick_setup(kwargs)

    def _quick_setup(self, settings: dict) -> NoReturn:
        """
        Method for defining style settings from class
        instanciation kwargs.

        :type settings: dict
        :param settings: Kwargs dictionnary
        """

        if not settings:
            return

        xmlc.PyScribusElement._quick_setup(self, settings)

        for setting_name, setting_value in settings.items():

            if self.style_type in ["paragraph", "character"]:

                if setting_name == "defaultstyle":
                    if setting_value:
                        self.is_default = True
                    else:
                        self.is_default = False

            if setting_name == "name":
                self.name = setting_value

            if setting_name == "parent":
                self.parent = setting_value

            if self.style_type in ["paragraph", "character"]:

                if setting_name == "fontsize":
                    self.font["size"] = setting_value

                if setting_name == "font":
                    self.font["name"] = setting_value

    def _choose_att(self, atts_dict: dict) -> str:
        """
        Returns the correct XML attribute according to the
        StyleAbstract *class* attribute atts_dict.
        """
        for att, types in atts_dict.items():
            if self.style_type in types:
                return att

        return False

    def fromdefault(self) -> bool:
        self.name = StyleAbstract.default_name[self.style_type]

        if self.style_type in ["paragraph", "character"]:
            self.font |= StyleAbstract.default_font

        # TODO Le reste

        return True

    def fromxml(
        self, xml: ET.Element, onlybool: bool = False
    ) -> BoolOrElement:

        if xml.tag != StyleAbstract.type_xml[self.style_type]:
            return False

        # Name -------------------------------------------------

        if self.style_type in ["paragraph", "table", "cell", "character"]:
            name_att = self._choose_att(StyleAbstract.name_xml)

        name = xml.get(name_att)
        if name is not None:
            self.name = name

        # Common attributes ------------------------------------

        default = xml.get("DefaultStyle")
        if default is not None:
            self.is_default = xmlc.num_to_bool(default)

        # Specific attributes for paragraph --------------------
        # Moved in ParagraphStyle

        # Specific attributes for character --------------------
        # Moved in CharacterStyle

        # Specific attributes for table ------------------------

        if self.style_type == "table":
            pass

        # Specific attributes for cell -------------------------
        # Moved in CellStyle

        # Common attributes to paragraphs + characters ---------

        if self.style_type in ["paragraph", "character"]:

            bshade_att = self._choose_att(StyleAbstract.bg_shade_xml)
            bcolor_att = self._choose_att(StyleAbstract.bg_color_xml)

            back_color = xml.get(bcolor_att)
            if back_color is not None:
                self.background["color"] = back_color

            back_shade = xml.get(bshade_att)
            if back_shade is not None:
                self.background["shade"].value = float(back_shade)

            # Font and font features ---------------------------------

            font = xml.get("FONT")
            if font is not None:
                self.font["name"] = font

            font_size = xml.get("FONTSIZE")
            if font_size is not None:
                self.font["size"].value = float(font_size)

            font_features = xml.get("FONTFEATURES")
            if font_features is not None:
                self.font["features"] = font_features.split(",")

            font_color = xml.get("FCOLOR")
            if font_color is not None:
                self.font["color"] = font_color

            # NOTE Weird FEATURES duplicate
            features = xml.get("FEATURES")
            if features is not None:
                self.features = features

            strike_width = xml.get("TXTSTW")
            if strike_width is not None:
                self.font["strike"]["width"] = dimensions.Dim(
                    float(strike_width), unit="pcdecim"
                )

            strike_offset = xml.get("TXTSTP")
            if strike_offset is not None:
                self.font["strike"]["offset"] = dimensions.Dim(
                    float(strike_offset), unit="pcdecim"
                )

            underline_width = xml.get("TXTULW")
            if underline_width is not None:
                self.font["underline"]["width"] = dimensions.Dim(
                    float(underline_width), unit="pcdecim"
                )

            underline_offset = xml.get("TXTULP")
            if underline_offset is not None:
                self.font["underline"]["offset"] = dimensions.Dim(
                    float(underline_offset), unit="pcdecim"
                )

            shadow_hoffset = xml.get("TXTSHX")
            if shadow_hoffset is not None:
                self.font["shadow"]["hoffset"] = dimensions.Dim(
                    float(shadow_hoffset), unit="pcdecim"
                )

            shadow_voffset = xml.get("TXTSHY")
            if shadow_voffset is not None:
                self.font["shadow"]["voffset"] = dimensions.Dim(
                    float(shadow_voffset), unit="pcdecim"
                )

            outline_width = xml.get("TXTOUT")
            if outline_width is not None:
                self.font["outline"]["width"] = dimensions.Dim(
                    float(outline_width), unit="pcdecim"
                )

            kerning = xml.get("KERN")
            if kerning is not None:
                self.font["kerning"] = dimensions.Dim(
                    float(kerning), unit="pc"
                )

            # Lang ---------------------------------------------------

            lang = xml.get("LANGUAGE")
            if lang is not None:
                if lang:
                    self.lang = lang

            # Parent style -------------------------------------------

            parent_att = self._choose_att(StyleAbstract.parent_xml)

            parent = xml.get(parent_att)
            if parent is not None:
                if parent:
                    self.parent = parent

            # Shortcut -----------------------------------------------

            shortcut_att = self._choose_att(StyleAbstract.shortcut_xml)

            shortcut = xml.get(shortcut_att)
            if shortcut is not None:
                if shortcut:
                    self.shortcut = shortcut

        # Common attributes to tables, celles, characters ------

        if self.style_type in ["table", "cell", "character", "paragraph"]:
            fshade_att = self._choose_att(StyleAbstract.fshade_xml)
            fcolor_att = self._choose_att(StyleAbstract.fcolor_xml)

            fill_color = xml.get(fcolor_att)
            if fill_color is not None:
                self.fill["color"] = fill_color

            fill_shade = xml.get(fshade_att)
            if fill_shade is not None:
                self.fill["shade"] = float(fill_shade)

        # Childs -----------------------------------------------

        # Moved StyleTabs check in ParagraphStyle

        # ------------------------------------------------------

        # FIXME This records undocumented attributes -----------

        if self.style_type not in ["character", "paragraph"]:
            self.undocumented = xmlc.all_undocumented_to_python(xml)

        # ------------------------------------------------------

        # Returns lxml.etree._Element instead of True, for
        # inheritance purposes

        if onlybool:
            return True

        return xml

    def toxml(self) -> ET.Element:
        xml = ET.Element(StyleAbstract.type_xml[self.style_type])

        # Name -------------------------------------------------

        if self.style_type in ["paragraph", "table", "cell", "character"]:
            name_att = self._choose_att(StyleAbstract.name_xml)

        xml.attrib[name_att] = self.name

        # Common attributes ------------------------------------

        if self.is_default:
            xml.attrib["DefaultStyle"] = xmlc.bool_to_num(self.is_default)

        # Specific attributes for table ------------------------

        if self.style_type == "table":
            pass

        # Common attributes to paragraphs + characters ---------

        if self.style_type in ["paragraph", "character"]:

            bshade_att = self._choose_att(StyleAbstract.bg_shade_xml)
            bcolor_att = self._choose_att(StyleAbstract.bg_color_xml)

            if self.background["color"] == "None":
                xml.attrib[bcolor_att] = "None"
            else:
                xml.attrib[bcolor_att] = self.background["color"]

            if self.background["shade"].value <= 100:
                xml.attrib[bshade_att] = self.background["shade"].toxmlstr(True)

            if self.font["name"]:
                xml.attrib["FONT"] = self.font["name"]

            if self.style_type == "character":
                xml.attrib["FONTSIZE"] = self.font["size"].toxmlstr(True)

            # TODO FIXME Handle font features as a dict instead
            # of a list, like in other styles
            # xml.attrib["FONTFEATURES"] = " ".join(self.font["features"].keys())

            if self.font["features"]:
                xml.attrib["FONTFEATURES"] = ",".join(self.font["features"])

            if self.font["color"]:
                xml.attrib["FCOLOR"] = self.font["color"]

            if self.font["strike"]["width"] is not None:
                xml.attrib["TXTSTW"] = self.font["strike"]["width"].toxmlstr(
                    True
                )

            if self.font["strike"]["offset"] is not None:
                xml.attrib["TXTSTP"] = self.font["strike"]["offset"].toxmlstr(
                    True
                )

            if self.font["shadow"]["hoffset"] is not None:
                xml.attrib["TXTSHX"] = self.font["shadow"]["hoffset"].toxmlstr(
                    True
                )

            if self.font["shadow"]["voffset"] is not None:
                xml.attrib["TXTSHY"] = self.font["shadow"]["voffset"].toxmlstr(
                    True
                )

            if self.font["outline"]["width"] is not None:
                xml.attrib["TXTOUT"] = self.font["outline"]["width"].toxmlstr(
                    True
                )

            if self.font["underline"]["width"] is not None:
                xml.attrib["TXTULW"] = self.font["underline"][
                    "width"
                ].toxmlstr(True)

            if self.font["underline"]["offset"] is not None:
                xml.attrib["TXTULP"] = self.font["underline"][
                    "offset"
                ].toxmlstr(True)

            if self.font["kerning"] is not None:
                xml.attrib["KERN"] = self.font["kerning"].toxmlstr(True)

            if self.features:
                xml.attrib["FEATURES"] = self.features

            if self.lang is not None:
                xml.attrib["LANGUAGE"] = self.lang

            if self.shortcut is not None:
                shortcut_att = self._choose_att(StyleAbstract.shortcut_xml)
                xml.attrib[shortcut_att] = self.shortcut

            if self.parent is not None:
                # Parent style of same style type
                # CPARENT -> parent character style for this character style
                # PARENT  -> parent paragraph style for this paragraph style
                parent_att = self._choose_att(StyleAbstract.parent_xml)
                xml.attrib[parent_att] = self.parent

        # Common attributes to tables, celles, characters ------

        if self.style_type in ["table", "cell", "character"]:
            fshade_att = self._choose_att(StyleAbstract.fshade_xml)
            fcolor_att = self._choose_att(StyleAbstract.fcolor_xml)

            xml.attrib[fcolor_att] = xmlc.none_or_str(self.fill["color"])

            if self.fill["shade"] is not None:
                xml.attrib[fshade_att] = xmlc.float_or_int_string(
                    self.fill["shade"]
                )

        # ------------------------------------------------------

        # FIXME This exports undocumented attributes ----------

        try:
            if self.style_type not in ["paragraph", "character"]:
                xml, undoc_attribs = xmlc.all_undocumented_to_xml(
                    xml,
                    self.undocumented,
                    True,
                    self.style_type + " style " + self.name,
                    logger=logs.getLogger(),
                )

        except AttributeError:
            # NOTE If fromxml was not used
            pass

        return xml

    def fromstyle(self, style, override: bool = False):
        """
        Set attributes according to another style.

        :type style: ParagraphStyle, CharacterStyle, ...
        :param style: Style to load attributes from.
        :type override: boolean
        :param override: Override attributes that differs from style
        """
        # TODO
        pass


class ParagraphStyle(StyleAbstract):
    """
    Paragraph style in SLA (STYLE)

    :type default: boolean
    :param default: Use default settings (False by default)
    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +--------------+------------------------------------+
    | Kwargs       | Setting                            |
    +==============+====================================+
    | name         | Style name                         |
    +--------------+------------------------------------+
    | defaultstyle | Scribus default paragraph style?   |
    +--------------+------------------------------------+
    | parent       | Parent style name (paragraph)      |
    +--------------+------------------------------------+
    | cparent      | Parent style name (character)      |
    +--------------+------------------------------------+
    | alignment    | Text alignment. Must be in         |
    |              | ``pyscribus.common.xml.alignment`` |
    |              | keys                               |
    +--------------+------------------------------------+
    | direction    | Text direction. Either "ltr"       |
    |              | (left to right) or "rtl" (right to |
    |              | left.                              |
    +--------------+------------------------------------+
    | font         | Font name                          |
    +--------------+------------------------------------+
    | fontsize     | Font size                          |
    +--------------+------------------------------------+
    | spacebefore  | Space before paragraph             |
    +--------------+------------------------------------+
    | spaceafter   | Space after paragraph              |
    +--------------+------------------------------------+
    | leading      | Leading mode. Must be in           |
    |              | ``ParagraphStyle.leading_xml``.    |
    |              | If "fixed" mode, you must define   |
    |              | leadingValue setting.              |
    +--------------+------------------------------------+
    | leadingValue | Leading value in pica points if    |
    |              | leading mode is "fixed".           |
    +--------------+------------------------------------+
    | default      | Equivalent to a fromdefault        |
    |              | call, value being True or the      |
    |              | default name                       |
    +--------------+------------------------------------+

    :Example:

    .. code:: python

       title_style = styles.ParagraphStyle(
           name="Title", fontsize=18, alignment="center",
           leading="fixed", leadingValue=16
       )

       normal_style = styles.ParagraphStyle(
           name="Normal", fontsize=12, alignment="justify",
           leading="automatic"
       )

    """

    leading_xml = {
        "fixed": "0",
        "automatic": "1",
        "grid": "2",
    }

    glyph_scale_xml = {
        "max": "MaxGlyphExtend",
        "min": "MinGlyphShrink",
    }

    optical_margins_xml = {
        "both": "14",
        "left": "4",
        "right": "8",
        "none": "0",
        "undef": None,
    }

    ol_types = {
        "decimal": "0",
        "decimal-ar": "1",
        "lower-roman": "2",
        "upper-roman": "3",
        "lower-latin": "4",
        "upper-latin": "5",
        "alpha-ar": "6",
        "abjad-ar": "7",
        # SEUL CONTRE LES DIEUX CONTRE L'ODIEUX CESAR
        "asterix": "8",
        "cjk": "9",
        "hebrew": "10",
    }

    def __init__(self, doc_parent, default=False, **kwargs):
        StyleAbstract.__init__(self, "paragraph", doc_parent, default)

        self.indentations = {"left": None, "right": None, "first-line": None}

        self.listing = {"type": None, "char": None, "subtype": None}

        self.hyphen_following_lines = None

        self.glyph_scaling = {
            "min": dimensions.Dim(1.0, unit="pcscale"),
            "max": dimensions.Dim(1.0, unit="pcscale"),
        }

        self.initial = {
            "active": False,
            "lines": 2,
            "offset": dimensions.Dim(0),
            # NOTE The initial capital offset is documented as @DROPDIST but
            # implemented as @ParagraphEffectOffset so we store the attribute
            # used in the file for later.
            "__offset_att": "paragrapheffectoffset",
            # NOTE If there no auto_indent set, the value is not saved in SLA file.
            "auto_indent": False,
        }

        self.optical_margins = ParagraphStyle.optical_margins_xml["undef"]
        self.text_direction = TextDirection.LTR

        self._quick_setup(kwargs)

    def fromxml(self, xml: ET.Element) -> bool:
        is_paragraph = StyleAbstract.fromxml(self, xml, True)

        if not is_paragraph:
            return False

        # Hyphenation ---------------------------------------------------

        hyphen_lines = xml.get("HyphenConsecutiveLines")
        if hyphen_lines is not None:
            try:
                hyphen_lines = int(hyphen_lines)

                self.hyphen_following_lines = hyphen_lines
            except ValueError:
                self.hyphen_following_lines = 2

        # Text direction ------------------------------------------------

        text_direction = xml.get("DIRECTION")
        if text_direction is not None:

            if xmlc.num_to_bool(text_direction):
                self.text_direction = TextDirection.RTL
            else:
                self.text_direction = TextDirection.LTR

        # Optical margins -----------------------------------------------

        optic_margin = xml.get("OpticalMargins")
        if optic_margin is None:
            self.optical_margins = "undef"
        else:
            for human, value in ParagraphStyle.optical_margins_xml.items():
                if value is None or value != optic_margin:
                    continue

                self.optical_margins = human
                break

        # Initial capital (aka drop capital) ----------------------------

        initial_used = xml.get("DROP")
        if initial_used is not None:
            self.initial["active"] = xmlc.num_to_bool(initial_used)

        initial_lines = xml.get("DROPLIN")
        if initial_lines is not None:
            self.initial["lines"] = int(initial_lines)

        initial_indent = xml.get("ParagraphEffectIndent")
        if initial_indent is not None:
            self.initial["auto_indent"] = xmlc.num_to_bool(initial_indent)

        for att_name in ["ParagraphEffectOffset", "DROPDIST"]:
            initial_offset = xml.get(att_name)
            if initial_offset is not None:
                self.initial["__offset_att"] = att_name
                self.initial["offset"].value = float(initial_offset)
                break

        # Glyph scaling -------------------------------------------------

        mgs = xml.get("MinGlyphShrink")
        if mgs is not None:
            self.glyph_scaling["min"].value = float(mgs)

        mge = xml.get("MaxGlyphExtend")
        if mge is not None:
            self.glyph_scaling["max"].value = float(mge)

        # Indentation ---------------------------------------------------

        # Left indentation of all paragraph lines

        left = xml.get("INDENT")
        if left is not None:
            self.indentations["left"] = dimensions.Dim(float(left))

        # Right indentation of all paragraph lines

        right = xml.get("RMARGIN")
        if righ is not None:
            self.indentations["right"] = dimensions.Dim(float(right))

        # Indentation of the first line of the paragraph

        first = xml.get("FIRST")
        if first is not None:
            self.indentations["first-line"] = dimensions.Dim(
                float(first), negative=True
            )

        # Lists ---------------------------------------------------------

        is_ul, is_ol = False, False

        is_bullet = xml.get("Bullet")
        if is_bullet is not None:
            if is_bullet == "1":
                self.listing["type"] = "ul"
                is_ul = True

        is_numeroted = xml.get("Numeration")
        if is_numeroted is not None:
            if is_numeroted == "1":
                self.listing["type"] = "ol"
                is_ol = True

        num_format = xml.get("NumerationFormat")
        if num_format is not None:
            if is_ol:
                for human, code in ParagraphStyle.ol_types.items():
                    if code == num_format:
                        self.listing["subtype"] = human
                        break

        if is_ol and is_ul:
            raise exceptions.InsaneSLAValue(
                "Style {} is both bullet and numeroted list.".format(self.name)
            )

        bullet_char = xml.get("BulletStr")
        if bullet_char is not None:
            self.listing["char"] = bullet_char

        # Parent character style ----------------------------------------

        character_parent = xml.get("CPARENT")
        if character_parent is not None:
            self.character_parent = character_parent

        # Leading -------------------------------------------------------

        leading = xml.get("LINESPMode")
        if leading is not None:

            for human, code in ParagraphStyle.leading_xml.items():
                if leading == code:
                    self.leading["mode"] = human
                    break

        leading_value = xml.get("LINESP")
        if leading_value is not None:
            # NOTE Leading value unit is pica in fixed mode, in points in
            #      automatic mode.
            if self.leading["mode"] == "automatic":
                self.leading["value"].set_unit("pt")

            if self.leading["mode"] in ["fixed", "automatic"]:
                self.leading["value"].value = float(leading_value)

        # Alignment -----------------------------------------------------

        alignment = xml.get("ALIGN")
        if alignment is not None:
            for human, code in xmlc.alignment.items():
                if alignment == code:
                    self.font["alignment"] = human
                    break

        # Spaces before and after paragraph -----------------------------

        for case in [["VOR", "before"], ["NACH", "after"]]:

            space_att = xml.get(case[0])
            if space_att is not None:
                self.space[case[1]] = dimensions.Dim(float(space_att))

        # Tabs ----------------------------------------------------------

        for child in xml:

            if child.tag == "Tabs":
                to = StyleTab()

                success = to.fromxml(child)
                if success:
                    self.tabs.append(to)

        # End of parsing ------------------------------------------------

        self.undocumented = xmlc.all_undocumented_to_python(xml)

        return True

    def toxml(self) -> ET.Element:
        xml = StyleAbstract.toxml(self)

        # Text direction ------------------------------------------------

        xml.attrib["DIRECTION"] = str(int(self.text_direction))

        # Hyphenation ---------------------------------------------------

        if self.hyphen_following_lines is not None:
            xml.attrib["HyphenConsecutiveLines"] = str(
                self.hyphen_following_lines
            )

        # Optical margins -----------------------------------------------

        if self.optical_margins is not None:
            if self.optical_margins != "undef":
                xml.attrib["OpticalMargins"] = str(
                    ParagraphStyle.optical_margins_xml[self.optical_margins]
                )

        # Initial capital (aka drop capital) ----------------------------

        xml.attrib["DROP"] = xmlc.bool_to_num(self.initial["active"])
        xml.attrib["DROPLIN"] = str(self.initial["lines"])

        xml.attrib[self.initial["__offset_att"]] = self.initial[
            "offset"
        ].toxmlstr(True)

        if self.initial["auto_indent"]:
            xml.attrib["ParagraphEffectIndent"] = xmlc.bool_to_num(
                self.initial["auto_indent"]
            )

        # Glyph scaling ---------------------------------------------

        for human, att in ParagraphStyle.glyph_scale_xml.items():
            if self.glyph_scaling[human].value != 1.0:
                xml.attrib[att] = self.glyph_scaling[human].toxmlstr()

        # -----------------------------------------------------------

        xml.attrib["ALIGN"] = xmlc.alignment[self.font["alignment"]]

        if self.leading["mode"] is not None:
            xml.attrib["LINESPMode"] = ParagraphStyle.leading_xml[
                self.leading["mode"]
            ]

        if self.leading["mode"] in ["fixed", "automatic"]:
            if self.leading["value"].value > 0:
                xml.attrib["LINESP"] = self.leading["value"].toxmlstr(True)

        # Indentation -----------------------------------------------

        for case in [
            ["left", "INDENT"],
            ["right", "RMARGIN"],
            ["first-line", "FIRST"],
        ]:

            if self.indentations[case[0]] is None:
                xml.attrib[case[1]] = "0"
            else:
                xml.attrib[case[1]] = self.indentations[case[0]].toxmlstr(True)

        # Lists ---------------------------------------------------------

        if self.listing["type"] == "ol":
            att_seq = [False, True]
        elif self.listing["type"] == "ul":
            att_seq = [True, False]
        else:
            att_seq = [False, False]

        for list_val, list_att in zip(att_seq, ["Bullet", "Numeration"]):
            xml.attrib[list_att] = xmlc.bool_to_num(list_val)

        if self.listing["type"] == "ol":
            xml.attrib["NumerationFormat"] = ParagraphStyle.ol_types[
                self.listing["subtype"]
            ]

        if self.listing["type"] is not None:
            xml.attrib["BulletStr"] = xmlc.none_or_str(self.listing["char"])

        # Parent character style ------------------------------------

        # NOTE To not confuse with parent paragraph style which is
        # in @PARENT, and handled in StyleAbstract

        if self.character_parent:
            xml.attrib["CPARENT"] = self.character_parent

        for case in [["before", "VOR"], ["after", "NACH"]]:
            if self.space[case[0]] is not None:
                xml.attrib[case[1]] = self.space[case[0]].toxmlstr(True)

        # xml.attrib["VOR"] = self.space["before"].toxmlstr()
        # xml.attrib["NACH"] = self.space["after"].toxmlstr()

        # FONT SIZE -------------------------------------------------

        font_size = str(self.font["size"]).strip()

        if font_size != "0":
            xml.attrib["FONTSIZE"] = str(
                mathc.necessary_float(float(font_size))
            )

            if self.character_parent:
                # If the font size of the paragraph is not defined
                # because it is defined in a parent character style,
                # don't write FONTSIZE attribute
                pass

        # -----------------------------------------------------------

        try:
            xml, undoc_attribs = xmlc.all_undocumented_to_xml(
                xml,
                self.undocumented,
                True,
                self.style_type + " style " + self.name,
                logger=logs.getLogger(),
            )

        except AttributeError:
            # NOTE If fromxml was not used
            pass

        return xml

    def fromdefault(self) -> bool:
        StyleAbstract.fromdefault(self)

        self.leading = {"mode": None, "value": dimensions.Dim(12)}

        return True

    def _quick_setup(self, settings: dict) -> NoReturn:
        """
        Method for defining style settings from class
        instanciation kwargs.

        :type settings: dict
        :param settings: Kwargs dictionnary
        """

        if not settings:
            return

        StyleAbstract._quick_setup(self, settings)

        for setting_name, setting_value in settings.items():

            if setting_name == "direction":
                setting_value = setting_value.strip().lower()

                if setting_value in ["ltr", "rtl"]:
                    if setting_value == "ltr":
                        self.text_direction = TextDirection.LTR
                    else:
                        self.text_direction = TextDirection.RTL
                else:
                    raise ValueError(
                        "Wrong direction setting '{}'. "
                        "Use either 'ltr' (left to right) 'rtl' "
                        "(right to left).".format(setting_value)
                    )

            if setting_name == "spacebefore":
                self.space["before"] = dimensions.Dim(float(setting_value))

            if setting_name == "spaceafter":
                self.space["after"] = dimensions.Dim(float(setting_value))

            if setting_name == "cparent":
                self.character_parent = setting_value

            if setting_name == "leading":
                if setting_value in ParagraphStyle.leading_xml:
                    self.leading["mode"] = setting_value

            if setting_name == "leadingValue":
                self.leading["value"] = dimensions.Dim(float(setting_value))

            if setting_name == "alignment":

                if setting_value.lower() in xmlc.alignment.keys():
                    self.font["alignment"] = setting_value
                else:
                    raise ValueError(
                        "Wrong alignement setting '{}'. "
                        "Alignement setting must be {}".format(
                            setting_value, ", ".join(xmlc.alignment.keys())
                        )
                    )

    def set_leadingmode(self, leadingmode: LeadingMode) -> bool:
        """
        Set leading mode.

        :type leadingmode: string
        :param leadingmode: "fixed", "automatic", "grid"
        """

        if leadingmode.lower() in ParagraphStyle.leading_xml:
            self.leading["mode"] = leadingmode
            return True

        raise ValueError()


class CharacterStyle(StyleAbstract):
    """
    Character style in SLA (CHARSTYLE)

    :type default: boolean
    :param default: Use default settings (False by default)
    :type kwargs: dict
    :param kwargs: Quick setting (see kwargs table)

    +--------------+-----------------------------+----------+
    | Kwargs       | Setting                     | Type     |
    +==============+=============================+==========+
    | name         | Style name                  | string   |
    +--------------+-----------------------------+----------+
    | defaultstyle | Scribus default character   | boolean  |
    |              | style ?                     | boolean  |
    +--------------+-----------------------------+----------+
    | parent       | Parent style name           | string   |
    +--------------+-----------------------------+----------+
    | font         | Font name                   | string   |
    +--------------+-----------------------------+----------+
    | fontsize     | Font size                   | string   |
    +--------------+-----------------------------+----------+
    | default      | Equivalent to a fromdefault | boolean, |
    |              | call, value being True or   | string   |
    |              | the default name.           |          |
    +--------------+-----------------------------+----------+
    """

    scale_xml = {
        "SCALEH": "horizontal",
        "SCALEV": "vertical",
        "BASEO": "baseline_offset",
    }

    def __init__(self, doc_parent, default=False, **kwargs):
        StyleAbstract.__init__(self, "character", doc_parent, default)
        StyleAbstract._quick_setup(self, kwargs)

        self.font["space_width"] = dimensions.Dim(1, unit="pcdecim")

        self.hyphen_word_min = None

        self.scale = {
            "horizontal": 100,
            "vertical": 100,
            "baseline_offset": 0,
        }

        self.stroke = {
            "color": "Black",
            "shade": dimensions.Dim(100, unit="pc", integer=True),
        }

    def fromxml(self, xml: ET.Element) -> bool:
        is_character = StyleAbstract.fromxml(self, xml, True)

        if not is_character:
            return False

        # Stroke settings -----------------------------------------------

        stroke_color = xml.get("SCOLOR")
        if stroke_color is not None:
            self.stroke["color"] = stroke_color

        stroke_shade = xml.get("SSHADE")
        if stroke_shade is not None:
            self.stroke["shade"].value = float(stroke_shade)

        # Hyphenation ---------------------------------------------------

        hyphen_word = xml.get("HyphenWordMin")
        if hyphen_word is not None:
            try:
                word_length = int(hyphen_word)

                if word_length < 3:
                    raise exceptions.InsaneSLAValue(
                        "HyphenWordMin in '{}' character style must be an "
                        "integer >= 3.".format(self.name)
                    )

                self.hyphen_word_min = word_length

            except ValueError:
                raise exceptions.InsaneSLAValue(
                    "HyphenWordMin in '{}' character style must be an "
                    "integer >= 3.".format(self.name)
                )

        # Font settings -------------------------------------------------

        wordtrack = xml.get("wordTrack")
        if wordtrack is not None:
            self.font["space_width"] = dimensions.Dim(
                float(wordtrack), unit="pcdecim"
            )

        # Scales --------------------------------------------------------

        for att, human in CharacterStyle.scale_xml.items():
            scale_att = xml.get(att)
            if scale_att is not None:
                self.scale[human] = float(scale_att)

        # End of parsing ------------------------------------------------

        self.undocumented = xmlc.all_undocumented_to_python(xml)

        return True

    def toxml(self) -> ET.Element:
        xml = StyleAbstract.toxml(self)

        # Stroke settings -----------------------------------------------

        xml.attrib["SCOLOR"] = self.stroke["color"]
        xml.attrib["SSHADE"] = self.stroke["shade"].toxmlstr(True)

        # Hyphenation ---------------------------------------------------

        if self.hyphen_word_min is not None:
            xml.attrib["HyphenWordMin"] = str(self.hyphen_word_min)

        # Font settings -------------------------------------------------

        if self.font["space_width"] is not None:
            if self.font["space_width"].value != 1.0:
                xml.attrib["wordTrack"] = self.font["space_width"].toxmlstr()

        # Scales --------------------------------------------------------

        for att, human in CharacterStyle.scale_xml.items():
            xml.attrib[att] = str(mathc.necessary_float(self.scale[human]))

        # ---------------------------------------------------------------

        try:
            xml, undoc_attribs = xmlc.all_undocumented_to_xml(
                xml,
                self.undocumented,
                True,
                self.style_type + " style " + self.name,
                logger=logs.getLogger(),
            )

        except AttributeError:
            # NOTE If fromxml was not used
            pass

        return xml


class TabularStyleAbstract(StyleAbstract):
    """Abstract middle class for Table and Cell styles."""

    def __init__(self, style_type, doc_parent, default=False, **kwargs):
        StyleAbstract.__init__(self, style_type, doc_parent, default)

    def fromxml(self, xml) -> bool:
        x = StyleAbstract.fromxml(self, xml)

        if len(x) == 0:
            return False

        for border in x:

            if border.tag in TableBorder.sides_xml.values():
                tb = TableBorder()

                success = tb.fromxml(border)
                if success:
                    self.borders.append(tb)

        return True

    def toxml(self) -> ET.Element:
        xml = StyleAbstract.toxml(self)

        for border in self.borders:
            bx = border.toxml()
            xml.append(bx)

        return xml


class TableBorder(xmlc.PyScribusElement):
    """
    Table border settings in SLA
    (TableBorderLeft, TableBorderRight, TableBorderTop, TableBorderBottom)

    :type side: str
    :param side: (Cell) Side of the border
    """

    sides_xml = {
        "left": "TableBorderLeft",
        "right": "TableBorderRight",
        "top": "TableBorderTop",
        "bottom": "TableBorderBottom",
    }

    def __init__(self, side: Optional[str] = False):
        super().__init__()

        if side:
            if side.lower() in TableBorder.sides_xml.keys():
                self.side = side.lower()
            else:
                self.side = False
        else:
            self.side = False

        self.lines = []

        self.width = None

    def fromxml(self, xml: ET.Element) -> bool:
        self.side = False

        # Find the side of the table border -------------------------

        if xml.tag in TableBorder.sides_xml.values():

            for h, x in TableBorder.sides_xml.items():
                if x == xml.tag:
                    self.side = h
                    break

        if not self.side:
            msg = "Invalid side for TableBorder"

            if self.style_type == "table":
                msg += " in TableStyle"

            if self.style_type == "cell":
                msg += " in CellStyle"

            raise exceptions.InsaneSLAValue(msg)

        # If the table border's side was found ----------------------

        # -------------------------------------------------

        width = xml.get("Width")
        if width is not None:
            self.width = dimensions.Dim(float(width))

        # -------------------------------------------------

        for line in xml:

            if line.tag == "TableBorderLine":
                lo = TableBorderLine()

                success = lo.fromxml(line)
                if success:
                    self.lines.append(lo)

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element(TableBorder.sides_xml[self.side])

        if self.width is not None:
            xml.attrib["Width"] = self.width.toxmlstr(True)

        for line in self.lines:
            lx = line.toxml()
            xml.append(lx)

        return xml


class TableBorderLine(xmlc.PyScribusElement):
    """
    Cell border line in SLA (TableBorderLine)
    """

    def __init__(self):
        super().__init__()

        self.width = 0
        self.pen_style = "1"
        self.color = "Black"
        self.shade = 100

    def fromdefault(self) -> NoReturn:
        self.width = 1
        self.pen_style = "1"
        self.color = "Black"
        self.shade = 100

    def fromxml(self, xml: ET.Element) -> bool:
        if xml.tag != "TableBorderLine":
            return False

        width = xml.get("Width")
        if width is not None:
            self.width = float(width)

        color = xml.get("Color")
        if color is not None:
            self.color = color

        shade = xml.get("Shade")
        if shade is not None:
            self.shade = int(shade)

        style = xml.get("PenStyle")
        if style is not None:
            self.pen_style = style

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element("TableBorderLine")

        if float(self.width) == int(self.width):
            xml_width = int(self.width)
        else:
            xml_width = self.width

        xml.attrib["Width"] = str(xml_width)
        xml.attrib["PenStyle"] = str(self.pen_style)
        xml.attrib["Color"] = self.color
        xml.attrib["Shade"] = str(self.shade)

        return xml


class TableStyle(TabularStyleAbstract):
    """
    Table style in  (TableStyle)
    """

    def __init__(self, doc_parent, default=False, **kwargs):
        TabularStyleAbstract.__init__(self, "table", doc_parent, default)


class CellStyle(TabularStyleAbstract):
    """
    Cell style in SLA (CellStyle)
    """

    def __init__(self, doc_parent, default=False, **kwargs):
        TabularStyleAbstract.__init__(self, "cell", doc_parent, default)

    def fromxml(self, xml: ET.Element) -> BoolOrElement:
        success = TabularStyleAbstract.fromxml(self, xml)

        for case in ["left", "right", "top", "bottom"]:
            att = xml.get("{}Padding".format(case.capitalize()))

            if att is not None:
                self.padding[case] = att

        return True

    def toxml(self) -> ET.Element:
        xml = TabularStyleAbstract.toxml(self)

        for case in ["left", "right", "top", "bottom"]:
            att_name = "{}Padding".format(case.capitalize())
            xml.attrib[att_name] = self.padding[case]

        return xml


class StyleTab(xmlc.PyScribusElement):
    tab_type_xml = {
        "left": "0",
        "right": "1",
        "period": "2",
        "comma": "3",
        "center": "4",
    }

    def __init__(self):
        super().__init__()

        self.type = False
        self.fill = False
        self.position = dimensions.Dim(0, unit="pica")

    def fromxml(self, xml: ET.Element) -> bool:
        """"""

        tab_type = xml.get("Type")
        if tab_type is not None:
            try:
                for human, code in StyleTab.tab_type_xml.items():
                    if code == tab_type:
                        self.type = human
                        break

            except IndexError:
                self.type = "left"

        pos = xml.get("Pos")
        if pos is not None:
            pos = float(pos)
            self.position.value = pos

        fill = xml.get("Fill")
        if fill is not None:
            self.fill = fill

        return True

    def toxml(self) -> ET.Element:
        xml = ET.Element()
        xml.attrib["Type"] = StyleTab.tab_type_xml(self.type)
        xml.attrib["Pos"] = self.position.toxmlstr()
        xml.attrib["Fill"] = self.fill

        return xml

    def fromdefault(self) -> bool:
        self.type = "left"
        self.fill = False
        self.position = dimensions.Dim(0, unit="pica")

        return True


class RuleStyle(xmlc.PyScribusElement):
    """
    Rule style (filet) in SLA (MultiLine)
    """

    def __init__(self):
        super().__init__()

        self.name = None
        self.lines = []

    def fromxml(self, xml: ET.Element) -> bool:
        """"""

        if xml.tag != "MultiLine":
            return False

        name = xml.get("Name")
        if name is not None:
            self.name = name

        for element in xml:

            if element.tag == "SubLine":
                sl = RuleStyleLine()

                success = sl.fromxml(element)
                if success:
                    self.lines.append(sl)

        return True

    def toxml(self) -> ET.Element:
        """"""

        xml = ET.Element("MultiLine")
        xml.attrib["Name"] = self.name

        for line in self.lines:
            lx = line.toxml()
            xml.append(lx)

        return xml


class RuleStyleLine(xmlc.PyScribusElement):
    """
    Sub-line in rule style in SLA (MultiLine/SubLine)
    """

    # Line end human <-> XML
    lineend_xml = {"square": "16", "round": "32", "flat": "0"}

    # Line join human <-> XML
    linejoin_xml = {"pointy": "0", "bevelled": "64", "round": "128"}

    # Line style human <-> XML
    dash_xml = {
        # Most common and named line styles
        "line": "1",
        "dashed": "2",
        "dots": "3",
        "line-dash": "4",
        "line-dash-dash": "5",
        # Here be dragons, and a lot of untitled line styles
        "untitled-6": "6",
        "untitled-7": "7",
        "untitled-8": "8",
        "untitled-9": "9",
        "untitled-10": "10",
        "untitled-11": "11",
        "untitled-12": "12",
        "untitled-13": "13",
        "untitled-14": "14",
        "untitled-15": "15",
        "untitled-16": "16",
        "untitled-17": "17",
        "untitled-18": "18",
        "untitled-19": "19",
        "untitled-20": "20",
        "untitled-21": "21",
        "untitled-22": "22",
        "untitled-23": "23",
        "untitled-24": "24",
        "untitled-25": "25",
        "untitled-26": "26",
        "untitled-27": "27",
        "untitled-28": "28",
        "untitled-29": "29",
        "untitled-30": "30",
        "untitled-31": "31",
        "untitled-32": "32",
        "untitled-33": "33",
        "untitled-34": "34",
        "untitled-35": "35",
        "untitled-36": "36",
        "untitled-37": "37",
    }

    def __init__(self):
        super().__init__()

        self.color = None
        self.shortcut = ""

        self.width = None
        self.opacity = None

        self.end = None
        self.join = None
        self.style = None

    def fromdefault(self) -> NoReturn:
        self.end = "flat"
        self.join = "pointy"
        self.opacity = dimensions.Dim(100, unit="pc")

    def fromxml(self, xml: ET.Element) -> bool:
        """ """

        if xml.tag != "SubLine":
            return False

        # --- Shortcut -----------------------------------------------

        shortcut = xml.get("Shortcut")
        if shortcut is not None:
            self.shortcut = shortcut

        # --- Color and opacity --------------------------------------

        color = xml.get("Color")
        if color is not None:
            self.color = color

        opacity = xml.get("Shade")
        if opacity is not None:
            self.opacity = dimensions.Dim(float(opacity), unit="pc")

        # --- Line width ---------------------------------------------

        width = xml.get("Width")
        if width is not None:
            self.width = dimensions.Dim(float(width))

        # --- Line style ---------------------------------------------

        dash = xml.get("Dash")
        if dash is not None:

            for human, code in RuleStyleLine.dash_xml.items():
                if code == dash:
                    self.style = human
                    break

        # --- Line end -----------------------------------------------

        line_end = xml.get("LineEnd")
        if line_end is not None:

            for human, code in RuleStyleLine.lineend_xml.items():
                if code == line_end:
                    self.end = human
                    break

        # --- Line join ----------------------------------------------

        line_join = xml.get("LineJoin")
        if line_join is not None:

            for human, code in RuleStyleLine.linejoin_xml.items():
                if code == line_join:
                    self.join = human
                    break

        return True

    def toxml(self) -> ET.Element:
        """ """

        xml = ET.Element("SubLine")

        # --- Color and opacity --------------------------------------

        if self.color is not None:
            xml.attrib["Color"] = self.color

        if self.opacity is not None:
            xml.attrib["Shade"] = self.opacity.toxmlstr(True)
        else:
            xml.attrib["Shade"] = "100"

        # --- Line style, end, join ----------------------------------

        xml.attrib["Dash"] = RuleStyleLine.dash_xml[self.style]
        xml.attrib["LineEnd"] = RuleStyleLine.lineend_xml[self.end]
        xml.attrib["LineJoin"] = RuleStyleLine.linejoin_xml[self.join]

        # --- Line width ---------------------------------------------

        if self.width is not None:
            xml.attrib["Width"] = self.width.toxmlstr(True)

        # --- Shortcut -----------------------------------------------

        xml.attrib["Shortcut"] = self.shortcut

        return xml


# Fonctions =============================================================#


def fromSLA(
    filepath: StringOrPath = "", slastring: str = ""
) -> Union[dict, bool]:
    """
    Parse a SLA file / string and returns a dictionary of all styles in it.

    :type filepath: string
    :param filepath: SLA filepath
    :type slastring: string
    :param slastring: SLA XML string
    :rtype: dict,boolean
    :returns: Dictionary of styles usable by document.Document, or False
    """

    styles = {
        "note": [],
        "paragraph": [],
        "character": [],
        "table": [],
        "rule": [],
    }

    if filepath:
        xml = ET.parse(str(filepath)).getroot()
    else:
        xml = ET.fromstring(slastring)

    if len(xml):

        for style_type in [
            [TableStyle, "table", "DOCUMENT/TableStyle"],
            [ParagraphStyle, "paragraph", "DOCUMENT/STYLE"],
            [CharacterStyle, "character", "DOCUMENT/CHARSTYLE"],
            [NoteStyle, "note", "DOCUMENT/NotesStyles/notesStyle"],
            [RuleStyle, "rule", "DOCUMENT/MultiLine"],
        ]:

            tmp_styles = xml.findall(style_type[2])

            if len(tmp_styles):

                for style_item in tmp_styles:
                    si = style_type[0]()
                    success = si.fromxml(style_item)

                    if success:
                        styles[style_type[1]].append(si)

        return styles

    return False


# vim:set shiftwidth=4 softtabstop=4 spl=en:
