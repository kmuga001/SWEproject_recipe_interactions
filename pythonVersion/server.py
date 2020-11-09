from flask import Flask, render_template, url_for, request, jsonify
import csv
import json
#%matplotlib inline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import numpy as np 


app=Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    app.route('/', methods = ['POST', 'GET'])
    
    return render_template("index.html")



@app.route('/results1/')
def sendResultPage():
    return render_template('results1.html')

@app.route('/results2/')
def sendResult2Page():
    return render_template('results2.html')

@app.route('/results3/')
def sendResult3Page():
    return render_template('results3.html')

#create a png file for each plot using function: 

@app.route('/linearplot', methods = ['POST'])
def linearPlot():           #plot time vs ingredients
    steps = getSteps()        

    plt.hist(steps,density=True,bins=30)
    plt.xlabel('# of Steps')

    plt.savefig('static/histstepall.png')
    
    
    #return 'here is a linear plot that measures time (minutes) vs rating (out of 5) <br /> <a href="/">Back Home</a>'
    return render_template('results1.html')

@app.route('/secondplot', methods = ['POST'])
def barPlot():           #plot time vs rating
    ratingVals = getRatingResult()
    #print(ratingVals)       
    rateLabel = ['0.0','1.0','2.0','3.0','4.0','5.0']
    #plt.bar(ratings, ingredients, color='blue')
    plt.bar(rateLabel, ratingVals, color='blue')
    plt.xlabel('Ratings (out of 5)')
    plt.ylabel('# of recipes')

    plt.savefig('static/ratingsBar.png')
    
    
    #return 'here is a linear plot that measures time (minutes) vs rating (out of 5) <br /> <a href="/">Back Home</a>'
    return render_template('results2.html')


@app.route('/thirdplot', methods = ['POST'])
def boxPlot():           #plot time vs rating
    ingredients = getIngredients()        

    #plt.plot(time,rating, 'g---')
    #plt.scatter(time, rating, s=area, c=colors, alpha=0.5)
    #plt.plot(ratings,ingredients,'o',color='black')
    plt.boxplot(ingredients)
    plt.title("range of ingredients")
    

    plt.savefig('static/boxplot_full.png')
    
    
    #return 'here is a linear plot that measures time (minutes) vs rating (out of 5) <br /> <a href="/">Back Home</a>'
    return render_template('results3.html')




def getTime():    #get time from RAW_recipes
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
      

def getRatingResult():    #get rating from interactions_test
    ratingList = getRating()
    #print(ratingList[:20])
    #need to find how many values have each rating value (0, 5)
    count_0, count_1, count_2, count_3, count_4, count_5 = 0, 0, 0, 0, 0, 0
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
    with open('datasets/RAW_recipes.csv') as ingredients:
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
    with open('datasets/RAW_recipes.csv') as grabsteps:
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
    category = "sex"

    #search through category for input. 
    items = parser('test.csv')

    results = findRow(category, items, search_value)


    return render_template('index.html', results=json.dumps(results))


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


    return 'You searched for a recipe with id: %s <br /> Here is the information of the recipe that you saved: %s <br /> <a href="/">Back Home</a>' % (r_id, str_result_str)



@app.route('/clear', methods=['POST'])
def clearSavedRecipes():
    file_clear = open('saved.csv','w')
    file_clear.truncate()
    file_clear.close()

    return 'You cleared your saved recipes. <br /> <a href="/">Back Home</a>'


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

        return items




    

#def update(csvFile,id,name,age,sex,status):
#    with open('test.csv', 'w', newline='') as csvfile:
#        fieldnames = ['id', 'name', 'age', 'sex', 'status']
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#        writer.writeheader()
#        writer.writerow({'id': '1111', 'name': 'Marvin', 'age': '50', 'sex': 'male', 'status': 'single'})
#        writer.writerow({'id': '1786', 'name': 'Kieth', 'age': '52', 'sex': 'male', 'status': 'married'})
#        writer.writerow({'id': '7857', 'name': 'Elizabeth', 'age': '22', 'sex': 'female', 'status': 'dating'})

#   edited_rows = []
#     edits = {   # a dictionary of changes to make, find 'key' substitue with 'value'
#         '0000, James, 18, male, single' : '0000, Cartman, 19, male, single'

#         }

#     with open('test.csv', 'rb') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             edited_row = row      #takes the row and copies it
#             for key in edits.items(): #iterate through edits
#                 edited_row = [ x.replace(key, value) for x in edited_row ] #changes values in row
#             edited_rows.append(edited_row) # add the modified rows

#     with open('test.csv', 'wb') as f: #Updates old file with new rows
#         writer = csv.writer(f)
#         writer.writerows(edited_rows) 

if __name__=="__main__":
    app.run(debug=True)


