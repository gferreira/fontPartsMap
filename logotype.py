import os
import drawBot
from fontPartsMap import FontPartsMap, FontPartsColorScheme
from fontTools.agl import UV2AGL
from fontParts.world import OpenFont

def getKerningForPair(font, glyphName1, glyphName2):
    for kPair in font.kerning.keys():
        print(glyphName, kPair, glyphName==kPair[0])

def countContoursPoints(f):
    nContours = 0
    nPoints = 0
    for g in f:
        for c in g:
            nContours += 1
            for pt in c.points:
                nPoints += 1
    return nContours, nPoints

class FontPartsLogoType:

    colorScheme = FontPartsColorScheme()
    txt = 'FontParts'

    layers = {
        'font'      : False,
        'glyph'     : True,
        'font lib'  : False,
        'info'      : True,
        'kerning'   : False,
        'features'  : False,
        'glyph lib' : False,
        'anchor'    : True,
        'component' : True,
        'image'     : False,
        'guideline' : False,
        'contour'   : True,
        'point'     : True,
        'bPoint'    : False,
        'segment'   : False,
        'layer'     : False,
    }
    scale = 0.2

    fontSizeLarge = 90

    captionFont = 'Menlo'
    captionSize = 42

    pointSize = 16

    bPointSize = pointSize * 2

    anchorSize = pointSize * 2
    anchorStrokeWidth = 5
    anchorDraw = True

    infoStrokeWidth = anchorStrokeWidth
    infoLineDash = 10, 10
    infoValuesDraw = True

    glyphWidthDraw = True
    glyphWidthStrokeWidth = anchorStrokeWidth
    glyphDataDraw = True

    contourStrokeWidth = anchorStrokeWidth

    def __init__(self, font):
        self.font = font

    @property
    def textLength(self):
        w = 0
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            w += self.font[glyphName].width
        return w

    @property
    def lineGap(self):
        L  = self.font.info.unitsPerEm
        L -= abs(self.font.info.descender) + self.font.info.ascender
        return L

    @property
    def yBottom(self):
        return -abs(self.font.info.descender) - self.lineGap * 0.5

    @property
    def yTop(self):
        return self.font.info.ascender + self.lineGap * 0.5

    def drawFont(self):
        color = self.colorScheme.colorsRGB['font']
        drawBot.save()
        drawBot.fill(*color)
        drawBot.fontSize(self.fontSizeLarge)
        h = self.fontSizeLarge * 1.5
        m = 20
        y = self.yBottom - h - 20
        txt  = '%s glyphs / ' % len(self.font)
        txt += '%s contours / %s points ' % countContoursPoints(self.font)
        drawBot.textBox(txt, (0, y, self.textLength, h), align='center')
        drawBot.restore()

    def drawGlyph(self):
        color = self.colorScheme.colorsRGB['glyph']
        drawBot.save()
        drawBot.fontSize(self.captionSize)
        drawBot.font(self.captionFont)
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            # contours
            drawBot.fill(*color)
            B = drawBot.BezierPath()
            for contour in glyph.contours:
                contour.draw(B)
            drawBot.drawPath(B)
            # advance width
            if self.glyphWidthDraw:
                drawBot.save()
                drawBot.strokeWidth(self.glyphWidthStrokeWidth)
                drawBot.stroke(*color)
                drawBot.line((0, self.yBottom), (0, self.yTop))
                drawBot.restore()
            # glyph data
            if self.glyphDataDraw:
                h = self.captionSize * 1.5
                m = 40
                w = glyph.width - m * 2
                drawBot.save()
                drawBot.stroke(None)
                drawBot.fill(*color)
                y = self.yBottom
                drawBot.textBox(glyph.name, (m, y, w, h))
                drawBot.textBox(str(glyph.unicode), (m, y, w, h), align='right')
                y = self.yTop - h
                drawBot.textBox(str(int(glyph.width)), (m, y, w, h), align='center')
                drawBot.restore()
            # done glyph
            drawBot.translate(glyph.width, 0)
        # last margin
        if self.glyphWidthDraw:
            drawBot.strokeWidth(self.glyphWidthStrokeWidth)
            drawBot.stroke(*color)
            drawBot.line((0, self.yBottom), (0, self.yTop))
        # done
        drawBot.restore()

    def drawFontLib(self):
        pass

    def drawInfo(self):
        color = self.colorScheme.colorsRGB['info']
        drawBot.save()

        # font info
        # fill(*color)
        # fontSize(self.fontSizeLarge)
        # h = 200
        # y = self.yTop
        # txt  = '%s %s' % (self.font.info.familyName, self.font.info.styleName)
        # txt += ' (%s)' % self.font.info.designer
        # textBox(txt, (0, y, self.textLength, h))

        # blue zones
        # for i, y in enumerate(self.font.info.postscriptBlueValues):
        #     if not i % 2:
        #         yNext = self.font.info.postscriptBlueValues[i+1]
        #         h = yNext - y
        #         fill(*color + (0.35,))
        #         rect(0, y, self.textLength, h)

        # vertical dimensions
        yValues = [
            0,
            self.font.info.xHeight,
            # self.font.info.capHeight,
            self.font.info.descender,
            self.font.info.ascender,
        ]
        drawBot.font(self.captionFont)
        drawBot.fontSize(self.captionSize)
        for y in yValues:
            # draw guide
            drawBot.stroke(*color)
            drawBot.strokeWidth(self.infoStrokeWidth)
            if not self.infoLineDash:
                drawBot.lineDash(None)
            else:
                drawBot.lineDash(*self.infoLineDash)
            drawBot.line((0, y), (self.textLength, y))
            # draw y value
            if self.infoValuesDraw:
                w = 300
                m = 50
                drawBot.save()
                drawBot.stroke(None)
                drawBot.fill(*color)
                drawBot.textBox('%.1f'% y, (-w-m, y-self.captionSize*0.5, w, self.captionSize*1.2), align='right')
                drawBot.restore()
        # done
        drawBot.restore()

    def drawKerning(self):
        # for i, char in enumerate(self.txt):
        #     if i < len(self.txt) - 1:
        #         glyphName = char
        #         glyphNameNext = charNext = self.txt[i+1]
        #         print(glyphName, glyphNameNext)
        pass

    def drawFeatures(self):
        pass

    def drawGlyphLib(self):
        # print('glyph lib')
        pass

    def drawAnchor(self):
        r = self.anchorSize * 0.5
        color = self.colorScheme.colorsRGB['anchor']
        drawBot.save()
        drawBot.strokeWidth(self.anchorStrokeWidth)
        drawBot.stroke(*color)
        drawBot.fill(None)
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            if len(glyph.anchors):
                for anchor in glyph.anchors:
                    x, y = anchor.x, anchor.y
                    drawBot.oval(x-r, y-r, r*2, r*2)
                    drawBot.line((x-r, anchor.y), (x+r, anchor.y))
                    drawBot.line((anchor.x, y-r), (anchor.x, y+r))
            drawBot.translate(glyph.width, 0)
        drawBot.restore()

    def drawComponent(self):
        color = self.colorScheme.colorsRGB['component']
        tempName = '_tmp_'
        drawBot.save()
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            drawBot.fill(*color + (0.5,))
            drawBot.stroke(*color)
            if len(glyph.components):
                B = drawBot.BezierPath()
                for component in glyph.components:
                    component.draw(B)
                drawBot.drawPath(B)
            # done glyph
            drawBot.translate(glyph.width, 0)
        drawBot.restore()

    def drawImage(self):
        # print('image')
        pass

    def drawGuideline(self):
        # print('guideline')
        pass

    def drawContour(self):
        color = self.colorScheme.colorsRGB['contour']
        drawBot.save()
        drawBot.fontSize(self.captionSize)
        drawBot.font(self.captionFont)
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            # draw contours
            drawBot.stroke(*color)
            drawBot.strokeWidth(self.contourStrokeWidth)
            drawBot.fill(None)
            B = drawBot.BezierPath()
            for contour in glyph.contours:
                contour.draw(B)
            drawBot.drawPath(B)
            # done glyph
            drawBot.translate(glyph.width, 0)
        drawBot.restore()

    def drawPoint(self):
        r = self.pointSize * 0.5
        color = self.colorScheme.colorsRGB['point']
        drawBot.save()
        drawBot.fill(*color)
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            for c in glyph.contours:
                for pt in c.points:
                    x, y = pt.x, pt.y
                    drawBot.oval(x-r, y-r, r*2, r*2)
            drawBot.translate(glyph.width, 0)
        drawBot.restore()

    def drawBPoint(self):
        r = self.bPointSize * 0.5
        color = self.colorScheme.colorsRGB['bPoint']
        drawBot.save()
        drawBot.fill(None)
        drawBot.stroke(*color)
        drawBot.strokeWidth(5)
        for char in self.txt:
            uni = ord(char)
            glyphName = UV2AGL.get(uni)
            glyph = self.font[glyphName]
            for c in glyph.contours:
                for pt in c.bPoints:
                    x, y = pt.anchor
                    drawBot.oval(x-r, y-r, r*2, r*2)
                    xIn,  yIn  = pt.bcpIn
                    xOut, yOut = pt.bcpOut
                    drawBot.line((x, y), (x + xIn, y + yIn))
                    drawBot.line((x, y), (x + xOut, y + yOut))
            drawBot.translate(glyph.width, 0)
        drawBot.restore()

    def drawSegment(self):
        # print('segment')
        pass

    def drawLayer(self):
        # print('layer')
        pass

    def draw(self, pos):
        x, y = pos
        drawBot.save()
        drawBot.translate(x, y)
        drawBot.scale(self.scale)
        if self.layers['font']:      self.drawFont()
        if self.layers['info']:      self.drawInfo()
        if self.layers['glyph']:     self.drawGlyph()
        if self.layers['font lib']:  self.drawFontLib()
        if self.layers['kerning']:   self.drawKerning()
        if self.layers['features']:  self.drawFeatures()
        if self.layers['glyph lib']: self.drawGlyphLib()
        if self.layers['anchor']:    self.drawAnchor()
        if self.layers['component']: self.drawComponent()
        if self.layers['image']:     self.drawImage()
        if self.layers['guideline']: self.drawGuideline()
        if self.layers['contour']:   self.drawContour()
        if self.layers['point']:     self.drawPoint()
        if self.layers['bPoint']:    self.drawBPoint()
        if self.layers['segment']:   self.drawSegment()
        if self.layers['layer']:     self.drawLayer()
        drawBot.restore()

#---------
# testing
#---------

if __name__ == '__main__':

    folder = os.getcwd()
    ufoPath = os.path.join(folder, 'FontParts.ufo')

    size('A4Landscape')

    f = OpenFont(ufoPath)
    L = FontPartsLogoType(f)
    L.draw((60, 100))

    L.scale = 0.11
    L.layers['contour'] = True
    L.layers['anchor'] = False
    L.layers['bPoint'] = False
    L.layers['point'] = False
    L.infoStrokeWidth = 10
    L.infoValuesDraw = False
    L.infoLineDash = None # 90, 30
    L.contourStrokeWidth = 20
    L.glyphWidthStrokeWidth = 15
    L.glyphDataDraw = False
    L.pointSize = 40
    L.captionSize = 70
    L.captionFont = 'Menlo-Bold'
    L.draw((60, 400))
