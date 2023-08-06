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

Scribus file. Document UI settings classes.
"""

# Imports ===============================================================#

# Standard library ---------------------------------------------

# To avoid Sphinx complaints from methods annotations referencing same class
from __future__ import annotations

import copy

from typing import Union, Any, NoReturn, Optional, Literal
from collections import OrderedDict

# PyScribus model ----------------------------------------------

from pyscribus.model.sla import SLA
from pyscribus.model.common.math import PicaConverter

# PyScribus file -----------------------------------------------

import pyscribus.file as pyf
import pyscribus.file.exceptions as pyfe

# Global variables / Annotations ========================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

BoolOrNone = Union[bool, None]

RenderOrderItems = Literal["baseline", "grids", "guides", "margins", "objects"]

# Tool classes ==========================================================#


class Tool:
    """
    Abstract class for the default settings, document-wide, of a Scribus tool.
    """

    def __init__(self, model: SLA, converter: Optional[PicaConverter] = None):
        self.model = model
        self._tool_id = None
        self._converter = converter

    def _picas(self, value: Union[int, float]) -> float:
        if self._converter is None:
            return value

        return self._converter.picas(value)

    @pyfe.has_document
    def _get(self, key) -> Union[Any, None]:
        return self.model.document.tools[self._tool_id].get(key)

    @pyfe.has_document
    def _subget(self, key, subkey) -> Union[Any, None]:
        return self.model.document.tools[self._tool_id][key].get(subkey)

    @pyfe.has_document
    def _set(self, key: str, value: Any, dimension=False) -> NoReturn:
        """
        Set a tool preference named ``key`` to ``value``.


        :type key: str
        :param key: Key of the tool preference.
        :type value: Any
        :param value: Value to set to the tool preference ``key``.
        :type dimension: bool
        :param dimension: Set the value of a preference that is a
            ``pyscribus.model.dimension.Dim`` object?
        """

        if dimension:
            self.model.document.tools[self._tool_id][key].value = value
        else:
            self.model.document.tools[self._tool_id][key] = value

    @pyfe.has_document
    def _subset(
        self,
        key: str,
        subkey: str,
        value: Any,
        dimension=False
    ) -> NoReturn:
        """
        Set a tool preference named ``key``:``subkey`` to ``value``.


        :type key: str
        :param key: Key of the tool preference.
        :type subkey: str
        :param subkey: Sub-key of the tool preference.
        :type value: Any
        :param value: Value to set to the tool preference ``key``.
        :type dimension: bool
        :param dimension: Set the value of a preference that is a
            ``pyscribus.model.dimension.Dim`` object?
        """

        if dimension:
            self.model.document.tools[self.tool_id][key][subkey].value = value
        else:
            self.model.document.tools[self.tool_id][key][subkey] = value


class TextTool(Tool):
    """
    Default settings, document-wide, of the Scribus tool “Text”.
    """

    def __init__(self, model: SLA, converter: Optional[PicaConverter] = None):
        Tool.__init__(self, model, converter)
        self._tool_id = "text"

    # Text size ------------------------------------------------

    @property
    def size(self) -> float:
        """Text size (in points)."""
        return self._get("size").value

    @size.setter
    def size(self, value: float) -> NoReturn:
        """Text size (setter)."""
        self._set("size", value, True)

    # Columns gap size -----------------------------------------

    @property
    def columns_gap(self) -> int:
        """Gap between columns size (in picas)"""
        return self._get("columns_gap")

    @columns_gap.setter
    def columns_gap(self, value: float) -> NoReturn:
        """Gap between columns size (setter)"""
        self._set("columns_gap", self._picas(value), True)

    # Font -----------------------------------------------------

    # TODO Font
    # I don't know how to represent/give access to font for now.
    # Maybe use an interface around fonts in common with file.document.Fonts ?

    # Columns --------------------------------------------------

    @property
    def columns(self) -> int:
        """Default column number."""
        return self._get("columns")

    @columns.setter
    def columns(self, value: float) -> NoReturn:
        """Default column number (setter)"""
        self._set("columns", value)


class ShapeTool(Tool):
    """
    Default settings, document-wide, of the Scribus tool “Shape”.
    """

    def __init__(self, model: SLA, converter: Optional[PicaConverter] = None):
        Tool.__init__(self, model, converter)
        self._tool_id = "shape"

    # ----------------------------------------------------------

    def __set_color(self, subtool: str, value: str):
        # TODO : Maybe use a Color object instead of a string
        self._subset(subtool, "color", value)

    def __get_color(self, subtool: str) -> str:
        return self._subget(subtool, "color")

    def __set_shade(self, subtool: str, value: int):
        # TODO : Maybe use a Color object instead of a string
        self._subset(subtool, "shade", value, True)

    def __get_shade(self, subtool: str) -> int:
        return self._subget(subtool, "shade")

    # Pen ------------------------------------------------------

    @property
    def pen_color(self) -> str:
        """Color used by the shape tool pen."""
        return self.__get_color("pen")

    @pen_color.setter
    def pen_color(self, value: str) -> NoReturn:
        """Color used by the shape tool pen (setter)."""
        # TODO : Maybe use a Color object instead of a string
        self.__set_color("pen", value)

    @property
    def pen_shade(self) -> int:
        """Opacity the shape tool pen (integer percentage)."""
        return self.__get_shade("pen")

    @pen_shade.setter
    def pen_shade(self, value: int) -> NoReturn:
        """Opacity the shape tool pen (setter)."""
        self.__set_shade("pen", value)

    # Brush ----------------------------------------------------

    @property
    def brush_color(self) -> str:
        """Color used by the shape tool brush."""
        return self.__get_color("brush")

    @brush_color.setter
    def brush_color(self, value: str) -> NoReturn:
        """Color used by the shape tool brush (setter)."""
        # TODO : Maybe use a Color object instead of a string
        self.__set_color("brush", value)

    @property
    def brush_shade(self) -> int:
        """Opacity the shape tool brush (integer percentage)."""
        return self.__get_shade("brush")

    @brush_shade.setter
    def brush_shade(self, value: int) -> NoReturn:
        """Opacity the shape tool brush (setter)."""
        self.__set_shade("brush", value)

    # Width ----------------------------------------------------

    @property
    def width(self) -> float:
        """Width of the shape (in picas)."""
        return self._get("width").value

    @width.setter
    def width(self, value: float) -> NoReturn:
        """Width of the shape (setter)."""
        self._set("width", self._picas(value), True)

    # Style ----------------------------------------------------

    @property
    def style(self) -> int:
        """Style of the shape (from 0 to 37)."""
        return self._get("style")

    @style.setter
    def style(self, value: int) -> NoReturn:
        """Style of the shape (setter)."""
        value = int(value)

        if value < 0 or value > 37:
            raise ValueError(
                f"Shape style value must range from 0 to 37, got {value}."
            )

        self._set("style", value)


class Tools:
    """
    Interface for document's default tools settings for Scribus.

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile

       doc = ScribusFile("1.5.5", "example.sla")

       scribus_ui_tools = doc.ui.tools

       scribus_ui_tools.text.size = 12
       scribus_ui_tools.shape.pen_shade = 50

    """

    def __init__(self, model: SLA, converter: Optional[PicaConverter] = None):
        self.model = model
        self.converter = converter

    @property
    def text(self) -> TextTool:
        """
        Default settings, document-wide, of the Scribus tool “Text”.

        .. seealso:: :class:`pyscribus.file.ui.TextTool`
        """
        return TextTool(self.model, self.converter)

    @property
    def shape(self) -> ShapeTool:
        """
        Default settings, document-wide, of the Scribus tool “Shape”.

        .. seealso:: :class:`pyscribus.file.ui.ShapeTool`
        """
        return ShapeTool(self.model, self.converter)

    # TODO Image tool
    # TODO Polygon tool
    # TODO Line tool
    # TODO Calligraphic pen tool
    # TODO Arc tool
    # TODO Spiral tool


class UIGrid:
    """
    Abstract class for interfaces around UI grids settings.
    """

    def __init__(self, model: SLA, converter: Optional[PicaConverter] = None):
        self.model = model
        self.grid_name = None
        self._converter = converter

    def _picas(self, value: Union[int, float]) -> float:
        if self._converter is None:
            return value

        return self._converter.picas(value)

    @pyfe.has_document
    def _get_grid_show(self) -> bool:
        return self.model.document.ui_show.get(self.grid_name)

    @pyfe.has_document
    def _set_grid_show(self, value) -> NoReturn:
        self.model.document.ui_show[self.grid_name] = bool(value)

    @pyfe.has_document
    def _set_grid_setting(
        self,
        key: str,
        value: Any,
        grid_name: Optional[str] = None,
        dimension: bool = False
    ) -> NoReturn:
        grid = None

        if grid_name is None:
            grid = self.grid_name
        else:
            grid = grid_name

        if dimension:
            self.model.document.grids[grid][key].value = value
        else:
            self.model.document.grids[grid][key] = value

    @pyfe.has_document
    def _get_grid_setting(
        self, attrib: str, grid_name: Optional[str] = None
    ) -> Any:
        if grid_name is None:
            return self.model.document.grids[self.grid_name].get(attrib)

        return self.model.document.grids[grid_name].get(attrib)

    @property
    def show(self) -> bool:
        """Show this grid?"""
        return self._get_grid_show()

    @show.setter
    def show(self, do_show: bool) -> NoReturn:
        self._set_grid_show(do_show)


class Baseline(UIGrid):
    """
    Interface to UI baseline settings.
    """

    def __init__(self, model: SLA):
        UIGrid.__init__(self, model)
        self.grid_name = "baseline"

    # Baseline color -----------------------------------------------------

    @property
    def color(self):
        """Base line color showed in Scribus UI."""
        return self._get_grid_setting("color")

    # Baseline step ------------------------------------------------------

    @property
    def step(self):
        """Baseline step (in points)."""
        return self._get_grid_setting("spacing")

    @step.setter
    def step(self, value: float) -> NoReturn:
        """Baseline step (setter)."""
        self._set_grid_setting("spacing", value, dimension=True)

    # Baseline offset ----------------------------------------------------

    @property
    def offset(self):
        """Baseline offset (in points)."""
        return self._get_grid_setting("offset")

    @offset.setter
    def offset(self, value: float) -> NoReturn:
        """Baseline offset (setter)."""
        self._set_grid_setting("offset", value, dimension=True)


class Grids(UIGrid):
    """
    Interface to UI grid settings.
    """

    def __init__(self, model: SLA):
        UIGrid.__init__(self, model)
        self.grid_name = "grid"

    # Minor grid ---------------------------------------------------------

    @property
    def minor_color(self):
        """Minor grid: Color showed in Scribus UI."""
        return self._get_grid_setting("color", grid_name="minor")

    @property
    def minor_step(self):
        """Minor grid: step."""
        return self._get_grid_setting("spacing", grid_name="minor")

    @minor_step.setter
    def minor_step(self, value: float) -> NoReturn:
        self._set_grid_setting("spacing", self._picas(value), "minor", True)

    # Major grid ---------------------------------------------------------

    @property
    def major_color(self):
        """Major grid: Color showed in Scribus UI."""
        return self._get_grid_setting("color", grid_name="major")

    @property
    def major_step(self):
        """Major grid: step."""
        return self._get_grid_setting("spacing", grid_name="major")

    @major_step.setter
    def major_step(self, value: float) -> NoReturn:
        self._set_grid_setting("spacing", self._picas(value), "major", True)


class ShowOrder:
    items = [
        "baseline",
        "grids",
        "guides",
        "margins",
        "objects",
    ]

    def __init__(self, model: SLA):
        self.model = model

        self.__order = OrderedDict(
            item_1=None,
            item_2=None,
            item_3=None,
            item_4=None,
            item_5=None,
        )

        self.__from_model()

    @property
    @pyfe.has_document
    def __model_stack(self):
        return self.model.document.ui_show["stack"]

    @pyfe.has_document
    def __from_model(self):
        for model_index, file_key in [
            [0, "item_1"],
            [1, "item_2"],
            [2, "item_3"],
            [3, "item_4"],
            [4, "item_5"],
        ]:
            self.__order[file_key] = self.__model_stack[model_index]

    @pyfe.has_document
    def __iter__(self):
        """
        Special method to make RenderOrder class iterable.
        """
        self.__apply_changes()

        for item in self.__model_stack:
            yield item

    @pyfe.has_document
    def __apply_changes(self):
        """
        Apply the render order of this interface to the model datas.
        """
        self.__model_stack["stack"] = list(self.__order.values())

    def move(self, ui_item: RenderOrderItems, new_order: int) -> bool:
        """
        Move the render order of the UI element ``ui_item`` to ``new_order``.

        :type ui_item: RenderOrderItems
        :param ui_item: UI element to change its render order
        :type new_order: int
        :param new_order: New render order of the UI element, ranging from 1
            to 5.
        :rtype: bool
        :returns: Success.
        """

        if ui_item not in ShowOrder.items:
            raise ValueError(
                "UI render item must be one of these values: {}.".format(
                    ", ".join([f"'{s}'" for s in ShowOrder.items])
                )
            )

        if new_order < 1 or new_order > 5:
            raise ValueError("UI render order must be between 1 to 5.")

        # Nothing to do

        if self.__order[f"order_{new_order}"] == ui_item:
            return True

        # Swap item and older item at new_order position

        old_order = None
        old_value = copy.deepcopy(self.__order[f"order_{new_order}"])

        for order_key, item_value in self.__order.items():
            if item_value == ui_item:
                old_order = order_key
                break

        self.__order[old_order] = old_value
        self.__order[f"order_{new_order}"] = ui_item

        self.__apply_changes()

        return True


# UI interface ==========================================================#


class UI:
    """
    Interface for document's UI settings for Scribus.

    :Example:

    .. code:: python

       from pyscribus.file import ScribusFile

       doc = ScribusFile("1.5.5", "example.sla", coding_unit="mm")

       scribus_ui = doc.ui

       # Make Scribus show invisible caracters and links between text frames
       scribus_ui.caracters = True
       scribus_ui.links = True

       # Some elements have more settings.
       scribus_ui.baseline.show = False
       scribus_ui.grids.show = True
       scribus_ui.grids.minor_step = 10
       scribus_ui.grids.major_step = 50

    """

    def __init__(self, file: pyf.ScribusFile):
        self.file = file
        self.model = file.model

    @pyfe.has_document
    def __get(self, key) -> Union[str, list[str], None]:
        return self.model.document.ui_show.get(key)

    # UI settings properties ---------------------------------------------

    # Scribus UI elements not strictely related to the document

    @property
    def rulers(self) -> BoolOrNone:
        """Show Scribus' rulers?"""
        return self.__get("rulers")

    @property
    def layer_hints(self) -> BoolOrNone:
        """Show Scribus' layer hints?"""
        return self.__get("layer_hints")

    # Default settings, document wide, of Scribus tools --------

    @property
    def tools(self) -> Tools:
        """
        Default settings, document-wide, of Scribus' tools.

        .. seealso:: :class:`pyscribus.file.ui.Tools`
        """
        return Tools(self.model, self.file.pica_converter)

    # Document grid, lines -------------------------------------

    @property
    def grids(self) -> Grids:
        """
        Document's minor and major grids.

        .. seealso:: :class:`pyscribus.file.ui.Grids`
        """
        return Grids(self.model)

    @property
    def guides(self) -> BoolOrNone:
        """Show document's guides?"""
        return self.__get("guides")

    @property
    def baseline(self) -> Baseline:
        """
        Document's base line.

        .. seealso:: :class:`pyscribus.file.ui.Baseline`
        """
        return Baseline(self.model)

    @property
    def margins(self) -> BoolOrNone:
        """Show document's margins?"""
        return self.__get("margins")

    # Page objects : images frames -----------------------------

    @property
    def images(self) -> BoolOrNone:
        """Show images of the images frames?"""
        return self.__get("images")

    # Page objects : text frames -------------------------------

    @property
    def links(self) -> BoolOrNone:
        """Show links between text frames?"""
        return self.__get("links")

    @property
    def text_columns(self) -> BoolOrNone:
        """Show the borders of text frames columns?"""
        return self.__get("colborders")

    @property
    def caracters(self) -> BoolOrNone:
        """Show invisible/control caracters in text frames?"""
        return self.__get("caracters")

    # Render order of everything in the UI ---------------------

    @property
    def show_order(self) -> ShowOrder:
        """
        Order of render of some Scribus UI elements (baseline, grids, guides,
        margins, objects).

        .. seealso:: :class:`pyscribus.file.ui.ShowOrder`
        """
        return ShowOrder(self.model)


# vim:set shiftwidth=4 softtabstop=4:
