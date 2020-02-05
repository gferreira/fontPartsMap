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

typeAttrs = {
    'scale'  : 0.17,
    'interpolationFactor' : 0.5,
    'layers' : {
        'font'      : False,
        'font lib'  : False,
        'info'      : False,
        'groups'    : False, 
        'kerning'   : False,
        'features'  : False,
        'layer'     : True,
        'glyph'     : False,
        'glyph lib' : False,
        'anchor'    : False,
        'component' : False,
        'image'     : False,
        'guideline' : True,
        'contour'   : False,
        'point'     : False,
        'bPoint'    : True,
        'segment'   : False,
    },
    'infoStrokeWidth'       : 7,
    'infoValuesDraw'        : True,
    'infoLineDash'          : None, # 20, 20
    'contourStrokeWidth'    : 8,
    'glyphWidthStrokeWidth' : 8,
    'glyphWidthDraw'        : True,
    'glyphDataDraw'         : True,
    'guidelineValuesDraw'   : False,
    'segmentStrokeWidth'    : 10,
    'bPointSize'            : 25,
    'pointSize'             : 20,
    'captionSize'           : 40,
    'captionSizeLarge'      : 60,
    'captionFont'           : 'Menlo-Bold'
}

length = 180

mapAttrs = {
    'textDraw'           : False,
    'dimColor'           : (0.8,),
}

f = OpenFont(ufoPath)
L = FontPartsLogoType(f)
L.setAttributes(typeAttrs)

M = FontPartsMap()
M.setAttributes(mapAttrs)

def drawPage(L, M, index=True):
    frameDuration(2)
    fill(1)
    rect(0, 0, width(), height())

    translate(50, 100)
    L.draw((0, 0))

    translate(100, 352)
    with savedState():
        scale(0.4)
        M.draw((0, 0))
    
    if index:
        objectNames = L.layers.keys()
        T = FormattedString(font='Menlo-Bold', fontSize=10, lineHeight=14)
        for obj in objectNames:
            c = L.colorScheme.colorsRGB[obj] if not obj in M.dimObjects else M.dimColor
            txt = f'{obj}\n' # if obj in M.tree.keys() else f'\t{obj}\n' 
            T.append(txt, fill=c)
        text(T, (300, 80))

# ----------    
# make pages
# ----------
    
index = True
    
for step in ['font', 'info', 'layer', 'glyph', 'anchor', 'guideline', 'contour', 'point', 'bPoint', 'segment']:
    newPage('A4Landscape')
    for layer in L.layers:
        L.layers[layer] = True if layer == step else False
    M.dimObjects = [k for k, v in typeAttrs['layers'].items() if not v]
    drawPage(L, M, index)

newPage('A4Landscape')
for layer in L.layers:
    L.layers[layer] = True
    M.dimObjects = []
L.layers['layer'] = False
L.layers['contour'] = False
drawPage(L, M, index)

folder = os.getcwd()
pdfPath = os.path.join(folder, 'FontParts.gif')
print(pdfPath)
saveImage(pdfPath)
