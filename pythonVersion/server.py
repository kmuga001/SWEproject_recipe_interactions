from flask import Flask, render_template, url_for, request
#from forms import SearchForm
import csv

app=Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    app.route('/', methods = ['POST', 'GET'])
    #items = parser()
    #category = "Name"
    #results = performSearch(category, items)
    #print(results)
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def searchingInput():
    search_value = request.form['search_value']
    str_result = ""
    #test_array = ["1", "2", "3"]
    items = parser('datasets/interactions_test.csv')
    category = search_value
    results = performSearch(category, items)
    for val in range(8):
        str_result += results[val]
        str_result += " "


    return 'The category you searched for is: %s <br /> These are the results: %s <br /> <a href="/">Back Home</a>' % (search_value,str_result)


@app.route('/savings', methods=['POST'])
def saveRecipe():
    r_id_int = request.form['savedRecipe_id']
    r_id = str(r_id_int)
    items = parser('datasets/interactions_test.csv')
    recipe_col = performSearch('recipe_id', items)
    recipeInfo = getRecipeInfo(r_id, recipe_col, items)
    print(recipeInfo)
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
        str_result_str += " "


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


def performSearch(category, items):
    searchedItems = []
    k = -1
    for a in range(len(items[0])-1):
        if items[0][a] == category:
            k = a
            break
    searchedItems = [sub[k] for sub in items]
    searchedItems.pop(0)

    #print(category, ":", searchedItems)
    return searchedItems

 
def parser(filename):
    items = []
    with open(filename, newline='') as myFile:
        dataSet = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in dataSet:#take in row at a time
            #print(row)
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
