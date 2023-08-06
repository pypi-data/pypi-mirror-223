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

Scribus file. Stories wrapper.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, Literal

import pyscribus.file as pyf
import pyscribus.file.exceptions as pyfe
import pyscribus.model.stories as model_stories

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

StoryFieldType = Literal["page_number", "page_count"]

# Classes ===============================================================#


class Stories:
    """
    Wrapper around Scribus stories.

    :type file: pyscribus.file.ScribusFile
    :param file: Scribus file wrapper
    :type templatable: bool
    :param templatable: Only load templatable stories

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile
       from pyscribus.file import Paragraph

       doc = ScribusFile("1.5.5", "example.sla")

       len(doc.stories)
       first_story = doc.stories[0]
       text = doc.stories.rawtext(first_story)

       for story in doc.stories.templatable:
           doc.stories.feed(story, data)

       # BELOW THIS LINE, EVERYTHING IS NOT IMPLEMENTED --------

    """

    def __init__(self, file: pyf.ScribusFile, templatable: bool = False):
        self.file = file
        self.model = file.model

        self.only_templatable = templatable

    def __len__(self) -> int:
        """

        :Example:

        .. code:: python

           from pyscribus.file import ScribusFile
           doc = ScribusFile("1.5.5", "example.sla")
           len(doc.stories)

        """
        return len(self.__stories())

    def __getitem__(self, item: int):
        """

        :Example:

        .. code:: python

           from pyscribus.file import ScribusFile
           doc = ScribusFile("1.5.5", "example.sla")
           first_story = doc.stories[0]

        """
        return self.__stories()[item]

    @property
    def items(self) -> list:
        """List of all stories."""
        return self.__stories()

    @property
    def templatable(self) -> list[model_stories.Story]:
        """
        Stories that contains templatable elements.

        :Example:

        .. code:: python

           from pyscribus.file import ScribusFile
           doc = ScribusFile("1.5.5", "example.sla")

           for story in doc.stories.templatable:
               doc.stories.feed(story, data)

        """
        return [
            story
            for story in self.__stories()
            if self.__story_is_templatable(story)
        ]

    def rawtext(self, story: model_stories.Story) -> str:
        """
        Returns a text string equivalent to **what Scribus story editor
        saves** as txt file.

        :Example:

        .. code:: python

           from pyscribus.file import ScribusFile
           doc = ScribusFile("1.5.5", "example.sla")

           story = doc.stories[1]
           text = doc.stories.rawtext(story)

        :rtype: string
        """
        text = ""

        for par in story.bypars():
            for element in par:
                # Text formatting is not saved
                if isinstance(element, model_stories.StoryFragment):
                    text += element.text
                if isinstance(element, model_stories.NonBreakingSpace):
                    text += " "
                # Line breaks are exported by Scribus... as spaces
                if isinstance(element, model_stories.StoryLineBreak):
                    text += " "
                # We dont care about StoryFrameBreak and StoryColumnBreak
                if isinstance(element, model_stories.StoryParagraphEnding):
                    text += "\n"

        return text

    def feed(
        self, story: model_stories.Story, datas: dict
    ) -> Union[bool, list[model_stories.StoryFragment]]:
        """
        Feed template-able datas into this story.

        :Example:

        .. code:: python

           from pyscribus.file import ScribusFile
           doc = ScribusFile("1.5.5", "example.sla")

           story = doc.stories[0]
           doc.stories.feed(story, data)

        :type story: pyscribus.model.stories.Story
        :type datas: dict
        :returns: List of modified elements in this story, or False
        :rtype: Union[bool, list]
        """

        elements = self.__story_templatable(story)

        if not elements:
            return False

        modified = []

        for element in elements:
            for template_key, template_value in datas.items():
                if template_key not in element.text:
                    continue

                new_value = None

                if isinstance(datas[template_key], list):
                    # We have %key% -> ["Value1", "Value2", …]
                    # So the first occurrence of %key% is "Value1", the
                    # second "Value2", etc.

                    if len(datas[template_key]):
                        new_value = datas[template_key].pop(0)
                else:
                    # We have %key% -> "Value"
                    new_value = template_value

                if new_value is None:
                    continue

                element.text = element.text.replace(template_key, new_value)

                modified.append(element)

        return modified

    def __story_templatable(self, story) -> list:
        """
        Return elements of Story sequence that are available for templating.

        :type story: pyscribus.model.stories.Story
        :rtype: list
        :returns: List of pyscribus.stories.StoryFragment
        """

        contents = []

        pattern = self.file.templating["intext-pattern"]

        for element in story.model_object.sequence:
            if isinstance(element, model_stories.StoryFragment):
                if pattern.findall(element.text) is not None:
                    contents.append(element)

        return contents

    def __story_is_templatable(self, story) -> bool:
        pattern = self.file.templating["intext-pattern"]

        for element in story.model_object.sequence:
            if isinstance(element, model_stories.StoryFragment):
                if pattern.findall(element.text) is not None:
                    return True

        return False

    @pyfe.has_document
    def __stories(self) -> list[model_stories.Story]:
        """
        Returns all stories in the document.

        :rtype: list
        :returns: List of stories
        """

        stories = []

        # Text frames stories --------------------------------------------

        filtered = [
            page_object
            for page_object in self.model.document.page_objects
            if page_object.have_stories and page_object.stories
        ]

        if filtered:
            for page_object in filtered:
                stories.extend(page_object.stories)

        # Table cells stories --------------------------------------------

        tables = [
            page_object
            for page_object in self.model.document.page_objects
            if page_object.ptype == "table"
        ]

        if tables:
            cells = []

            for page_object in tables:
                cells.extend(page_object.cells)

            for cell in cells:
                if cell.story is not None:
                    stories.append(cell.story)

        # Convert stories ------------------------------------------------

        # This converts stories from the model subpackage to stories
        # from the file subpackage.
        stories = [Story(model_object=story) for story in stories]

        # ----------------------------------------------------------------

        if self.only_templatable:
            return [
                story
                for story in stories
                if self.__story_is_templatable(story)
            ]

        return stories


