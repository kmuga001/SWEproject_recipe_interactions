from flask import Flask, render_template, url_for, request, jsonify
import csv
import json
import os
import time
#%matplotlib inline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import numpy as np 


app=Flask(__name__)
appendNum = 0
originalLen = 0
delCheck = False
upCheck = False
getRatingRes = False
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0


@app.route('/', methods = ['POST', 'GET'])
def home():
    #append('test.csv')
    #delete('test.csv')
    #update('datasets/interactions_test.csv')
    app.route('/', methods = ['POST', 'GET'])
    
    return render_template("index.html")


@app.route('/recipe/<name>',methods = ['POST', 'GET'])
def buildRecipePage(name):
    with open('newtest.csv') as iTests:
        recipelist = csv.DictReader(iTests)
        for recipe in recipelist:
            if name == recipe["name"]:
                print(recipe)
                result = recipe
                steps = result["steps"]
                ingredients = result["ingredients"]
                break  
        del result["steps"]
        del result["ingredients"]
        return render_template('recipe.html', results = json.dumps(result), steps = json.dumps(steps), ingredients = json.dumps(ingredients))


def findNames(category, input):
    with open('newtest.csv') as iTests:
        recipeList = csv.DictReader(iTests)
        searchResults = []

        if input.isnumeric() == True:
            for recipe in recipeList:
                if input == recipe[category]:
                    searchResults.append(recipe["name"])
        else:
            for recipe in recipeList:
                if input in recipe[category]:
                    searchResults.append(recipe["name"])

    
        print(searchResults)
        return searchResults

@app.route('/savedrecipes/')
def sendSavedRecipesPage():
    return render_template('savedrecipes.html')

@app.route('/update/')
def sendUpdatePage():
    return render_template('update.html')

@app.route('/results1/')
def sendResultPage():
    return render_template('results1.html')

@app.route('/results2/')
def sendResult2Page():
    return render_template('results2.html')

@app.route('/results3/')
def sendResult3Page():
    return render_template('results3.html')

@app.route('/results4/')
def sendResult4Page():
    return render_template('results4.html')

@app.route('/results5/')
def sendResult5Page():
    return render_template('results5.html')

@app.route('/results6/')
def sendResult6Page():
    return render_template('results6.html')

#create a png file for each plot using function: 

@app.route('/firstplot', methods = ['POST'])
def linearPlot():           #plot time vs ingredients
    steps = getSteps()        

    plt.xlabel('# of Steps')
    plt.ylabel('frequency')
    plt.title('first analytic - # of steps vs. frequency')
    #plt.hist(globalSteps,density=True,bins=30)
    plt.hist(steps,density=True,bins=30)
    newplot_name = "firstGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('firstGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results1.html", graph=newplot_name)
    
    

@app.route('/secondplot', methods = ['POST'])
def barPlot():           #plot time vs rating
    global appendNum, originalLen, delCheck, upCheck
    ratingVals = getFinalRatingResult()
    count_0 = str(ratingVals[0])
    count_1 = str(ratingVals[1])
    count_2 = str(ratingVals[2])
    count_3 = str(ratingVals[3])
    count_4 = str(ratingVals[4])
    count_5 = str(ratingVals[5])
    #print(ratingVals)       
    rateLabel = ['0.0','1.0','2.0','3.0','4.0','5.0']
    #plt.bar(ratings, ingredients, color='blue')
    plt.bar(rateLabel, ratingVals, color='blue')
    plt.xlabel('Ratings (out of 5)')
    plt.ylabel('# of recipes')
    plt.title('second analytic - rating value vs. # of recipes')

    newplot_name = "secondGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('secondGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    #clear
    appendNum = 0
    originalLen = getFileLength('datasets/interactions_test.csv')
    delCheck = False
    upCheck = False
    return render_template("results2.html", graph=newplot_name, value0=count_0, value1=count_1, value2=count_2, value3=count_3, value4=count_4, value5=count_5)




