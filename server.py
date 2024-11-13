import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    MONGODB_URL = os.getenv("MONGODB_URL")
    DB_NAME = os.getenv("DB_NAME")

    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/todo')
    def home():
        return render_template('todo.html')

    @app.route("/todolist", methods=["POST"])
    def todolist_post():
        todolist_receive = request.form['todolist']
        count = db.todolist.count_documents({})
        num = count + 1
        doc = {
            'num': num,
            'todolist': todolist_receive,
            'done': 0
        }
        db.todolist.insert_one(doc)
        return jsonify({'msg': 'Item berhasil disimpan!'})

    @app.route("/todolist", methods=["GET"])
    def todolist_get():
        todolist_list = list(db.todolist.find({}, {'_id': False}))
        return jsonify({'todolists': todolist_list})
    # delete
    @app.route("/todolist/delete", methods=["POST"])
    def todolist_delete():
        num_receive = request.form['num_give']
        db.todolist.delete_one({'num': int(num_receive)})
        return jsonify({'msg': 'Item berhasil dihapus!'})

    @app.route("/todolist/done", methods=["POST"])
    def todolist_done():
        num_receive = request.form['num_give']
        db.todolist.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
        return jsonify({'msg': 'Item berhasil ditandai selesai!'})

    @app.route("/todolist/update", methods=["POST"])
    def todolist_update():
        num_receive = request.form['num_give']
        todolist_receive = request.form['todolist']
        
        db.todolist.update_one({'num': int(num_receive)}, {'$set': {'todolist': todolist_receive}})
        return jsonify({'msg': 'Item berhasil diupdate!'})

    if __name__ == '__main__':
        app.run('0.0.0.0', port=4090, debug=True)
except Exception as e:
    print(e)
