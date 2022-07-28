#!/bin/python3.9
import copy

board = {"8":{"a":" BR","b":"BKn","c":" BB","d":" BQ","e":" BK","f":" BB","g":"BKn","h":" BR"},
         "7":{"a":" BP","b":" BP","c":" BP","d":" BP","e":" BP","f":" BP","g":" BP","h":" BP"},
         "6":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "5":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "4":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "3":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "2":{"a":" WP","b":" WP","c":" WP","d":" WP","e":" WP","f":" WP","g":" WP","h":" WP"},
         "1":{"a":" WR","b":"WKn","c":" WB","d":" WQ","e":" WK","f":" WB","g":"WKn","h":" WR"}}

epav = False
wRCastle = True
wLCastle = True
bRCastle = True
bLCastle = True

def printHeatMap(hMap):
    for y in ["8", "7", "6", "5", "4", "3", "2", "1"]:
        for x in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print(" ", end="")
            if hMap[y][x] == "":
                print(".", end="")
            else:
                print(hMap[y][x], end="")
            print(" ", end="")
        print("")
    print("------------------------")

def formCheck(pos):
    if (pos[1:2] in "12345678") and (pos[:1] in "abcdefgh"):
        return True
    else:
        return False

def makeMove(moveIn, board, real):
    if real:
        if board[moveIn[1]][moveIn[0]][1] == "W":
            col = "W"
            startY = "1"
            epPos = "5"
            pPos = "8"
        else:
            col = "B"
            startY = "8"
            epPos = "4"
            pPos = "1"
        if board[moveIn[1]][moveIn[0]] == " " + col + "P" and moveIn[1] == epPos and moveIn[2] != moveIn[0]:
            board[moveIn[1]][moveIn[2]] = "   "
        if board[moveIn[1]][moveIn[0]] == " " + col + "P" and moveIn[3] == pPos:
            while True:
                promotion = input("Select a piece to promote to (R, Kn, B, Q):")
                if promotion in ("R", "Kn", "B", "Q"):
                    if promotion == "Kn":
                        board[moveIn[1]][moveIn[0]] = (col + promotion)
                    else:
                        board[moveIn[1]][moveIn[0]] = (" " + col + promotion)
                    break
                else:
                    print("Invalid input")
        if board[moveIn[1]][moveIn[0]] == (" " + col + "K") and moveIn[2] == "g" and moveIn[0:2] == "e" + startY:
            board[moveIn[1]]["h"] = "   "
            board[moveIn[1]]["f"] = " " + col + "R"
        elif board[moveIn[1]][moveIn[0]] == " " + col + "K" and moveIn[2] == "c" and moveIn[0:2] == "e" + startY:
            board[moveIn[1]]["a"] = "   "
            board[moveIn[1]]["d"] = " " + col + "R"
    board[moveIn[-1:]][moveIn[-2:-1]] = board[moveIn[1:2]][moveIn[:1]]
    board[moveIn[1:2]][moveIn[:1]] = "   "
    return board

def printBoard(board, count):
    if count == 1:
        print(("\033cSean's terminal chess\n\n" + 
               "To move you must put the position of the peice \n" +
               "you want to move then the position you want to \n" +
               "move it to. You can exit the program by typing \n" +
               "exit.\n\n" + 
               "   ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗"))
    else:
        print("\033c\n" + "   ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗")
#       print("\n" + "   ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗")
    for y in ("87654321"):
        print(" " + y + " ║", end="")
        for x in ("abcdefgh"):
            print(board[y][x], end="")
            if x == "h":
                print("║")
                break
            print("│", end="")
        if y == "1":
            print("   ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝" + "\n     A   B   C   D   E   F   G   H\n")
            break
        print("   ╟───┼───┼───┼───┼───┼───┼───┼───╢")

def intCon(val):
    yAxis = {"8" : 0, "7" : 1, "6" : 2, "5" : 3, "4" : 4, "3" : 5, "2" : 6, "1" : 7}
    xAxis = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    if val in "87654321":
        return yAxis[val]
    elif val in "abcdefgh":
        return xAxis[val]

def strCon(val, axis):
    yAxis = ("8" ,"7" ,"6" ,"5" ,"4" ,"3" ,"2" ,"1")
    xAxis = ("a" ,"b" ,"c" ,"d" ,"e" ,"f" ,"g" ,"h")
    if axis == "y":
        return yAxis[val]
    elif axis == "x":
        return xAxis[val]

def validPiece(col, board, Y, X):
    for piece in ("K", "P", "B", "Q", "R"):
        if board[Y][X] == (" " + col + piece) or board[Y][X] == (col + "Kn"):
            return True

def direcCheck(board, x, y, direction, col):
    atkPositions = []
    if direction == "h": 
        stateList = [{"y":1, "x":0}, {"y":-1, "x":0}, {"y":0, "x":-1}, {"y":0, "x":1}]
        mulList = range(1,8)
    elif direction == "d":
        stateList = [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}]
        mulList = range(1,8)
    else: 
        return atkPositions
    for state in stateList:
        for mul in range(1, 8):
            yVal = intCon(y) + (mul * state["y"])
            xVal = intCon(x) + (mul * state["x"])
            if (yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1):
                break
            else:
                Y = (strCon(yVal, "y"))
                X = (strCon(xVal, "x"))
                if validPiece(col, board, Y, X):
                    break
                else:
                    atkPositions.append(Y+X)
                    if board[Y][X] != "   ":
                        break
    return atkPositions

