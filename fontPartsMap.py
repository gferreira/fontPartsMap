# fontParts object map

import os
import sys

from drawBot import *
from grapefruit import Color
from collections import OrderedDict

FontPartsConnections = [
    ('font',    'info'),
    ('font',    'font lib'),
    ('font',    'kerning'),
    ('font',    'features'),
    ('font',    'layer'),
    ('layer',   'glyph'),
    ('glyph',   'glyph lib'),
    ('glyph',   'anchor'),
    ('glyph',   'component'),
    ('glyph',   'image'),
    ('glyph',   'guideline'),
    ('glyph',   'contour'),
    ('contour', 'point'),
    ('contour', 'bPoint'),
    ('contour', 'segment')
]

class FontPartsColorScheme(object):

    colorSets = [
        ['font', 'font lib', 'info', 'kerning', 'features'],
        ['glyph', 'glyph lib', 'anchor', 'component', 'image', 'guideline', 'contour'],
        ['contour', 'point', 'bPoint', 'segment'],
        ['font', 'layer', 'glyph'],
    ]

    def __init__(self):
        self.makeColors()

    def makeColors(self):

        colors = {
            # use original RoboFab colors for Font and Glyph objects
            'font'  : Color.from_hsl(80, 0.50, 0.49),
            'glyph' : Color.from_hsl(38, 0.91, 0.69),
        }

        # color set 1: Font sub-objects
        for i, obj in enumerate(self.colorSets[0][1:]):
            color = colors['font'].with_hue(colors['font'].hsl[0] + (i+1) * 25)
            colors[obj] = color

        # color set 2: Glyph sub-objects
        for i, obj in enumerate(self.colorSets[1][1:]):
            color = colors['glyph'].with_hue(colors['glyph'].hsl[0] - (i+1) * 15)
            colors[obj] = color

        # color set 3: Contour sub-objects
        for i, obj in enumerate(self.colorSets[2][1:]):
            color = colors['contour'].with_hue(colors['contour'].hsl[0] - (i+1) * 20)
            colors[obj] = color

        # color set 4: Layer
        colors['layer'] = colors['font'].blend(colors['glyph'], percent=0.5)

        self.colors = colors

    @property
    def colorsRGB(self):
        colors = {}
        for obj, color in self.colors.items():
            colors[obj] = color.rgb
        return colors

    @property
    def colorsCMYK(self):
        colors = {}
        for obj, color in self.colors.items():
            colors[obj] = color.cmyk
        return colors

    def drawSwatches(self, pos, cellSize, padding, captions=False):
        x, y = pos
        w, h = cellSize
        save()
        translate(x, y)
        fontSize(w * .12)
        for colorSet in reversed(self.colorSets):
            save()
            for obj in colorSet:
                color = self.colorsRGB[obj]
                fill(*color)
                rect(0, 0, w, h)
                if captions:
                    fill(0)
                    text(obj, (w * .1, h * .2))
                translate(w + padding, 0)
            restore()
            translate(0, (h + padding))
        restore()

class FontPartsMap(object):

    colors = FontPartsColorScheme().colorsRGB
    connections = FontPartsConnections

    radius1 = 50
    radius2 = 70

    length1 = 160
    length2 = 200
    length3 = 170

    angle1  = 180 / 3
    angleStart1 = 0

    angle2  = 180 / 4
    angleStart2 = 0

    angle3  = 180 / 3.5
    angleStart3 = 0

    font = 'RoboType-Bold'
    fontSize1 = 18
    fontSize2 = 32

    textDraw = True

    linesStrokeColor = 0.6,
    linesStrokeWidth = 4
    linesDash = 3, 7

    circlesStrokeColor = 0,
    circlesStrokeWidth = 3

    circlesShadowDraw     = True
    circlesShadowDistance = 10, 0
    circlesShadowBlur     = 15
    circlesShadowColor    = 0, 0.25

    randomness = 0

    tree = {
        'font'    : ['font lib', 'info', 'kerning', 'features'],
        'glyph'   : ['glyph lib', 'anchor', 'component', 'image', 'guideline', 'contour'],
        'contour' : ['point', 'bPoint', 'segment'],
    }

    positions = {}

    def setAttributes(self, attrsDict):
        for key, value in attrsDict.items():
            setattr(self, key, value)

    def makePositions(self, pos):
        x, y = pos

        # font etc.
        xFont, yFont = x, y
        self.positions['font'] = xFont, yFont
        for i, obj in enumerate(self.tree['font']):
            x_ = xFont + cos(radians(self.angleStart1 + self.angle1 * i)) * self.length1
            y_ = yFont + sin(radians(self.angleStart1 + self.angle1 * i)) * self.length1
            self.positions[obj] = x_, y_

        # layer
        xLayer = xFont
        yLayer = yFont - self.length2
        self.positions['layer'] = xLayer, yLayer

        # glyph etc.
        xGlyph = xLayer
        yGlyph = yLayer - self.length2
        self.positions['glyph'] = xGlyph, yGlyph
        for i, obj in enumerate(self.tree['glyph']):
            x_ = xGlyph + cos(radians(self.angleStart2 + self.angle2 * i)) * self.length2
            y_ = yGlyph + sin(radians(self.angleStart2 + self.angle2 * i)) * self.length2
            self.positions[obj] = x_, y_

        # point etc.
        xContour, yContour = self.positions['contour']
        for i, obj in enumerate(self.tree['contour']):
            x_ = xContour + cos(radians(self.angleStart3 + self.angle3 * i)) * self.length3
            y_ = yContour + sin(radians(self.angleStart3 + self.angle3 * i)) * self.length3
            self.positions[obj] = x_, y_

        # randomize
        if self.randomness != 0:
            for obj, (x, y) in self.positions.items():
                x += randint(-self.randomness, self.randomness)
                y += randint(-self.randomness, self.randomness)
                self.positions[obj] = x, y

    def drawLines(self):
        save()
        if self.linesStrokeColor:
            stroke(*self.linesStrokeColor)
        else:
            stroke(None)
        strokeWidth(self.linesStrokeWidth)
        lineDash(self.linesDash)
        lineCap('round')
        for obj1, obj2 in self.connections:
            line(self.positions[obj1], self.positions[obj2])
        restore()

    def drawCircles(self):
        save()
        stroke(*self.circlesStrokeColor)
        strokeWidth(self.circlesStrokeWidth)
        if self.circlesShadowDraw:
            shadow(self.circlesShadowDistance, blur=self.circlesShadowBlur, color=self.circlesShadowColor)
        for obj, pos in self.positions.items():
            if obj not in ['font', 'glyph']:
                r = self.radius1
            else:
                r = self.radius2
            c = self.colors[obj]
            fill(*c)
            x, y = pos
            oval(x - r, y - r, r*2, r*2)
        restore()

    def drawCaptions(self):
        if self.textDraw:
            save()
            fill(1)
            shadow((2, -2), blur=5, color=(0, 0.3))
            font(self.font)
            for obj in self.positions.keys():
                x, y = self.positions[obj]
                if obj not in ['font', 'glyph']:
                    r = self.radius1
                    fontSize(self.fontSize1)
                    h = r - self.fontSize1 * -0.6
                else:
                    r = self.radius2
                    fontSize(self.fontSize2)
                    h = r - self.fontSize2 * -0.65
                if len(obj.split('_')) > 1:
                    obj = obj.split('_')[-1]
                textBox(obj, (x - r, y - r, r * 2, h), align='center')
            restore()

    def draw(self, pos):
        self.makePositions(pos)
        self.drawLines()
        self.drawCircles()
        self.drawCaptions()

class FontPartsMapUI(object):

    def __init__(self):

        M = FontPartsMap()

        a1 = 360 / len(M.tree['font'])
        a2 = 360 / len(M.tree['glyph'])
        a3 = 360 / len(M.tree['contour'])

        Variable([
            dict(name="x",           ui="Slider", args=dict(value=500, minValue=0,  maxValue=1000)),
            dict(name="y",           ui="Slider", args=dict(value=500, minValue=0,  maxValue=1000)),
            dict(name="radius1",     ui="Slider", args=dict(value=60,  minValue=30, maxValue=100)),
            dict(name="radius2",     ui="Slider", args=dict(value=120, minValue=50, maxValue=200)),
            dict(name="length1",     ui="Slider", args=dict(value=190, minValue=80, maxValue=300)),
            dict(name="length2",     ui="Slider", args=dict(value=210, minValue=80, maxValue=300)),
            dict(name="length3",     ui="Slider", args=dict(value=190, minValue=80, maxValue=300)),
            dict(name="angle1",      ui="Slider", args=dict(value=60,  minValue=0,  maxValue=a1)),
            dict(name="angleStart1", ui="Slider", args=dict(value=-10, minValue=0,  maxValue=360)),
            dict(name="angle2",      ui="Slider", args=dict(value=-50, minValue=0,  maxValue=a2)),
            dict(name="angleStart2", ui="Slider", args=dict(value=40,  minValue=0,  maxValue=360)),
            dict(name="angle3",      ui="Slider", args=dict(value=55,  minValue=0,  maxValue=a3)),
            dict(name="angleStart3", ui="Slider", args=dict(value=85,  minValue=0,  maxValue=360)),
            dict(name="randomness",  ui="Slider", args=dict(value=0,   minValue=0,  maxValue=20)),
        ], globals())

        M.radius1 = radius1
        M.radius2 = radius2
        M.length1 = length1
        M.length2 = length2
        M.length3 = length3

        M.angle1 = angle1
        M.angle2 = angle2
        M.angle3 = angle3

        M.angleStart1 = angleStart1
        M.angleStart2 = angleStart2
        M.angleStart3 = angleStart3

        M.randomness = int(randomness)

        M.linesDash = 2, 7
        M.linesStrokeColor = 0.7,
        M.linesStrokeWidth = 4
        M.circlesStrokeColor = 0,
        M.circlesStrokeWidth = 0

        fill(1)
        rect(0, 0, width(), height())

        M.draw((x, y))

