from importlib import reload

import fontPartsMap
reload(fontPartsMap)

from fontPartsMap import *

size('A4Landscape')
position = 40, 100
cellSize = 100, 80
padding  = 5

C = FontPartsColorScheme()
C.drawSwatches(position, cellSize, padding, captions=True)
