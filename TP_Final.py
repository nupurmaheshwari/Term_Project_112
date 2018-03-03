from tkinter import *
import random
import enchant
from itertools import permutations
from itertools import combinations
#line of code below from Pyenchant homepage
Y = enchant.Dict("en_US")
#5 lines of code below from 112 course website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
searchfile = readFile("words.txt")
stuff = set(line.strip() for line in open('words.txt'))


def init(data):
    data.margin = 25
    data.rows = 15
    data.cols = 15
    data.emptyColor = 'gray64'
    data.board = baseBoard(data)
    data.origBoard = baseBoard(data)
    data.key = spaceTypes(data)
    data.points = {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10}
    data.tiles = tiles(data)
    data.playerHand = createHand(data)
    data.compHand = createHand(data)
    data.playerScore, data.compScore, data.tempScore = 0, 0, 0
    data.letter = ' '
    data.remove = -1
    data.undoList = []
    data.boardLetters = [([0] * data.cols) for val in range(data.rows)]
    data.play = False
    data.turns = 0
    data.wordError, data.frontError, data.placeError, data.emptyError, data.positionError = False, False, False, False, False
    data.tripleWord, data.doubleWord = 0, 0
    data.startPage = True
    data.playPage, data.helpPage1, data.helpPage2, data.rulesPage = False, False, False, False
    data.AIplay = False
    data.twoPlay = False
    data.optionPlay = False
    data.validBlocks, data.validWords = [], []
    data.first = False
    data.gameOver = False

def tiles(data):
    return ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A','I','I','I',
    'I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N','N','N','R','R','R','R','R','R',
    'T','T','T','T','T','T','L','L','L','L','S','S','S','S','U','U','U','U','D','D','D','D','G','G','G','B',
    'B','C','C','M','M','P','P','F','F','H','H','V','V','W','W','Y','Y','K','J','J','X','Q','Z']

def spaceTypes(data):
    types = dict()
    types['red'] = 'TRIPLE\nWORD'
    types['cyan2'] = 'TRIPLE\nLETTER'
    types['lightBlue'] = 'DOUBLE\nLETTER'
    types['pink'] = 'DOUBLE\nWORD'
    return types

def baseBoard(data):
    board = [([data.emptyColor] * data.cols) for val in range(data.rows)]
    total = 14
    for row in range(data.rows):
        for col in range(data.cols):
            if row == col or row + col == total:
                if row in [0, 14] or col in [0, 14]:
                    board[row][col] = 'red'
                elif row in [5, 9] or col in [5, 9]:
                    board[row][col] = 'cyan2'
                elif row in [6, 8] or col in [6, 8]:
                    board[row][col] = "lightBlue"
                else:
                    board[row][col] = 'pink'
            elif row in [0, 7] and col in [0, 7]:
                board[row][col] = 'red'
            elif row in [7, 14] and col in [7, 14]:
                board[row][col] = 'red'
            elif row in [0, 3] and col in [0, 3]:
                board[row][col] = 'lightBlue'
            elif row in [0, 11] and col in [0, 11]:
                board[row][col] = 'lightBlue'
            elif row in [3, 14] and col in [3, 14]:
                board[row][col] = 'lightBlue'
            elif row in [11, 14] and col in [11, 14]:
                board[row][col] = 'lightBlue'
            elif row in [2, 6] and col in [2, 6]:
                board[row][col] = 'lightBlue'
            elif row in [2, 8] and col in [2, 8]:
                board[row][col] = 'lightBlue'
            elif row in [3, 7] and col in [3, 7]:
                board[row][col] = 'lightBlue'
            elif row in [7, 11] and col in [7, 11]:
                board[row][col] = 'lightBlue'
            elif row in [6, 12] and col in [6, 12]:
                board[row][col] = 'lightBlue'
            elif row in [8, 12] and col in [8, 12]:
                board[row][col] = 'lightBlue'
            elif row in [1, 5] and col in [1, 5]:
                board[row][col] = 'cyan2'
            elif row in [1, 9] and col in [1, 9]:
                board[row][col] = 'cyan2'
            elif row in [5, 13] and col in [5, 13]:
                board[row][col] = 'cyan2'
            elif row in [9, 13] and col in [9, 13]:
                board[row][col] = 'cyan2'
    return board

