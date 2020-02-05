from fontPartsMap import FontPartsMap

M = FontPartsMap()
M.randomness = 10

for i in range(20):
    newPage(600, 400)
    fill(1)
    rect(0, 0, width(), height())
    frameDuration(0.05)
    scale(0.63)
    translate(285, 373)
    M.draw()

saveImage('fontPartsMap.gif')
