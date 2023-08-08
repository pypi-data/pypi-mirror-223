"""
glyph
===============================================================================
"""
from __future__ import annotations

from copy import deepcopy
from typing import Optional

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseGlyph
from fontParts.base.base import interpolate
from fontParts.base.deprecated import DeprecatedGlyph, RemovedGlyph
from fontParts.base.errors import FontPartsError
from fontParts.base.normalizers import normalizeColor, normalizeVisualRounding

from .anchor import RAnchor
from .color import Color
from .component import RComponent
from .contour import RContour
from .guideline import RGuideline
from .image import RImage
from .lib import RLib

BaseGlyph.__bases__ = tuple(
    b for b in BaseGlyph.__bases__ if b not in (RemovedGlyph, DeprecatedGlyph)
)


class RGlyph(fontshell.RGlyph):
    wrapClass = wbDefcon.Glyph
    contourClass = RContour
    componentClass = RComponent
    anchorClass = RAnchor
    guidelineClass = RGuideline
    imageClass = RImage
    libClass = RLib
    colorClass = Color

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Glyph = wrap

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value: bool):
        self._wrapped.selected = value

    def _transformBy(self, matrix, **kwargs) -> None:
        self._wrapped.holdNotifications()
        super()._transformBy(matrix, **kwargs)
        self._wrapped.releaseHeldNotifications()
        self._wrapped.postNotification(notification="Glyph.ContoursChanged")

    def _moveBy(self, value, **kwargs) -> None:
        self._wrapped.move(value)

    def show(self, newPage=False, view=None) -> None:
        self._wrapped.show(newPage, view)

    def naked(self) -> wbDefcon.Glyph:
        return self._wrapped

    # Mark
    def _get_base_markColor(self) -> Optional[Color]:
        value = self._get_markColor()
        if value is not None:
            value = self.colorClass(normalizeColor(value))
        return value

    def _set_base_markColor(self, value):
        if value is not None:
            value = normalizeColor(self.colorClass(value))
        self._set_markColor(value)

    # --------------------
    # Interpolation & Math
    #
    # Don't add offcurve points to all straight segments to improve
    # compatibility when a MathGlyph is created.
    # Don't filter redundant points when converted back from MathGlyph.
    # --------------------
    def _toMathGlyph(self, scaleComponentTransform=True, strict=False):
        import fontMath

        mathGlyph = fontMath.MathGlyph(
            None, scaleComponentTransform=scaleComponentTransform, strict=strict
        )
        pen = mathGlyph.getPointPen()
        pen.strict = strict
        self.drawPoints(pen)
        for anchor in self.anchors:
            d = dict(
                x=anchor.x,
                y=anchor.y,
                name=anchor.name,
                identifier=anchor.identifier,
                color=anchor.color,
            )
            mathGlyph.anchors.append(d)
        for guideline in self.guidelines:
            d = dict(
                x=guideline.x,
                y=guideline.y,
                angle=guideline.angle,
                name=guideline.name,
                identifier=guideline.identifier,
                color=guideline.color,
            )
            mathGlyph.guidelines.append(d)
        mathGlyph.lib = deepcopy(self.lib)
        mathGlyph.name = self.name
        mathGlyph.unicodes = self.unicodes
        mathGlyph.width = self.width
        mathGlyph.height = self.height
        mathGlyph.note = self.note
        return mathGlyph

    def __mul__(self, factor):
        mathGlyph = self._toMathGlyph(strict=True)
        result = mathGlyph * factor
        copied = self._fromMathGlyph(result, filterRedundantPoints=False)
        return copied

    __rmul__ = __mul__

    def __truediv__(self, factor):
        mathGlyph = self._toMathGlyph(strict=True)
        result = mathGlyph / factor
        copied = self._fromMathGlyph(result, filterRedundantPoints=False)
        return copied

    # py2 support
    __div__ = __truediv__

    def __add__(self, other: RGlyph):
        selfMathGlyph = self._toMathGlyph(strict=True)
        otherMathGlyph = other._toMathGlyph(strict=True)
        result = selfMathGlyph + otherMathGlyph
        copied = self._fromMathGlyph(result, filterRedundantPoints=False)
        return copied

    def __sub__(self, other: RGlyph):
        selfMathGlyph = self._toMathGlyph(strict=True)
        otherMathGlyph = other._toMathGlyph(strict=True)
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result, filterRedundantPoints=False)
        return copied

    # Interpolation
    def _interpolate(
        self,
        factor: float,
        minGlyph: RGlyph,
        maxGlyph: RGlyph,
        round: bool = True,
        suppressError: bool = True,
    ):
        from fontMath.mathFunctions import setRoundIntegerFunction

        setRoundIntegerFunction(normalizeVisualRounding)

        minGlyph = minGlyph._toMathGlyph(strict=True)
        maxGlyph = maxGlyph._toMathGlyph(strict=True)
        try:
            result = interpolate(minGlyph, maxGlyph, factor)
        except IndexError:
            result = None
        if result is None and not suppressError:
            raise FontPartsError(
                ("Glyphs '%s' and '%s' could not be " "interpolated.")
                % (minGlyph.name, maxGlyph.name)
            )
        if result is not None:
            if round:
                result = result.round()
            self._fromMathGlyph(result, toThisGlyph=True, filterRedundantPoints=False)