@app.route('/thirdplot', methods = ['POST'])
def boxPlot():           #plot time vs rating
    ingredients = getIngredients()        

    #plt.plot(time,rating, 'g---')
    #plt.scatter(time, rating, s=area, c=colors, alpha=0.5)
    #plt.plot(ratings,ingredients,'o',color='black')
    #plt.boxplot(globalIngredient)
    plt.ylabel('# of ingredients')
    plt.boxplot(ingredients)
    plt.title("analytic 3 - distribution of # of ingredients")
    
    newplot_name = "thirdGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('thirdGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results3.html", graph=newplot_name)

@app.route('/fourth', methods = ['POST'])
def itemsPlot():
    numItems = getNumItems()
    xVals = getUserNums()
    plt.scatter(xVals, numItems)
    #plt.boxplot(numItems)
    plt.xlabel('user id #')
    plt.ylabel('# of recipes reviewed')
    plt.title('analytic 4 - number of recipes reviewed by users')

    newplot_name = "fourthGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('fourthGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results4.html", graph=newplot_name)

@app.route('/fifth', methods = ['POST'])
def numRatingPlot(): #how many 5 star ratings did eaach user give
    numFive = getFiveRatings()
    #plt.hist(numFive, density=True, bins=[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300])
    #plt.hist(numFive, density=True, bins=15)
    plt.title('analytic 5 - distribution of total # of five star ratings given by user')
    plt.xlabel('total # of 5 star ratings')
    plt.ylabel('frequency')
    plt.hist(numFive, density=True, bins=[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300])
    
    newplot_name = "fifthGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('fifthGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results5.html", graph=newplot_name)

@app.route('/sixth', methods = ['POST'])
def timePlot():           #plot time vs ingredients
    minutes = getMinutes()        
    print(minutes)
    plt.xlabel('# of Minutes')
    plt.ylabel('frequency')
    plt.title('sixth analytic - # of minutes vs. frequency')
    #plt.hist(globalSteps,density=True,bins=30)
    bins_list = [0,100,200,300,400,500,600,700,800,900,1000]
    plt.hist(minutes,density=True,bins=bins_list)
    
    newplot_name = "sixthGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('sixthGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results6.html", graph=newplot_name)



"""
@app.route('/sixth', methods = ['POST'])
def interactPlot():
    items_interact = getInteractArray()
    plt.hist(items_interact, density=True, bins=40)
    plt.xlabel('recipes that were viewed by users')
    plt.title('sixth analytic')
    newplot_name = "sixthGraph" + str(time.time()) + ".png"

    for filename in os.listdir('static/'):
        if filename.startswith('sixthGraph'):
            os.remove('static/' + filename)

    plt.savefig('static/' + newplot_name)
    plt.clf()
    return render_template("results6.html", graph=newplot_name)
"""

def getMinutes():
    #with open('datasets/RAW_recipes.csv') as grabsteps:
    with open('newtest.csv') as grabmin:
        allminList = csv.DictReader(grabmin)
        minList = []

        for mi in allminList:
            minVal = int(mi['minutes'])
            minList.append(minVal)
            
        
        return minList


def getTime():    #get time from RAW_recipes, prob not used right now
    with open('datasets/RAW_recipes.csv') as rawRecipes:
        recipeList = csv.DictReader(rawRecipes)
        timeList = []
        count = 0
        for recipe in recipeList:
            if count <= 200:
                time = int(recipe['minutes'])
                timeList.append(time)
            else:
                break
            count += 1

        return timeList

def getNumItems():
    with open('datasets/PP_users.csv') as ppUsers:
        user_fullList = csv.DictReader(ppUsers)
        itemsList = []
        
        for iVal in user_fullList:
            itemAppend = int(iVal['n_items'])
            itemsList.append(itemAppend)
        

        return itemsList

def getNumRatings():
    with open('datasets/PP_users.csv') as ppUsers:
        user_fullList = csv.DictReader(ppUsers)
        ratingsList = []

        for rVal in user_fullList:
            rateAppend = int(rVal['n_ratings'])
            ratingsList.append(rateAppend)

        return ratingsList
        
def getFiveRatings():
    with open('datasets/PP_users.csv') as ppUsers:
        user_fullList = csv.DictReader(ppUsers)
        fiveList = []

        for fRow in user_fullList:
            currRow = fRow['ratings'].strip('][').split(', ')
            fiveSum = 0
            for currVal in currRow:   
                numVal = float(currVal)
                if numVal == 5.0:
                    fiveSum += 1
            fiveList.append(fiveSum)

        return fiveList
    