def knightCheck(board, x, y, col):
    atkPositions = []
    for state in [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}]:
        for mul in ((1, 2), (2, 1)):
            yVal = intCon(y) + (mul[0] * state["y"])
            xVal = intCon(x) + (mul[1] * state["x"])
            if not ((yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1)):
                Y = (strCon(yVal, "y"))
                X = (strCon(xVal, "x"))
                if validPiece(col, board, Y, X):
                    pass
                else:
                    atkPositions.append(Y+X)
    return atkPositions

def kingCheck(board, x, y, col):
    atkPositions = []
    for state in [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}, 
                  {"y":1, "x":0}, {"y":-1, "x":0}, {"y": 0, "x":-1}, {"y":0, "x": 1}]:
        yVal = intCon(y) + state["y"]
        xVal = intCon(x) + state["x"]
        if not ((yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1)):
            Y = (strCon(yVal, "y"))
            X = (strCon(xVal, "x"))
            if validPiece(col, board, Y, X):
                pass
            else:
                atkPositions.append(Y+X)
    return atkPositions

def pawnCheck(board, x, y, col):
    atkPositions = []
    global epav
    if col == "B":
        stateList = [{"y":1, "x":1}, {"y":1, "x":-1}]
        row = "4"
        eprow = "5"
        pass
        oppCol = " WP"
    elif col == "W":
        stateList = [{"y":-1, "x":1}, {"y":-1, "x":-1}]
        row = "5"
        eprow = "4"
        oppCol = " BP"
    else:
        return atkPositions
    for state in stateList:
       yVal = (intCon(y) + state["y"])
       xVal = (intCon(x) + state["x"])
       if not (intCon(x) + state["x"] >= 8 or intCon(x) + state["x"] <= -1):
            if board[row][strCon(intCon(x) + state["x"], "x")] == oppCol and y == row and epav:
                atkPositions.append(row + strCon(intCon(x) + state["x"], "x"))
            Y = (strCon(yVal, "y"))
            X = (strCon(xVal, "x"))
            atkPositions.append(Y+X)
    return atkPositions

def attackMap(board, col):
    atkMap = {"8":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "7":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "6":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "5":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "4":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "3":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "2":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "1":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""}}
    for y in ("87654321"):
        for x in ("abcdefgh"):
            if board[y][x][:2] == (" " + col) or board[y][x][:1] == col:
                peice = board[y][x]
                if peice == (col + "Kn"):
                    for i in knightCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
                elif peice == (" " + col + "R"):
                    for i in direcCheck(board, x, y, "h", col):
                        atkMap[i[0]][i[1]] = "x"
                elif peice == (" " + col + "B"):
                    for i in direcCheck(board, x, y, "d", col):
                        atkMap[i[0]][i[1]] = "x"
                elif peice == (" " + col + "Q"):
                    for i in (direcCheck(board, x, y, "d", col) + direcCheck(board, x, y, "h", col)):
                        atkMap[i[0]][i[1]] = "x"
                elif peice == (" " + col + "K"):
                    for i in kingCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
                elif peice == (" " + col + "P"):
                    for i in pawnCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
    return atkMap

def oppositeCol(col):
    if col == "white":
        return "B"
    elif col == "black":
        return "W"

def findCol(col):
    if col == "white":
        return "W"
    elif col == "black":
        return "B"

def pawnMoveCheck(board, x, y, col):
    movePos = []
    global epav
    if y == "2" or y == "7":
        jumpList = (1, 2)
    else:
        jumpList = (0,1)
    for i in jumpList:
        if col == "W":
            if y == "5" and board[y][strCon((intCon(x) + 1), "x")] == " BP" and epav:
                movePos.append(strCon((intCon(y) - 1), "y") + strCon((intCon(x) + 1), "x"))
            if y == "5" and board[y][strCon((intCon(x) - 1), "x")] == " BP" and epav:
                movePos.append(strCon((intCon(y) - 1), "y") + strCon((intCon(x) - 1), "x"))
            if board[strCon((intCon(y) - i), "y")][x] == "   ":
                movePos.append(strCon((intCon(y) - i), "y") + x)
        elif col == "B":
            if y == "4" and board[y][strCon((intCon(x) + 1), "x")] == " WP" and epav:
                movePos.append(strCon((intCon(y) + 1), "y") + strCon((intCon(x) + 1), "x"))
            if y == "4" and board[y][strCon((intCon(x) - 1), "x")] == " WP" and epav:
                movePos.append(strCon((intCon(y) + 1), "y") + strCon((intCon(x) - 1), "x"))
            if board[strCon((intCon(y) + i), "y")][x] == "   ":
                movePos.append(strCon((intCon(y) + i), "y") + x)
    return movePos

