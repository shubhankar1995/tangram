from collections import namedtuple
import re
from math import sqrt

def available_coloured_pieces(file):
    #input = file.read()
    input = ''
    for line in file:
        if 'path' in line:
            input = input + line
    ListPointDict = getCoordinates(input)
    return ListPointDict

def are_identical_sets_of_coloured_pieces(coloured_pieces_1, coloured_pieces_2):
    if len(coloured_pieces_1) != len(coloured_pieces_2):
        return False
    if coloured_pieces_1.keys() != coloured_pieces_2.keys():
        return False
    normalized_coloured_pieces_1_dict = {} #only 1st one will contain the refections as well
    normalized_coloured_pieces_2_dict = {}
    for piece in coloured_pieces_1:
        #need to check based on colour
        #from dict pull individual values and pass the list to get the normalized list 
        coloured_piece = coloured_pieces_1[piece] 
        normalized_coloured_piece = normalizePoints(coloured_piece) #input is list and output is list
        #now get all the reflections of the normazied point
        normalized_coloured_pieces_1_dict[piece] = getReflections(normalized_coloured_piece)
    for piece in coloured_pieces_2:
        coloured_piece = coloured_pieces_2[piece] 
        normalized_coloured_pieces_2_dict[piece] = normalizePoints(coloured_piece)
    #now compare the 2 dicts to look for a match
    if checkNormalizedPieces(normalized_coloured_pieces_1_dict, normalized_coloured_pieces_2_dict):
        return True
    return False

def checkNormalizedPieces(normalized_coloured_pieces_1_dict, normalized_coloured_pieces_2_dict):
    #compare the dict and return True or False
    #normalized_coloured_pieces_1_dict is the anchor (contains all the possible orientations)
    resultDict = {}
    for colour in normalized_coloured_pieces_1_dict:
        resultDict[colour] = False
        piece1List = normalized_coloured_pieces_1_dict[colour]
        piece2 = normalized_coloured_pieces_2_dict[colour]
        piece2.sort()
        for val in piece1List:
            val.sort()
            if val == piece2:
                resultDict[colour] = True
                break
                #return True
    for result in resultDict:
        if resultDict[result] == False:
            return False
    return True

def getReflections(normalized_coloured_piece):
    #input is a list of points and output the list of list of points of refelction and self
    normalized_coloured_piece_refelction = []
    normalized_coloured_piece_flipped = []
    normalized_coloured_piece_quad2 = []
    normalized_coloured_piece_quad3 = []
    normalized_coloured_piece_quad4 = []
    normalized_coloured_piece_quad2_flipped = []
    normalized_coloured_piece_quad3_flipped = []
    normalized_coloured_piece_quad4_flipped = []
    Point = namedtuple('Point', 'x y')
    #get the reflections of the points
    for points in normalized_coloured_piece:
        normalized_coloured_piece_flipped.append(Point(points.y, points.x))
        normalized_coloured_piece_quad2.append(Point(points.x*(-1), points.y))
        normalized_coloured_piece_quad3.append(Point(points.x*(-1), points.y*(-1)))
        normalized_coloured_piece_quad4.append(Point(points.x, points.y*(-1)))
        normalized_coloured_piece_quad2_flipped.append(Point(points.y, points.x*(-1)))
        normalized_coloured_piece_quad3_flipped.append(Point(points.y*(-1), points.x*(-1)))
        normalized_coloured_piece_quad4_flipped.append(Point(points.y*(-1), points.x))
    # create the final list
    normalized_coloured_piece_refelction.append(normalized_coloured_piece)
    normalized_coloured_piece_refelction.append(normalized_coloured_piece_flipped)
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad2))
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad3))
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad4))
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad2_flipped))
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad3_flipped))
    normalized_coloured_piece_refelction.append(getTranslateReflection(normalized_coloured_piece_quad4_flipped))
    return normalized_coloured_piece_refelction