def getUserNums():
    with open('datasets/PP_users.csv') as ppUsers:
        user_fullList = csv.DictReader(ppUsers)
        userList = []

        for userRow in user_fullList:
            userid = int(userRow['u'])
            userList.append(userid)

        return userList

def getInteractArray():
    with open('datasets/PP_users.csv') as ppUsers:
        user_fullList = csv.DictReader(ppUsers)
        itemList = []

        for itemOut in user_fullList:
            #currRow = list(itemOut['items'])
            currRow = itemOut['items'].strip('][').split(', ')
            for currVal in currRow:
                itemList.append(int(currVal)) #appending value inside inner items array
        
        return itemList


def getFinalRatingResult():
    finalList = []
    global count0, count1, count2, count3, count4, count5, getRatingRes, delCheck, upCheck, appendNum
    if delCheck == True or upCheck == True: 
         finalList = getRatingResult(0,0,0,0,0,0)
         count0 = finalList[0]
         count1 = finalList[1]
         count2 = finalList[2]
         count3 = finalList[3]
         count4 = finalList[4]
         count5 = finalList[5]
         print('DELCHECK: ')
         print(count0)
    elif appendNum > 0:
        #need to only go through last appendNum rows of file, use global count variables to append
        print('BEFOREAPPEND:')
        print(count0)
        if getRatingRes == False: 
            finalList = getRatingResult(count0, count1, count2, count3, count4, count5)
            count0 = finalList[0]
            count1 = finalList[1]
            count2 = finalList[2]
            count3 = finalList[3]
            count4 = finalList[4]
            count5 = finalList[5]
        else:
            with open("datasets/interactions_test.csv") as filename:
                tempList = list(csv.DictReader(filename))
                #reverse iteration to get last few rows
                tempAppendCount = appendNum
                countList = []
                for revRow in reversed(tempList):
                    #revRow = list(revRow)
                    if(tempAppendCount > 0):
                        tempVal = float(revRow['rating'])
                        countList.append(tempVal)
                    else:
                        break

                    tempAppendCount -= 1


                for rVal in countList: #sort out counts
                    if rVal == 0.0:
                        count0 += 1
                    elif rVal == 1.0:
                        count1 += 1
                    elif rVal == 2.0:
                        count2 += 1
                    elif rVal == 3.0:
                        count3 += 1
                    elif rVal == 4.0:
                        count4 += 1
                    else:           #rVal == 5.0
                        count5 += 1

                finalList.append(count0)
                finalList.append(count1)
                finalList.append(count2)
                finalList.append(count3)
                finalList.append(count4)
                finalList.append(count5) 

        print('CHECKAPPEND:')
        print(finalList)

    else: 
        print('BEFOREELSE:')
        print(count0)
        
        if getRatingRes == False: 
            finalList = getRatingResult(count0, count1, count2, count3, count4, count5)
            count0 = finalList[0]
            count1 = finalList[1]
            count2 = finalList[2]
            count3 = finalList[3]
            count4 = finalList[4]
            count5 = finalList[5]
        else:
            finalList.append(count0)
            finalList.append(count1)
            finalList.append(count2)
            finalList.append(count3)
            finalList.append(count4)
            finalList.append(count5) 
        print('ELSECHECK:')
        print(finalList)

    return finalList


def getRatingResult(c0, c1, c2, c3, c4, c5):    #get rating from interactions_test
    ratingList = getRating()
    global getRatingRes
    #print(ratingList[:20])
    #need to find how many values have each rating value (0, 5)
    count_0, count_1, count_2, count_3, count_4, count_5 = c0, c1, c2, c3, c4, c5
    rateResult = []
    for rVal in ratingList:
        if rVal == 0.0:
            count_0 += 1
        elif rVal == 1.0:
            count_1 += 1
        elif rVal == 2.0:
            count_2 += 1
        elif rVal == 3.0:
            count_3 += 1
        elif rVal == 4.0:
            count_4 += 1
        else:           #rVal == 5.0
            count_5 += 1
    
    rateResult.append(count_0)
    rateResult.append(count_1)
    rateResult.append(count_2)
    rateResult.append(count_3)
    rateResult.append(count_4)
    rateResult.append(count_5)
    
    getRatingRes = True
    return rateResult

