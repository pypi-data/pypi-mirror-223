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

Scribus file. Document classes : hyphenation.
"""

# Imports ===============================================================#

# Standard library ---------------------------------------------

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from typing import Union

# PyScribus model ----------------------------------------------

from pyscribus.model.document import HyphenationExclusion, HyphenationException

# PyScribus file -----------------------------------------------

import pyscribus.file.exceptions as pyfe

# Global variables / Annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# Classes ===============================================================#


class HyphenRule:
    """
    Abstract class for high-level hyphenation rules.
    """

    def __init__(self, word: str):
        self.word = word

    def __str__(self) -> str:
        return str(self.word)


class HyphenException(HyphenRule):
    """
    Hyphenation rule: excepting a word from hyphenation.
    """

    def __eq__(self, other) -> bool:
        if isinstance(other, HyphenException):
            return self.word == other.word

        return False


class HyphenExclusion(HyphenRule):
    """
    Hyphenation rule: excluding a word from hyphenation.
    """

    def __eq__(self, other) -> bool:
        if isinstance(other, HyphenExclusion):
            return self.word == other.word

        return False


# Global variables / Annotations ========================================#

HyphenationRule = Union[HyphenException, HyphenExclusion]

# =======================================================================#


class Hyphenation:
    """
    Interface for document's hyphenation settings.

    :Example:

    .. code:: python

       from pyscribus.file.document import HyphenExclusion

       # To avoid writing "scribus_file.hyphenation" again and again
       doc_hyphen = scribus_file.hyphenation

       doc_hyphen.remove_exception("anticonstitutionnellement")
       doc_hyphen.add_exception("anticonstitutionnellement")

       # Those two lines are equivalent to:
       #    doc_hyphen.add_exclusion("PyScribus")
       hyphen_rule = HyphenExclusion("PyScribus")
       doc_hyphen.append(hyphen_rule)

       has_pys = doc_hyphen.has_exclusion("PyScribus")

    """

    def __init__(self, model):
        self.model = model

    @pyfe.has_document
    def __iter__(self):
        """
        Special method to make Hyphenation class iterable.

        Yields ``HyphenException`` and ``HyphenExclusion`` instances.
        """

        for rule in self.model.document.hyphenation.rules:
            yield self.__model_to_pyf(rule)

    def __model_to_pyf(
        self, hyphen_rule: Union[HyphenationException, HyphenationExclusion]
    ):
        """
        Converts an hyphenation rule object from PyScribus model to an
        hyphenation rule for PyScribus file.
        """

        if isinstance(hyphen_rule, HyphenationException):
            return HyphenException(hyphen_rule.word)

        return HyphenExclusion(hyphen_rule.word)

    def __pyf_to_model(
        self, hyphen_rule: HyphenationRule
    ) -> Union[HyphenationException, HyphenationExclusion]:
        """
        Converts an hyphenation rule object from PyScribus file to an
        hyphenation rule for PyScribus model.
        """

        if isinstance(hyphen_rule, HyphenException):
            new_rule = HyphenationException()
        if isinstance(hyphen_rule, HyphenExclusion):
            new_rule = HyphenationExclusion()

        new_rule.word = hyphen_rule.word

        return new_rule

    @pyfe.has_document
    def __excluded_words(self) -> list[str]:
        return [
            rule.word
            for rule in self.model.document.hyphenation.rules
            if isinstance(rule, HyphenationExclusion)
        ]

    @pyfe.has_document
    def __excepted_words(self) -> list[str]:
        return [
            rule.word
            for rule in self.model.document.hyphenation.rules
            if isinstance(rule, HyphenationException)
        ]

    @pyfe.has_document
    def __remove_rule(self, word: str, rule_class, already_in) -> bool:
        """
        :rtype: bool
        """
        if not already_in(self, word):
            return True

        rule_index = None

        for idx, rule in self.model.document.hyphenation.rules:
            if not isinstance(rule, rule_class):
                continue

            if rule.word != word:
                continue

            rule_index = idx
            break

        if rule_index is None:
            return True

        self.model.document.hyphenation.rules.pop(rule_index)
        return True

    def remove_exception(self, word: str) -> bool:
        """
        Delete the rule making the word ``word`` an hyphenation exception.

        :type word: str
        :param word: Word
        :rtype: bool
        """
        return self.__remove_rule(
            word, HyphenationException, self.has_exception
        )

    def remove_exclusion(self, word: str) -> bool:
        """
        Delete the rule making the word ``word`` an hyphenation exclusion.

        :type word: str
        :param word: Word
        :rtype: bool
        """
        return self.__remove_rule(
            word, HyphenationExclusion, self.has_exclusion
        )

    def has_exclusion(self, word: str) -> bool:
        """
        :type word: str
        :param word: Word
        :rtype: bool
        """
        return word in self.__excluded_words()

    def has_exception(self, word: str) -> bool:
        """
        :type word: str
        :param word: Word
        :rtype: bool
        """
        return word in self.__excepted_words()

    @pyfe.has_document
    def __append_pyf_rule(self, rule: HyphenationRule):
        self.model.document.hyphenation.rules.append(self.__pyf_to_model(rule))

    def append(self, hyphenation_rule: HyphenationRule) -> bool:
        """
        Add a hyphenation rule.

        :rtype: bool
        """

        if isinstance(hyphenation_rule, HyphenException):
            if self.has_exception(hyphenation_rule.word):
                return True

            if self.has_exception(hyphenation_rule.word):
                self.remove_exclusion(hyphenation_rule.word)

            self.model.document.hyphenation.rules.append(
                self.__pyf_to_model(hyphenation_rule)
            )

            return True

        if self.has_exclusion(hyphenation_rule.word):
            return True

        if self.has_exclusion(hyphenation_rule.word):
            self.remove_exception(hyphenation_rule.word)

        self.__append_pyf_rule(hyphenation_rule)

        return True

    def add_exclusion(self, word: str) -> bool:
        """
        :type word: str
        :param word: Word
        :rtype: bool
        """

        if self.has_exclusion(word):
            return True

        if self.has_exception(word):
            self.remove_exception(word)

        self.__append_pyf_rule(HyphenExclusion(word))

        return True

    def add_exception(self, word: str) -> bool:
        """
        :type word: str
        :param word: Word
        :rtype: bool
        """

        if self.has_exception(word):
            return True

        if self.has_exclusion(word):
            self.remove_exclusion(word)

        self.__append_pyf_rule(HyphenException(word))

        return True


# vim:set shiftwidth=4 softtabstop=4:
