from importlib import reload

import logotype
reload(logotype)

import fontPartsMap
reload(fontPartsMap)

import os
from fontTools.agl import UV2AGL
from fontParts.world import OpenFont

from fontPartsMap import FontPartsMap
from logotype import FontPartsLogoType

folder = os.getcwd()
ufoPath = os.path.join(folder, 'FontParts.ufo')

size('A4Landscape')

f = OpenFont(ufoPath)
L = FontPartsLogoType(f)

L.scale = 0.11
L.layers['contour'] = False
L.layers['anchor'] = False
L.layers['bPoint'] = False
L.layers['point'] = False
L.layers['info'] = False
L.infoStrokeWidth = 7
L.infoValuesDraw = False
L.infoLineDash = 20, 20
L.contourStrokeWidth = 20
L.glyphWidthStrokeWidth = 15
L.glyphWidthDraw = False
L.glyphDataDraw = False
L.pointSize = 40
L.captionSize = 70
L.captionFont = 'Menlo-Bold'
L.draw((226, 233))

mapAttrs = {
    'radius1'            : 55,
    'radius2'            : 87,
    'length1'            : 180,
    'length2'            : 180,
    'length3'            : 160,
    'angle1'             : 50,
    'angleStart1'        : 0,
    'angle2'             : -45,
    'angleStart2'        : 30,
    'angle3'             : -55,
    'angleStart3'        : -165,
    'randomness'         : 0,
    'linesStrokeColor'   : None, # (0.8,),
    'linesStrokeWidth'   : 5,
    'linesDash'          : None,
    'circlesStrokeColor' : (0.8,),
    'circlesStrokeWidth' : 0,
    'circlesShadowDraw'  : False,
    'textDraw'           : False,
}

translate(88, 276)
rotate(90)
scale(0.2)
M2 = FontPartsMap()
M2.setAttributes(mapAttrs)
M2.draw((0, 0))