def createHand(data):
    hand = []
    for val in range (7):
        num = random.randint(0, len(data.tiles)-1)
        hand.append(data.tiles[num])
        data.tiles.pop(num)
    return hand

def newHandPlayer(data):
    for space in range (len(data.playerHand)):
        if data.playerHand[space] == ' ':
            data.playerHand.pop(space)
            num = random.randint(0, len(data.tiles)-1)
            data.playerHand.insert(space, data.tiles[num])
            data.tiles.pop(num)
    return data.playerHand

def newHandComp(data):
    for space in range (len(data.compHand)):
        if data.compHand[space] == ' ':
            data.compHand.pop(space)
            num = random.randint(0, len(data.tiles)-1)
            data.compHand.insert(space, data.tiles[num])
            data.tiles.pop(num)
    return data.compHand

def passButton(canvas, data):
    canvas.create_rectangle(815, 510, 905, 550, width = 2, fill = 'medium sea green')
    canvas.create_text(860, 530, text = 'PASS', font = "Times 14")

def exchangeButton(canvas, data):
    canvas.create_rectangle(1038, 510, 1128, 550, width = 2, fill = 'medium sea green')
    canvas.create_text(1083, 530, text = 'SWITCH', font = "Times 14")

def mousePressed(event, data):
    if data.startPage == True:
        if (950 <= event.x <= 1150) and (145 <= event.y <= 205):
            data.startPage = False
            data.playPage = True
        elif (950 <= event.x <= 1150) and (320 <= event.y <= 380):
            data.startPage = False
            data.rulesPage = True
        elif (950 <= event.x <= 1150) and (495 <= event.y <= 555):
            data.startPage = False
            data.helpPage1 = True
    if data.rulesPage == True:
        if (1025 <= event.x <= 1165) and (600 <= event.y <= 640):
            data.rulesPage = False
            data.startPage = True
    if data.helpPage1 == True:
        if (1025 <= event.x <= 1165) and (600 <= event.y <= 640):
            data.helpPage1 = False
            data.startPage = True
    elif data.playPage == True:
        if data.turns % 2 == 0:
            if 328.3 <= event.y <= 371.7:
                if 820 <= event.x <= 863.4:
                    data.letter = data.playerHand[0]
                    data.remove = 0
                elif 867 <= event.x <= 910.4:
                    data.letter = data.playerHand[1]
                    data.remove = 1
                elif 914 <= event.x <= 957.4:
                    data.letter = data.playerHand[2]
                    data.remove = 2
                elif 961 <= event.x <= 1004.4:
                    data.letter = data.playerHand[3]
                    data.remove = 3
                elif 1008 <= event.x <= 1051.4:
                    data.letter = data.playerHand[4]
                    data.remove = 4
                elif 1055 <= event.x <= 1098.4:
                    data.letter = data.playerHand[5]
                    data.remove = 5
                elif 1102 <= event.x <= 1145.4:
                    data.letter = data.playerHand[6]
                    data.remove = 6
            if (815 <= event.x <= 905) and (510 <= event.y <= 550):
                data.turns += 1
            if (1038 <= event.x <= 1128) and (510 <= event.y <= 550):
                for r in range (7):
                    letter = data.playerHand[r]
                    data.tiles.append(letter)
                data.playerHand = createHand(data)
                data.turns += 1
            if data.letter != ' ' and (25 <= event.x <= 675) and (25 <= event.y <= 675):
                col = int((event.x - data.margin)/43.3)
                row = int((event.y - data.margin)/43.3)
                data.undoList.append([data.board[row][col], data.remove, data.letter, (row, col)])
                data.board[row][col] = 'khaki2'
                data.boardLetters[row][col] = data.letter
                data.playerHand[data.remove] = ' '
                data.letter, data.remove = ' ', ' '
            elif data.letter == ' ' and (25 <= event.x <= 675) and (25 <= event.y <= 675):
                col = int((event.x - data.margin)/43.3)
                row = int((event.y - data.margin)/43.3)
                for r in range (len(data.undoList)):
                    if (row, col) == data.undoList[r][3]:
                        data.board[row][col] = data.origBoard[row][col]
                        # data.boardLetters[row][col] = 0
                        data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
                        data.undoList.pop(r)
            if (915 <= event.x <= 1035) and (160 <= event.y <= 200):
                if "khaki2" not in data.board and data.undoList == []:
                    data.emptyError = True
                else:
                    data.emptyError = False
                    data.play = True  
                    data.rowVals, data.colVals = set(), set()
                    for i in range(len(data.undoList)):
                        data.rowVals.add(data.undoList[i][3][0])
                        data.colVals.add(data.undoList[i][3][1])
                    if ("khaki2" in data.board) and len(data.rowVals) != 1 and len(data.colVals) != 1:
                        data.placeError = True
                        for r in range (len(data.undoList)):
                            if data.undoList[r][1] != -1:
                                data.board[data.undoList[r][3][0]][data.undoList[r][3][1]] = data.origBoard[data.undoList[r][3][0]][data.undoList[r][3][1]]
                                data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
                        data.undoList = []
                        data.play = False
                        data.wordError, data.frontError, data.positionError = False, False, False
                    else:
                        data.placeError = False
                        if len(data.rowVals) == 1:
                            data.undoList = sorted(data.undoList, key=lambda x: x[3][1])
                        if len(data.colVals) == 1:
                            data.undoList = sorted(data.undoList, key=lambda x: x[3][0])
                        word = ''
                        for val in range(len(data.undoList)):
                            word += data.undoList[val][2]
                        if data.turns == 0:
                            firstWord(event, data, word)
                        else:
                            otherWord(event, data, word)
            if data.turns % 2 == 1:
                validBlocks(data)
                if data.first == True:
                    first(data)
                else:
                    perms(data)
                    checkWords(data)
                    placeWord(data)


def validBlocks(data):
    for row in range(len(data.board)):
        for col in range(len(data.board)):
            if data.board[row][col] == 'khaki2':
                if 0 < col < 14 and data.board[row][col + 1] != 'khaki2' and data.board[row][col - 1 ] != 'khaki2':
                    data.validBlocks.append([data.boardLetters[row][col], (row, col), "col"])
                if 0 < row < 14 and data.board[row + 1][col] != 'khaki2' and data.board[row - 1][col] != 'khaki2':
                    data.validBlocks.append([data.boardLetters[row][col], (row, col), "row"])
    if len(data.validBlocks) == 0:
        data.first = True


def first(data):
    score = []
    most = []
    l = list(permutations(data.compHand))
    most.append(l)
    for r in range (2, 7):
        c = list(combinations(data.compHand, r))
        for combo in range (len(c)):
            l = tuple(permutations(c[combo]))
            most.append(l)
    for a in range (len(most)):
        for b in range(len(most[a])):
            word = ''.join(most[a][b]).lower()
            if (word.strip() in stuff):
                data.validWords.append([most[a][b], (7, 7), 'any'])
    for word in range(len(data.validWords)):
        count = 0
        points = 0
        for letter in range(len(data.validWords[word][0])):
            if count != 4:
                points += data.points[data.validWords[word][0][letter]]
            else:
                points += (2*data.points[data.validWords[word][0][letter]])
        score.append([2*points, data.validWords[word][0]])
    score = sorted(score)[::-1]
    data.compScore += score[0][0]
    for r in range (len(score[0][1])):
        data.board[7][7+r] = 'khaki2'
        data.boardLetters[7][7+r] = score[0][1][r]
    data.validBlocks = []
    data.validWords = []
    data.compHand = newHandComp(data)
    data.first = False
    data.turns += 1


def perms(data):
    most = []
    for block in range(len(data.validBlocks)):
        data.compHand.append(data.validBlocks[block][0])
        l = list(permutations(data.compHand))
        most.append(l)
        for r in range (2, 8):
            c = list(combinations(data.compHand, r))
            for combo in range (len(c)):
                l = tuple(permutations(c[combo]))
                most.append(l)
        data.compHand.pop(7)
    data.turns += 1
    return (most)


def flattenmybund(l):
    a=[]
    for row in l:
        for item in row:
            a.append(item)
    return a


def checkWords(data):
    total = perms(data)
    for a in range (len(total)):
        for b in range(len(total[a])):
            word = ''.join(total[a][b]).lower()
            if (word.strip() in stuff) and (data.validBlocks[a//247][0] in total[a][b]):
                data.validWords.append([total[a][b], data.validBlocks[a//247][1], data.validBlocks[a//247][2]])
    return list(set(flattenmybund(data.validWords)))


def getAIScores(data):
    final = []
    for word in range (len(data.validWords)):
        points = 0
        score = []
        f_count, b_count = 0, 0
        f_word, b_word = [], []
        valid = True
        switch = False
        row, col = data.validWords[word][1][0], data.validWords[word][1][1]
        letter = data.boardLetters[row][col]
        for r in range(len(data.validWords[word][0])):
            if data.validWords[word][0][r] != letter:
                if switch == False:
                    f_count += 1
                    f_word.append(data.validWords[word][0][r])
                else:
                    b_count += 1
                    b_word.append(data.validWords[word][0][r])
            else:
                switch = True
        if data.validWords[word][2] == 'col':
            for f in range(f_count):
                if (col-(f+1) < 0) or data.board[row][col-(f+1)] == 'khaki2':
                    valid = False
                else:
                    score.append([[data.board[row][col-(f+1)]], f_word[::-1][f], (row, col-(f+1)), 'col'])
            for b in range(b_count):
                if (col+(b+1) > 14) or data.board[row][col+(b+1)] == 'khaki2':
                    valid = False
                else:
                    score.append([[data.board[row][col+(b+1)]], b_word[b], (row, col+(b+1)), 'col'])
        else:
            for f in range(f_count):
                if (row-(f+1) < 0) or data.board[row-(f+1)][col] == 'khaki2':
                    valid = False
                else:
                    score.append([[data.board[row-(f+1)][col]], f_word[::-1][f], (row-(f+1), col), 'row'])
            for b in range(b_count):
                if (row+(b+1) > 14) or data.board[row+(b+1)][col] == 'khaki2':
                    valid = False
                else:
                    score.append([[data.board[row+(b+1)][col]], b_word[b], (row+(b+1), col), 'row'])
        if valid == True:
            if score != []:
                if score[0][3] == 'col':
                    score = sorted(score, key=lambda x: x[2][1])
                else:
                    score = sorted(score, key=lambda x: x[2][0])
                for let in range (len(score)):
                    if score[let][0] == 'red':
                        data.tripleWord += 1
                        points += (data.points[score[let][1]])
                    elif score[let][0] == 'cyan2':
                        points += (3 * (data.points[score[let][1]]))
                    elif score[let][0] == 'lightBlue':
                        points += (2 * (data.points[score[let][1]]))
                    elif score[let][0] == 'pink':
                        data.doubleWord += 1
                        points += (data.points[score[let][1]])
                    else:
                        points += (data.points[score[let][1]])
                for d in range(data.doubleWord):
                    points *= 2
                for t in range(data.tripleWord):
                    points *= 3
                points += data.points[letter]
                data.doubleWord, data.tripleWord = 0, 0
                final.append([points, data.validWords[word][0], data.validWords[word][1], data.validWords[word][2]])
    return final


def placeWord(data):
    final = getAIScores(data)
    final = sorted(final)[::-1]
    valid = False
    while (valid == False):
        yes = True
        row = final[0][2][0]
        col = final[0][2][1]
        length = len(final[0][1])
        letter = data.boardLetters[row][col]
        index = final[0][1].index(letter)
        if final[0][3] == 'col':
            for i in range(index):
                if (row > 0 and data.board[row-1][col-index+i] == 'khaki2') or (row < 14 and data.board[row+1][col-index+i] == 'khaki2'):
                    yes = False
            for r in range(length-(index+1)):
                if (row > 0 and data.board[row-1][col+r+1] == 'khaki2') or (row < 14 and data.board[row + 1][col+r+1] == 'khaki2'):
                    yes = False
        else:
            for i in range(index):
                if (col > 0 and data.board[row-index+i][col-1] == 'khaki2') or (col < 14 and data.board[row-index+i][col+1] == 'khaki2'):
                    yes = False
            for r in range(length-(index+1)):
                if (col > 0 and data.board[row+r+1][col-1] == 'khaki2') or (col < 14 and data.board[row+r+1][col+1] == 'khaki2'):
                    yes = False
        if yes == True:
            valid = True
        else: final.pop(0)
    data.compScore += final[0][0]
    row = final[0][2][0]
    col = final[0][2][1]
    letter = data.boardLetters[row][col]
    count = 0
    for val in range (len(data.compHand)):
        if (data.compHand[val] in final[0][1] or count == 1):
            data.compHand[val] = ' ' 
        else:
            if data.compHand[val] == letter:
                count += 1
            else:
                if data.compHand[val] in final[0][1]:
                    data.compHand[val] = ' '
    index = final[0][1].index(letter)
    length = len(final[0][1])
    count = 1
    if final[0][3] == 'col':
        for i in range(index):
            data.boardLetters[row][col-index+i] = final[0][1][i]
            data.board[row][col-index+i] = 'khaki2'
        for r in range(index + 1, length):
            data.boardLetters[row][col+count] = final[0][1][r]
            data.board[row][col+count] = 'khaki2'
            count += 1
    else:
        for i in range(index):
            data.boardLetters[row-index+i][col] = final[0][1][i]
            data.board[row-index+i][col] = 'khaki2'
        for r in range(index + 1, length):
            data.boardLetters[row+count][col] = final[0][1][r]
            data.board[row+count][col] = 'khaki2'
            count += 1
    data.validBlocks = []
    data.validWords = []
    data.compHand = newHandComp(data)
    data.turns += 1
    

def firstWord(event, data, word):
    if data.undoList[0][3] != (7, 7):
        data.frontError = True
        for r in range (len(data.undoList)):
            if data.undoList[r][1] != -1:
                data.board[data.undoList[r][3][0]][data.undoList[r][3][1]] = data.origBoard[data.undoList[r][3][0]][data.undoList[r][3][1]]
                data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
        data.undoList = []
        data.play = False
        data.placeError, data.wordError, data.positionError = False, False, False
    else: 
        data.frontError = False
        if Y.check(word) != True:
            data.wordError = True
            for r in range (len(data.undoList)):
                if data.undoList[r][1] != -1:
                    data.board[data.undoList[r][3][0]][data.undoList[r][3][1]] = data.origBoard[data.undoList[r][3][0]][data.undoList[r][3][1]]
                    data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
            data.undoList = []
            data.play = False
            data.placeError, data.frontError, data.positionError = False, False, False
        else:
            calcScore(event, data)


def otherWord(event, data, word):
    if len(data.rowVals) == 1:
        start = data.undoList[0][3][1]
        roww = data.undoList[0][3][0]
        stop = False
        while (stop  == False):
            if data.boardLetters[roww][start-1] != 0:
                start -= 1
            else:
                stop = True
        newWord = ' '
        end = False
        lis = 0
        count = 0
        while (end == False):
            yes = 0
            for r in range(len(data.undoList)):
                if (roww, start) in data.undoList[r]:
                    yes += 1
            if yes == 0 and start < 15 and data.boardLetters[roww][start] != 0:
                newWord += data.boardLetters[roww][start]
                if data.boardLetters[roww][start] != ' ':
                    data.undoList.append([data.board[roww][start], -1, data.boardLetters[roww][start], (roww, start)])
                start += 1
                count += 1                               
            elif (lis < len(data.undoList) and data.undoList[lis][3][1] == start):
                newWord += data.undoList[lis][2]
                lis += 1
                start += 1
            else:
                end = True
    elif len(data.colVals) == 1:
        start = data.undoList[0][3][0]
        coll = data.undoList[0][3][1]
        stop = False
        while (stop  == False):
            if data.boardLetters[start-1][coll] != 0:
                start -= 1
            else:
                stop = True
        newWord = ' '
        end = False
        lis = 0
        count = 0
        while (end == False):
            yes = 0
            for r in range(len(data.undoList)):
                if (start, coll) in data.undoList[r]:
                    yes += 1
            if yes == 0 and start < 15 and data.boardLetters[start][coll] != 0:
                newWord += data.boardLetters[start][coll]
                if data.boardLetters[start][coll] != ' ':
                    data.undoList.append([data.board[start][coll], -1, data.boardLetters[start][coll], (start, coll)])
                start += 1
                count += 1                               
            elif (lis < len(data.undoList) and data.undoList[lis][3][0] == start): newWord += data.undoList[lis][2]; lis += 1; start += 1
            else:
                end = True
    if count <= 0:
        data.positionError = True
        for r in range (len(data.undoList)):
            if data.undoList[r][1] != -1:
                data.board[data.undoList[r][3][0]][data.undoList[r][3][1]] = data.origBoard[data.undoList[r][3][0]][data.undoList[r][3][1]]
                data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
        data.undoList = []
        data.frontError, data.placeError, data.wordError = False, False, False
        data.play = False
    else:
        data.positionError = False 
        if Y.check(newWord) != True:
            data.wordError = True
            for r in range (len(data.undoList)):
                if data.undoList[r][1] != -1:
                    data.board[data.undoList[r][3][0]][data.undoList[r][3][1]] = data.origBoard[data.undoList[r][3][0]][data.undoList[r][3][1]]
                    data.playerHand[data.undoList[r][1]] = data.undoList[r][2]
            data.undoList = []
            data.play = False
            data.placeError, data.frontError, data.positionError = False, False, False
        else:
            calcScore(event, data)


def calcScore(event, data):
    data.wordError = False
    for let in range(len(data.undoList)):
        if data.undoList[let][0] == 'red':
            data.tripleWord += 1
            data.tempScore += (data.points[data.undoList[let][2]])
        elif data.undoList[let][0] == 'cyan2':
            data.tempScore += (3 * (data.points[data.undoList[let][2]]))
        elif data.undoList[let][0] == 'lightBlue':
            data.tempScore += (2 * (data.points[data.undoList[let][2]]))
        elif data.undoList[let][0] == 'pink':
            data.doubleWord += 1
            data.tempScore += (data.points[data.undoList[let][2]])
        else:
            data.tempScore += (data.points[data.undoList[let][2]])
    for d in range(data.doubleWord):
        data.tempScore *= 2
    for t in range(data.tripleWord):
        data.tempScore *= 3
    data.playerScore += data.tempScore
    data.doubleWord, data.tripleWord, data.tempScore = 0, 0, 0
    data.turns += 1
    data.undoList = []
    data.play = False
    data.playerHand = newHandPlayer(data)


def keyPressed(event, data):
    if event.keysym == "p":
        init(data)
    elif event.keysym == 'g':
        data.gameOver = True
    elif data.playPage == True:
        if event.keysym == "space":
            data.playPage = False
            data.helpPage2 = True
    elif data.helpPage2 == True:
        if event.keysym == "space":
            data.helpPage2 = False
            data.playPage = True

def timerFired(data):
    pass


def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = 650
    gridHeight = 650
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)


def drawPieces(canvas, data):
    x0 = 820
    y0 = 328.3
    x1 = 820 + 43.4
    y1 = 328.3 + 43.4
    num = 0
    count = 0
    for val in range (7):
        if data.playerHand[count] != ' ':
            if data.playerHand[count] == data.letter:
                canvas.create_rectangle(x0 + num, y0, x1 + num, y1, width = 2, fill='khaki2')
            else:
                canvas.create_rectangle(x0 + num, y0, x1 + num, y1, width = 1, fill='khaki2')
            canvas.create_text(x0 + num + 21.7, y0 + 21.7, text = data.playerHand[count], font = "Times 20")
            canvas.create_text(x0 + num + 36, y0 + 36, text = data.points[data.playerHand[count]], font = "Times 12")
        num += 47
        count += 1


def drawCell(canvas, data, row, col, fill):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 0.1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
    if fill == 'khaki2':
        canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, width = 2, fill=fill)
        canvas.create_text(x0+((x1-x0)/2), y0+((y1-y0)/2), text = data.boardLetters[row][col], font = "Times 20")
        canvas.create_text((x0+((x1-x0)/2)) + 14, (y0+((y1-y0)/2)) + 14, text = data.points[data.boardLetters[row][col]], font = "Times 12")
    else:
        canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=fill)
        if data.board[row][col] in data.key:
            canvas.create_text(x0+((x1-x0)/2), y0+((y1-y0)/2), text = data.key[data.board[row][col]], font = "Times 9")
    

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])


def drawTitle(canvas, data):
    canvas.create_text(975, 100, text='SCRABBLE', font="Times 50")


def drawPlay(canvas, data):
    if (data.play == True) and ("khaki2" in data.board):
        canvas.create_rectangle(915, 160, 1035, 200, width = 3, fill = 'orange')
    else:
        canvas.create_rectangle(915, 160, 1035, 200, width = 2, fill = 'orange')
    canvas.create_text(975, 180, text = "Make Move", font = "Times 20")


def drawScore(canvas, data):
    canvas.create_text(775, 655, text = 'PLAYER SCORE: ' + str(data.playerScore), font = 'Times 15 bold')
    canvas.create_text(1150, 655, text = 'COMP SCORE: ' + str(data.compScore), font = 'Times 15 bold')



def startGame(canvas, data):
    canvas.create_text(450, 350, text = "Welcome to Scrabble!", font = "Times 50")
    canvas.create_rectangle(950, 145, 1150, 205, width = 2, fill = 'medium sea green')
    canvas.create_text(1050, 175, text = "PLAY", font = "Times 25")
    canvas.create_rectangle(950, 320, 1150, 380, width = 2, fill = 'medium sea green')
    canvas.create_text(1050, 350, text = "RULES", font = "Times 25")
    canvas.create_rectangle(950, 495, 1150, 555, width = 2, fill = 'medium sea green')
    canvas.create_text(1050, 525, text = "HELP", font = "Times 25")

def tileHolder(canvas, data):
    canvas.create_rectangle(817, 371.7, 1148.5, 376.7, width=0.5, fill='tan4')

def passButton(canvas, data):
    canvas.create_rectangle(815, 510, 905, 550, width = 2, fill = 'medium sea green')
    canvas.create_text(860, 530, text = 'PASS', font = "Times 14")

def exchangeButton(canvas, data):
    canvas.create_rectangle(1038, 510, 1128, 550, width = 2, fill = 'medium sea green')
    canvas.create_text(1083, 530, text = 'SWAP', font = "Times 14")

def message(canvas, data):
    canvas.create_text(970, 35, text = "Press the space bar for HELP", fill = 'gray50', font = "Times 13")

def rulesPage(canvas, data):
    canvas.create_text(30, 30, text = "RULES", anchor = 'nw', font = "Times 45 bold")
    canvas.create_text(30, 110, text = "#1", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 130, text = "The first player combines two or more of his or her letters to form a word and places it on the board to read either across or down with one letter on the center square.", anchor = 'nw', font="Times 15")
    canvas.create_text(50, 150, text = "Diagonal words are not allowed.", anchor = 'nw', font = "Times 15")
    canvas.create_text(30, 190, text = "#2", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 210, text = "Players take turns with the computer. All letters played on a turn must be placed in one row across or down the board, to form at least one complete word. If, at the same time, they touch", anchor = 'nw', font="Times 15")
    canvas.create_text(50, 230, text = "other letters in adjacent rows, those must also form complete words, crossword fashion, with all such letters. The player gets full credit for all words formed or modified on his or her turn.", anchor = 'nw', font = "Times 15")
    canvas.create_text(30, 270, text = "#3", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 290, text = "New words may be formed by: ", anchor = 'nw', font = "Times 15")
    canvas.create_text(70, 310, text = "* Adding one or more letters to a word or letters already on the board.", anchor = 'nw', font = "Times 15")
    canvas.create_text(70, 330, text = "* Placing a word at right angles to a word already on the board. The new word must use one of the letters already on the board or must add a letter to it.", anchor = 'nw', font = "Times 15")
    canvas.create_text(70, 350, text = "* Placing a complete word parallel to a word already played so that adjacent letters also form complete words. ", anchor = 'nw', font = "Times 15")
    canvas.create_text(30, 390, text = "#3", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 410, text = "No tile may be shifted or replaced after it has been played and scored.", anchor = 'nw', font = "Times 15")
    canvas.create_text(30, 450, text = "#4", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 470, text = "You may use a turn to exchange your letters or pass the turn altogether.", anchor = 'nw', font = "Times 15")
    canvas.create_text(30, 510, text = "#5", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 530, text = "The game ends when all letters have been drawn and one player uses his or her last letter; or when a player gets to 150 points.", anchor = 'nw', font = "Times 15")
    canvas.create_rectangle(1025, 600, 1165, 640, width=2, fill='orange')
    canvas.create_text(1095, 620, text ="BACK", font="Times 18")

