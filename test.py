from importlib import reload

import fontPartsMap
reload(fontPartsMap)

from fontPartsMap import FontPartsMap

M = FontPartsMap()

M.radius1 = 55
M.radius2 = 87

M.length1 = 180
M.length2 = 180
M.length3 = 150

M.angle1, M.angleStart1 = 50, 0
M.angle2, M.angleStart2 = -45, 30
M.angle3, M.angleStart3 = -55, -165

M.randomness = 0

M.linesStrokeColor = 0.6,
M.linesStrokeWidth = 5
M.linesDash = 1, 8
M.circlesStrokeColor = 0.8,
M.circlesStrokeWidth = 0

M.landscape = False

fill(1)
rect(0, 0, width(), height())
M.draw((500, 700))
