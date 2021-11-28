from flask import Flask,render_template,redirect,request,url_for
from pymongo import MongoClient
import datetime

app=Flask(__name__,template_folder='../public/templates/',static_folder='../public/static/')#public/

#mongodb part
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.todo_task_db
my_collection = db.task_collection

@app.route('/')
def home_view():
    return render_template('index.html')

@app.route('/completed',methods=['POST','GET'])
def completed_tasks():
    if request.method=='POST':
        prev_val={
            'task_desc':request.form.get('task_desc')
        }
        new_val={
            '$set':{
                'completed':'True'
            }
        }

        my_collection.update_one(prev_val,new_val)
    else:
        pass
    return redirect('/tasks')

@app.route('/add',methods=['POST','GET'])
def add_task():
    if request.method == 'POST':
        task_desc = request.form.get('task_content')
        task={
            'task_desc':task_desc,
            'completed':"False"
        }
        my_collection.insert_one(task)
        
        return redirect('/')
    else:
        return redirect('/')


@app.route('/tasks')
def view_task():
    tasks=my_collection.find({'completed':'False'})
    if tasks is None:
        tasks=[]
    return render_template('tasks.html',tasks=tasks)


@app.route('/completedtasks')
def completed_list():
    tasks=my_collection.find({'completed':'True'})

    return render_template('completed.html',tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)