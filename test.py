from importlib import reload

import fontPartsMap
reload(fontPartsMap)

from fontPartsMap import FontPartsMap

size(1000, 700)

attrsDict = {

    'radius1'            : 60,
    'radius2'            : 70,

    'length1'            : 180,
    'length2'            : 180,
    'length3'            : 170,

    'angle1'             : 50,
    'angle2'             : -50,
    'angle3'             : 50,

    'angleStart0'        : 5,
    'angleStart1'        : 63,
    'angleStart2'        : 124,
    'angleStart3'        : 186,
    'angleStart4'        : 0,

    'randomness'         : 0,

    'linesStrokeColor'   : (0.6,),
    'linesStrokeWidth'   : 13,
    'linesDash'          : (1, 5),
    'linesDraw'          : True,
    'linesGradient'      : True,

    # 'circlesStrokeColor' : (0.8,),
    # 'circlesStrokeWidth' : 0,
    'circlesShadowDraw'  : False, 

}

M = FontPartsMap()
M.setAttributes(attrsDict)
M.draw((270, 400))
