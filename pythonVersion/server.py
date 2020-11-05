from flask import Flask, render_template, url_for, request
import csv

app=Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    app.route('/', methods = ['POST', 'GET'])
    return render_template("index.html")


@app.route('/results', methods = ['POST', 'GET'])
def recipeResults():
    app.route('/results', methods = ['POST', 'GET'])
    return render_template("results.html")

""" steps for search function
 - 
 - search through that category with input 
 - if the input is found, take everything else in that row. 
 """



#@app.route('/search', methods=['POST'])
#def searchingInput():
    #step 1: take in input and selected category 
  #  search_value = request.form['search_value']
   # category = "user_id"

    #search through category for input. 
   # items = parser('datasets/interactions_test.csv')
   # results = findRow(category, items, search_value)






#For testing purposes
@app.route('/search', methods=['POST'])
def searchingInput():
    #step 1: take in input and selected category 
    search_value = request.form['search_value']
    category = "sex"

    #search through category for input. 
    items = parser('test.csv')
    results = findRow(category, items, search_value)

    return render_template('results.html', results)
    #return 'You searched for %s in the category of %s <br /> These are your results:  <br /> %s <a href="/">Back Home</a> <a href="/recipe">more info</a>' % (search_value,category,str(results))


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
    k = -1
    for a in range(len(items[0])-1):
        if items[0][a] == category:
            k = a
            break
    c = [sub[k] for sub in items]
    c.pop(0)

    return c

def findRow(category, items, input):
    searchedItems = []
    for c in range(len(items[0])-1):
        if items[0][c] == category:   
            column = [sub[c] for sub in items]
            break
    
    for r in range(len(column)):
        if column[r] == input:
            searchedItems.append({items[0][i]:items[r][i] for i in range(1,len(items[0]))})

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