def kingSafetyCheck(board, col, oppCol, start, end):
    if board[start[1]][start[0]] == (" " + col + "K"):
        return attackMap(makeMove(start + end, copy.deepcopy(board), False), oppCol)[end[1]][end[0]]
    else:
        for y in ["8", "7", "6", "5", "4", "3", "2", "1"]:
            for x in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                if board[y][x] == (" " + col + "K"):
                    return attackMap(makeMove(start + end, copy.deepcopy(board), False), oppCol)[y][x]

def castleCheck(col, oppCol, start, end, board):
    global wLCastle
    global wRCastle
    global bLCastle
    global bRCastle
    if end != "c1" and end != "g1" and end != "c8" and end != "g8":
        return False
    if col == "W" and (wRCastle or wLCastle):
        trueStart = "e1"
    elif col == "B" and (bRCastle or bLCastle):
        trueStart = "e8"
    else:
        return False
    if end[0] == "c" and board[trueStart[1]]["a"] == (" " + col + "R"):
        if (wLCastle and col == "W") or (bLCastle and col == "B"):
            aCheckList = ["b", "c", "d"]
            bCheckList = ["c", "d", "e"]
        else:
            return False
    elif end[0] == "g" and board[trueStart[1]]["h"] == (" " + col + "R"):
        if (wRCastle and col == "W") or (bRCastle and col == "B"):
            aCheckList = ["f", "g"]
            bCheckList = ["e", "f", "g"]
        else:
            return False
    if board[trueStart[1]][trueStart[0]] == (" " + col + "K"):
        for x in aCheckList:
            if board[trueStart[1]][x] != "   ":
                return False
        for x in bCheckList:
            if attackMap(board, oppCol)[trueStart[1]][x] == "x":
                return False
        return True

def posCheck(start, end, trnCol, board):
    col = findCol(trnCol)
    oppCol = oppositeCol(trnCol)
    s0 = start[0]
    s1 = start[1]
    endr = end[1] + end[0]
    global epav
    global wLCastle
    global wRCastle
    global bLCastle
    global bRCastle
    if kingSafetyCheck(board, col, oppCol, start, end) == "x":
        print("You are in check!")
        return False
    elif board[s1][s0][:2] == (" " + col) or board[s1][s0][:1] == col:
        peice = board[s1][s0]
        if peice == (col + "Kn"):
            if endr in knightCheck(board, s0, s1, col):
                epav = False
                return True
        elif peice == (" " + col + "R"):
            if endr in direcCheck(board, s0, s1, "h", col):
                if col == "W":
                    if s0 == "a":
                        wLCastle = False
                    elif s0 == "h":
                        wRCastle = False
                elif col == "B":
                    if s0 == "a":
                        bLCastle = False
                    elif s0 == "h":
                        bRCastle = False
                epav = False
                return True
        elif peice == (" " + col + "B"):
            if endr in direcCheck(board, s0, s1, "d", col):
                epav = False
                return True
        elif peice == (" " + col + "Q"):
            if endr in (direcCheck(board, s0, s1, "d", col) + direcCheck(board, s0, s1, "h", col)):
                epav = False
                return True
        elif peice == (" " + col + "K"):
            if ((endr in kingCheck(board, s0, s1, col) and attackMap(board, oppCol)[end[1]][end[0]] != "x") 
            or castleCheck(col, oppCol, start, end, board)):
                if col == "W":
                    wLCastle = False
                    wRCastle = False
                elif col == "B":
                    bLCastle = False
                    bRCastle = False
                epav = False
                return True
        elif peice == (" " + col + "P"):
            if (endr in pawnMoveCheck(board, s0, s1, col) 
            or (endr in pawnCheck(board, s0, s1, col) and board[end[1]][end[0]] != "   ")):
                epav = False
                if end[1] == "4" and col == "W" and s1 == "2":
                    epav = True
                elif end[1] == "5" and col == "B" and s1 == "7":
                    epav = True
                return True

def moveCheck(moveIn, trnCol, board):
    if moveIn == "exit":
        print("Exiting now...")
        quit()
    elif moveIn == "ehm":
        return "ehm"
    start = moveIn[:2]
    end = moveIn[-2:]
    if start != end and formCheck(start) and formCheck(end) and posCheck(start, end, trnCol, board):
         return (start + end)
    return False

whiteCount = 0
blackCount = 0
enableHeatMap = False
while True:
    for turnColour in ("white", "black"):
        if turnColour == "white":
            whiteCount += 1
        else:
            blackCount += 1
        printBoard(board, whiteCount + blackCount)
        if enableHeatMap == True:
            print("white")
            printHeatMap(attackMap(board, "W"))
            print("black")
            printHeatMap(attackMap(board, "B"))
        while True:
            moveIn = moveCheck(input(turnColour + "'s move: "), turnColour, board)
            if moveIn == "ehm":
                if enableHeatMap == False:
                    enableHeatMap = True
                else:
                    enableHeatMap = False
            elif moveIn != False:
                board = makeMove(moveIn, board, True)
                break
            else:
                print("Invalid move")
