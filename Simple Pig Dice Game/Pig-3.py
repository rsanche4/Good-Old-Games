#By Rafael Sanchez
#2019

import random
import time

POINTS_TO_WIN = 100

def main():
    welcome()
    while True:
        playGame()
        print("Bye!")
        time.sleep(5)
        sys.exit()

def playGame():
    scores = initScores()
    while (not gameOver(scores)): 
        player = 1
        print()
        print('Current Scores:')
        printScore(scores)
        getMove(scores, player)
        if gameOver(scores):
            if scores[0] >= POINTS_TO_WIN:
                printWinMessage(1, scores)
                break
        player = 2
        print()
        print('Current Scores:')
        printScore(scores)
        getMove(scores, player)
        if gameOver(scores):
            if scores[1] >= POINTS_TO_WIN:
                printWinMessage(2, scores)

def initScores():
    p1score = 0
    p2score = 0
    return [p1score, p2score]

def gameOver(scores):
    if scores[0] >= POINTS_TO_WIN:
        return True
    elif scores[1] >= POINTS_TO_WIN:
        return True
    else:
        return False

def getMove(scores, player):
    printPlayerMessage(player)
    roundScore = 0
    while True:
        printCurrentPlayerScore(scores, player, roundScore)
        if (not wantsRollAgain(player)):
            printScore(scores)
            break
        roll = rollDice()
        showRoll(roll)
        result = list(filter(lambda x: x == 1, roll))
        addedResult = sum(result)
        if addedResult == 4:
            print("Rolled four 1s... Game Over")
            if player == 1:
                printWinMessage(2, scores)
                break
            else:
                printWinMessage(1, scores)
                break
        elif addedResult == 3:
            print("Rolled three 1s. Score reset!")
            if player == 1:
                scores[0] = 0
                break
            else:
                scores[1] = 0
                break
        elif addedResult == 2:
            print("Rolled two 1s! Round ended, no score added")
            addedResult -= addedResult
            break
        elif addedResult == 1:
            print("Rolled a 1! Round ended, score added")
            roundScore = sum(roll)
            if player == 1:
                scores[0] += roundScore
                break
            if player == 2:
                scores[1] += roundScore
                break
        else:
            roundScore = sum(roll)
            if player == 1:
                scores[0] += roundScore
            if player == 2:
                scores[1] += roundScore

def rollDie():
    return random.randint(1, 6)

def rollDice():
    roll = []
    roll.append(rollDie())
    roll.append(rollDie())
    roll.append(rollDie())
    roll.append(rollDie())
    return roll

def wantsContinue(player, response):
    ans = response
    if ans == 'Y' or ans == 'y':
        return True
    elif ans == 'N' or ans == 'n':
        return False
    else:
        print("You did not type a correct input. Try again.")
        wantsRollAgain(player)

def wantsRollAgain(player):
    response = input("Would you like to roll? Y for yes, N for no: ")
    if wantsContinue(player, response):
        return True
    else:
        return False

def welcome():
    print('Welcome to Pig!')
    time.sleep(3)
    print('Which player will make it to 100 first? We shall see. Make sure you stop rolling the dices once you reached 100!')
    time.sleep(3)

def printScore(scores):
    print("Player 1: " + str(scores[0]) + " & Player 2: " + str(scores[1]))

def printWinMessage(winningPlayer, scores):
    print()
    print('***********************Player ' + str(winningPlayer) + ' Won!************************')
    print('***********************Final Score:*************************')
    printScore(scores)

def showRoll(roll):
    print("Roll: " + str(roll))

def printPlayerMessage(player):
    print()
    print('--------------------------------------------------------------')
    print('-------------------Player ' + str(player) + '\'s turn----------------------------')
    print('--------------------------------------------------------------')
    print()

def printCurrentPlayerScore(scores, player, roundScore):
    print("Player " + str(player) + " has a round score of " + str(roundScore) + " and an overall score of " + str(scores[player-1]))

if __name__ == '__main__':
    main()