def getRating():    #get rating from interactions_test
    with open('datasets/interactions_test.csv') as iTests:
        recipeList = csv.DictReader(iTests)
        ratingValList = []
        
        for recipe in recipeList:
            ratingVal = float(recipe['rating'])
            ratingValList.append(ratingVal)
        
        

        return ratingValList

def getIngredients():
    #with open('datasets/RAW_recipes.csv') as ingredients:
    with open('newtest.csv') as ingredients:
        ingredientsList = csv.DictReader(ingredients)
        numOfIngredients = []
        #for ingredient in ingredientsList:
        #    ingredientVal = int(ingredient['n_ingredients'])
        #    numOfIngredients.append(ingredientVal)


        
        #count = 0
        for ingredient in ingredientsList:
            ingredientVal = int(ingredient['n_ingredients'])
            numOfIngredients.append(ingredientVal)
            
        
        
        return numOfIngredients


def getSteps():
    #with open('datasets/RAW_recipes.csv') as grabsteps:
    with open('newtest.csv') as grabsteps:
        allstepList = csv.DictReader(grabsteps)
        stepList = []
        #for ingredient in ingredientsList:
        #    ingredientVal = int(ingredient['n_ingredients'])
        #    numOfIngredients.append(ingredientVal)


        for st in allstepList:
            stVal = int(st['n_steps'])
            stepList.append(stVal)
            
        
        return stepList


@app.route('/results', methods = ['POST', 'GET'])
def recipeResults():
    app.route('/results', methods = ['POST', 'GET'])
    return render_template("results.html")


""" steps for search function
 - 
 - search through that category with input 
 - if the input is found, take everything else in that row. 
 """


#For testing purposes

@app.route('/search', methods=['GET','POST'])
def searchingInput():
    #step 1: take in input and selected category 
    search_value = request.form['search_value']
    category = request.form['search_category']
    if len(category) == 0:
        return "Error, need a category. Return and try again."
    
    #search through category for input. 
    results = findNames(category, search_value)
    s = json.dumps(results)
    return render_template('index.html', results=s)


@app.route('/savings', methods=['POST'])
def saveRecipe():
    r_id_int = request.form['savedRecipe_id']
    r_id = str(r_id_int)
    items = parser('datasets/interactions_test.csv')
    recipe_col = findColumn('recipe_id', items)
    recipeInfo = getRecipeInfo(r_id, recipe_col, items)
    #write the recipe into a csv file
    with open('saved.csv','a') as output:
        for recipeVal in range(len(recipeInfo)):
            if recipeVal == (len(recipeInfo) - 1):
                output.write(recipeInfo[recipeVal])
            else:
                output.write(recipeInfo[recipeVal] + ',')

        output.write('\n')

    #display result to website
    str_result_str = ""
    for value in recipeInfo:
        str_result_str += value
        str_result_str += ' '


    #return 'You searched for a recipe with id: %s <br /> Here is the information of the recipe that you saved: %s <br /> <a href="/">Back Home</a>' % (r_id, str_result_str)
    return render_template("savedrecipes.html", savedResult=str_result_str)


@app.route('/clear', methods=['POST'])
def clearSavedRecipes():
    file_clear = open('saved.csv','w')
    file_clear.truncate()
    file_clear.close()
    str_result_str = "Your saved recipes are cleared!"

    #return 'You cleared your saved recipes. <br /> <a href="/">Back Home</a>'
    return render_template("savedrecipes.html", clearMessage=str_result_str)


def getRecipeInfo(r_id, recipe_col, items):
    rowNum = 0
    recipeInfo = []

    for val in range(len(recipe_col)):
        if recipe_col[val] == r_id:
            rowNum = val
            break
    
    recipeInfo = items[rowNum + 1]
    return recipeInfo

def findColumn(category, items):
    c = []
    index = items[0].index(category)
    c = [sub[index] for sub in items]
    c.pop(0)

    return c

def findRow(category, items, input):
    searchedItems = []
    c = items[0].index(category)
    column = [sub[c] for sub in items]
    
    for r in range(len(column)):
       if column[r] == input:
            searchedItems.append({items[0][i]:items[r][i] for i in range(len(items[0]))})

    return searchedItems

 