def helpPage1(canvas, data):
    canvas.create_text(30, 30, text = "HELP", anchor = 'nw', font = "Times 45 bold")
    canvas.create_text(30, 110, text = "How to play: ", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 140, text = "* To create a word on the board, click letters on the right and click place on board", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 170, text = "* To take letters off the board, click on that letter", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 200, text = "* Click MAKE MOVE to finish a turn and get the points for that move", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 230, text = "* To exchange letters in your hand for a new set, click SWAP", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 260, text = "* To skip your turn, click PASS", anchor = 'nw', font="Times 17")

    canvas.create_text(30, 310, text = "Things to look out for: ", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 340, text = "* Scores are displayed at the bottom of the screen", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 370, text = "* Error messages are displayed if an illegal move is attempted", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 400, text = "* Click the SPACE bar to refer back to the Help page at any point while playing", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 430, text = "* Error messages are displayed if an illegal move is attempted", anchor = 'nw', font="Times 17")

    canvas.create_rectangle(1025, 600, 1165, 640, width=2, fill='orange')
    canvas.create_text(1095, 620, text ="BACK", font="Times 18")


def helpPage2(canvas, data):
    canvas.create_text(30, 30, text = "HELP", anchor = 'nw', font = "Times 45 bold")
    canvas.create_text(30, 110, text = "How to play: ", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 140, text = "* To create a word on the board, click letters on the right and click place on board", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 170, text = "* To take letters off the board, click on that letter", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 200, text = "* Click MAKE MOVE to finish a turn and get the points for that move", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 230, text = "* To exchange letters in your hand for a new set, click SWAP", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 260, text = "* To skip your turn, click PASS", anchor = 'nw', font="Times 17")

    canvas.create_text(30, 310, text = "Things to look out for: ", anchor = 'nw', font = "Times 15 bold")
    canvas.create_text(50, 340, text = "* Scores are displayed at the bottom of the screen", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 370, text = "* Error messages are displayed if an illegal move is attempted", anchor = 'nw', font="Times 17")
    canvas.create_text(50, 400, text = "* Click 'r' to restart game", anchor = 'nw', font="Times 17")

    canvas.create_text(634, 560, text="Press SPACE to return to Scrabble", fill='gray50', font="Times 20 bold")