class Story:
    """
    High-level wrapper around model's ``Story`` class.
    """

    def __init__(self, **kwargs):
        self.sequence = []
        self.model_object = None

        seq = kwargs.get("sequence")
        if seq is not None:
            self.sequence = seq

        mstory = kwargs.get("model_object")
        if mstory is not None:
            self.model_object = mstory

    def append(self, item):
        """
        Append something to this story.

        .. warning:: Not implemented.

        """
        raise NotImplementedError()

    def __notes(self) -> list:
        """
        Returns the list of notes used in this story.

        .. warning:: Not implemented.

        """
        raise NotImplementedError()


class Paragraph:
    """
    Paragraph in a story.

    High-level wrapper around many elements that can make a paragraph in a
    Scribus story.

    (This class doesn't match any SLA element itself)
    """

    def __init__(self, **kwargs):
        self.sequence = []

        seq = kwargs.get("sequence")
        if seq is not None:
            self.sequence = seq

    def append(self, item):
        """
        .. warning:: Not implemented.

        """
        raise NotImplementedError()

    def len(self) -> int:
        """
        .. warning:: Not implemented.

        """
        raise NotImplementedError()

    def __notes(self) -> list:
        """
        .. warning:: Not implemented.

        """
        raise NotImplementedError()


class Notes:
    """
    Notes in a story or paragraph.
    """


class Fragment:
    def __init__(self, **kwargs):
        self.text = ""

        text = kwargs.get("text")
        if text is not None:
            self.text = text

    def append(self, item):
        """
        .. warning:: Not implemented.

        """
        raise NotImplementedError()


class SpanText(Fragment):
    """
    Formatted fragment of text in a paragraph
    """


class Text(Fragment):
    """
    Fragment of text in a paragraph, without any formatting.
    """


class Field:
    """
    Special field in a Story paragraph
    """

    var_types = {
        "page_number": "pgno",
        "page_count": "pgco",
    }

    def __init__(self, field_type: StoryFieldType):
        self.model_object = None

        if field_type not in Field.var_types:
            raise ValueError("Unknown field name.")

        self.field_type = field_type

        self.model_object = {
            "pgno": model_stories.PageNumberVariable,
            "pgco": model_stories.PageCountVariable,
        }[Field.var_types[field_type]]()


# vim:set shiftwidth=4 softtabstop=4:
