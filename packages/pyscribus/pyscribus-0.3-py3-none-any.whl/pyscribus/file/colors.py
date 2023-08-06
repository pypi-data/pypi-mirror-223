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

Scribus file. Colors and gradients wrappers.
"""

# Imports ===============================================================#

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

from pyscribus.model.sla import SLA
from pyscribus.model.colors import Color
import pyscribus.file.exceptions as pyfe

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

# Classes ===============================================================#


class Colors:
    """
    Wrapper around Scribus colors.

    :type file: pyscribus.file.ScribusFile
    :param file: Scribus file wrapper

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile

       doc = ScribusFile("1.5.5", "example.sla")

       how_many_colors = len(doc.colors)
       black_color = doc.colors["Black"]
       cmyk_colors = doc.colors.filter(space="cmyk")

    """

    def __init__(self, model: SLA):
        self.model = model

    def __len__(self) -> int:
        # > len(x.colors)
        return len(self.__colors())

    def __getitem__(self, item: int):
        # > x.colors["black"]
        return self.__colors()[item]

    @pyfe.has_document
    def __colors(self) -> dict:
        return {color.name: color for color in self.model.document.colors}

    @pyfe.has_document
    def filter(self, **kwargs) -> list[Color]:
        """
        Returns a selection of colors.

        :type kwargs: dict
        :param kwargs: kwargs
        :rtype: list[Color]
        :returns: Selection of colors

        **Kwargs options :**

        +-----------------------+-------------+-------------------------+
        | Kwarg key             | Filter on   | Type                    |
        +=======================+=============+=========================+
        | space                 | Color space | ``"cmyk"`` or ``"rgb"`` |
        +-----------------------+-------------+-------------------------+
        """

        colors = self.__colors()

        filter_space = False

        if (space := kwargs.get("space")) is not None:
            if space.lower() in ["cmyk", "rgb"]:
                filter_space = space.lower()

        if filter_space:
            colors = {
                color.name: color
                for color in colors.values()
                if color.space == filter_space
            }

        return colors

    @property
    def items(self) -> dict:
        """
        Colors dictionary organized by color name.

        .. seealso:: :class:`pyscribus.model.colors.Color`

        :rtype: dict
        """
        return self.__colors()


# vim:set shiftwidth=4 softtabstop=4:
