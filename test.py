from importlib import reload

import fontPartsMap
reload(fontPartsMap)

from fontPartsMap import FontPartsMap

#------------------
# big vertical map
#------------------

attrsDict = {
    'radius1'            : 55,
    'radius2'            : 87,
    'length1'            : 180,
    'length2'            : 180,
    'length3'            : 150,
    'angle1'             : 50,
    'angleStart1'        : 0,
    'angle2'             : -45,
    'angleStart2'        : 30,
    'angle3'             : -55,
    'angleStart3'        : -165,
    'randomness'         : 1,
    'linesStrokeColor'   : (0.6,),
    'linesStrokeWidth'   : 5,
    'linesDash'          : (1, 8),
    'circlesStrokeColor' : (0.8,),
    'circlesStrokeWidth' : 0,
}

M = FontPartsMap()
M.setAttributes(attrsDict)
M.draw((450, 700))

#----------------------
# small horizontal map
#----------------------

attrsDict2 = {
    'radius1'            : 55,
    'radius2'            : 87,
    'length1'            : 160,
    'length2'            : 160,
    'length3'            : 140,
    'angle1'             : 50,
    'angleStart1'        : 0,
    'angle2'             : -45,
    'angleStart2'        : 30,
    'angle3'             : -55,
    'angleStart3'        : -165,
    'randomness'         : 0,
    'linesStrokeColor'   : None,
    'linesStrokeWidth'   : 5,
    'linesDash'          : None,
    'circlesStrokeColor' : (0.8,),
    'circlesStrokeWidth' : 0,
    'circlesShadowDraw'  : False,
    'textDraw'           : False,
}

translate(818, 898)
rotate(90)
scale(0.2)
M2 = FontPartsMap()
M2.setAttributes(attrsDict2)
M2.draw((0, 0))