def parser(filename):
    items = []
    with open(filename, newline='') as myFile:
        dataSet = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in dataSet:#take in row at a time
            items.append(row)
        myFile.close()
        return items

def writer(header, data, filename, option):
    with open (filename, "w", newline = "") as csvfile:
        if option == "write":

            recipes = csv.writer(csvfile)
            recipes.writerow(header)
            for x in data:
                recipes.writerow(x)
        elif option == "update":
            recipes = csv.DictWriter(csvfile, fieldnames = header)
            recipes.writeheader()
            recipes.writerows(data)
        else:
            print("Option is not known")
        csvfile.close()

@app.route('/updateRow', methods=['POST'])
def userUpdate():
    global upCheck
    userid = request.form['userid']
    newVal = request.form['newVal']
    returnValue = "none"

    rowNum = findUserRow(int(userid),'datasets/interactions_test.csv')

    if rowNum == -1:
        returnValue = "inputted user id does not exist."
    else:
        update('datasets/interactions_test.csv', int(rowNum), newVal)
        returnValue = newVal
        upCheck = True
    #return 'You updated the rating for a recipe. <br /> <a href="/">Back Home</a>'
    
    return render_template("update.html", updateValue=returnValue)


def findUserRow(userid, filename):
    with open(filename) as filen:
        file_list = csv.DictReader(filen)
        rowNumber = 0
        for each_row in file_list:
            currUser = int(each_row['user_id'])
            if currUser == userid:
                return rowNumber
            else:
                rowNumber += 1

        rowNumber = -1
        
        return rowNumber


def update(filename, rowNum, newVal):
    with open(filename, newline="") as file:
        readData = [row for row in csv.DictReader(file)]
        #find rowNum by finding userid's row number
        #rowNum = findUserRow(userid, filename)
        readData[rowNum]['rating'] = newVal 
        file.close()
    readHeader = readData[0].keys()
    writer(readHeader, readData, filename, "update")



@app.route('/appendRow', methods=['POST'])
def userAppend():
    global appendNum
    user_id = request.form['user_id']
    rec_id = request.form['rec_id']
    date = request.form['date']
    rating = request.form['rating']
    u_ = request.form['u_']
    i_ = request.form['i_']
    append('datasets/interactions_test.csv', user_id, rec_id, date, rating, u_, i_)
    appendNum += 1
    print(appendNum)
    #return 'You appended a row. <br /> <a href="/">Back Home</a>'
    returnValue = date
    return render_template("update.html", appendValue=returnValue)


def append(filename, user_id, rec_id, date, rating, u_, i_):
    with open(filename, 'a', newline='') as file:
        field = ['user_id', 'recipe_id', 'date', 'rating', 'u', 'i']
        writer = csv.DictWriter(file, fieldnames = field)
        uidVal = user_id
        ridVal = rec_id
        dateVal = date
        rateVal = rating
        uVal = u_
        iVal = i_

        writer.writerow({'user_id': uidVal, 'recipe_id': ridVal, 'date': dateVal, 'rating': rateVal, 'u': uVal, 'i': iVal})
        file.close()
  


@app.route('/deleteRow', methods=['POST'])
def userDelete():
    user_id = request.form['user_id']
    delete('datasets/interactions_test.csv', user_id)
    returnValue = user_id
    return render_template("update.html", deleteValue=returnValue)
    #return 'You deleted a row. <br /> <a href="/">Back Home</a>'


def delete(filename, userid):
    global originalLen, delCheck
    with open(filename, 'r') as inp, open('test1.csv', 'w') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            #if row[0] != "9999":
            if row[0] != userid:
                writer.writerow(row)
    os.rename('test1.csv', filename)
    originalLen = getFileLength(filename)
    delCheck = True
    print(originalLen)


def getFileLength(filename):
    with open(filename) as f:
        templist = csv.DictReader(f)
        return sum(1 for line in templist)




if __name__=="__main__":
    #globalIngredient = getIngredients()
    #globalIngredient = []
    #globalSteps = getSteps()
    #globalSteps = []
    #global interactLength
    originalLen = getFileLength('datasets/interactions_test.csv')
    #interactLength = getFileLength('datasets/interactions_test.csv')
    app.run(debug=True)