def getTranslateReflection(normalized_coloured_piece_quad):
    # translate the list into ++ quadrant
    maxX = getMaxX(normalized_coloured_piece_quad)
    maxY = getMaxY(normalized_coloured_piece_quad)
    new_normalized_coloured_piece_quad = []
    Point = namedtuple('Point', 'x y')
    quad = getQuadrant(normalized_coloured_piece_quad)
    if quad == 1:
        for point in normalized_coloured_piece_quad:
            new_normalized_coloured_piece_quad.append(Point(point.x, point.y))
    elif quad == 2:
        for point in normalized_coloured_piece_quad:
            new_normalized_coloured_piece_quad.append(Point(point.x + maxX , point.y))
    elif quad == 3:
        for point in normalized_coloured_piece_quad:
            new_normalized_coloured_piece_quad.append(Point(point.x + maxX, point.y + maxY))
    elif quad == 4:
        for point in normalized_coloured_piece_quad:
            new_normalized_coloured_piece_quad.append(Point(point.x , point.y + maxY))
    return new_normalized_coloured_piece_quad


def getQuadrant(normalized_coloured_piece_quad):
    x = 1
    y = 1
    for point in normalized_coloured_piece_quad:
        if point.x < 0:
            x = -1
        if point.y < 0:
            y = -1
    if x > 0 and y > 0:
        return 1
    elif x < 0 and y > 0:
        return 2
    elif x < 0 and y < 0: 
        return 3
    elif x > 0 and y < 0:
        return 4


def normalizePoints(coloured_piece):
    #input is list of all the points and should return the normalized points
    Point = namedtuple('Point', 'x y')
    new_Points = []
    minX = getMinX(coloured_piece)
    minY = getMinY(coloured_piece)
    for points in coloured_piece:
        new_Points.append(Point(points.x - minX, points.y - minY))
    return new_Points #returns the points in the normalized form

def getMinX(points):
    minX = abs(points[0].x)
    for point in points:
        if minX > abs(point.x):
            minX = abs(point.x)
    return minX

def getMinY(points):
    minY = abs(points[0].y)
    for point in points:
        if minY > abs(point.y):
            minY = abs(point.y)
    return minY

def getMaxX(points):
    maxX = abs(points[0].x)
    for point in points:
        if maxX < abs(point.x):
            maxX = abs(point.x)
    return maxX

def getMaxY(points):
    maxY = abs(points[0].y)
    for point in points:
        if maxY < abs(point.y):
            maxY = abs(point.y)
    return maxY

def getCoordinates(input):
    Point = namedtuple('Point', 'x y')
    temp_list = []
    PiecesList = []
    ColourList = []
    PiecesDict = {}
    inputCordinates = re.findall('"([^"]*)"', input)
    for cord in inputCordinates:
        if 'M ' in cord and ' z' in cord:
            cord = cord.replace('M ','')
            cord = cord.replace(' z','')
            cord = cord.replace(' L ','L')
            temp_list.append(cord)
        else:
            ColourList.append(cord.strip())
    #print(temp_list)
    #print(ColourList)
    for val in temp_list:
        cordList = val.split('L')
        ListPoint = []
        for co in cordList:
            co = co.strip()
            coList = co.split(' ')
            ListPoint.append(Point(int(coList[0].strip()), int(coList[1].strip())))
        PiecesList.append(ListPoint)
    #print(PiecesList)
    for i in range(len(ColourList)):
        PiecesDict[ColourList[i]] = PiecesList[i]
    return PiecesDict

def getOrientation(pt1, pt2, pt3):
    det = (pt2.x - pt1.x)*(pt3.y - pt1.y) - (pt3.x - pt1.x)*(pt2.y - pt1.y)
    #print(pt1,pt2,pt3,det)
    return det

def checkConvexOrientation(val1, val2):
    if (val1 > 0 and val2 >0) or (val1 < 0 and val2 < 0):
        #print(val1,val2,'True')
        return True
    #print(val1,val2,'False')
    return False

def isCollinear(line1,line2):
    val1 = getOrientation(line1[0],line1[1],line2[0])
    val2 = getOrientation(line1[0],line1[1],line2[1])
    if val1 == 0 and val2 == 0:
        return True

