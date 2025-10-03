from flask import Flask, render_template, request, redirect, url_for

import database

# remember to $ pip install flask

database.initialize("pets.db")

app = Flask(__name__)

@app.route("/", methods=["GET"]) 
@app.route("/pet/list", methods=["GET"])
def get_list():
    pets = database.get_pets()
    return render_template("pet_list.html", pets=pets)     


@app.route("/kind", methods=["GET"])
@app.route("/kind/list", methods=["GET"])
def get_kind_list():
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/pet/create", methods=["GET"])
def get_create():
    kinds = database.get_kinds()
    owners = database.get_owners()
    #print("KINDS = ",kinds)
    return render_template("pet_create.html", kinds=kinds, owners=owners)     

@app.route("/pet/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    print("DATA=",data)
    database.create_pet(data)
    return redirect(url_for("get_list"))  

@app.route("/pet/delete/<id>", methods=["GET"])
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for("get_list"))  

@app.route("/pet/update/<id>", methods=["GET"])
def get_update(id):
    data = database.get_pet(id)
    kinds = database.get_kinds()
    owners = database.get_owners()
    return render_template("pet_update.html",data=data, kinds=kinds, owners=owners)

@app.route("/pet/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    database.update_pet(id, data)
    return redirect(url_for("get_list"))  

@app.route("/kind/create", methods=["GET"])
def get_kind_create():
        return render_template("kind_create.html")

@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    data = dict(request.form)
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))

@app.route("/kind/delete/<id>", methods=["GET"])
def get_kind_delete(id):
    try:
        database.delete_kind(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_kind_list"))

@app.route("/kind/update/<id>", methods=["GET"])
def get_kind_update(id):
    data = database.get_kind(id)
    return render_template("kind_update.html",data=data)

@app.route("/kind/update/<id>", methods=["POST"])
def post_kind_update(id):
    data = dict(request.form)
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))

@app.route("/owner/list", methods=["GET"])
def get_owner_list():
    owners = database.get_owners()
    return render_template("owner_list.html", owners=owners)

@app.route("/owner/create", methods=["GET"])
def get_owner_create():
    return render_template("owner_create.html")

@app.route("/owner/create", methods=["POST"])
def post_owner_create():
    data = dict(request.form)
    database.create_owner(data)
    return redirect(url_for("get_owner_list"))

@app.route("/owner/update/<id>", methods=["GET"])
def get_owner_update(id):
    data = database.get_owner(id)
    print("DATA=",data)
    return render_template("owner_update.html", data=data)

@app.route("/owner/update/<id>", methods=["POST"])
def post_owner_update(id):
    data = dict(request.form)
    database.update_owner(id, data)
    return redirect(url_for("get_owner_list"))

@app.route("/owner/delete/<id>", methods=["GET"])
def get_owner_delete(id):
    try:
        database.delete_owner(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_owner_list"))