import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify , session ,url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt


try:
    
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    MONGODB_URL = os.getenv("MONGODB_URL")
    DB_NAME = os.getenv("DB_NAME")

    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]
    print("Koneksi ke MongoDB berhasil!")

    app = Flask(__name__)
    bcrypt = Bcrypt(app)


    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/todo')
    def todolist():
        # if "username" not in session:
        #     return redirect(url_for('logintodolist'))
        # username = session["username"]
        # return render_template('todo.html', username=username)
        return render_template('todo.html')

    @app.route("/api/logintodolist")
    def login():
        userdata = db.usertodo.find({})
        print(userdata)

    @app.route('/logintodolist', methods=['GET', 'POST'])
    def logintodolist():
        if request.method == "POST":
            data = request.get_json()  
            print('Data Toko', data)
            username = data.get("username")
            password = data.get("password")
            
            user = db.usertodo.find_one({"username": username})

            if user and bcrypt.check_password_hash(user["password"], password):
                username = user["username"] 
                # session["username"] = username
                # session["user_id"] = str(user["_id"])
                # session["username"] = user["username"]
                return jsonify({"message": f"Hi Selamat Datang "}), 200
            else:
                return jsonify({"error": "Username atau password salah"}), 401
        return render_template("login.html")

    @app.route("/registodolist", methods=["POST", "GET"])
    def registrasi():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirmmpassword = request.form.get("confirmmpassword")

            if not username or not password or not confirmmpassword:
                return jsonify({"error": "Semua field harus diisi"}), 400
            if password != confirmmpassword:
                return jsonify({"error": "Password dan konfirmasi password tidak cocok"}), 400

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user_data = {
                "username": username,
                "password": hashed_password,
            }

            db.usertodo.insert_one(user_data)
            return jsonify({"message": "Registrasi berhasil!"}), 201

        return render_template("daftar.html")

    @app.route("/todolist", methods=["POST"])
    def todolist_post():
        todolist_receive = request.form['todolist']
        count = db.todolist.count_documents({})
        print('ini hasil cound',count)
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
    
    # @app.route('/')
    # def number():
    #     number1 = 1
    #     number2 = 2
    #     print("data number",number1 + number2)

    

    if __name__ == '__main__':
        app.run('0.0.0.0', port=4090, debug=True)
except Exception as e:
    print('database connetion error',e)