def checkIntersection(line1, line2):
    #print("in checkIntersection")
    #print(line1, line2)
    #print(line1[0],line1[1],line2[0])
    #print(line1[0],line1[1],line2[1])
    val1 = getOrientation(line1[0],line1[1],line2[0])
    val2 = getOrientation(line1[0],line1[1],line2[1])
    if (val1 > 0 and val2 < 0) or (val1 < 0 and val2 > 0):
        #print('Checking IntersectionTrue', line1, line2)
        return True
    #print('False', line1, line2)
    return False

def checkSpecialIntersection(line1, line2):
    #print("in checkIntersection")
    #print(line1, line2)
    #print(line1[0],line1[1],line2[0])
    #print(line1[0],line1[1],line2[1])
    val1 = getOrientation(line1[0],line1[1],line2[0])
    val2 = getOrientation(line1[0],line1[1],line2[1])
    if not ((val1 > 0 and val2 >0) or (val1 < 0 and val2 < 0)):
        #print('Checking IntersectionTrue', line1, line2)
        return True
    #print('False', line1, line2)
    return False

def getLines(coloured_piece):
    lineList = []
    for i in range(len(coloured_piece) - 1):
        lineList.append([coloured_piece[i], coloured_piece[i+1]])
    lineList.append([coloured_piece[len(coloured_piece) -1], coloured_piece[0]])
    return lineList

def are_valid(coloured_pieces): 
    if len(coloured_pieces) < 1:
        return False 
    for piece in coloured_pieces:
        coloured_piece = coloured_pieces[piece]
        num = len(coloured_piece)
        if num < 3:
            return False
        else:
            orientations = []
            for i in range(num - 2):
                orientations.append(getOrientation(coloured_piece[i],coloured_piece[i+1],coloured_piece[i+2]))
            orientations.append(getOrientation(coloured_piece[num - 2], coloured_piece[num- 1], coloured_piece[0]))
            orientations.append(getOrientation(coloured_piece[num - 1], coloured_piece[0], coloured_piece[1]))
            #print('Reached orientations',orientations)
            for i in range(len(orientations) - 1):
                if not checkConvexOrientation(orientations[i], orientations[i+1]):
                    return False
            lineList = getLines(coloured_piece)
            #print('Reached lines',lineList)
            for i in range(len(lineList)):
                for j in range(len(lineList)):
                    if i != j and j>i+1 and not (i == 0 and j == len(lineList) - 1):
                        if (checkIntersection(lineList[i], lineList[j]) and checkIntersection(lineList[j], lineList[i])) or isCollinear(lineList[i], lineList[j]) and isCollinear(lineList[j], lineList[i]):
                            return False
    return True


def areaOfPiece(vertices):
    vertices.append(vertices[0])
    count = len(vertices)
    area = 0.0
    for i in range(count - 1):
        area = area + ((vertices[i+1].x + vertices[i].x) * (vertices[i+1].y - vertices[i].y))
    area = abs(area)
    area = area/2
    return area

def pointPositionInside(ptx, pty, shape):
    #define a point linearly on the the x axis at a near infinity x value as 100000 point
    #this line should intersect with the shape lines
    #use odd-even rule
    #print("in pointPositionInside")
    #print(ptx, pty)
    #print(shape)
    Point = namedtuple('Point', 'x y')
    pointLine = [Point(ptx, pty), Point(100000, pty)]
    count = 0
    #print(pointLine)
    vertexHit = 0
    for shape_line in shape:
        if checkSpecialIntersection(pointLine, shape_line) and checkSpecialIntersection(shape_line, pointLine):
            if checkIntersection(pointLine, shape_line) and checkIntersection(shape_line, pointLine):
                count = count + 1
            else:
                vertexHit = vertexHit + 1
    #if vertexHit > 0:
    #    count = count + 1
    #print(vertexHit, count)
    if count%2 == 1:
        return True
    else:
        if vertexHit > 0:
            count = count + 1
            if count%2 == 1:
                return True
    return False

def pointOnShape(ptx, pty, shape):
    #sum of distance from the point to the vertex will be equal to the length of the line segment
    Point = namedtuple('Point', 'x y')
    for shape_line in shape:
        if round(distanceBetweenPoint(shape_line[0], shape_line[1])) == round(distanceBetweenPoint(shape_line[0], Point(ptx, pty)) + distanceBetweenPoint(shape_line[1], Point(ptx, pty))):
            return True
    return False

