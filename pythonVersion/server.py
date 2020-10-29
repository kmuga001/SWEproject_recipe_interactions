
from flask import Flask, render_template, url_for, request
from forms import SearchForm
import csv

app=Flask(__name__)


@app.route('/')
def home():
    app.route('/')
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route('/results',methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      searchval = request.form['searchbar']
      return redirect(url_for('success',name = searchval))
   else:
      user = request.args.get('searchbar')
      return redirect(url_for('success',name = searchval))
        



#def parser(csvFile):
def parser():
    items = []
    
    with open('test.csv', newline='') as myFile:
        dataSet = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in dataSet:#take in row at a time
            print(row)#test print
            items.append(row)

        #return items

    

def update(csvFile,id,name,age,sex,status):
#    with open('test.csv', 'w', newline='') as csvfile:
#        fieldnames = ['id', 'name', 'age', 'sex', 'status']
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#        writer.writeheader()
#        writer.writerow({'id': '1111', 'name': 'Marvin', 'age': '50', 'sex': 'male', 'status': 'single'})
#        writer.writerow({'id': '1786', 'name': 'Kieth', 'age': '52', 'sex': 'male', 'status': 'married'})
#        writer.writerow({'id': '7857', 'name': 'Elizabeth', 'age': '22', 'sex': 'female', 'status': 'dating'})

    edited_rows = []
    edits = {   # a dictionary of changes to make, find 'key' substitue with 'value'
        '0000, James, 18, male, single' : '0000, Cartman, 19, male, single'

        }

    with open('test.csv', 'rb') as file:
        reader = csv.reader(file)
        for row in reader:
            edited_row = row      #takes the row and copies it
            for key in edits.items(): #iterate through edits
                edited_row = [ x.replace(key, value) for x in edited_row ] #changes values in row
            edited_rows.append(edited_row) # add the modified rows

    with open('test.csv', 'wb') as f: #Updates old file with new rows
        writer = csv.writer(f)
        writer.writerows(edited_rows)
