from importlib import reload
import fontPartsMap
reload(fontPartsMap)

from grapefruit import Color
from fontPartsMap import FontPartsColorScheme

size('A4Landscape')
position = 40, 100
cellSize = 100, 80
padding  = 5
C = FontPartsColorScheme()
C.makeColors()
C.drawSwatches(position, cellSize, padding, captions=True)

for obj in C.colorsRGB.keys():
    print(obj, C.colorsRGB[obj])