def distanceBetweenPoint(pt1, pt2):
    return sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)

def checkPieceOnShape(piece, shape):
    #move the coordinate to check if the value is still on the piece and also in the shape
    Point = namedtuple('Point', 'x y')
    flag = True
    temp_point = Point((piece[0].x + piece[1].x)/2 + 1, (piece[0].y + piece[1].y)/2 + 1)
    if pointPositionInside(temp_point.x, temp_point.y, getLines(piece)):
        #print("1")
        flag = False
    if flag:
        temp_point = Point((piece[0].x + piece[1].x)/2 + 1, (piece[0].y + piece[1].y)/2 - 1)
        if pointPositionInside(temp_point.x, temp_point.y, getLines(piece)):
            #print("2")
            flag = False
    if flag:
        temp_point = Point((piece[0].x + piece[1].x)/2 - 1, (piece[0].y + piece[1].y)/2 + 1)
        if pointPositionInside(temp_point.x, temp_point.y, getLines(piece)):
            #print("3")
            flag = False
    if flag:
        temp_point = Point((piece[0].x + piece[1].x)/2 - 1, (piece[0].y + piece[1].y)/2 - 1)
        if pointPositionInside(temp_point.x, temp_point.y, getLines(piece)):
            #print("4")
            flag = False
    if not flag:
        #print(temp_point)
        if not pointPositionInside(temp_point.x, temp_point.y, shape):
            return False
    return True

def is_solution(tangram, shape):
    #check if the area of all peices in the tangram are equal to the shape
    area_tangram = 0
    area_shape = 0
    for piece in shape:
        area_shape = area_shape + areaOfPiece(shape[piece])   
    for piece in tangram:
        area_tangram = area_tangram + areaOfPiece(tangram[piece])
    if area_shape != area_tangram:
        #print(area_shape, area_tangram)
        return False
    #check for intersection of peices
    shapePoints = []
    for val in shape:
        shapePoints = shape[val]
        ShapeLineList = getLines(shape[val])
    for piece1 in tangram:
        pieceLineList1 = getLines(tangram[piece1])
        #check for intersection of the peice and the shape
        for shapeLine in ShapeLineList:
            for line1 in pieceLineList1:
                if checkIntersection(line1, shapeLine) and checkIntersection(shapeLine, line1):
                    #print(line1, shapeLine)
                    return False
        for piece2 in tangram:
            if piece1 != piece2:
                pieceLineList2 = getLines(tangram[piece2])
                for line1 in pieceLineList1:
                    for line2 in pieceLineList2:
                        if checkIntersection(line1, line2) and checkIntersection(line2, line1):
                            #print(line1, line2)
                            return False
    for piece in tangram:
        for point in tangram[piece]:
            if not pointPositionInside(point.x, point.y, getLines(shapePoints)):
                #print("failed here")
                if not pointOnShape(point.x, point.y, getLines(shapePoints)):
                    #print(point.x, point.y)
                    #print("failed")
                    return False
        if not checkPieceOnShape(tangram[piece], getLines(shapePoints)):
            return False
    #to check overlapping of pieces
    '''for piece1 in tangram:
        for piece2 in tangram:
            if piece1 != piece2:
                for points in tangram[piece1]:
                    if pointSpecialPositionInside(points.x, points.y, getLines(tangram[piece2])):
                        #if not pointOnShape(points.x, points.y, getLines(tangram[piece2])):
                        return False'''
    return True

def pointSpecialPositionInside(ptx, pty, shape):
    #define a point linearly on the the x axis at a near infinity x value as 100000 point
    #this line should intersect with the shape lines
    #use odd-even rule
    #print("in pointPositionInside")
    #print(ptx, pty)
    #print(shape)
    Point = namedtuple('Point', 'x y')
    pointLine = [Point(ptx, pty), Point(100000, pty)]
    count = 0
    #print(pointLine)
    vertexHit = 0
    for shape_line in shape:
        if checkIntersection(pointLine, shape_line) and checkIntersection(shape_line, pointLine):
            count = count + 1
    #if vertexHit > 0:
    #    count = count + 1
    #print(vertexHit, count)
    if count%2 == 1:
        return True
    return False
