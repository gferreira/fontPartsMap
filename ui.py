from importlib import reload
import fontPartsMap
reload(fontPartsMap)

from fontPartsMap import FontPartsMapUI

size(1000, 800)
fill(1)
rect(0, 0, width(), height())

M = FontPartsMapUI()
