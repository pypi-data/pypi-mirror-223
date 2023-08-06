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

Scribus file. Classes for page objects.
"""

# Imports ===============================================================#

# Standard library ---------------------------------------------

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union, Any

import fnmatch

# PyScribus model ----------------------------------------------

import pyscribus.model.dimensions as dimensions
import pyscribus.model.pageobjects as pageobjects

# PyScribus file -----------------------------------------------

import pyscribus.file as pyf
import pyscribus.file.exceptions as pyfe
import pyscribus.file.document as document

# Global variables / Annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

StringOrNone = Union[str, None]

# Classes ===============================================================#

class PageObjects:
    """
    Interface for document's page objects.

    :type file: pyscribus.file.ScribusFile
    :param file: Scribus file wrapper

    :Example:

    .. code:: python

       # To avoid writing "scribus_file.pageobjects" again and again
       doc_objects = scribus_file.pageobjects

       # Filtering page objects ------------------------------------------

       templatable_text_frames = doc_objects.filter(
          object_type="text", templatable=True
       )

       on_page_two = doc_objects.filter(page_number=1)

       # Is an object on page 2 on page 1 ? No.
       is_on_page_one = doc_objects.on_page(on_page_two[0], 0)

       # Access page objects by loading order ----------------------------

       po_two = doc_objects[1]

       # To access all objects, use item property…

       all_objects = doc_objects.items

       # … or iterate on doc_objects:

       for object in doc_objects:
           print(object.name)

    """

    def __init__(self, file: pyf.ScribusFile):
        self.file = file
        self.model = file.model

    def __get_page(self, page_number: int, master: bool = False):
        """
        Get the page number ``page_number`` and the full page set (normal /
        master pages).

        :type page_number: int
        :param page_number: Page number of the page to copy.
        :type master: bool
        :param master: Use the master pages set instead of normal pages.
        :returns: Page number ``page_number`` and the full page set.
        """

        if page_number < 0:
            raise pyfe.PageNotFound("Page number asked inferior to 0.")

        if master:
            pages = document.Pages(self.model).masterpages
        else:
            pages = document.Pages(self.model).pages

        try:
            page = pages[page_number]
        except IndexError as not_found:
            raise pyfe.PageNotFound(
                f"There is no page number {page_number}"
            ) from not_found

        return page, pages

    def __on_page(self, page_object, page) -> bool:
        """
        Is the page object ``page_object`` on page ``page`` ?

        :rtype: bool
        """

        # We just use numeric values of the Dim objects
        def corner_values(corner: list[dimensions.Dim]) -> list[float]:
            return [dim.value for dim in corner]

        # Get the top-left and bottom-right corners coordinates of the page
        page_tl = corner_values(page.box.coords["top-left"])
        page_br = corner_values(page.box.coords["bottom-right"])
        # Get the top-left and bottom-right corners coordinates of the object
        object_tl = corner_values(page_object.box.coords["top-left"])
        object_br = corner_values(page_object.box.coords["bottom-right"])

        # Object in X of the page
        in_x = object_tl[0] >= page_tl[0] and object_br[0] <= page_br[0]
        # Object in Y of the page
        in_y = object_tl[1] >= page_tl[1] and object_br[1] <= page_br[1]
        # Object in the page
        on_page = in_x and in_y

        return on_page

    def __overlaps_page(
        self, page_object, page, strict: bool = False
    ) -> Union[bool, dict]:
        """
        Is the page object ``page_object`` overlaping on page ``page`` ?

        :param page_object: Page object
        :param page: Page.
        :type strict: bool
        :param strict: Filter out page object that are totally contained in
            the page.

        :rtype: Union[bool, dict]
        """

        # We just use numeric values of the Dim objects
        def corner_values(corner: list[dimensions.Dim]) -> list[float]:
            return [dim.value for dim in corner]

        obj = {
            corner_name: corner_values(corner_coords)
            for corner_name, corner_coords in page_object.box.coords.items()
        }

        page_tl = corner_values(page.box.coords["top-left"])
        page_br = corner_values(page.box.coords["bottom-right"])

        overlaping = {
            "top-left": False,
            "top-right": False,
            "bottom-left": False,
            "bottom-right": False,
        }

        for corner in ["top-left", "top-right", "bottom-left", "bottom-right"]:
            # Corner in X of the page
            in_x = (
                obj[corner][0] >= page_tl[0] and obj[corner][0] <= page_br[0]
            )
            # Corner in Y of the page
            in_y = (
                obj[corner][1] >= page_tl[1] and obj[corner][1] <= page_br[1]
            )
            # Corner in the page
            overlaping[corner] = in_x and in_y

        corner_overlaping = len(
            [status for status in overlaping.values() if status]
        )

        if corner_overlaping == 0:
            return False

        # If we want to know if the page object is overlaping on page but not
        # totally contained in that page, then having the four corners
        # overlaping should return False.
        if strict and corner_overlaping == 4:
            return False

        return overlaping

    def __is_model_object(self, page_object: Any) -> bool:
        """
        Is the object ``page_object`` an object from the list of the model
        page objects?

        :type page_object: Any
        :param page_object: A page object.
        :rtype: bool
        """

        for object_class in pageobjects.po_type_classes.values():
            if not isinstance(page_object, object_class):
                continue

            return True

        return False

    def append(self, page_object) -> bool:
        """
        Append the page object ``page_object``.

        .. warning:: This method only append page objects of the model
             classes. It does not do anything else and will change it's
             arguments and behaviour across versions.

        :rtype: bool
        :returns: Success.
        """

        if not self.__is_model_object(page_object):
            return False

        self.model.document.page_objects.append(page_object)

        return True

    def on_page(
        self,
        page_object,
        page_number: int,
        master: bool = False,
    ) -> bool:
        """
        Is the page object ``page_object`` on page number ``page_number`` ?

        .. note:: This methods detects objects strictely *contained* on pages
             — not objects overlaping in/out of pages. To detect overlaping
             objects, use ``overlaps_page`` method instead.

        :param page_object: Page object
        :type page_number: int
        :param page_number: Page number of the page to copy.
        :type master: bool
        :param master: Use the master pages set instead of normal pages.
        :rtype: bool
        :returns: ``True`` if the object is on the page.
        """

        # Get the relevant page
        page, _ = self.__get_page(page_number, master)

        return self.__on_page(page_object, page)

    def overlaps_page(
        self,
        page_object,
        page_number: int,
        master: bool = False,
        strict: bool = False,
        corners: bool = False,
    ) -> Union[bool, dict]:
        """
        Do the page object ``page_object`` overlaps on page number
        ``page_number`` ?

        .. warning:: This method checks only the non-rotated box of the page
            object.

        :param page_object: Page object
        :type page_number: int
        :param page_number: Page number.
        :type master: bool
        :param master: Use the master pages set instead of normal pages.
        :type strict: bool
        :param strict: Filter out page object that are totally contained in
            the page.
        :type corners: bool
        :param corners: Return the overlaping status of each corner of the page
            object. Returns a dictionary if there is overlaping corners, if
            not, returns ``False``.

        :rtype: Union[bool, dict]
        """
        page, _ = self.__get_page(page_number, master)

        overlaping = self.__overlaps_page(page_object, page, strict)

        if overlaping:
            if corners:
                return overlaping

            return True

        return False

    def __filter_name(self, lookup_set: list, pattern: StringOrNone) -> list:
        """
        Sub-filter for ``PageObjects.filter()``.

        Filter out page object not matching ``pattern``.

        Use fnmatch to match ``pattern`` like a file glob.

        :type lookup_set: list
        :param lookup_set: List of page objects to filter against.
        :type pattern: str
        :param page_number: Name pattern (glob) to match.
        :rtype: list
        """

        if pattern is None:
            return lookup_set

        return [
            page_object
            for page_object in lookup_set
            if fnmatch.fnmatchcase(page_object.name, pattern)
        ]

    def __filter_page(
        self,
        lookup_set: list,
        page_number: Union[int, None],
        master: Union[bool, None] = False,
    ) -> list:
        """
        Sub-filter for ``PageObjects.filter()``.

        Filter out page object not in the page number ``page_number``.

        :type lookup_set: list
        :param lookup_set: List of page objects to filter against.
        :type page_number: int
        :param page_number: Page number.
        :type master: bool
        :param master: Use the master pages set instead of normal pages.
        :rtype: list
        """

        if page_number is None:
            return lookup_set

        # If master is None, then the user did not specified master
        # in PageObjects.filter, so we can assume the user want regular pages.
        if master is None:
            master = False

        page, _ = self.__get_page(page_number, master)

        filtered_set = [
            page_object
            for page_object in lookup_set
            if self.__on_page(page_object, page)
        ]

        return filtered_set

    def __filter_page_overlap(
        self,
        lookup_set: list,
        page_number: Union[int, None],
        master: Union[bool, None] = False,
        strict: bool = False,
    ) -> list:
        """
        Sub-filter for ``PageObjects.filter()``.

        Filter out page object not overlaping on the page number ``page_number``.

        :type lookup_set: list
        :param lookup_set: List of page objects to filter against.
        :type page_number: int
        :param page_number: Page number.
        :type master: bool
        :param master: Use the master pages set instead of normal pages.
        :type strict: bool
        :param strict: Filter out page object that are totally contained in
            the page.
        :rtype: list
        """

        if page_number is None:
            return lookup_set

        # If master_page is None, then the user did not specified master_page
        # in PageObjects.filter, so we can assume the user want regular pages.
        if master is None:
            master = False

        page, _ = self.__get_page(page_number, master)

        filtered_set = [
            page_object
            for page_object in lookup_set
            if self.__overlaps_page(page_object, page, strict)
        ]

        return filtered_set

    def __filter_type(
        self, lookup_set: list, object_type: Union[str, bool, None]
    ) -> list:
        """
        Sub-filter for ``PageObjects.filter()``.

        Filter by object type.

        :type lookup_set: list
        :param lookup_set: List of page objects to filter against.
        :type object_type: Union[str, bool, None]
        :param object_type: Page object type to filter, or do not filter at
            all. See pageobjects.po_type_classes for valid values.
        :rtype: list
        """
        if object_type is None:
            return lookup_set

        if not object_type:
            return lookup_set

        if object_type not in pageobjects.po_type_classes:
            raise ValueError(
                f"Wrong object type when filtering page objects: {object_type}"
            )

        filtered_set = [
            page_object
            for page_object in lookup_set
            if isinstance(
                page_object, pageobjects.po_type_classes[object_type]
            )
        ]

        return filtered_set

    def __filter_templatable(
        self, lookup_set: list, templatable: Union[bool, None] = False
    ) -> list:
        """
        Sub-filter for ``PageObjects.filter()``.

        Filter out non-templatable page objects.

        :type lookup_set: list
        :param lookup_set: List of page objects to filter against.
        :type templatable: Union[bool, None]
        :param templatable: Only return templatable page objects.
        :rtype: list
        """
        if templatable is None:
            return lookup_set

        if not templatable:
            return lookup_set

        if not self.file.templating["active"]:
            return []

        filtered_set = []

        for object_item in lookup_set:
            # If the page object is a text frame with templatable
            # stories, we add these templatable stories

            if isinstance(object_item, pageobjects.TextObject):
                po_templatable_stories = object_item.templatable()

                if po_templatable_stories:
                    filtered_set.extend(po_templatable_stories)

            else:
                # TODO If this page object is another type of page
                # object, we look its properties and find if it
                # is templatable through sla.SLA.templating settings

                if object_item.templatable():
                    filtered_set.append(object_item)

        return filtered_set

    @pyfe.has_document
    def filter(self, **kwargs) -> list:
        """
        Return document page objects.

        :rtype: list
        :returns: Filtered document page objects.

        .. seealso:: ``pyscribus.model.pageobjects.po_type_classes`` for valid
            values expected by ``object_type`` filter.

        +---------------------+-------------------------------------------+------+
        | Kwarg key           | Filter on                                 | Type |
        +=====================+===========================================+======+
        | object_type         | Object type                               | str  |
        +---------------------+-------------------------------------------+------+
        | name                | Name of the page object. Glob-like and    | str  |
        |                     | case sensitive.                           |      |
        +---------------------+-------------------------------------------+------+
        | templatable         | Templatable objects                       | bool |
        +---------------------+-------------------------------------------+------+
        | page                | Objects in page X                         | int  |
        +---------------------+-------------------------------------------+------+
        | page_overlap        | Objects overlaping in page X.             | int  |
        |                     |                                           |      |
        |                     | Objects totally contained in page X are   |      |
        |                     | also returned.                            |      |
        +---------------------+-------------------------------------------+------+
        | page_overlap_strict | Objects overlaping in page X.             | int  |
        |                     |                                           |      |
        |                     | Objects totally contained in page X are   |      |
        |                     | NOT returned.                             |      |
        +---------------------+-------------------------------------------+------+
        | master_page         | When using the filters ``page`` and       | bool |
        |                     | ``page_overlap``, filter on master pages  |      |
        +---------------------+-------------------------------------------+------+

        :Example:

        .. code:: python

           # To avoid writing "scribus_file.pageobjects" again and again
           doc_objects = scribus_file.pageobjects

           templatable_text_frames = doc_objects.filter(
              object_type="text", templatable=True
           )

           on_page_two = doc_objects.filter(page=1)

           # Returns all the objects named after daleks, so we can EXTERMINATE
           # them instead of us humans.
           daleks = doc_objects.filter(name="Dalek *")

        """

        # Filter on page object name -------------------------------------

        filtered_set = self.__filter_name(self.items, kwargs.get("name"))

        # Filter on page object type -------------------------------------

        filtered_set = self.__filter_type(
            filtered_set, kwargs.get("object_type")
        )

        # Filter on page -------------------------------------------------

        filtered_set = self.__filter_page(
            filtered_set, kwargs.get("page"), kwargs.get("master_page")
        )

        # Filter on overlaping pages -------------------------------------

        filtered_set = self.__filter_page_overlap(
            filtered_set,
            kwargs.get("page_overlap"),
            kwargs.get("master_page"),
            False,
        )

        # Filter on overlaping pages (strict) ----------------------------

        filtered_set = self.__filter_page_overlap(
            filtered_set,
            kwargs.get("page_overlap_strict"),
            kwargs.get("master_page"),
            True,
        )

        # Filter off templatable page objects ----------------------------

        filtered_set = self.__filter_templatable(
            filtered_set, kwargs.get("templatable")
        )

        # ----------------------------------------------------------------

        return filtered_set

    @property
    @pyfe.has_document
    def items(self) -> list:
        """List of all page objects."""
        return self.model.document.page_objects

    def __iter__(self):
        for page_object in self.model.document.page_objects:
            yield page_object

    def __getitem__(self, item: int):
        return self.model.document.page_objects[item]


# vim:set shiftwidth=4 softtabstop=4:
