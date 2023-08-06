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

Scribus file. Document classes.
"""

# Imports ===============================================================#

# Standard library ---------------------------------------------

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

import copy

from typing import Any, Union, Optional, Literal, NoReturn
from collections import OrderedDict

# PyScribus model ----------------------------------------------

import pyscribus.model.layers as layers
import pyscribus.model.dimensions as dimensions
import pyscribus.model.pageobjects as pageobjects

from pyscribus.model.sla import SLA
from pyscribus.model.pages import Page, MasterPage

# PyScribus file -----------------------------------------------

import pyscribus.file as pyf
import pyscribus.file.exceptions as pyfe

# Global variables / Annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

FirstLast = Literal["first", "last"]
StringOrNone = Union[str, None]

# Classes ===============================================================#

class Metadatas:
    """
    Interface for document's metadatas.

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile

       doc = ScribusFile("1.5.5", "example.sla")

       title = doc.metadatas.title
       date = doc.metadatas.date

       doc.metadatas.add_keyword("NewKeyword")

       metadatas_dump = dict(doc.metadatas)

    """

    def __init__(self, model: SLA):
        self.model = model

    @pyfe.has_document
    def __get(self, key) -> Union[str, list[str], None]:
        return self.model.document.metadata.get(key)

    def __iter__(self):
        """
        Special method to make Metadatas class iterable.
        """
        for key, value in self.model.document.metadata.items():
            yield (key, value)

    # Keywords -----------------------------------------------------------

    @property
    def keywords(self) -> Union[list[str], None]:
        return self.__get("keywords")

    def add_keyword(self, new_keyword: str) -> NoReturn:
        """
        Add a new keyword to the document's metadatas.

        :type new_keyword: str
        :param new_keyword: New keyword to add.
        """

        keywords = self.__get("keywords")

        if keywords is None:
            keywords = []
        else:
            keywords = list(set(keywords))

        if new_keyword not in keywords:
            keywords.append(new_keyword)

        self.model.document.metadata["keywords"] = keywords

    # --------------------------------------------------------------------

    @property
    def title(self) -> StringOrNone:
        return self.__get("title")

    @property
    def author(self) -> StringOrNone:
        """Author(s) of the document"""
        return self.__get("author")

    @property
    def subject(self) -> StringOrNone:
        return self.__get("subject")

    @property
    def comments(self) -> StringOrNone:
        return self.__get("comments")

    @property
    def publisher(self) -> StringOrNone:
        return self.__get("publisher")

    @property
    def contributor(self) -> StringOrNone:
        """Contributor(s) to the document"""
        return self.__get("contributor")

    @property
    def date(self) -> StringOrNone:
        return self.__get("date")

    @property
    def type(self) -> StringOrNone:
        return self.__get("type")

    @property
    def format(self) -> StringOrNone:
        return self.__get("format")

    @property
    def identifier(self) -> StringOrNone:
        return self.__get("identifier")

    @property
    def source(self) -> StringOrNone:
        return self.__get("source")

    @property
    def lang(self) -> StringOrNone:
        return self.__get("lang")

    @property
    def related(self) -> StringOrNone:
        return self.__get("related")

    @property
    def cover(self) -> StringOrNone:
        return self.__get("cover")

    @property
    def rights(self) -> StringOrNone:
        return self.__get("rights")


class Pages:
    """
    Interface for document's pages.

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile
       from pyscribus.model.pages import Page

       doc = ScribusFile("1.5.5", "example.sla")

       doc_pages = doc.pages

       # Equivalent to doc.pages[0]
       page_one = doc_pages.pages[0]
       how_many_pages = len(doc_pages)
       first_page_copy = doc_pages.copy(0)

       # Master pages are in a attribute of Pages
       master_pages = doc_pages.master_pages
       how_many_master_pages = len(doc_pages.master_pages)

       # BELOW THIS LINE, EVERYTHING IS NOT IMPLEMENTED --------

       doc_pages.remove(5)
       new_page = Page()
       doc_pages.insert(2, new_page)

    """

    def __init__(self, model: SLA):
        self.model = model

    def __len__(self) -> int:
        # > len(x.pages)
        return len(self.__pages_number_sorted("normal"))

    def __getitem__(self, item: int):
        # > x.pages[0]
        # return self.pages[item]
        return list(self.__pages_number_sorted("normal").values())[item]

    @pyfe.has_document
    def __pages_number_sorted(self, page_set="normal") -> OrderedDict:
        if page_set == "normal":
            p_set = self.model.document.pages
        elif page_set == "master":
            p_set = self.model.document.master_pages
        else:
            raise ValueError(f"Asked for invalid page set {page_set}")

        ordered_pages = OrderedDict()
        numbers = sorted([page.number for page in p_set])

        for number in numbers:
            for page in p_set:
                if page.number != number:
                    continue

                ordered_pages[number] = page
                break

        return ordered_pages

    @pyfe.has_document
    def insert(self, position: Union[int, FirstLast], page: Any):
        """
        .. warning:: Not implemented.

        Insert page at page_number ``position``.

        :type position: Union[int, FirstLast]
        :param position: Page number where to insert the page.
        """
        # > x.pages.insert(2, new_page)

        len_pages = len(self)

        insert_last = position == "last" or position == len_pages
        insert_first = position == "first" or position == 0

        if insert_first:
            pass
        if insert_last:
            pass
        else:
            pass

        raise NotImplementedError()

    def copy(
        self,
        position: int,
        new_page_number: Optional[int] = None,
        master_page: bool = False,
    ) -> Union[Page, MasterPage]:
        """
        Returns a copy of the (master)page at ``position`` page_number.

        .. note:: It does not copy page objects, nor does it add the returned
            page to the document.

        :type position: int
        :param position: Page number of the page to copy.
        :type new_page_number: Optional[int]
        :param new_page_number: New page number to attribute to the copy.
        :type master_page: bool
        :param master_page: Copy a master page instead of a regular page.
        :rtype: Union[Page, MasterPage]
        :returns: Copy of the (master)page.
        """
        page_set = {False: "normal", True: "master"}[bool(master_page)]

        try:
            original = list(self.__pages_number_sorted(page_set).values())[
                position
            ]
        except IndexError as not_found:
            raise pyfe.PageNotFound(
                f"There is no page number {position}"
            ) from not_found

        page_copy = copy.deepcopy(original)

        if new_page_number is not None:
            page_copy.number = new_page_number

        return page_copy

    @pyfe.has_document
    def remove(self, page_number: int):
        """
        .. warning:: Not implemented.

        """
        # > x.pages.remove(5)
        # How to :
        # - Catch the coords of the page to delete
        # - Catch the coords of the pages following page_number index
        # - Attribute coords of page_number + 1 the position of page_number + 0
        # - Modify page_number attribute of page_number + 1
        # -   Etc.
        raise NotImplementedError()

    @property
    def pages(self) -> list[Page]:
        # > x.pages
        # return self.model.document.pages
        return list(self.__pages_number_sorted("normal").values())

    @property
    def masterpages(self) -> list[MasterPage]:
        # return self.model.document.master_pages
        return list(self.__pages_number_sorted("master").values())


class Fonts:
    """
    .. warning:: Not implemented.

    Interface for document's fonts.
    """

    # This should inspect styles, Story elements to produce a list/dict of
    # used fonts and their use context.

    def __init__(self, model):
        self.model = model
        self.document = model.document

    def __getitem__(self, item):
        return self.__fonts()[item]

    @pyfe.has_document
    def __fonts(self) -> dict:
        pass


class Layers:
    """
    .. warning:: Not implemented.

    Interface for document's layers.
    """

    def __init__(self, model):
        self.model = model

    def __getitem__(self, item):
        return self.__layers()[item]

    def __iter__(self):
        """
        Special method to make Layers class iterable.
        """

        for layer in self.model.document.layers:
            yield layer

    @pyfe.has_document
    def __layers(self) -> dict:
        return self.model.document.layers

    def insert(self, layer: str, after: int, before: int):
        """
        .. warning:: Not implemented.

        Move layer.
        """

# vim:set shiftwidth=4 softtabstop=4 spl=en:
