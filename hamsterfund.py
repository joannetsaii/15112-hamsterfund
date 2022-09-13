'''
Term Project: Hamster Fund - Personal Budgeting Application
Name: Joanne Tsai
Andrew ID: chihant
'''
# use pip3 install packagename in terminal
from cmu_112_graphics import *
from matplotlib import pyplot as plt
import numpy as np
from tkinter import *
from datetime import date
import math, csv, json
import requests
from bs4 import BeautifulSoup

################################################################
# Welcome Screen Mode
################################################################
def welcomeScreenMode__init__(app):
    app.coverImage = app.loadImage('assets/hamster.png')
    app.scaledCoverImage = app.scaleImage(app.coverImage, 1/18)
    app.data = {}
    app.message = ''
    #current date
    today = date.today()
    app.today = ("%s/%s/%s" % (today.year, today.month, today.day))
    app.yearMonth = app.today.split('/')[0] + '/' + app.today.split('/')[1]
    #user entries & buttons
    app.typingName, app.typingPass = False, False
    app.username, app.password, app.config = '', '', ''
    app.changeLoginColor, app.changeSignUpColor = False, False

def welcomeScreenMode_mouseMoved(app, event): #detect if mouse moves to buttons
    if clickOnSignUp(app, event.x, event.y):
        app.changeSignUpColor = True
    else: 
        app.changeSignUpColor = False
    if clickOnLogin(app, event.x, event.y):
        app.changeLoginColor = True
    else: 
        app.changeLoginColor = False

def clickOnUsername(app, x, y):
    return (app.width//2-32 <= x <= app.width-92 and app.height//2+40 <= y <= app.height//2+65)

def clickOnPassword(app, x, y):
    return (app.width//2-32 <= x <= app.width-92 and app.height//2+85 <= y <= app.height//2+110)

def clickOnSignUp(app, x, y):
    return (app.width//2+30 <= x <= app.width//2+110 and app.height-170 <= y <= app.height-140)

def clickOnLogin(app, x, y):
    return (app.width//2-110 <= x <= app.width//2-30 and app.height-170 <= y <= app.height-140)
 

def welcomeScreenMode_mousePressed(app, event):
    if clickOnUsername(app, event.x, event.y): 
        app.typingName = True
        if app.username == '': 
            app.username = '|'
    elif clickOnPassword(app, event.x, event.y):
        app.typingName = False
        app.typingPass = True
        if app.config == '':
            app.config = '|'
    elif clickOnSignUp(app, event.x, event.y):
        try:
            myFile = getJson(f'./{app.username}.json')
            app.message = 'User already signed up. Please login.'
        except:
            app.message = ''
            app.data['password'] = app.password
            app.data['income'] = {}
            app.data['expenses'] = {}
            app.data['record'] = []
            app.data['budgets'] = {}
            app.data['budgetRecord'] = {}
            app.data['savePct'] = 20 #default value = 20%
            app.data['savings'] = {}
            app.data['ratingRecord'] = {} #store rating distribution each year
            app.data['expense>expected'] = False
            app.data['budget_pct_cat'] = {'Food':'0', 'Entertainment':'0', 'Transportation':'0', 'Utilities':'0', 'Clothing':'0',
                                          'Health':'0', 'Insurance':'0', 'Education':'0', 'Other':'0', 'Savings':str(app.data['savePct'])}
            writeToJsonFile('./', app.username, app.data) #'./' = current directory
    elif clickOnLogin(app, event.x, event.y):
        try:
            myFile = getJson(f'./{app.username}.json')
            if myFile['password'] == app.password:
                #load all user data from the json file
                app.mode = 'setBudgetsInCategoriesMode'
                app.income = myFile.get('income', {})
                app.expenses = myFile.get('expenses', {})
                app.record = myFile.get('record', [])
                app.budgets = myFile.get('budgets', {})
                app.budgetRecord = myFile.get('budgetRecord', {})
                app.savePct = myFile.get('savePct', 20)
                app.savings = myFile.get('savings', {})
                app.ratingRecord = myFile.get('ratingRecord', {})
                app.budget_pct_cat = myFile.get('budget_pct_cat', {'Food':'0', 'Entertainment':'0', 'Transportation':'0', 'Utilities':'0',
                                                                   'Clothing':'0', 'Health':'0', 'Insurance':'0', 'Education':'0', 'Other':'0', 'Savings':str(app.savePct)})
                app.data = getJson(f'./{app.username}.json')
            else:
                app.message = 'Incorrect password. Please try again.'
        except:
            app.message = 'User has not signed up. Please sign up first.'


def welcomeScreenMode_keyPressed(app, event):
    if app.typingName:
        if app.username == '|':
            app.username = event.key
        elif len(event.key) == 1 and event.key.isalnum():
            app.username += event.key
        elif event.key == 'Delete':
            app.username = app.username[:-1]
    elif app.typingPass:
        if app.config == '|':
            app.password = event.key
            app.config = '*'
        elif len(event.key) == 1 and event.key.isalnum():
            app.password += event.key
            app.config += '*'
        elif event.key == 'Delete':
            app.password = app.password[:-1]
            app.config = app.config[:-1]


def drawUserEntryBoxes(app, canvas):
    #username
    canvas.create_text(app.width//2-40, app.height//2+51, anchor='e', text='Username:', font='Galvji 15 bold', fill='#373737')
    canvas.create_rectangle(app.width//2-32, app.height//2+40, app.width-92, app.height//2+65, fill='#fcfcfa', width=1.5, outline='#373737')
    canvas.create_text(app.width//2-27, app.height//2+52.5, anchor='w', text=app.username, font='Galvji 14')

    #password
    canvas.create_text(app.width//2-40, app.height//2+96.5, anchor='e', text='Password:', font='Galvji 15 bold', fill='#373737')
    canvas.create_rectangle(app.width//2-32, app.height//2+85, app.width-92, app.height//2+110, fill='#fcfcfa', width=1.5, outline='#373737')
    canvas.create_text(app.width//2-27, app.height//2+98, anchor='w', text=app.config, font='Galvji 15')


def drawUserButtons(app, canvas):
    # login button
    if app.changeLoginColor: color1 = '#dfe0db'
    else: color1 = '#fcfcfa'
    canvas.create_rectangle(app.width//2-110, app.height-170, app.width//2-30, app.height-140, fill=color1, width=1.5, outline='#373737')
    canvas.create_text(app.width//2-70, app.height-155, text='Login', font='Galvji 14 bold', fill='#373737')

    # sign up (register) button
    if app.changeSignUpColor: color2 = '#dfe0db'
    else: color2 = '#fcfcfa'
    canvas.create_rectangle(app.width//2+30, app.height-170, app.width//2+110, app.height-140, fill=color2, width=1.5, outline='#373737')
    canvas.create_text(app.width//2+70, app.height-155, text='Register', font='Galvji 14 bold', fill='#373737')

    # if password is not correct/ user already signed up.
    if (app.message != ''):
        canvas.create_text(app.width//2, app.height//2+128, text=app.message, font='Galvji 13', fill='red')


def welcomeScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_image(app.width//2, app.height//2-120, 
                        image=ImageTk.PhotoImage(app.scaledCoverImage))
    canvas.create_text(app.width//2, app.height//2-16, text='Hamster Fund', 
                       fill='#683c0f', font='Galvji 30 bold')
    drawUserEntryBoxes(app, canvas)
    drawUserButtons(app, canvas)
    

################################################################
# Budgets in Specific Categories Mode
################################################################
def setBudgetsInCategoriesMode__init__(app):
    #app.budget_pct_cat called when user logs in
    app.changeSaveColor = False
    app.changeSkipColor = False
    app.typingFood, app.typingEnt, app.typingTrans, app.typingUti = False, False, False, False
    app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False
    
    
def setBudgetsInCategoriesMode_mouseMoved(app, event):
    if (app.width//2-35 <= event.x <= app.width//2+35 and app.height-80 <= event.y <= app.height-50):
        app.changeSaveColor = True
    else:
        app.changeSaveColor = False


def setBudgetsInCategoriesMode_mousePressed(app, event):
    myFile = getJson(f'./{app.username}.json')
    if clickOnReturn(app, event.x, event.y):
        app.changeSaveColor = False
        for category in myFile['budget_pct_cat']:
            if myFile['budget_pct_cat'][category] == '|':
                myFile['budget_pct_cat'][category] = '0' #reset
        app.mode = 'welcomeScreenMode'
    elif (app.width//2-35 <= event.x <= app.width//2+35 and app.height-80 <= event.y <= app.height-50): #click on save->turn page
        for category in myFile['budget_pct_cat']:
            if myFile['budget_pct_cat'][category] == '|':
                myFile['budget_pct_cat'][category] = '0' #reset
        app.mode = 'selectionScreenMode'
    elif (178 <= event.x <= 218):
        dx = (app.height-25-140)//11 -5
        if (130+dx-12 <= event.y <= 130+dx+12):
            app.typingFood = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Food'] == '0':
                myFile['budget_pct_cat']['Food'] = '|'
            else:
                myFile['budget_pct_cat']['Food'] += '|'

        elif (130+(dx*2)-12 <= event.y <= 130+(dx*2)+12):
            app.typingEnt = True
            app.typingFood, app.typingTrans, app.typingUti, app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Entertainment'] == '0':
                myFile['budget_pct_cat']['Entertainment'] = '|'
            else:
                myFile['budget_pct_cat']['Entertainment'] += '|'

        elif (130+(dx*3)-12 <= event.y <= 130+(dx*3)+12):
            app.typingTrans = True
            app.typingEnt, app.typingFood, app.typingUti, app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Transportation'] == '0':
                myFile['budget_pct_cat']['Transportation'] = '|'
            else:
                myFile['budget_pct_cat']['Transportation'] += '|'
        
        elif (130+(dx*4)-12 <= event.y <= 130+(dx*4)+12):
            app.typingUti = True
            app.typingEnt, app.typingTrans, app.typingFood, app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Utilities'] == '0':
                myFile['budget_pct_cat']['Utilities'] = '|'
            else:
                myFile['budget_pct_cat']['Utilities'] += '|'
        
        elif (130+(dx*5)-12 <= event.y <= 130+(dx*5)+12):
            app.typingCloth = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingFood, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Clothing'] == '0':
                myFile['budget_pct_cat']['Clothing'] = '|'
            else:
                myFile['budget_pct_cat']['Clothing'] += '|'
        
        elif (130+(dx*6)-12 <= event.y <= 130+(dx*6)+12):
            app.typingHealth = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingCloth, app.typingFood, app.typingIns, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Health'] == '0':
                myFile['budget_pct_cat']['Health'] = '|'
            else:
                myFile['budget_pct_cat']['Health'] += '|'
        
        elif (130+(dx*7)-12 <= event.y <= 130+(dx*7)+12):
            app.typingIns = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingCloth, app.typingHealth, app.typingFood, app.typingEdu, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Insurance'] == '0':
                myFile['budget_pct_cat']['Insurance'] = '|'
            else:
                myFile['budget_pct_cat']['Insurance'] += '|'
        
        elif (130+(dx*8)-12 <= event.y <= 130+(dx*8)+12):
            app.typingEdu = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingCloth, app.typingHealth, app.typingIns, app.typingFood, app.typingOther = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Education'] == '0':
                myFile['budget_pct_cat']['Education'] = '|'
            else:
                myFile['budget_pct_cat']['Education'] += '|'
        
        elif (130+(dx*9)-12 <= event.y <= 130+(dx*9)+12):
            app.typingOther = True
            app.typingEnt, app.typingTrans, app.typingUti, app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingFood = False, False, False, False, False, False, False, False
            if myFile['budget_pct_cat']['Other'] == '0':
                myFile['budget_pct_cat']['Other'] = '|'
            else:
                myFile['budget_pct_cat']['Other'] += '|'

    app.data['budget_pct_cat'] = myFile['budget_pct_cat']
    writeToJsonFile('./', app.username, app.data)



def setBudgetsInCategoriesMode_keyPressed(app, event):
    myFile = getJson(f'./{app.username}.json')
    boolName = ['Food', 'Entertainment', 'Transportation', 'Utilities', 
                'Clothing', 'Health', 'Insurance', 'Education', 'Other']
    boolList = [app.typingFood, app.typingEnt, app.typingTrans, app.typingUti, 
               app.typingCloth, app.typingHealth, app.typingIns, app.typingEdu, app.typingOther]
    for i in range(len(boolList)):
        if boolList[i] == True:
            if (event.key.isdigit() and myFile['budget_pct_cat'][boolName[i]] == '|'):
                myFile['budget_pct_cat'][boolName[i]] = event.key
            elif event.key.isdigit():
                myFile['budget_pct_cat'][boolName[i]] += event.key
            elif (event.key == 'Delete' and myFile['budget_pct_cat'][boolName[i]] != '|'):
                myFile['budget_pct_cat'][boolName[i]] = myFile['budget_pct_cat'][boolName[i]][:-2] + '|'
        else:
            if '|' in myFile['budget_pct_cat'][boolName[i]]:
                myFile['budget_pct_cat'][boolName[i]].replace('|', '')
        app.data['budget_pct_cat'] = myFile['budget_pct_cat']
        writeToJsonFile('./', app.username, app.data)
    

def drawCurrentPercentageLeft(app, canvas): #display current percentage available for planning
    canvas.create_rectangle(0, 60, app.width, 110, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    myFile = getJson(f'./{app.username}.json')
    sumPct = 0
    for category in myFile['budget_pct_cat']:
        try:
            if myFile['budget_pct_cat'][category] == '|':
                sumPct += 0
            elif '|' in myFile['budget_pct_cat'][category]:
                myFile['budget_pct_cat'][category].replace('|', '')
                sumPct += int(myFile['budget_pct_cat'][category])
            else:
                sumPct += int(myFile['budget_pct_cat'][category])
        except:
            sumPct += 0
    pctLeft = 100-sumPct
    canvas.create_text(app.width//2-23, 85, text=f'Percentage of Income Available for Budgeting:',
                       font='Galvji 14', fill='#373737')
    canvas.create_text(app.width//2+153, 85, text=f'{pctLeft}%', font='Galvji 14 bold', fill='#373737')


def drawTitles(app, canvas):
    canvas.create_rectangle(0, 110, app.width, 140, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    text = ['Category', 'Percentage', 'Amount($)']
    x0 = 70
    for i in range(3):
        canvas.create_text(x0, 125, text=text[i], font='Galvji 15 bold', fill='#373737')
        x0 += 136


def drawCategoryNames(app, canvas):
    canvas.create_rectangle(0, 140, app.width, app.height-25, fill='#f8f8f4', outline='#9f6c59', width=1.5) #bg
    categories = ['Food', 'Entertainment', 'Transportation', 'Utilities', 'Clothing', 'Health', 'Insurance', 'Education', 'Other', 'Savings']
    dx = (app.height-25-140)//11 -5 #10 gaps
    for i in range(10):
        canvas.create_text(70, 130+(dx*(i+1)), text=categories[i], font='Galvji 13', fill='#373737')


def drawSaveButton(app, canvas):
    #save button
    if app.changeSaveColor: color = '#dfe0db'
    else: color = '#fcfcfa'
    canvas.create_rectangle(app.width//2-35, app.height-80, app.width//2+35, app.height-50, fill=color, width=1.5, outline='#373737')
    canvas.create_text(app.width//2, app.height-65, text='Save', fill='#373737', font='Galvji 16 bold')


def drawPercentages(app, canvas):
    myFile = getJson(f'./{app.username}.json')
    #boxes
    dx = (app.height-25-140)//11 -5 #10 gaps
    for i in range(9):
        canvas.create_rectangle(178, 130+(dx*(i+1))-12, 218, 130+(dx*(i+1))+12, fill='#fcfcfa')
    for i in range(10):
        canvas.create_text(229, 130+(dx*(i+1)), text='%', font='Galvji 13', fill='#373737')
    #content (__%)
    i = 0
    for category in myFile['budget_pct_cat']:
        canvas.create_text(198, 130+(dx*(i+1)), text=myFile['budget_pct_cat'][category], font='Galvji 13', fill='#373737')
        i += 1


def drawAvailableAmt(app, canvas):
    myFile = getJson(f'./{app.username}.json')
    dx = (app.height-25-140)//11 -5 #10 gaps
    if app.yearMonth in myFile['income']:
        incomeInCurMonth = myFile['income'][app.yearMonth]
        amtList = []
        for category in myFile['budget_pct_cat']:
            if myFile['budget_pct_cat'][category] == '|':
                amtList.append(0.0)
            else:
                amtList.append(incomeInCurMonth * int(myFile['budget_pct_cat'][category])/100)
        for i in range(10):
            canvas.create_text(342, 130+(dx*(i+1)), text=str(amtList[i]), font='Galvji 13', fill='#373737')
    else:
        for i in range(10):
            canvas.create_text(342, 130+(dx*(i+1)), text='No Data', font='Galvji 13', fill='#373737')


def setBudgetsInCategoriesMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#906c4f', width=1.5)
    canvas.create_text(app.width//2, 33, text='Budgets in Specific Categories', font='Courier 17 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    drawCurrentPercentageLeft(app, canvas)
    drawTitles(app, canvas)
    drawCategoryNames(app, canvas)
    drawPercentages(app, canvas)
    drawAvailableAmt(app, canvas)
    drawSaveButton(app, canvas)
    


################################################################
# Selection Screen Mode
################################################################
def selectionScreenMode__init__(app):
    app.typingRate = False
    app.changeUpdateColor = False
    app.rate = '' #the savings rate user enters


def selectionScreenMode_keyPressed(app, event):
    if app.typingRate:
        if (app.rate == '|') and event.key.isdigit():
            app.rate = event.key 
        elif event.key.isdigit() and len(event.key) == 1:
            app.rate += event.key 
        elif event.key == 'Delete':
            app.rate = app.rate[:-1]


def selectionScreenMode_mousePressed(app, event):
    if clickOnReturn(app, event.x, event.y):
        app.rate = ''
        app.mode = 'welcomeScreenMode'
    #access to different modes
    (y0, dy) = (app.height//2+15, 40)
    if (30 <= event.x <= app.width//2-10) and (y0+dy <= event.y <= y0+(dy*2)):
        app.mode = 'guideMode'
    elif (30 <= event.x <= app.width//2-10) and (y0+(dy*2) <= event.y <= y0+(dy*3)):
        app.mode = 'recordMode'
    elif (30 <= event.x <= app.width//2-10) and (y0+(dy*3) <= event.y <= y0+(dy*4)):
        app.mode = 'budgetMode'
    elif (30 <= event.x <= app.width//2-10) and (y0+(dy*5) <= event.y <= y0+(dy*6)):
        app.graphInfo = {'GraphType':'', 'Classification':'', 'Year':'', 'Month':''}
        app.mode = 'analysisMode'
    elif (30 <= event.x <= app.width//2-10) and (y0+(dy*6) <= event.y <= y0+(dy*7)):
        app.mode = 'ratingMode'

    #click on rate entry box
    if (app.width//2+20 <= event.x <= app.width//2+65) and (y0+dy*6+7 <= event.y <= y0+dy*7-7): 
        app.typingRate = True
        app.rate = '|'
    #click on update button
    if (app.width-100 <= event.x <= app.width-40) and (y0+dy*6+7 <= event.y <= y0+dy*7-7) and app.rate != '' and int(app.rate) <= 100:
        if ('.' in app.rate):
            app.savePct = float(app.rate)
            app.data['savePct'] = app.savePct
        else:
            app.savePct = int(app.rate)
            app.data['savePct'] = app.savePct
        writeToJsonFile('./', app.username, app.data)
        app.rate = '' #re-initialize
        app.typingRate = False


def getBarData(app):
    myFile = getJson(f'./{app.username}.json')
    expenses = myFile.get('expenses', {})
    income = myFile.get('income', {})
    savings = myFile.get('savings', {})
    budgets = myFile.get('budgets', {})
    expense = 0
    if app.yearMonth in expenses:
        for category in expenses[app.yearMonth]:
            expense += expenses[app.yearMonth][category]
    if app.yearMonth in income:
        income = income[app.yearMonth]
    else: income = 0
    if app.yearMonth in savings:
        savings = savings[app.yearMonth]
    else: savings = 0
    budget = 0
    if app.yearMonth in budgets:
        for category in budgets[app.yearMonth]:
            for item in budgets[app.yearMonth][category]:
                budget += item[1]
    remaining = income - expense
    return ([expense, remaining, budget, savings])
    

def calcMaxAmt(app, amt_list):
    bestAmt = 0
    for amt in amt_list:
        if amt > bestAmt: bestAmt = amt
    return bestAmt


def drawBars(app, canvas): #bars displayed on the main menu page
    canvas.create_rectangle(0, 60, app.width, app.height//2-15, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    margin = 18 #distance between bars
    amt_list = getBarData(app)
    highestAmt = calcMaxAmt(app, amt_list)
    barHeight = (app.height//2-25-105-margin*5)//4
    maxWidth = app.width-105-20  #distance between longest bar & border is 20
    title_list = ['Expense', 'Remaining', 'Budget', 'Savings']
    y0 = 105+margin
    for i in range(len(amt_list)): #[expense, remaining, savings, budget]
        if amt_list[i] == 0:
            canvas.create_text(15, y0+(margin*i)+(barHeight*(i+0.5)), text=title_list[i], anchor='w', font='Galvji 15 bold', fill='#9f6c59')
            canvas.create_text(140, y0+(margin*i)+(barHeight*(i+0.5)), text='No Data', font='Galvji 13', fill='#9f6c59')
        else:
            canvas.create_text(15, y0+(margin*i)+(barHeight*(i+0.5)), text=title_list[i], anchor='w', font='Galvji 15 bold', fill='#9f6c59')
            barWidth = maxWidth * (amt_list[i]/highestAmt)
            canvas.create_rectangle(105, y0+(margin*i)+(barHeight*i), 105+barWidth, y0+(margin*i)+(barHeight*(i+1)), fill='#9f6c59', outline='#fcfcfa')
            if barWidth >= len(str(amt_list[i]))*10:
                canvas.create_text(105+barWidth//2, y0+(margin*i)+(barHeight*(i+0.5)), 
                                   text=f'$ {str(amt_list[i])}', font='Galvji 13', fill='#fcfcfa')
            else: 
                canvas.create_text(105+barWidth+8, y0+(margin*i)+(barHeight*(i+0.5)), 
                                   text=f'$ {str(amt_list[i])}', anchor='w', font='Galvji 13', fill='#9f6c59')

    canvas.create_line(105, 105, 105, app.height//2-25, fill='#9f6c59', width=2.5) #line that separates words and bars



def drawMenuBox(app, canvas):
    (y0, dy) = (app.height//2+15, 40)
    text_list_1 = ['Main', 'Guide', 'Record', 'Budget Plan']
    text_list_2 = ['Report', 'Graph Analysis', 'Ratings']
    for i in range(4):
        if i == 0: 
            color_bg = '#ce8e73'
            color_wd = '#fcfcfa'
            font = 'Courier 17 bold'
        else: 
            color_bg = '#f8f8f4'
            color_wd = '#9f6c59'
            font = 'Courier 15'
        canvas.create_rectangle(25, y0+(dy*i), app.width//2-15, y0+(dy*(i+1)), 
                                fill=color_bg, outline='#9f6c59', width=1.5)
        canvas.create_text(25+(app.width//2-40)//2, y0+(dy*(i+0.5))+2, 
                               text=text_list_1[i], font=font, fill=color_wd)
    for i in range(4,7):
        if i == 4: 
            color_bg = '#ce8e73'
            color_wd = '#fcfcfa'
            font = 'Courier 17 bold'
        else: 
            color_bg = '#f8f8f4'
            color_wd = '#9f6c59'
            font = 'Courier 15'
        canvas.create_rectangle(25, y0+(dy*i), app.width//2-15, y0+(dy*(i+1)), 
                                fill=color_bg, outline='#9f6c59', width=1.5)
        canvas.create_text(25+(app.width//2-40)//2, y0+(dy*(i+0.5))+2, 
                           text=text_list_2[i-4], font=font, fill=color_wd)


def drawSavingsEnvelope(app, canvas):
    (y0, dy) = (app.height//2+15, 40)
    #"Savings" title
    canvas.create_rectangle(app.width//2+15, y0, app.width-25, y0+dy, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2+10+(app.width-32-app.width//2)//2, y0+(0.5*dy), 
                       text='Savings', font='Courier 17 bold', fill='#fcfcfa')
    #current savings $ box
    canvas.create_rectangle(app.width//2+15, y0+dy, app.width-25, y0+dy*3, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    
    #"Savings Rate" title
    canvas.create_rectangle(app.width//2+15, y0+dy*3, app.width-25, y0+dy*4, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2+16+(app.width-40-app.width//2)//2, y0+(dy*3.5), 
                       text='Savings Rate', font='Courier 17 bold', fill='#fcfcfa')

    #current savings rate box
    canvas.create_rectangle(app.width//2+15, y0+dy*4, app.width-25, 645, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    #line that separates text and entry box
    canvas.create_line(app.width//2+15, y0+dy*6, app.width-25, y0+dy*6, fill='#9f6c59', width=1.5)
 
    #shows the current savings rate %
    myFile = getJson(f'./{app.username}.json')
    savingsDict = myFile.get('savings', {})
    totalSavings = 0
    if savingsDict != {}:
        for yearMonth in savingsDict:
            totalSavings += savingsDict[yearMonth]
    canvas.create_text(app.width//2+25, y0+dy+25, text=f'Current Total\nSavings:', anchor='w', font='Galvji 14 bold', fill='#9f6c59')
    canvas.create_text(app.width//2+25, y0+(dy*4)+25, text=f'Current Percentage\nSaved:', anchor='w', font='Galvji 14 bold', fill='#9f6c59')
    canvas.create_text(app.width-35, y0+(dy*3)-18, text=f'$ {totalSavings}', anchor='e', font='Galvji 16 bold', fill='#9f6c59')
    canvas.create_text(app.width-35, y0+(dy*6)-18, text=f'{str(app.savePct)} %', anchor='e', font='Galvji 16 bold', fill='#9f6c59')

    #rate entry box
    canvas.create_rectangle(app.width//2+25, y0+dy*6+7, app.width//2+70, y0+dy*7-7, fill='#fcfcfa', width=1)
    canvas.create_text(app.width//2+33, y0+dy*6.5, anchor='w', text=app.rate, font='Galvji 14', fill='#373737')
    canvas.create_text(app.width//2+81, y0+dy*6.5, text='%', font='Galvji 16', fill='#373737')
    #update button
    if app.changeUpdateColor: color = '#dfe0db'
    else: color = '#fcfcfa'
    canvas.create_rectangle(app.width-95, y0+dy*6+7, app.width-35, y0+dy*7-7, fill=color, width=1)
    canvas.create_text(app.width-65, y0+dy*6.5, text='update', font='Galvji 13', fill='#373737')



def selectionScreenMode_redrawAll(app, canvas):
    #canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#f8f8f4')
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#906c4f', width=1.5)
    canvas.create_text(app.width//2, 33, text='Main Account', font='Courier 20 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas) #change afterwards
    drawBottomBorder(app, canvas)
    drawBars(app, canvas) #draw out the actual bars
    drawMenuBox(app, canvas) #draw LHS menu
    drawSavingsEnvelope(app, canvas) #draw RHS menu
    #subtitle: "My data in year/month"
    canvas.create_text(app.width//2, 80, text=f'My Data in {app.yearMonth}', font='Galvji 16 bold', fill='#9f6c59')
    


################################################################
# Guide Mode
################################################################
def drawGuide_1(app, canvas):
    #1.savings envelope
    (y0, dy) = (86, 15)
    canvas.create_rectangle(0, 60, app.width, app.height//2-25, fill='#f8f8f4', outline='#9f6c59', width=1.5) #bg
    canvas.create_text(25, y0, anchor='w', text='Savings Rate', font='Galvji 18 bold', fill='#373737') #title
    content = [ "\n",
                "-   Savings rate is the percentage of the user’s monthly",
                "     income that is saved rather than consumed.",
                "\n",
                "-   According to the commonly used 50/30/20 budget rule,",
                "     the default savings rate is 20%.",
                "\n",
                "-   The saved portion every month will not be included in",
                "     the user’s budget and its aggregate value will be shown", 
                "     on the main menu.",
                "\n", 
                "-   If the user’s expense exceeds his/her budget, the system",
                "     will deduct the additional expense from the user’s",
                "     aggregate savings." ]
    for i in range(1, len(content)+1):
        canvas.create_text(25, y0+(dy*i), text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')


def drawGuide_2(app, canvas):
    #2.budget planning
    (y0, dy) = (app.height//2+1, 15)
    canvas.create_rectangle(0, app.height//2-25, app.width, app.height-25, fill='#f8f8f4', outline='#9f6c59', width=1.5) #bg
    canvas.create_text(25, y0, anchor='w', text='Budget Planning', font='Galvji 18 bold', fill='#373737') #title
    content = [ "\n",
                "-   Steps:",
                "     1. The user enters budgets for ONLY the current month",
                "         at any time ONLY during the current month.",
                "     2. The user can click the “Plan” button to know what items", 
                "          should be purchased in order to prevent overspending", 
                "          and misspending and build good financial habits.",
                "\n",
                "-   The budget planner is designed based on the commonly", 
                "     used 50/30/20 budget rule.",
                f"     -   50% of the user’s monthly income is expected to be", 
                "          spent on the “needs.”", 
                f"     -   30% of the user’s monthly income is expected to be",
                "          spent on the “wants.”",
                "\n", 
                "-   Reminder: Budget planning is only available in the current", 
                "     month. Details of the user’s past budgets are not available", 
                "     for planning or viewing. " ]
    for i in range(1, len(content)+1):
        if (i >= 13):
            canvas.create_text(25, y0+(dy*i)+25, text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')
        elif (i >= 11):
            canvas.create_text(25, y0+(dy*i)+20, text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')
        elif (i >= 5):
            canvas.create_text(25, y0+(dy*i)+10, text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')
        elif (i >= 3):
            canvas.create_text(25, y0+(dy*i)+5, text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')
        else:
            canvas.create_text(25, y0+(dy*i), text=content[i-1], anchor='w', font='Galvji 12', fill='#373737')


def guideMode_mousePressed(app, event):
    if clickOnReturn(app, event.x, event.y):
        app.mode = 'selectionScreenMode'


def guideMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#906c4f', width=1.5)
    canvas.create_text(app.width//2, 33, text='Guide', font='Courier 20 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    drawGuide_1(app, canvas)
    drawGuide_2(app, canvas)


################################################################
# Record Mode
################################################################
def recordMode__init__(app):
    app.changeEnterColor = False
    app.scrolling = False #up or down scrolling
    app.curIndex = 0 #for scrolling
    app.tempRecord = []
    app.recordSelected = None  #user wants to remove the record
    app.delete = False

def recordMode_mouseMoved(app, event):
    if clickOnEnterExpense(app, event.x, event.y):
        app.changeEnterColor = True
    else:
        app.changeEnterColor = False

def recordMode_mousePressed(app, event):
    if clickOnEnterExpense(app, event.x, event.y):
        app.scrolling = False
        app.delete = False
        app.recordSelected = None
        app.mode = 'enterRecordMode'
        app.date, app.amt, app.des = app.today, '', '' # re-initialize
    if clickOnReturn(app, event.x, event.y):
        app.scrolling = False
        app.delete = False
        app.recordSelected = None
        app.mode = 'selectionScreenMode'
    selectRecord(app, event.x, event.y) #detect which record(index) is clicked on
    if (app.recordSelected != None):
        app.delete = False
        entries = (app.height-190)//30 #dy = 30
        myFile = getJson(f'./{app.username}.json')
        record = myFile['record'][::-1]
        if len(record) < entries: #draw blanks in this case
            app.tempRecord = record + [['','','','']]*(entries-len(record))
        else:
            #records that are available for display
            app.tempRecord = record[app.curIndex:entries+app.curIndex]
        if clickOnTrash(app, event.x, event.y):
            app.delete = True
            #remove record's amount from expenses/income dictionary (json file)
            i = app.recordSelected
            if (i <= len(record)-1):
                date = app.tempRecord[i][0].split('/')[0] + '/' + app.tempRecord[i][0].split('/')[1]
                (category, description, amount) = (app.tempRecord[i][1], app.tempRecord[i][2], app.tempRecord[i][3])
                if (category == 'Income'):
                    if ('.' in amount): app.data['income'][date] -= float(amount)
                    else: app.data['income'][date] -= int(amount)
                else: # add expenses back
                    if ('.' in amount): app.data['expenses'][date][category] -= float(amount)
                    else: app.data['expenses'][date][category] -= int(amount)
                (tempRecord, i) = (app.tempRecord, app.recordSelected)
                app.data['record'].remove(app.tempRecord[i])
                #After removing the expense/income from all records, we modify app.tempRecord.
                app.tempRecord.pop(i)
                if len(record)-1 < entries:
                    app.tempRecord += [['','','','']]
                else:
                    app.tempRecord = app.data['record'][app.curIndex:entries+app.curIndex]
        writeToJsonFile('./', app.username, app.data)


def selectRecord(app, x, y): #detect which record(index) is selected
    (y0, dy) = (86, 30)
    entries = (app.height-190)//dy
    for index in range(entries):
        if (0 <= x <= app.width and y0 <= y <= y0+dy):
            app.recordSelected = index
            break
        y0 += dy


def recordMode_keyPressed(app, event):
    if (event.key == 'Up' or event.key == 'Down'):
        app.scrolling = True
    entries = (app.height-190)//30 #dy = 30
    myFile = getJson(f'./{app.username}.json')
    record = myFile['record'][::-1] #all record entries show in opposite order
    if len(record) < entries: #display blank rectangles to fill in
        record += [['','','','']]*(entries-len(record))
        app.tempRecord = record
    else:
        app.tempRecord = record[app.curIndex:entries]
    if (event.key == 'Down' and app.tempRecord[-1] != record[-1]):
        app.curIndex += 1
        app.tempRecord = record[app.curIndex:entries+1]
    elif (event.key == 'Up' and app.tempRecord[0] != record[0]):
        app.curIndex -= 1
        app.tempRecord = record[app.curIndex:entries-1]
    

def drawTitle(app, canvas):
    canvas.create_rectangle(0, 60, app.width, 86, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    (x0, dx) = (38, 0)
    for title in ['Date', 'Category', 'Description', 'Amount']:
        canvas.create_text(x0+dx, 73, text=title, font='Galvji 14 bold', fill='#373737')
        if (title == 'Category'): dx += 127
        elif (title == 'Description'): dx += 124
        else: dx += 92


def drawRecord(app, canvas):
    (y0, dy) = (86, 30)
    entries = (app.height-190)//dy
    #refresh data after user enters new data
    myFile = getJson(f'./{app.username}.json')
    record = myFile['record'][::-1]
    if len(record) < entries:
        tempRecord = record + [['','','','']]*(entries-len(record))
    else:
        tempRecord = record[:entries]
    #If the user scrolls, we change the items' order.
    if (app.scrolling or app.delete):
        tempRecord = app.tempRecord
    for i in range(entries):
        if tempRecord[i][1] == 'Income':
            if i == app.recordSelected:
                #border of the item becomes bold when being selected
                canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#eedbd5', width=1.5)
            else:
                canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#eedbd5')
        else:
            if i == app.recordSelected: 
                #border of the item becomes bold when being selected
                canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#f8f8f4', width=1.5)
            else:
                canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#f8f8f4')
        (x0, dx) = (35, 0)
        for j in range(4): #app.tempRecord[i]=(date0, cat1, des2, amt3)
            if j == 0:
                if i == app.recordSelected: 
                    canvas.create_text(x0+dx+2, y0+(dy/2), text=tempRecord[i][j], font='Galvji 12 bold', fill='#373737')
                else:
                    canvas.create_text(x0+dx+2, y0+(dy/2), text=tempRecord[i][j], font='Galvji 12', fill='#373737')
            else:
                if i == app.recordSelected: 
                    canvas.create_text(x0+dx, y0+(dy/2), text=tempRecord[i][j], font='Galvji 12 bold', fill='#373737')
                else:
                    canvas.create_text(x0+dx, y0+(dy/2), text=tempRecord[i][j], font='Galvji 12', fill='#373737')
            if (j == 1): dx += 130
            elif (j == 2): dx += 124
            else: dx += 92
        y0 += dy


def clickOnEnterExpense(app, x, y):
    return (distance(x, y, app.width//2, app.height-65) <= 28)


def drawEnterButton(app, canvas):
    if app.changeEnterColor:
        color = '#b97f67'
    else: color = '#ce8e73'
    # circle's outline
    canvas.create_oval(app.width//2-28, app.height-93, app.width//2+28, app.height-37, 
                       outline=color, fill='#fcfcfa', width=3)
    # circle
    canvas.create_oval(app.width//2-24, app.height-89, app.width//2+24, app.height-41, fill=color, outline=color)
    canvas.create_text(app.width//2, app.height-68, text='+', font='Galvji 42 bold', fill='#fcfcfa')


def recordMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_image(app.width-40, app.height-42, image=ImageTk.PhotoImage(app.trashScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2, 32, text='Record', font='Courier 20 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    drawTitle(app, canvas)
    drawRecord(app, canvas)
    drawEnterButton(app, canvas) #button to enter (-> enterMode)


################################################################
# Enter Record Mode
################################################################
def enterRecordMode__init__(app):
    app.enteringExpense, app.enteringIncome = False, False
    app.changeSaveButtonColor = False
    app.typingDate, app.choosingCat, app.typingAmt, app.typingDes = False, False, False, False
    app.date, app.category, app.amt, app.des = f'{app.today}', '', '', ''
    app.chosenCat = False  #detect if category is selected
    app.category = '' #the category selected (temp)
    app.categories = ['Income', 'Food', 'Entertainment', 'Transportation', 'Utilities', 
                      'Clothing', 'Health', 'Insurance', 'Education', 'Emergency', 'Other']


def enterExpenseOrIncome(app, x, y): #detect clicking on income/expense
    if (app.width//2-80 <= x <= app.width//2 and 100 <= y <= 130):
        app.enteringExpense = True
        app.enteringIncome = False
    elif (app.width//2 <= x <= app.width+80 and 100 <= y <= 130):
        app.enteringIncome = True
        app.enteringExpense = False
        

def enterInfo(app, x, y): #detect user's input and selection
    (dy, d) = (60, 30)
    if (app.width//2+120 <= x <= app.width//2+145 and 160+dy <= y <= 160+dy+d):
        if app.choosingCat == False: app.choosingCat = True
        else: app.choosingCat = False
    elif (app.width//2-45 <= x <= app.width//2+145):
        if (160 <= y <= 160+d):
            app.typingDate = True
            app.typingAmt, app.typingDes = False, False
        elif (160+(dy*2) <= y <= 160+(dy*2)+d):
            app.typingAmt = True
            app.typingDate, app.typingDes = False, False
            if '|' in app.date: 
                app.date.replace('|', '') #get rid of the '|' in date section
        elif (160+(dy*3) <= y <= 160+(dy*3)+d):
            app.typingDes = True
            app.typingAmt, app.typingDate = False, False
            if '|' in app.date: 
                app.date.replace('|', '') #get rid of the '|' in date section


def clickOnCategory(app, x, y):
    (dy, d) = (60, 30)
    for i in range(len(app.categories)):
        if (app.width//2-45 <= x <= app.width//2+120 and 
            160+(dy+d)+(22*i) <= y <= 160+(dy+d)+22*(i+1)):
            app.category = app.categories[i]
            app.choosingCat = False  #hide the options
            app.chosenCat = True
            app.typingDate = app.typingAmt = app.typingDes = False 


def enterRecordMode_mousePressed(app, event):    
    if clickOnReturn(app, event.x, event.y):
        app.mode = 'recordMode'
    enterExpenseOrIncome(app, event.x, event.y) #detect if user is entering income or expense
    enterInfo(app, event.x, event.y) #check if the user clicks on any of the input boxes
    if (app.choosingCat or (not app.chosenCat)): #check which category is chosen
        clickOnCategory(app, event.x, event.y)
    if app.typingDate:
        if app.date == f'{app.today}': app.date = f'{app.today}|'
    elif app.typingAmt:
        if app.amt == '': app.amt = '|'
    elif app.typingDes:
        if app.des == '': app.des = '|'
    #After all input boxes are filled
    if clickOnSave(app, event.x, event.y):
        if '|' in app.date: app.date.replace('|', '')
        storeData(app, app.date, app.category, app.amt) #purpose: calculate/analyze
        storeRecord(app, app.date, app.category, app.des, app.amt) #purpose: display/modify
        checkSavings(app, app.date, app.amt)
        app.chosenCat = False
        app.enteringIncome, app.enteringExpense = False, False
        app.mode = 'recordMode'
        

def storeRecord(app, date, category, description, amount):
    #store expenses as a list of data: [date, category, amount, description]
    #purpose: display
    app.data['record'].append([date, category, description, amount])
    writeToJsonFile('./', app.username, app.data)


def checkSavings(app, date, amount):
    myFile = getJson(f'./{app.username}.json')
    yearMonth = date.split('/')[0] + '/' + date.split('/')[1]
    #calculate total expense (after the new expense is entered)
    totalExpense = 0
    for category in myFile['expenses'][yearMonth]:
        totalExpense += myFile['expenses'][yearMonth][category]

    #1.If the user's total expense "hasn't exceeded" the expected amount before adding the new expense,
    #  we calculate the exceeded amount and deduct it from the original savings.
    if (yearMonth in myFile['income']) and (myFile['expense>expected'] == False):
        if totalExpense > (1-app.savePct/100)*(myFile['income'][yearMonth]):
            exceeded = totalExpense - (1-app.savePct/100)*(myFile['income'][yearMonth])
            app.data['savings'][yearMonth] -= exceeded
            app.data['expense>expected'] = True 

    #2.If the user's total expense "has already exceeded" the expected amount before adding on the new expense,
    elif (myFile['expense>expected'] == True):
        exceeded = totalExpense - (1-app.savePct/100)*(myFile['income'][yearMonth])
        # we check again to make sure if the above statement is true:
        if (exceeded > 0): # yes -> we deduct the new expense from original savings
            app.data['savings'][yearMonth] -= amount
        # no -> (former expense is deleted/new income is added) -> we change boolean back to False
        else:
            app.data['expense>expected'] = False
    writeToJsonFile('./', app.username, app.data)



def storeData(app, date, category, amount):
    myFile = getJson(f'./{app.username}.json')
    #store expenses/income/savings
    yearMonth = date.split('/')[0] + '/' + date.split('/')[1]
    if ('.' in amount): amount = float(amount)
    else: amount = int(amount)
    if app.enteringExpense:
        #add amount to the dictionary
        if yearMonth in app.data['expenses']:
            if category in app.data['expenses'][yearMonth]:
                app.data['expenses'][yearMonth][category] += amount
            else:
                app.data['expenses'][yearMonth][category] = amount
        else:
            app.data['expenses'][yearMonth] = {}
            app.data['expenses'][yearMonth][category] = amount
    elif app.enteringIncome:
        if yearMonth in app.data['income']:
            app.data['income'][yearMonth] += amount
        else:
            app.data['income'][yearMonth] = amount
        #store "savings" at the same time
        if yearMonth in app.data['savings']:
            myFile = getJson(f'./{app.username}.json') #refresh data
            app.savePct = myFile['savePct']
            app.data['savings'][yearMonth] += amount*(app.savePct/100)
        else:
            app.data['savings'][yearMonth] = amount*(app.savePct/100)
    writeToJsonFile('./', app.username, app.data)



def enterRecordMode_keyPressed(app, event):
    if app.typingDate and (not app.typingDes) and (not app.typingAmt):
        if (event.key.isdigit() or event.key == '/'):
            app.date += event.key
        elif event.key == 'Delete':
            if '|' in app.date: app.date = app.date[:-2] #delete '|' automatically
            else: app.date = app.date[:-1]
    elif app.typingAmt and (not app.typingDes) and (not app.typingDate): 
    #avoid showing '|' in every box simutaneously
        if app.amt == '|':
            app.amt = event.key
        elif (event.key.isdigit() or event.key == '.'): #consider decimals
            app.amt += event.key
        elif event.key == 'Delete':
            app.amt = app.amt[:-1]
    elif app.typingDes and (not app.typingAmt) and (not app.typingDate):
        if app.des == '|':
            app.des = event.key
        elif event.key == 'Delete':
            app.des = app.des[:-1]
        elif event.key == 'Space':
            app.des += ' '
        else:
            app.des += event.key


def enterRecordMode_mouseMoved(app, event):
    if clickOnSave(app, event.x, event.y):
        app.changeSaveButtonColor = True
    else:
        app.changeSaveButtonColor = False


def clickOnSave(app, x, y):
    return (app.width//2-35 <= x <= app.width//2+35 and app.height-190 <= y <= app.height-160)


def drawAllButtons(app, canvas): # expense or income
    color1, color2 = '', ''
    if app.enteringExpense: color1 = '#ced2db'
    else: color1 = '#fcfcfa'
    canvas.create_rectangle(app.width//2-80, 100, app.width//2, 130, fill=color1)
    canvas.create_text(app.width//2-40, 115, text='Expense', font='Galvji 14')
    if app.enteringIncome: color2 = '#eedbd5'
    else: color2 = '#fcfcfa'
    canvas.create_rectangle(app.width//2, 100, app.width//2+80, 130, fill=color2)
    canvas.create_text(app.width//2+40, 115, text='Income', font='Galvji 14')
    # "Save" button
    if app.changeSaveButtonColor: color3 = '#dfe0db'
    else: color3 = '#fcfcfa'
    canvas.create_rectangle(app.width//2-35, app.height-190, app.width//2+35, 
                            app.height-160, fill=color3, outline='#373737', width=1.5)
    canvas.create_text(app.width//2, app.height-175, text='Save', font='Galvji 15 bold', fill='#373737')


def drawInputBoxes(app, canvas):
    (dy, d) = (60, 30)
    title = ['Date:', 'Category:', 'Amount($):', 'Description:']
    content = [app.date, '', app.amt, app.des] #category is selected, not typed
    for i in range(4):
        canvas.create_rectangle(app.width//2-45, 160+(dy*i), app.width//2+145, 160+(dy*i)+d, fill='#fcfcfa')
        canvas.create_text(app.width//2-100, 160+(dy*i)+6, anchor='n', text=title[i], font='Galvji 15 bold', fill='#373737') #title
        if (app.date != '' or app.amt != ''or app.des != ''):
            canvas.create_text(app.width//2+50, 160+(dy*i)+(d/2), text=content[i], font='Galvji 14', fill='#373737') #typed text
    canvas.create_rectangle(app.width//2+120, 160+dy, app.width//2+145, 160+dy+d, fill='#f6edea')
    canvas.create_text(app.width//2+132.5, 160+dy+(d/2), text='v', font='Galvji 16', fill='#373737')
    if app.choosingCat: #show the options
        for i in range(len(app.categories)):
            canvas.create_rectangle(app.width//2-45, 160+(dy+d)+(22*i), 
                                    app.width//2+120, 160+(dy+d)+22*(i+1), fill='#f6edea')
            canvas.create_text(app.width//2+37.5, 160+(dy+d+22*(i+0.5)), text=app.categories[i], font='Galvji 13', fill='#373737')
    if app.chosenCat: #category is selected
        canvas.create_text(app.width//2+45, 160+dy+(d/2), text=app.category, font='Galvji 14', fill='#373737')


def enterRecordMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2, 32, text='New Expense', font='Courier 20 bold', fill='#fcfcfa')
    canvas.create_rectangle(0, 60, app.width, app.height-120, fill='#f8f8f4', outline='#9f6c59', width=1.5) #main background
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    drawInputBoxes(app, canvas)
    drawAllButtons(app, canvas)


################################################################
# Budget Mode
################################################################
def budgetMode__init__(app):
    app.showPlan = False
    app.allBudgets = [] #budgets (user's input)
    app.plannedBudgets = [] #items that the user can purchase (temp)
    app.warning = ''
    app.changeAddItemColor = False
    app.changePlanColor = False
    app.budgetShifting = False
    app.tempBudgetRecord = False #for scrolling 


def budgetMode_mousePressed(app, event):
    myFile = getJson(f'./{app.username}.json')
    app.budgetRecord = myFile.get('budgetRecord', {}) 
    if clickOnReturn(app, event.x, event.y):
        app.warning = ''
        app.showPlan = False
        app.mode = 'selectionScreenMode'
    if clickOnAddItem(app, event.x, event.y):
        app.rank, app.categ, app.descrip, app.amount = '', '', '', ''
        app.mode = 'enterBudgetMode'
    if clickOnPlan(app, event.x, event.y):
        if (app.yearMonth not in app.budgetRecord) and (app.yearMonth not in app.income):
            app.warning = 'Please make sure your budgets and\nincome for this month are entered.'
        elif app.yearMonth not in app.budgetRecord:
            app.warning = 'Please enter your budgets for this\nmonth before making a budget plan.'
        elif app.yearMonth not in app.income:
            app.warning = 'Please enter your income for this\nmonth before making a budget plan.'
        else:
            app.warning = ''
            getPlanInfo(app)
            if app.showPlan == True: app.showPlan = False
            else: app.showPlan = True
    app.budgetShifting = False


def budgetMode_mouseMoved(app, event):
    if (75 <= event.x <= app.width//2-75 and app.height-70 <= event.y <= app.height-40):
        app.changeAddItemColor = True
    else:
        app.changeAddItemColor = False
    if (app.width//2+75 <= event.x <= app.width-75 and app.height-70 <= event.y <= app.height-40):
        app.changePlanColor = True
    else:
        app.changePlanColor = False


def budgetMode_keyPressed(app, event):
    if (event.key == 'Up' or event.key == 'Down'): 
        app.budgetShifting = True
    entries = (app.height-190)//30 # dy = 30
    myFile = getJson(f'./{app.username}.json')
    budgetRecord = myFile['budgetRecord'][app.yearMonth] # 2D list
    curIndex = 0
    if len(budgetRecord) < entries: # display blank rectangles in this case
        app.tempBudgetRecord = budgetRecord + [['','','','']]*(entries-len(budgetRecord))
    else: 
        app.tempBudgetRecord = budgetRecord[curIndex:entries] # records that are available for display
    if (event.key == 'Down' and app.tempBudgetRecord[-1] != budgetRecord[-1]):
        app.tempBudgetRecord = budgetRecord[curIndex+1:entries+1]
    elif (event.key == 'Up' and app.tempBudgetRecord[0] != budgetRecord[0]):
        app.tempBudgetRecord = budgetRecord[curIndex-1:entries-1]


def getPlanInfo(app):
    app.allBudgets = app.budgetRecord[app.yearMonth] #2D list, including all budgets in that month
    app.plannedBudgets = [] #re-initialize
    needList, wantList, needAmt, wantAmt = [], [], [], []
    for item in app.allBudgets: #item = [rank(int), category, descrip, amount(str), n/w(str)]
        amount = item[3]
        if '.' in amount: amount = float(amount)
        else: amount = int(amount)
        if (item[4] == 'need'):
            needList.append(item)  #follows ranked order
            needAmt.append(amount) #collect "amount" in one list and send it to backtracking fn
        else:
            wantList.append(item)
            wantAmt.append(amount)
    #Start backtracking for needs
    result_N = allocateExpense(app, needAmt, 'need')
    #After result is returned, we take only the expenses we want.
    for item in needList:
        amount = item[3]
        if '.' in amount: amount = float(amount)
        else: amount = int(amount)
        if amount in result_N: 
            #item = [rank(int), category, descrip, amount(num)] each in string format
            app.plannedBudgets.append(item)
            #If two or more have the same amount, make sure the amount matches with the item(s) w higher priority.
            result_N.remove(amount)
    #Start backtracking for wants
    result_W = allocateExpense(app, wantAmt, 'want')
    for item in wantList:
        amount = item[3]
        if '.' in amount: amount = float(amount)
        else: amount = int(amount)
        if amount in result_W:
            app.plannedBudgets.append(item)
            result_W.remove(amount)
    app.plannedBudgets.sort()


#Backtracking: To include the max number of planned expenses with higher 
#priorities while following the 50/30/20 percent budgeting rule.
def allocateExpense(app, expenses, nw):
    # expenses = [100, 100, 100, 100, ...]
    myFile = getJson(f'./{app.username}.json')
    app.savePct = myFile['savePct']
    app.income = myFile['income']
    needRate, wantRate = (5/8)*(1-int(app.savePct)/100), (3/8)*(1-int(app.savePct)/100)
    needMax = int(app.income[app.yearMonth]) * needRate
    wantMax = int(app.income[app.yearMonth]) * wantRate
    if nw == 'need': maxValue = [needMax, 10**10] 
    else: maxValue = [wantMax, 10**10]           
    buckets = [[] for value in maxValue]
    return allocateExpenseHelper(expenses, maxValue, buckets)
    

def allocateExpenseHelper(expenses, maxValue, buckets):  
    if len(expenses) == 0:
        return buckets[0]
    else:
        for bucket in range(len(maxValue)): 
            expense = float(expenses[0])
            if (sum(buckets[bucket]) + expense) <= maxValue[bucket]:
                buckets[bucket].append(expense)
                expenses.pop(0)
                result = allocateExpenseHelper(expenses, maxValue, buckets)
                if result != None:
                    return result
                expenses.append(expense)
                buckets[bucket].pop() #remove unfit expense from bucket 
        return None






#Compare the lists in the plan and the system's plan
def drawPlan(app, canvas): # the budgeting plan
    (y0, dy) = (86, 30)
    entries = (app.height-190)//dy - 1
    myFile = getJson(f'./{app.username}.json')
    budgetRecord = myFile.get('budgetRecord', {})
    budgetRecord[app.yearMonth].sort()
    if app.yearMonth in budgetRecord:
        curBudgets = budgetRecord[app.yearMonth] #budgets in current month
    else:
        curBudgets = []              #If there is no budget for this month yet,
    if len(curBudgets) < entries:    #display blank rectangles in this case.
        tempBudgets = curBudgets + [['','','','','']]*(entries-len(curBudgets))
    else:
        tempBudgets = curBudgets
    for i in range(entries):
        (x0, dx) = (31, 0)
        if tempBudgets[i] in app.plannedBudgets: #if the user should purchase it
            canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#df856f', outline='#fcfcfa')
            for j in range(5): #=app.tempBudgets[i] = [rank0, cat1, des2, amt3, n/w4]
                canvas.create_text(x0+dx, y0+(dy/2), text=tempBudgets[i][j], font='Galvji 12 bold', fill='#fcfcfa')
                if (j == 1): dx += 120
                elif (j == 2): dx += 105
                elif (j == 0): dx += 75
                else: dx += 60
        else:
            canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#f8f8f4')
            for j in range(5):
                canvas.create_text(x0+dx, y0+(dy/2), text=tempBudgets[i][j], font='Galvji 12', fill='#373737')
                if (j == 1): dx += 120
                elif (j == 2): dx += 105
                elif (j == 0): dx += 75
                else: dx += 60
        y0 += dy


def drawBudgetTitle(app, canvas):
    #display year and month in title
    if app.showPlan:
        canvas.create_text(app.width//2, 34, text=f'Items to Purchase in {app.yearMonth}', font='Courier 19 bold', fill='#fcfcfa')
    else:
        canvas.create_text(app.width//2, 34, text=f'Budget Plan for {app.yearMonth}', font='Courier 19 bold', fill='#fcfcfa')
    canvas.create_rectangle(0, 60, app.width, 86, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    (x0, dx) = (31, 0)
    for title in ['Rank', 'Category', 'Description', '$', 'N/W']:
        canvas.create_text(x0+dx, 73, text=title, font='Galvji 13 bold', fill='#373737')
        if (title == 'Category'): dx += 120
        elif (title == 'Description'): dx += 105
        elif (title == 'Rank'): dx += 75
        else: dx += 60


def drawBudgets(app, canvas):
    (y0, dy) = (86, 30)
    entries = (app.height-190)//dy - 1
    # refresh data after user enters new data
    myFile = getJson(f'./{app.username}.json')
    budgetRecord = myFile.get('budgetRecord', {})
    if app.yearMonth in budgetRecord:
        budgetRecord[app.yearMonth].sort()
        curBudgets = budgetRecord[app.yearMonth] # budgets in current month
    else:
        curBudgets = [] # if there is no budget for this month yet.
    if len(curBudgets) < entries: # display blank rectangles in this case
        tempBudgets = curBudgets + [['','','','','']]*(entries-len(curBudgets))
    else:
        tempBudgets = curBudgets
    if app.scrolling:
        tempBudgets = app.tempBudgetRecord
    for i in range(entries):
        canvas.create_rectangle(0, y0, app.width, y0+dy, fill='#f8f8f4')
        (x0, dx) = (31, 0)
        for j in range(5): # = app.tempBudgets[i] = [rank0, cat1, des2, amt3, n/w4]
            canvas.create_text(x0+dx, y0+(dy/2), text=tempBudgets[i][j], font='Galvji 12', fill='#373737')
            if (j == 1): dx += 120
            elif (j == 2): dx += 105
            elif (j == 0): dx += 75
            else: dx += 60
        y0 += dy


def clickOnAddItem(app, x, y):
    (app.rank, app.categ, app.descrip, app.amount) = ('', '', '', '')
    app.warning = ''
    if ((75 <= x <= app.width//2-75) and (app.height-77 <= y <= app.height-47)):
        app.mode = 'enterBudgetMode'

def clickOnPlan(app, x, y):
    return ((app.width//2+75 <= x <= app.width-75) and (app.height-77 <= y <= app.height-47))


def drawButtons(app, canvas):
    #add item button
    if app.changeAddItemColor: color1 = '#dfe0db'
    else: color1 = '#fcfcfa'
    canvas.create_rectangle(80, app.height-77, app.width//2-70, app.height-47, fill=color1, width=1.5, outline='#373737')
    canvas.create_text(80+(app.width//2-70-80)//2, app.height-62, text='+ Item', fill='#373737', font='Galvji 16 bold')
    #make plan button
    if app.changePlanColor: color2 = '#dfe0db'
    else: color2 = '#fcfcfa'
    canvas.create_rectangle(app.width//2+70, app.height-77, app.width-80, app.height-47, fill=color2, width=1.5, outline='#373737')
    canvas.create_text(app.width//2+70+((app.width-80-app.width//2-70)//2), app.height-62, 
                       text='Plan', fill='#373737', font='Galvji 16 bold')


def drawWarning(app, canvas): #drawn above the "make plan" button
    canvas.create_text(app.width//2+90, app.height-97, text=app.warning, font='Galvji 12', fill='red')


def budgetMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_image(app.width-40, app.height-42, image=ImageTk.PhotoImage(app.trashScaled))
    drawButtons(app, canvas)
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    if (app.warning != ''):
        drawWarning(app, canvas)
    else: 
        drawBudgets(app, canvas)
    drawBudgetTitle(app, canvas)
    if app.showPlan: drawPlan(app, canvas)



################################################################
# Enter Budget Mode (enter from the Make Plans mode)
################################################################
def enterBudgetMode__init__(app):
    (app.rank, app.categ, app.descrip, app.amount) = ('', '', '', '') # entered user input
    app.enteringNeed, app.enteringWant = False, False
    app.rankTyping, app.amtTyping, app.desTyping = False, False, False
    app.catChosen, app.catChoosing = False, False
    app.reminder = ''
    app.changeSaveColor = False # mouse detection

def chooseCategory(app, x, y): # check if user starts choosing categories
    (dy, d) = (60, 30)
    for i in range(len(app.categories)):
        if (app.width//2-45 <= x <= app.width//2+120 and 160+(dy+d)+(22*i) <= y <= 160+(dy+d)+22*(i+1)):
            app.categ = app.categories[i]
            app.catChoosing = False  # make the options disappear
            app.catChosen = True
            app.rankTyping = app.desTyping = app.amtTyping = False 


def enterBudgetMode_mouseMoved(app, event):
    if clickOnSave(app, event.x, event.y):
        app.changeSaveColor = True
    else:
        app.changeSaveColor = False

def enterBudgetMode_mousePressed(app, event):    
    if clickOnReturn(app, event.x, event.y):
        app.mode = 'budgetMode'
    enterNeedOrWant(app, event.x, event.y)
    enterBudget(app, event.x, event.y) # check if the user clicks on any of the input boxes
    if app.catChoosing: # check which category is chosen
        chooseCategory(app, event.x, event.y)
    if (app.rankTyping and not app.amtTyping and not app.desTyping):
        if app.rank == '': app.rank = '|'
    elif (app.amtTyping and not app.rankTyping and not app.desTyping):
        if app.amount == '': app.amount = '|'
    elif (app.desTyping and not app.amtTyping and not app.rankTyping):
        if app.descrip == '': app.descrip = '|'
    # after all input boxes are filled
    if clickOnSave(app, event.x, event.y):
        if (app.catChosen == False or app.rank == '' or app.descrip == '' or app.amount == ''):
            app.reminder = 'Please make sure all fields are filled in.'
        else:
            app.catChosen = False
            app.reminder = '' # set it back to blank
            if app.enteringNeed:
                storeBudgetData(app, app.categ, app.amount, 'need') # purpose: calculate/analyze
                storeBudgetRecord(app, app.rank, app.categ, app.descrip, app.amount, 'need') # purpose: display/modify
            elif app.enteringWant:
                storeBudgetData(app, app.categ, app.amount, 'want')
                storeBudgetRecord(app, app.rank, app.categ, app.descrip, app.amount, 'want') 
            else: 
                app.reminder = 'Please choose either "need" or "want".'
            for yearMonth in app.budgetRecord:       # sort in the order of ranking
                app.budgetRecord[yearMonth].sort()   # follows the order of priorities
            app.mode = 'budgetMode' # return to previous page
            

def enterBudgetMode_keyPressed(app, event):
    if app.rankTyping and (not app.desTyping) and (not app.amtTyping):
        if app.rank == '|':
            app.rank = event.key 
        elif event.key.isdigit():
            app.rank += event.key 
        elif event.key == 'Delete':
            app.rank = app.rank[:-1]
    elif app.amtTyping and (not app.desTyping) and (not app.rankTyping): 
    # avoid showing '|' in every box simutaneously
        if app.amount == '|':
            app.amount = event.key
        elif (event.key.isdigit() or event.key == '.'): # consider decimals
            app.amount += event.key
        elif event.key == 'Delete':
            app.amount = app.amount[:-1]
    elif app.desTyping and (not app.amtTyping) and (not app.rankTyping):
        if app.descrip == '|':
            app.descrip = event.key
        elif event.key == 'Delete':
            app.descrip = app.descrip[:-1]
        elif event.key == 'Space':
            app.descrip += ' '
        elif len(event.key) == 1:
            app.descrip += event.key


def enterBudget(app, x, y):
    (dy, d) = (60, 30)
    if (app.width//2+120 <= x <= app.width//2+145 and 160+dy <= y <= 160+dy+d):
        if app.catChoosing == False: app.catChoosing = True
        else: app.catChoosing = False
    elif (app.width//2-45 <= x <= app.width//2+145):
        if  (160 <= y <= 160+d):
            app.rankTyping = True
            app.amtTyping, app.desTyping = False, False
        elif  (160+(dy*2) <= y <= 160+(dy*2)+d):
            app.amtTyping = True
            app.rankTyping, app.desTyping = False, False
        elif  (160+(dy*3) <= y <= 160+(dy*3)+d):
            app.desTyping = True
            app.amtTyping, app.rankTyping = False, False


def enterNeedOrWant(app, x, y): # detect clicking on need/want
    if (app.width//2-80 <= x <= app.width//2 and 100 <= y <= 130):
        app.enteringNeed = True
        app.enteringWant = False
    elif (app.width//2 <= x <= app.width+80 and 100 <= y <= 130):
        app.enteringWant = True
        app.enteringNeed = False
        

def storeBudgetRecord(app, rank, category, description, amount, nw):
    #store expenses as a list of data: [rank, category, description, amount]
    #for the purpose of display
    curYearMonth = app.date.split('/')[0] + '/' + app.date.split('/')[1]
    rank = int(rank) # for the purpose of sorting
    if curYearMonth in app.data['budgetRecord']:
        app.data['budgetRecord'][curYearMonth].append([rank, category, description, amount, nw])
    else:
        app.data['budgetRecord'][curYearMonth] = [[rank, category, description, amount, nw]]
    writeToJsonFile('./', app.username, app.data)



def storeBudgetData(app, category, amount, nw): 
#app.data['budgets'] -> { '2021/5': {'category1': [ ['need', amount], ['need', amount] ], 
#                                    'category2': [ ['want', amount], ['need', amount] ]} 
#                         '2021/6': {'category1': [ ['need', amount] ], 
#                                    'category2': [ ['want', amount] ]}  }
    yearMonth = app.date.split('/')[0] + '/' + app.date.split('/')[1] # date is automatically set to Today's year/month
    if ('.' in amount): amount = float(amount)
    else: amount = int(amount)
    # add amount to the dictionary
    if nw == 'need':
        if (yearMonth in app.data['budgets']):
            if category in app.data['budgets'][yearMonth]:
                app.data['budgets'][yearMonth][category].append(['need', amount])
            else:
                app.data['budgets'][yearMonth][category] = [['need', amount]]
        else:
            app.data['budgets'][yearMonth] = {}
    elif nw == 'want':
        if (yearMonth in app.data['budgets']): 
            if (category in app.data['budgets'][yearMonth]): # category is dict key
                app.data['budgets'][yearMonth][category].append(['want', amount])
            else:
                app.data['budgets'][yearMonth][category] = [['want', amount]]
        else:
            app.data['budgets'][yearMonth] = {}
    # store the added data to json file
    writeToJsonFile('./', app.username, app.data)


def clickOnSave(app, x, y):
    return (app.width//2-35 <= x <= app.width//2+35 and app.height-190 <= y <= app.height-160)

def drawNWButtons(app, canvas): #need/want
    color1, color2 = '', ''
    if app.enteringNeed: color1 = '#ced2db'
    else: color1 = '#fcfcfa'
    canvas.create_rectangle(app.width//2-80, 100, app.width//2, 130, fill=color1)
    canvas.create_text(app.width//2-40, 115, text='Need', font='Galvji 14')
    if app.enteringWant: color2 = '#eedbd5'
    else: color2 = '#fcfcfa'
    canvas.create_rectangle(app.width//2, 100, app.width//2+80, 130, fill=color2)
    canvas.create_text(app.width//2+40, 115, text='Want', font='Galvji 14')
    # "Save" button
    if app.changeSaveColor: color3 = '#dfe0db'
    else: color3 = '#fcfcfa'
    canvas.create_rectangle(app.width//2-35, app.height-190, app.width//2+35, 
                            app.height-160, fill=color3, outline='#373737', width=1.5)
    canvas.create_text(app.width//2, app.height-175, text='Save', font='Galvji 15 bold', fill='#373737')
    #app.reminder drawn if some fields are not filled in by the user
    if app.reminder != '':
        canvas.create_text(app.width//2, app.height-200, text=app.reminder, font='Galvji 13', fill='red')


def drawEnterBoxes(app, canvas):
    (dy, d) = (60, 30)
    title = ['Rank:', 'Category:', 'Amount($):', 'Description:']
    content = [app.rank, '', app.amount, app.descrip] #category & nw are selected, not typed
    for i in range(4):
        canvas.create_rectangle(app.width//2-45, 160+(dy*i), app.width//2+145, 160+(dy*i)+d, fill='#fcfcfa')
        canvas.create_text(app.width//2-100, 160+(dy*i)+6, anchor='n', text=title[i], font='Galvji 15 bold', fill='#373737') #title
        if (app.rank != '' or app.descrip != ''or app.amount != ''):
            canvas.create_text(app.width//2+50, 160+(dy*i)+(d/2), text=content[i], font='Galvji 14', fill='#373737') #typed text
    canvas.create_rectangle(app.width//2+120, 160+dy, app.width//2+145, 160+dy+d, fill='#f6edea')
    canvas.create_text(app.width//2+132.5, 160+dy+(d/2), text='v', font='Galvji 16', fill='#373737')
    if app.catChoosing: #show the options
        for i in range(len(app.categories)):
            canvas.create_rectangle(app.width//2-45, 160+(dy+d)+(22*i), 
                                    app.width//2+120, 160+(dy+d)+22*(i+1), fill='#f6edea')
            canvas.create_text(app.width//2+37.5, 160+(dy+d+22*(i+0.5)), text=app.categories[i], font='Galvji 13', fill='#373737')
    if app.catChosen: #category is selected
        canvas.create_text(app.width//2+45, 160+dy+(d/2), text=app.categ, font='Galvji 14', fill='#373737')


def enterBudgetMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2, 32, text='New Budget', font='Courier 20 bold', fill='#fcfcfa')
    canvas.create_rectangle(0, 60, app.width, app.height-120, fill='#f8f8f4', outline='#9f6c59', width=1.5) #background
    drawEnterBoxes(app, canvas)
    drawNWButtons(app, canvas)
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)


################################################################
# Analysis Mode (charts)
################################################################
def analysisMode__init__(app):
    app.clickOnMonth = False
    app.clickOnYearMonth = False
    app.graphInfo = {'GraphType':'', 'Classification':'', 'Year':'', 'Month':''}
    app.typingYear1, app.typingYear2, app.typingMonth = False, False, False
    app.notAllFilled = False


def getPieData_C(app, year, month):
    myFile = getJson(f'./{app.username}.json')
    (labels, slices) = ([], [])
    for category in app.categories:
        total = 0
        for yearMonth in myFile['expenses']:
            if (month != ''): # if only observes a specific month
                if (category in myFile['expenses'][f'{year}/{month}'] and myFile['expenses'][f'{year}/{month}'][category] != 0):
                    labels.append(category)
                    total += myFile['expenses'][yearMonth][category]
            else: # if observes a whole year
                if (yearMonth[:4] == year): # if the month is in the year chosen
                    if (category in myFile['expenses'][yearMonth] and myFile['expenses'][yearMonth][category] != 0):
                        labels.append(category)
                        total += myFile['expenses'][yearMonth][category]
        if (total != 0): # only add if the category is chosen by the user before
            slices.append(total)
    return (labels, slices)


def drawPieCharts_C(app, year, month):
    labels, slices = getPieData_C(app, year, month)
    plt.style.use('fivethirtyeight')
    if month == '':
        plt.title(f'Expenses by Categories in {year}', fontsize=16)
    else:
        plt.title(f'Expenses by Categories in {year}/{month}', fontsize=16)
    plt.tight_layout()
    # we need to add a long list of color values (and do slicing)
    # colors = ['black', 'green']
    # loc values -> ‘upper left’, ‘upper right’, ‘lower left’, ‘lower right’
    plt.pie(slices, shadow=True, startangle=90, autopct='%1.1f%%', 
            wedgeprops={'edgecolor': 'white', 'linewidth': 0.7}, 
            textprops={'fontsize': 12})
    plt.legend(labels, loc = "lower right", edgecolor='grey', fontsize=10)
    plt.show()


def getGraphData_M(app, year):
    myFile = getJson(f'./{app.username}.json')
    expenses_y, income_y = [], []
    avg_expense, avg_income = 0, 0
    months_ex, months_in = 0, 0 #number of months with user input
    #expense
    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        if (f'{year}/{month}') in myFile['expenses']:
            total = 0
            months_ex += 1
            for category in myFile['expenses'][f'{year}/{month}']:
                total += myFile['expenses'][f'{year}/{month}'][category]
            expenses_y.append(total)
        else:
            expenses_y.append(0)
    #income
    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        if (f'{year}/{month}') in myFile['income']:
            months_in += 1
            total = myFile['income'][f'{year}/{month}']
            income_y.append(total)
        else:
            income_y.append(0)
    if months_ex != 0:
        avg_expense = [sum(expenses_y)/months_ex]*12
    else:
        avg_expense = [0]*12 #no data entered
    if months_in != 0:
        avg_income = [sum(income_y)/months_in]*12
    else:
        avg_income = [0]*12 #no data entered
    return (expenses_y, income_y, avg_expense, avg_income)


def drawBarGraphs_M(app, year):
    months_x = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    expenses_y, income_y, avg_expense, avg_income = getGraphData_M(app, year)
    x_indexes = np.arange(len(months_x))
    width = 0.4
    plt.figure(figsize=(6,5)) #plot size
    plt.style.use("fivethirtyeight")
    plt.rc('font', size=9) 
    #bar shows raw amount
    plt.bar(x_indexes-width/2, expenses_y, width=width, color="#494949", label="Expense")
    plt.bar(x_indexes+width/2, income_y, width=width, color="#ce8e73", label="Income")
    #line shows the average amount
    plt.plot(x_indexes, avg_expense, color="#8e8192", label="Average Expense")
    plt.plot(x_indexes, avg_income, color="#6c8cd8", label="Average Income")
    
    plt.legend(prop={"size":10})
    plt.xticks(ticks=x_indexes, labels=months_x)
    plt.title(f'Monthly Expense and Income in {year}')
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Expense and Income (USD)", fontsize=12)
    plt.tight_layout()
    plt.show()


def getGraphData_C(app, year, month):
    myFile = getJson(f'./{app.username}.json')
    (category_x, amount_y) = ([], [])
    if (month == ''): #if observes data in a whole year
        for category in app.categories:
            total = 0
            for yearMonth in myFile['expenses']:
                if (yearMonth[:4] == year) and (category in myFile['expenses'][yearMonth]) and (myFile['expenses'][yearMonth][category] != 0):
                    if category not in category_x:
                        category_x.append(category)
                        total += myFile['expenses'][yearMonth][category]
                    else:
                        total += myFile['expenses'][yearMonth][category]
            if (total != 0):
                amount_y.append(total)
    else: #if observes data in a specific month
        for category in app.categories:
            total = 0
            if (category in myFile['expenses'][f'{year}/{month}']) and (myFile['expenses'][f'{year}/{month}'][category] != 0):
                if category not in category_x:
                    category_x.append(category)
                    total += myFile['expenses'][f'{year}/{month}'][category]
                else:
                    total += myFile['expenses'][f'{year}/{month}'][category]
            if (total != 0):
                amount_y.append(total)
    return (category_x, amount_y)


def drawBarGraphs_C(app, year, month):
    (category_x, amount_y) = getGraphData_C(app, year, month)
    x_indexes = np.arange(len(category_x))
    plt.figure(figsize=(6,5)) #plot size
    plt.style.use("fivethirtyeight")
    plt.rc('font', size=9)
    #bar shows raw amount
    plt.bar(x_indexes, amount_y, width=0.8, color="#494949", label="Expense")
    plt.legend(prop={"size":10})
    plt.xticks(ticks=x_indexes, labels=category_x)
    if (month !=  ''):
        plt.title(f'Expenses by Categories in {year}/{month}')
    else:
        plt.title(f'Expenses by Categories in {year}')
    plt.xlabel("Category", fontsize=12)
    plt.ylabel("Categorized Expense (USD)", fontsize=12)
    plt.tight_layout()
    plt.show()


def analysisMode_mousePressed(app, event):
    if clickOnReturn(app, event.x, event.y):
        app.notAllFilled = False
        app.mode = 'selectionScreenMode'
    defineUserChoices(app, event.x, event.y)
    #click on Clear
    if (app.width//2+40 <= event.x <= app.width//2+116 and app.height-215 <= event.y <= app.height-185):
        app.graphInfo = {'GraphType':'', 'Classification':'', 'Year':'', 'Month':''}
    #click on Produce Graph
    if (app.width//2-116 <= event.x <= app.width//2+10 and app.height-215 <= event.y <= app.height-185):
        if (app.graphInfo['GraphType'] == '' or app.graphInfo['Classification'] == '' or app.graphInfo['Year'] == ''):
            app.notAllFilled = True
        else:
            app.notAllFilled = False
            if app.graphInfo['GraphType'] == 'Bar':
                if app.graphInfo['Classification'] == 'By Month':
                    drawBarGraphs_M(app, app.graphInfo['Year'])
                elif app.graphInfo['Classification'] == 'By Category':
                    if (app.graphInfo['Month'] != '' and app.graphInfo['Month'][0] == '0'): 
                        app.graphInfo['Month'] = app.graphInfo['Month'][1] #get rid of the 0
                    drawBarGraphs_C(app, app.graphInfo['Year'], app.graphInfo['Month'])
            elif app.graphInfo['GraphType'] == 'Pie':
                if app.graphInfo['Classification'] == 'By Category':
                    if (app.graphInfo['Month'] != '' and app.graphInfo['Month'][0] == '0'): 
                        app.graphInfo['Month'] = app.graphInfo['Month'][1] #get rid of the 0
                    drawPieCharts_C(app, app.graphInfo['Year'], app.graphInfo['Month'])


def analysisMode_keyPressed(app, event):
    if app.typingYear1:
        if (app.graphInfo['Year'] == '|') and event.key.isdigit():
            app.graphInfo['Year'] = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.graphInfo['Year'] += event.key
        elif event.key == 'Delete':
            app.graphInfo['Year'] = app.graphInfo['Year'][:-1]
    elif app.typingMonth:
        if (app.graphInfo['Month'] == '|') and event.key.isdigit():
            app.graphInfo['Month'] = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.graphInfo['Month'] += event.key
        elif event.key == 'Delete':
            app.graphInfo['Month'] = app.graphInfo['Month'][:-1]
    elif app.typingYear2:
        if (app.graphInfo['Year'] == '|') and event.key.isdigit():
            app.graphInfo['Year'] = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.graphInfo['Year'] += event.key
        elif event.key == 'Delete':
            app.graphInfo['Year'] = app.graphInfo['Year'][:-1]
        app.graphInfo['Month'] = '' #make sure no month is entered in this case


def defineUserChoices(app, x, y):
    #check graph type
    if (140 <= y <= 170):
        if (app.width//2-105 <= x <= app.width//2-15):
            app.graphInfo['GraphType'] = 'Bar'
        elif (app.width//2+15 <= x <= app.height//2+105):  
            app.graphInfo['GraphType'] = 'Pie'
    #check classification
    elif (255 <= y <= 285):
        if (app.width//2-105 <= x <= app.width//2-15):
            app.graphInfo['Classification'] = 'By Category'
        elif (app.width//2+15 <= x <= app.height//2+105):
            app.graphInfo['Classification'] = 'By Month'
    #check time period
    elif (370 <= y <= 400):
        if (app.width//2-110 <= x <= app.width//2-62):
            if app.graphInfo['Month'] == '|':
                app.graphInfo['Month'] = ''
            app.typingYear1 = True
            app.graphInfo['Year'] = '|'
            app.typingYear2, app.typingMonth = False, False
        elif (app.width//2-48 <= x <= app.width//2-10):
            if app.graphInfo['Year'] == '|':
                app.graphInfo['Year'] = ''
            app.typingMonth = True
            app.graphInfo['Month'] = '|'
            app.typingYear2, app.typingYear1 = False, False
        elif (app.width//2+36 <= x <= app.width//2+84): 
            app.graphInfo['Month'] = ''
            app.typingYear2 = True
            app.graphInfo['Year'] = '|'
            app.typingMonth, app.typingYear1 = False, False


def drawGraphingChoices(app, canvas):
    #background
    canvas.create_rectangle(0, 60, app.width, app.height-160, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    #graph types
    if app.graphInfo['GraphType'] == 'Bar':
        (color1, color2) = ('#dfe0db', '#fcfcfa')
    elif app.graphInfo['GraphType'] == 'Pie':
        (color1, color2) = ('#fcfcfa', '#dfe0db')
    else: (color1, color2) = ('#fcfcfa', '#fcfcfa')
    canvas.create_rectangle(0, 85, app.width, 125, fill='#e9e2d8', outline='#9f6c59', width=1.5) #graph type box
    canvas.create_text(app.width//2, 105, text='Graph Type', font='Galvji 15 bold', fill='#373737')
    canvas.create_rectangle(app.width//2-105, 140, app.width//2-15, 170, fill=color1)
    canvas.create_text(app.width//2-60, 155, text='Bar Chart', font='Galvji 14', fill='#373737')
    canvas.create_rectangle(app.width//2+15, 140, app.width//2+105, 170, fill=color2)
    canvas.create_text(app.width//2+60, 155, text='Pie Chart', font='Galvji 14', fill='#373737')
    
    #classification
    if app.graphInfo['Classification'] == 'By Category':
        (color3, color4) = ('#dfe0db', '#fcfcfa')
    elif app.graphInfo['Classification'] == 'By Month':
        (color3, color4) = ('#fcfcfa', '#dfe0db')
    else: (color3, color4) = ('#fcfcfa', '#fcfcfa')
    canvas.create_rectangle(0, 200, app.width, 240, fill='#e9e2d8', outline='#9f6c59', width=1.5) #classification box
    canvas.create_text(app.width//2, 220, text='Classification', font='Galvji 15 bold', fill='#373737')
    canvas.create_rectangle(app.width//2-105, 255, app.width//2-15, 285, fill=color3)
    canvas.create_text(app.width//2-60, 270, text='By Category', font='Galvji 14', fill='#373737')
    canvas.create_rectangle(app.width//2+15, 255, app.width//2+105, 285, fill=color4)
    canvas.create_text(app.width//2+60, 270, text='By Month', font='Galvji 14', fill='#373737')

    #time period
    canvas.create_rectangle(0, 315, app.width, 355, fill='#e9e2d8', outline='#9f6c59', width=1.5) #time period box
    canvas.create_text(app.width//2, 335, text='Time Period', font='Galvji 15 bold', fill='#373737')
    canvas.create_rectangle(app.width//2-110, 370, app.width//2-62, 400, fill='#fcfcfa')
    canvas.create_text(app.width//2-55, 385, text='/', font='Galvji 16', fill='#373737')
    canvas.create_rectangle(app.width//2-48, 370, app.width//2-10, 400, fill='#fcfcfa')
    canvas.create_rectangle(app.width//2+36, 370, app.width//2+84, 400, fill='#fcfcfa')

    if (app.typingYear2 or app.graphInfo['Year'] == ''):
        canvas.create_text(app.width//2-86, 385, text='YY', font='Galvji 14', fill='#bebebe')
    else:
        canvas.create_text(app.width//2-86, 385, text=app.graphInfo['Year'], font='Galvji 14', fill='#373737')
    if (app.typingYear2 or app.graphInfo['Month'] == ''):
        canvas.create_text(app.width//2-29, 385, text='MM', font='Galvji 14', fill='#bebebe')
    else: 
        canvas.create_text(app.width//2-29, 385, text=app.graphInfo['Month'], font='Galvji 14', fill='#373737')
    if (app.typingYear1 or app.typingMonth or app.graphInfo['Year'] == ''):
        canvas.create_text(app.width//2+60, 385, text='YY', font='Galvji 14', fill='#bebebe')
    elif app.typingYear2:
        canvas.create_text(app.width//2+60, 385, text=app.graphInfo['Year'], font='Galvji 14', fill='#373737')


def drawGraphButtons(app, canvas):
    #produce graph
    canvas.create_rectangle(app.width//2-116, app.height-215, app.width//2+10, app.height-185, width=1.5, fill='#fcfcfa')
    canvas.create_text(app.width//2-53, app.height-200, text='Produce Graph', font='Galvji 14 bold', fill='#373737')
    #clear
    canvas.create_rectangle(app.width//2+40, app.height-215, app.width//2+116, app.height-185, width=1.5, fill='#fcfcfa')
    canvas.create_text(app.width//2+78, app.height-200, text='Clear All', font='Galvji 14 bold', fill='#373737')
    #warning message
    if app.notAllFilled:
        canvas.create_text(app.width//2, app.height-235, text='Please make sure all fields above are filled in.', 
                           font='Galvji 12', fill='red')


def analysisMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2, 32, text='Graph Analysis', font='Courier 20 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas)
    drawBottomBorder(app, canvas)
    drawGraphingChoices(app, canvas)
    drawGraphButtons(app, canvas)


################################################################
# Rating Mode
################################################################
def ratingMode__init__(app):
    app.ratio_ExIn = 0 # ratio of expense/income
    app.rating = 0 # score of 0-5
    app.goodList, app.badList = [], [] # a list of good/bad reasons for the rating result
    app.showScore = False
    app.totalIncome, app.totalExpense = 0, 0
    app.year_r, app.month_r, app.year_r2 = '', '', ''
    app.typingYear_r, app.typingMonth_r = False, False
    app.typingYear_r2 = False
    app.matched= {} # expenses which match with budgets
    app.avgSpending = {}  # average spending of each main category (in the US)
    app.reminder_r = '' # shows up when user hasn't planned budgets.


def storeRatings(app, year, month): # {'2021': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    myFile = getJson(f'./{app.username}.json')
    app.ratingRecord = myFile['ratingRecord']
    currentYear = app.today.split('/')[0]
    if int(year) <= int(currentYear):
        if (year not in app.ratingRecord):
            app.ratingRecord[year] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        index = int(month)-1
        app.ratingRecord[year][index] = app.rating
        app.data['ratingRecord'] = app.ratingRecord
        writeToJsonFile('./', app.username, app.data)


def drawRatingDistribution(app, year):
    #prevent situations which user didn't get rating before seeing distribution
    currentYear = app.today.split('/')[0]
    if int(year) <= int(currentYear):
        if year not in app.ratingRecord:
            app.ratingRecord[year] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            app.data['ratingRecord'] = app.ratingRecord
            writeToJsonFile('./', app.username, app.data)
        x_val = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        y_val = app.ratingRecord[year] # a list
        plt.xlabel('Month')
        plt.ylabel('Rating')
        plt.plot(x_val, y_val)
        plt.title(f'Rating Distribution in {year}')
        plt.show()
    #User cannot check ratings data for years in the future.



#CITATION: I got the national income & expense data from the U.S. Bureau of Labor Statistics
#https://beta.bls.gov/dataViewer/view/timeseries/CXUTOTALEXPLB0101M (avg total spending) and
#https://beta.bls.gov/dataViewer/view/timeseries/CES0500000012 (average income)
def getData_ExIn(app):
    ##### average monthly income
    result1 = requests.get('https://beta.bls.gov/dataViewer/view/timeseries/CES0500000012')
    src1 = result1.content
    soup1 = BeautifulSoup(src1, 'html.parser')
    years, values = [], []
    for tr_class in soup1.find_all('tr'): # loop through three rows in the table
        for td_class in tr_class.find_all('td', class_='year'): # loop through class=year td-tag content
            years.append(td_class.get_text())
        for td_class2 in tr_class.find_all('td', class_=None): # loop through class=None td-tag content
            td_class2 = td_class2.get_text()
            if '\n' in td_class2: # '\n' is in the string we want to extract
                values.append(td_class2[2:8])
    # make a dictionary-> {year: annual value}
    tmp_income = {}
    for i in range(len(years)): # len(years) = len(values)
        if years[i] not in tmp_income:
            tmp_income[years[i]] = float(values[i])*4 # turn weekly to monthly
        else: 
            tmp_income[years[i]] += float(values[i])*4
    # turn annual data to monthly data-> monthly average income
    total1 = 0
    for year in tmp_income:
        tmp_income[year] /= years.count(year)
        total1 += tmp_income[year]
    avg_income = total1/len(tmp_income)

    ##### average monthly expense
    result2 = requests.get('https://beta.bls.gov/dataViewer/view/timeseries/CXUTOTALEXPLB0101M')
    src2 = result2.content
    soup2 = BeautifulSoup(src2, 'html.parser')
    tmp_expenses, avg_expenses = [], []
    for tr_class in soup2.find_all('tr'): # loop through three rows in the table
        for td_class in tr_class.find_all('td', class_=None): # loop through class=None td-tag content
            td_class = td_class.get_text()
            if '\n' in td_class: # '\n' is in the string we want to extract
                tmp_expenses.append(td_class[2:7])
    # turn to monthly data-> monthly average expense
    total2 = 0
    for value in tmp_expenses:
        total2 += int(value)/12
    avg_expense = total2/len(tmp_expenses) # ANS
    app.ratio_ExIn = avg_expense/avg_income


def clickOnYearOrMonth(app, x, y):
    if (102.5 <= x <= 157.5) and (77 <= y <= 103):
        app.typingYear_r = True
        app.typingMonth_r = False
        if app.year_r == '':
            app.year_r = '|'
        if app.month_r == '|':
            app.month_r = ''
    elif (172.5 <= x <= 212.5) and (77 <= y <= 103):
        app.typingMonth_r = True
        app.typingYear_r = False
        if app.month_r == '':
            app.month_r = '|'
        if app.year_r == '|':
            app.year_r = ''
    elif (app.width//2+22 <= x <= app.width//2+78) and (app.height-93 <= y <= app.height-67):
        app.typingYear_r2 = True
        app.typingYear_r, app.typingMonth_r = False, False
        if app.year_r2 == '':
            app.year_r2 = '|'
        if app.year_r == '|':
            app.year_r = ''
        if app.month_r == '|':
            app.month_r = ''


def ratingMode_mousePressed(app, event):
    clickOnYearOrMonth(app, event.x, event.y) #detect if click on year or month entry box
    if clickOnReturn(app, event.x, event.y):
        app.year_r, app.month_r, app.year_r2, app.reminder_r = '', '', '', ''
        app.mode = 'selectionScreenMode'
    elif (app.width-127 <= event.x <= app.width-38) and (77 <= event.y <= 103): # click on get rating
        app.rating = 0 #re-initialize
        app.goodList, app.badList = [], [] #re-initialize
        if app.plannedBudgets == []:
            app.reminder_r = 'Please plan your budgets before geting\n   rating for your spending record.'
        elif (app.year_r != '' and app.month_r != ''):
            app.reminder_r = ''
            compareExInRatio(app)
            compareCatBudgetPct(app)
            checkBudgetMatches(app)
            app.showScore = True
            storeRatings(app, app.year_r, app.month_r) #store score in dict
    elif (app.width-113 <= event.x <= app.width-52) and (122 <= event.y <= 148): #click on clear
        app.year_r, app.month_r, app.year_r2 = '', '', ''
    #click on enter to see score distibution
    elif (app.width-80 <= event.x <= app.width-25) and (app.height-93 <= event.y <= app.height-78):
        drawRatingDistribution(app, app.year_r2)



def ratingMode_keyPressed(app, event):
    if app.typingYear_r:
        if (app.year_r == '|') and event.key.isdigit():
            app.year_r = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.year_r += event.key
        elif event.key == 'Delete':
            app.year_r = app.year_r[:-1]
    elif app.typingMonth_r:
        if (app.month_r == '|') and event.key.isdigit():
            app.month_r = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.month_r += event.key
        elif event.key == 'Delete':
            app.month_r = app.month_r[:-1]
    elif app.typingYear_r2:
        if (app.year_r2 == '|') and event.key.isdigit():
            app.year_r2 = event.key
        elif event.key.isdigit() and len(event.key) == 1:
            app.year_r2 += event.key
        elif event.key == 'Delete':
            app.year_r2 = app.year_r2[:-1]


#Compare the user's expense/income ratio with the average ration in the US.
def compareExInRatio(app):
    getData_ExIn(app) # call to calculate
    myFile = getJson(f'./{app.username}.json')
    expenses = myFile['expenses']
    income = myFile['income']
    # get yearMonth through what the user types into entry box
    tgt_date = app.year_r + '/' + app.month_r # 2021/6
    totalIncome = income[tgt_date]
    totalExpense = 0
    for category in expenses[tgt_date]:
        totalExpense += expenses[tgt_date][category]
    # assign to global variable
    app.totalIncome, app.totalExpense = totalIncome, totalExpense
    if (totalExpense/totalIncome <= 1.1*app.ratio_ExIn): # to avoid slight decimal differences
        app.rating += 1
        app.goodList.append('Based on national data, your expense/income ratio is within\nthe reasonable range.')
    else:
        dif = (totalExpense/totalIncome - app.ratio_ExIn)
        app.badList.append(f'Based on national data, your expense/income ratio is {dif}% over the reasonable range.')


def compareCatBudgetPct(app):
    matches = 0 #budget(%) matches with actual expense/total expense
    catMatchCount = 0 #number of categories that both appear in budget & expense
    budgetCount = 0 #number of categories that have a planned budget percentage
    unmatched_categories = '' #for showing purpose
    myFile = getJson(f'./{app.username}.json')
    for category in myFile['budget_pct_cat']:
        if int(myFile['budget_pct_cat'][category]) > 0:
            budgetCount += 1
        tgt_pct = int(myFile['budget_pct_cat'][category])/100
        if category in myFile['expenses'][app.yearMonth]:
            catMatchCount += 1
            #if the actual expense for the category is similar (+-2.5%) to the budget
            if abs((myFile['expenses'][app.yearMonth][category]/app.totalExpense) - tgt_pct) <= 2.5:
                matches += 1
            else:
                if unmatched_categories == '': 
                    unmatched_categories = f'{category}'
                else:
                    unmatched_categories += (f', {category}')
    
    if (matches == len(myFile['expenses'][app.yearMonth]) and catMatchCount == budgetCount):
        app.rating += 2
        app.goodList.append('Your planned budgets in specific categories match with your\nexpenses well.')
        app.goodList.append('You planned for all your budgets in specific categories ahead of your spending.')
    elif matches == len(myFile['expenses'][app.yearMonth]):
        app.rating += 1
        app.goodList.append('Your planned budgets in specific categories match with your\nexpenses well.')
        app.badList.append('You did not plan for all your budgets in specific categories\nahead of your spending.')
    elif (matches >= len(myFile['expenses'][app.yearMonth])//2 and catMatchCount == budgetCount):
        app.rating += 1
        app.goodList.append('At least half of your planned\nbudgets in specific categories\nmatch with your expenses well.')
        app.goodList.append('You planned for all your budgets in specific categories ahead of your spending.')
        if (unmatched_categories.count(',') > 0): 
            app.badList.append(f'Your expenses in {unmatched_categories} account for quite different percentages of total income as planned.')
        else:
            app.badList.append(f'Your expense in {unmatched_categories} accounts for a quite different percentage of total income as planned.')
    elif catMatchCount == budgetCount:
        app.goodList.append('You planned for all your budgets in specific categories ahead of your spending.')
        app.badList.append(f'Your expenses in {unmatched_categories} account for quite different percentages of total income as planned.')
    else:
        app.badList.append(f'You did not plan for all your budgets in specific categories\nahead of your spending.')
        app.badList.append(f'Your expenses in {unmatched_categories} account for quite different percentages of total income as planned.')



#Check if actual expenses match with budget plan to see if user follows 50/30/20 rule.
def checkBudgetMatches(app):
    myFile = getJson(f'./{app.username}.json')
    app.expenses = myFile.get('expenses', {})
    if app.month_r[0] == '0':
        app.month_r = app.month_r[1]
    tgt_date = app.year_r + '/' + app.month_r
    (matches, overSpent, app.matched) = (0, '', {}) # re-initialize
    app.reminder_r = ''
    for item in app.plannedBudgets:
        category = item[1]
        if '.' in item[3]: amount = float(item[3]) # get rid of decimals
        else: amount = int(item[3])
        if category in app.expenses[tgt_date]:
            if category in app.matched: 
                app.matched[category] += amount
            else:
                app.matched[category] = amount
    for category in app.matched:
        total = app.matched[category]
        # if the actual expense <= planned expense
        if app.expenses[tgt_date][category] <= total:
            matches += 1
        else: # if expense > budget
            if overSpent == '':
                overSpent += category
            else:
                overSpent += (f', {category}')
    if matches == len(app.expenses[tgt_date]): # if expenses in every category match
        app.rating += 2
        app.goodList.append('Your expenses match with your planned budgets well.')
    elif matches >= len(app.expenses[tgt_date])/2: # if expenses in at least half of the categories match
        app.rating += 1
        app.goodList.append('At least half of your expenses match with your planned\nitems to purchase well.')
        if (overSpent.count(',') > 0): 
            app.badList.append(f'Your expenses in {overSpent} are\nhigher than their planned budgets.')
        else:
            app.badList.append(f'Your expense in {overSpent} is higher than its planned budget.')
    else:
        if (overSpent.count(',') > 0): 
            app.badList.append(f'Your expenses in {overSpent} are\nhigher than their planned budgets.')
        else:
            app.badList.append(f'Your expense in {overSpent} is higher than its planned budget.')


def drawTopBoxes(app, canvas): # all entry boxes at the top
    canvas.create_rectangle(0, 60, app.width, 175, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    canvas.create_text(25, 95, anchor='w', text='Date: ', font='Galvji 16 bold', fill='#373737') 
    # YYYY box
    canvas.create_rectangle(87.5, 82, 142.5, 108, fill='#fbfbfb')
    if app.year_r == '' or (app.typingMonth_r and app.year_r == '|'):
        canvas.create_text(115, 95, text='YYYY', font='Galvji 15', fill='#bebebe') 
    else:
        canvas.create_text(115, 95, text=app.year_r, font='Galvji 15', fill='#373737') 
    # MM box
    canvas.create_rectangle(157.5, 82, 197.5, 108, fill='#fbfbfb')
    if app.month_r == '' or (app.typingYear_r and app.month_r == ''):
        canvas.create_text(177.5, 95, text='MM', font='Galvji 15', fill='#bebebe') 
    else:
        canvas.create_text(177.5, 95, text=app.month_r, font='Galvji 15', fill='#373737') 
    canvas.create_text(151, 95, text='/', font='Galvji 18', fill='#373737')
    #Get Rating
    canvas.create_rectangle(app.width-114, 82, app.width-25, 108, fill='#fcfcfa') 
    canvas.create_text(app.width-69.5, 95, text='Get Rating', font='Galvji 14', fill='#373737') 
    #Clear
    canvas.create_rectangle(app.width-100, 127, app.width-39, 153, fill='#fcfcfa') 
    canvas.create_text(app.width-69.5, 140, text='Clear', font='Galvji 14', fill='#373737') 
    #Score
    canvas.create_text(25, 140, anchor='w', text='Score: ', font='Galvji 16 bold', fill='#373737') 
    if app.showScore:
        canvas.create_text(155, 140, text=f'{app.rating} / 5', font='Galvji 20 bold')
    else:
        canvas.create_text(155, 140, text=f'  / 5', font='Galvji 20 bold')


def drawAmtData(app, canvas):
    budget = 0
    if app.showScore:
        tgt_date = app.year_r + '/' + app.month_r
        for category in app.budgets[tgt_date]:
            for item in app.budgets[tgt_date][category]:
                budget += item[1]
    textColor = app.textColor
    canvas.create_rectangle(0, 175, app.width, 290, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    canvas.create_rectangle(0, 175, app.width-195, 205, fill='#e9e2d8', outline='#9f6c59', width=1.5)
    canvas.create_text(25, 191, anchor='w', text='Your record this month:', font='Galvji 15 bold', fill='#9f6c59')
    canvas.create_text(25, 230, anchor='w', text=f'Total Expense:  ${app.totalExpense}', font='Galvji 14', fill=textColor)
    canvas.create_text(25, 265, anchor='w', text=f'Total Income:  ${app.totalIncome}', font='Galvji 14', fill=textColor)
    canvas.create_text(app.width//2+8, 265, anchor='w', text=f'Remaining:  ${app.totalIncome-app.totalExpense}', font='Galvji 14', fill=textColor)
    canvas.create_text(app.width//2+8, 230, anchor='w', text=f'Budget:  ${budget}', font='Galvji 14', fill=textColor)


def drawRatingResultsBg(app, canvas):
    canvas.create_rectangle(0, 290, app.width, app.height-130, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    canvas.create_rectangle(0, 290, app.width-260, 320, fill='#e9e2d8', outline='#9f6c59', width=1.5)
    canvas.create_text(25, 306, anchor='w', text='Rating Results:', font='Galvji 15 bold', fill='#9f6c59')


def drawRatingResults(app, canvas):
    (y0, dy) = (355, 43)
    if app.goodList != []:
        for i in range(len(app.goodList)):
            canvas.create_image(28, y0+(dy*i), image=ImageTk.PhotoImage(app.scaled_check))
            canvas.create_text(45, y0+(dy*i), anchor='w', text=app.goodList[i], font='Galvji 12', fill=app.textColor)
    if app.badList != []:
        for i in range(len(app.badList)):
            canvas.create_image(28, y0+(dy*len(app.goodList)+(dy*i)), image=ImageTk.PhotoImage(app.scaled_x))
            canvas.create_text(45, y0+(dy*len(app.goodList)+(dy*i)), anchor='w', text=app.badList[i], font='Galvji 12', fill=app.textColor)


def drawRatingDistribution(app, canvas):
    canvas.create_rectangle(0, app.height-130, app.width, app.height-25, fill='#f8f8f4', outline='#9f6c59', width=1.5)
    canvas.create_rectangle(0, app.height-130, app.width-220, app.height-100, fill='#e9e2d8', outline='#9f6c59', width=1.5)
    canvas.create_text(25, app.height-114, anchor='w', text='Rating Distribution:', font='Galvji 15 bold', fill='#9f6c59')
    canvas.create_text(25, app.height-70, anchor='w', text='See rating distribution for', font='Galvji 14', fill=app.textColor)
    #year2 field
    canvas.create_rectangle(app.width//2-10, app.height-83, app.width//2+44, app.height-57, fill='#fcfcfa')
    if app.year_r2 == '' or ((app.typingMonth_r or app.typingYear_r) and app.year_r2 == '|'):
        canvas.create_text(app.width//2+17, app.height-70, text='YYYY', fill='#bebebe', font='Galvji 15')
    else:
        canvas.create_text(app.width//2+17, app.height-70, text=app.year_r2, font='Galvji 15', fill=app.textColor)
    #Enter button
    canvas.create_rectangle(app.width-80, app.height-83, app.width-25, app.height-57, fill='#fcfcfa')
    canvas.create_text(app.width-52.5, app.height-70, text='Enter', font='Galvji 14', fill=app.textColor)


# drawn if budgets are not planned yet.
def drawReminder_r(app, canvas):
    canvas.create_text(app.width//2, 320, text=app.reminder_r, font='Galvji 14', fill='red')


def ratingMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bgScaled))
    canvas.create_rectangle(0, 0, app.width, 60, fill='#ce8e73', outline='#9f6c59', width=1.5)
    canvas.create_text(app.width//2, 32, text='Ratings', font='Courier 20 bold', fill='#fcfcfa')
    drawReturnButton(app, canvas)
    drawTopBoxes(app, canvas)
    drawAmtData(app, canvas)
    drawRatingResultsBg(app, canvas)
    drawRatingDistribution(app, canvas)
    drawBottomBorder(app, canvas)
    if app.showScore: 
        drawRatingResults(app, canvas)
    if app.reminder_r != '':
        drawReminder_r(app, canvas)
    


################################################################
# Main App
################################################################

def appStarted(app):
    app.mode = 'welcomeScreenMode'
    # All images used in TP are created on my own.
    app.bgImage = app.loadImage('assets/background.png')
    app.bgScaled = app.scaleImage(app.bgImage, 1/6)
    app.trashIcon = app.loadImage('assets/trashcan.png')
    app.trashScaled = app.scaleImage(app.trashIcon, 1/15)
    app.checkMark = app.loadImage('assets/checkmark.png')
    app.xMark = app.loadImage('assets/xmark.png')
    app.scaled_check = app.scaleImage(app.checkMark, 1/22)
    app.scaled_x = app.scaleImage(app.xMark, 1/22)
    app.textColor = '#373737' #used for most text
    #variables from each mode
    welcomeScreenMode__init__(app)
    setBudgetsInCategoriesMode__init__(app)
    selectionScreenMode__init__(app)
    recordMode__init__(app)
    enterRecordMode__init__(app)
    budgetMode__init__(app)
    enterBudgetMode__init__(app)
    analysisMode__init__(app)
    ratingMode__init__(app)
    


def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2) 

#when user click on return button (used for EVERY page expect for welcome page)
def clickOnReturn(app, x, y):
    app.showScore = False
    return distance(30, 30, x, y) <= 20

def clickOnTrash(app, x, y):
    return (app.width-53 <= x <= app.width-28 and app.height-56 <= y <= app.height-26)

def drawBottomBorder(app, canvas): #additional border at the bottom of each page
    canvas.create_rectangle(0, app.height-25, app.width, app.height, fill='#ce8e73', outline='#9f6c59', width=1.5)

def drawReturnButton(app, canvas):
    canvas.create_oval(16, 16, 44, 44, fill='#f8f8f4', width=2, outline='#9f6c59')
    canvas.create_text(30, 30, text='<', font='Galvji 17 bold', fill='#9f6c59')

def writeToJsonFile(path, fileName, data):
    filePath = './' + path + '/' + fileName + '.json'
    with open(filePath, 'w') as fp:
        json.dump(data, fp)

def getJson(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)

# 3 : 5
runApp(width=420, height=700)