def gameOver(canvas, data):
    if data.compScore > data.playerScore:
        canvas.create_text(634, 320, text="The computer won.", font="Times 70 bold")
        canvas.create_text(634, 400, text="Better luck next time! Click 'p' to play again.", font="Times 35")
    if data.compScore < data.playerScore:
        canvas.create_text(634, 320, text="Congratulations!", font="Times 70 bold")
        canvas.create_text(634, 400, text="You have won! Click 'p' to play again.", font="Times 35")
    if data.compScore == data.playerScore:
        canvas.create_text(634, 320, text="The game is tied.", font="Times 70 bold")
        canvas.create_text(634, 400, text="Click 'p' to play again.", font="Times 35")


def redrawAll(canvas, data):
    # if len(data.tiles) < 6:
    #     data.gameOver == True
    #     canvas.create_text
    if data.compScore >= 150 or data.playerScore >= 150 or len(data.tiles) < 7 or data.gameOver == True:
        gameOver(canvas, data)
    elif data.startPage == True:
        startGame(canvas, data)
    # elif data.optionPage == True:
    #   options(canvas, data)
    elif data.playPage == True: 
        if data.emptyError == True:
            canvas.create_text(975, 245, text = "Please place letters on the board to make a move.", fill = 'red4', font = "Times 16")
        elif data.wordError == True:
            canvas.create_text(975, 245, text = "Not a valid word, please try again!", fill = 'red4', font = "Times 16")
        elif data.placeError == True:
            canvas.create_text(975, 245, text = "Not a valid placement, please try again!", fill = 'red4', font = "Times 16")
        elif data.frontError == True:
            canvas.create_text(975, 245, text = "First word must start at the center, please try again!", fill = 'red4', font = "Times 16")
        elif data.positionError == True:
            canvas.create_text(975, 245, text = "Not connected to another word, please try again!", fill = 'red4', font = "Times 16")
        drawTitle(canvas, data)
        drawPlay(canvas, data)
        drawScore(canvas, data)
        drawBoard(canvas, data)
        passButton(canvas, data)
        drawPieces(canvas, data)
        exchangeButton(canvas, data)
        tileHolder(canvas, data)
        message(canvas, data)
    elif data.helpPage1 == True:
        helpPage1(canvas, data)
    elif data.rulesPage == True:
        rulesPage(canvas, data)
    elif data.helpPage2 == True:
        helpPage2(canvas, data)



##############################################
# run function taken from 112 course website
##############################################

def run(width=1268, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='powder blue', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1268, 700)



