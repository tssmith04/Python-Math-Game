import pygame as pg
import random
import time
from collections import deque
from objects.linked import Linked
from objects.files import Files
from objects.answer import Answer
from objects.visual.button import Button
from objects.visual.display import Display
from initialize import *
pg.init()
pg.font.init()

#Resolution
resX = 800
resY = 800
#Difference in pixels
dif = int(resX/5)
output = ""
funcType = ""

#Creating window based onn resolution
game_window = pg.display.set_mode((resX, resY))

#Create Current Leaderboard and Load Files
leaderMasterNames = Linked()
leaderMasterScores = Linked()
fileMaster = Files(Files.createScores(), Files.createNames())

#Initialize All buttons/displays
buttons = buttonInit(resX, resY)
answerButtons = answerButtonInit()
display = displayInit(resX, resY, False)
settingsButtons = settingsButtonInit(resX, resY)

pg.display.set_caption("Math Game")

#Re-initialize game when size of window is changed
def initialize(hasInit):
    buttons = buttonInit(resX, resY)
    answerButtons = answerButtonInit(resX, resY)
    display = displayInit(resX, resY, hasInit)
    settingsButtons = settingsButtonInit(resX, resY)

#Updates drawing of buttons
#Visible just determines if they can be clicked or not; not if they are actually visible
def update(draw,maxNum,settings,screen,review,negative,timer,leader,perfect):
    game_window.fill((0, 150, 150))
    for x in range(len(settingsButtons)):
        settingsButtons[x].setVisible(False)
    for x in range(len(buttons)):
        buttons[x].setVisible(False)
    for x in range(10):
        answerButtons[x][0].setVisible(False)
    settingsButtons[0].draw(game_window,(0,0,0))
    settingsButtons[0].setVisible(True)
    if settings:
        for x in range(len(settingsButtons)):
            if x<3 or x>5:
                settingsButtons[x].draw(game_window,(0,0,0))
                settingsButtons[x].setVisible(True)
            elif screen:
                settingsButtons[x].draw(game_window, (0,0,0))
                settingsButtons[x].setVisible(True)
                
    else:
        if draw:
            if timer:
                display[5].setVisible(True)
                display[5].draw(game_window)
            if review:
                buttons[len(buttons)-1].setText("Done")
                buttons[len(buttons)-1].setX(0)
                buttons[len(buttons)-1].setY(resY-100)
                buttons[len(buttons)-1].draw(game_window,(0,0,0))
                buttons[len(buttons)-1].setVisible(True)
                if not leader:
                    display[4].setVisible(True)
                    display[4].draw(game_window)
                if leader:
                    for x in range(6):
                        display[x+8].draw(game_window)
                        display[x+8].setVisible(True)
                    buttons[16].setVisible(True)
                    buttons[17].setVisible(True)
                    buttons[16].draw(game_window, (0,0,0))
                    buttons[17].draw(game_window, (0,0,0))
                    if perfect:
                        display[14].draw(game_window)
                        display[14].setVisible(True)
                        buttons[18].setVisible(True)
                        buttons[19].setVisible(True)
                        buttons[18].draw(game_window, (0,0,0))
                        buttons[19].draw(game_window, (0,0,0))
            else:
                for x in range(10):
                    buttons[x].draw(game_window,(0,0,0))
                    buttons[x].setVisible(True)
                buttons[len(buttons)-1].draw(game_window,(0,0,0))
                buttons[len(buttons)-1].setVisible(True)
                buttons[15].draw(game_window,(0,0,0))
                buttons[15].setVisible(True)
                if negative:
                    buttons[14].draw(game_window,(0,0,0))
                    buttons[14].setVisible(True)
            if not leader:
                display[6].draw(game_window)
                display[6].setVisible(True)
            if not maxNum and not leader:
                for x in range(4):
                    display[x].setVisible(True)
                    display[x].draw(game_window)
                for x in range(10):
                    answerButtons[x][0].draw(game_window,(0,0,0))
                    answerButtons[x][0].setVisible(True)

        else:
            for x in range(10,14):
                buttons[x].draw(game_window,(0,0,0))
                buttons[x].setVisible(True)
        if maxNum:
            display[7].draw(game_window)
            display[7].setVisible(True)

running = True
#If a function has been selected: Multiplication, Division, Addition, Subtraction
isDoingFunction = False
#If the Maximum number has been received yet
getMaxNum = False
#If the question has been answered
Answered = False
#Include Negative answers for subtraction
doNegatives = False
#If settings is being shown
showSettings = False
#Determines if screen is being changed
changeScreen = False
#If 10 questions have been answered
showAnswers = False
#Whether timer is shown
showTimer = True
#Show leaderboard screen
showLeader = False
#Got perfect score or not
perfectScore = True
#Leaderboard temporary record string
record = ""
#The two numbers that are outputted
num1 = 0
num2 = 0
#Current Position of the top leaderboard page
currentPos = 0
#Beginning and End times
begin = 0
end = 0
#Maximum Number
MaxNum = 0
#The answer that is calculated by computer
answer = 0
#The answer that is entered by the user
userAnswer = 0
currentQuestion = 0
#Letter counter for leaderboard entry
counter = 0
firstInit = True
while running:
    if end==0 and isDoingFunction and not getMaxNum:
        display[5].setText("{:.2f}".format(time.time()-begin))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fileMaster.save()
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN: 
            for x in range(len(buttons)):
                if buttons[x].getVisible():
                    if buttons[x].isOver(pg.mouse.get_pos()):
                        if x<=9:
                            output=output+str(x)
                            display[6].setText(output)
                        elif x==10:
                            funcType="x"
                            isDoingFunction = True
                            getMaxNum = True
                        elif x==11:
                            funcType="÷"
                            isDoingFunction = True
                            getMaxNum = True
                        elif x==12:
                            funcType="+"
                            isDoingFunction = True
                            getMaxNum = True
                        elif x==13:
                            funcType="-"
                            isDoingFunction = True
                            getMaxNum = True
                        elif x==14 and not getMaxNum:
                            output = output +"-"
                            display[6].setText(output)
                        elif x==15 and len(output)>0:
                            output = output[0:len(output)-1]
                            display[6].setText(output)
                        elif x==16:
                            if(currentPos+5<leaderMasterScores.size):
                                currentPos+=5
                                if(leaderMasterScores.size>=currentPos+5):
                                    for x in range(5):
                                        display[x+9].setText(leaderMasterNames[currentPos+x]+" "+str(leaderMasterScores[currentPos+x]))
                                else:
                                    tempnum = 0
                                    for x in range(leaderMasterScores.size-currentPos):
                                        display[x+9].setText(leaderMasterNames[currentPos+x]+" "+str(leaderMasterScores[currentPos+x]))
                                        tempnum+=1
                                    for x in range(currentPos+5-leaderMasterScores.size):
                                        display[x+9+tempnum].setText("--- --.--")
                        elif x==17:
                            if(currentPos-5>=0):
                                currentPos-=5
                                for x in range(5):
                                    display[x+9].setText(leaderMasterNames[currentPos+x]+" "+str(leaderMasterScores[currentPos+x]))
                        elif x==18:
                            if(display[14].getText()=="Z"):
                                display[14].setText("A")
                            else:
                                display[14].setText(chr(ord(display[14].getText())+1))
                        elif x==19:
                            if(display[14].getText()=="A"):
                                display[14].setText("Z")
                            else:
                                display[14].setText(chr(ord(display[14].getText())-1))
                        elif x==len(buttons)-1:
                            if getMaxNum:
                                if output != "":
                                    MaxNum=int(output)
                                    Answered=True
                                    getMaxNum = False
                                    begin = time.time()
                                    leaderMasterNames = fileMaster.getMasterNames(funcType)
                                    leaderMasterScores = fileMaster.getMasterScores(funcType)
                            elif currentQuestion<=9 and not showLeader:
                                if output =="":
                                    output = "0"
                                userAnswer = int(output)
                                Answered=True
                                #Adds answers to array of answer buttons
                                answerButtons[currentQuestion].append(Answer(num1,num2,answer,userAnswer, userAnswer==answer,funcType,doNegatives))
                                #Checks if users answer is correct
                                if userAnswer == answer:
                                    answerButtons[currentQuestion][0].color = (17,247,5)
                                else:
                                    answerButtons[currentQuestion][0].color = (247,13,5)
                                    perfectScore = False
                                #Recognize when 10 questions have been answered
                                if currentQuestion < 9:
                                    currentQuestion = currentQuestion + 1
                                else:
                                    showAnswers = True
                                    currentQuestion=currentQuestion+1
                                    display[3].setText("Your Answer: " + str(answerButtons[9][1].userAnswer))
                                    display[0].setText("    "+str(answerButtons[9][1].num1))
                                    display[1].setText(funcType+"   "+str(answerButtons[9][1].num2))
                                    Answered = False
                                    end = time.time()
                            #Go to leaderboard screen
                            elif currentQuestion > 9 and showAnswers:
                                currentQuestion = 0
                                showLeader = True
                                if(leaderMasterScores.size>=5):
                                    for x in range(5):
                                        display[x+9].setText(leaderMasterNames[currentPos+x]+" "+str(leaderMasterScores[currentPos+x]))
                                else:
                                    for x in range(leaderMasterScores.size):
                                        display[x+9].setText(leaderMasterNames[currentPos+x]+" "+str(leaderMasterScores[currentPos+x]))
                                    for x in range(5-leaderMasterScores.size):
                                        display[x+9+leaderMasterScores.size].setText("--- --.--")
                            #Reset for another time around
                            elif showLeader and showAnswers:
                                if perfectScore and counter<3:
                                    counter+=1
                                    record+=display[14].getText()
                                else:
                                    if(counter==3):
                                        fileMaster.add(funcType, round(end-begin,2), record)
                                        record=""
                                    isDoingFunction = False
                                    showAnswers = False
                                    showLeader = False
                                    counter = 0
                                    perfectScore = True
                                    currentPos = 0
                                    buttons[len(buttons)-1].setText("Enter")
                                    buttons[len(buttons)-1].setX(0)
                                    buttons[len(buttons)-1].setY(resY-2*dif-102)
                                    for x in range(10):
                                        answerButtons[x].pop(1)
                                        answerButtons[x][0].color = (0,150,150)
                                    display[3].setText("")
                                    end = 0
                                    display[5].setText("0.00")
                            output=""
                            display[6].setText(output)
                            if showAnswers:
                                display[6].setText("Correct Answer: " + str(answerButtons[9][1].answer))
            for x in range(len(settingsButtons)):
                if settingsButtons[x].getVisible():
                    if settingsButtons[x].isOver(pg.mouse.get_pos()):
                        if x==0:
                            showSettings = not showSettings
                        elif x==1:
                            if doNegatives:
                                settingsButtons[x].color = (247,13,5)
                            else:
                                settingsButtons[x].color = (42,191,62)
                            doNegatives = not doNegatives
                        elif x==2:
                            changeScreen = not changeScreen
                        elif x==3 or x==4 or x==5:
                            resX = (int)(settingsButtons[x].getText()[0:settingsButtons[x].getText().find("x")])
                            resY = (int)(settingsButtons[x].getText()[settingsButtons[x].getText().find("x")+1:len(settingsButtons[x].getText())])
                            game_window = pg.display.set_mode((resX,resY))
                            initialize(firstInit)
                        elif x==6:
                            if showTimer:
                                settingsButtons[x].color = (247,13,5)
                            else:
                                settingsButtons[x].color = (42,191,62)
                            showTimer = not showTimer
                        elif x==7:
                            initialize(False)
                            getMaxNum = False
                            isDoingFunction = False
                            Answered = False
                            showSettings = False
                            showAnswers = False
                            perfectScore = True
                            showLeader = False
                            for x in range(10):
                                if len(answerButtons[x])>1:
                                    answerButtons[x].pop(1)
                                answerButtons[x][0].color = (0,150,150)
                            display[3].setText("")
                            end = 0
                            record = ""
                            display[5].setText("0.00")
                            buttons[len(buttons)-1].setText("Enter")
                            buttons[len(buttons)-1].setX(0)
                            buttons[len(buttons)-1].setY(resY-2*dif-102)
                            currentQuestion = 0
                        elif x==8:
                            fileMaster.clear()
            if showAnswers:
                for x in range(10):
                    if answerButtons[x][0].isOver(pg.mouse.get_pos()):
                        display[6].setText("Correct Answer: " + str(answerButtons[x][1].answer))
                        display[3].setText("Your Answer: " + str(answerButtons[x][1].userAnswer))
                        display[0].setText("    "+str(answerButtons[x][1].num1))
                        display[1].setText(funcType+"   "+str(answerButtons[x][1].num2))
                        display[4].setText(answerButtons[x][1].getExplanation())
                        
        elif event.type == pg.MOUSEMOTION:
            for x in range(len(buttons)):
                if buttons[x].isOver(pg.mouse.get_pos()):
                    buttons[x].color = (42,232,67)
                else:
                    buttons[x].color = (42,191,62)
            if showAnswers:
                for x in range(10):
                    if answerButtons[x][0].isOver(pg.mouse.get_pos()):
                        if not answerButtons[x][1].correct:
                            answerButtons[x][0].color = (209, 17, 10)
                        else:
                            answerButtons[x][0].color = (42,232,67)
                    else:
                        if not answerButtons[x][1].correct:
                            answerButtons[x][0].color = (247, 13, 5)
                        else:
                            answerButtons[x][0].color = (17,247,5)
        if funcType != "":
            if Answered:
                if funcType == "x":
                    num1 = random.randint(1,MaxNum)
                    num2 = random.randint(1,MaxNum)
                    answer = num1*num2
                elif funcType == "÷":
                    num2 = random.randint(1,MaxNum)
                    answer = random.randint(1,MaxNum)
                    num1 = num2*answer
                elif funcType =="+":
                    num1 = random.randint(1,MaxNum)
                    num2 = random.randint(1,MaxNum)
                    answer = num1+num2
                elif funcType =="-":
                    if doNegatives:
                        num1 = random.randint(1,MaxNum)
                        num2 = random.randint(1,MaxNum)
                        answer = num1-num2
                    else:
                        num1 = random.randint(1,MaxNum)
                        num2 = random.randint(1,num1)
                        answer = num1-num2
                display[0].setText("    "+ str(num1))
                display[1].setText(funcType+"   "+(str(num2)))
                Answered = False
    pg.display.update()
    update(isDoingFunction,getMaxNum,showSettings,changeScreen,showAnswers,doNegatives and len(output)==0,showTimer,showLeader,perfectScore)