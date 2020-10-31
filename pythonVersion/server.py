from flask import Flask, render_template, url_for, request
#from forms import SearchForm
import csv

app=Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    app.route('/', methods = ['POST', 'GET'])
    items = parser()
    category = "Name"
    performSearch(category, items)
    return render_template("index.html")

def performSearch(category, items):
    searchedItems = []
    k = -1
    for a in range(len(items[0])-1):
        if items[0][a] == category:
            k = a
            break
    searchedItems = [sub[k] for sub in items]
    searchedItems.pop(0)

    print(category, ":", searchedItems)
    return ""

 
def parser():
    items = []
    with open('test.csv', newline='') as myFile:
        dataSet = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in dataSet:#take in row at a time
            print(row)#test print
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
