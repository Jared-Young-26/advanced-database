from flask import Flask, render_template, request, redirect, url_for
import database

# Initialize the Peewee database with the SQLite file
database.initialize("pets.db")

app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/pet/list", methods=["GET"])
def get_list():
    """Display a list of all pets."""
    pets = database.get_pets()
    return render_template("pet_list.html", pets=pets)

@app.route("/kind", methods=["GET"])
@app.route("/kind/list", methods=["GET"])
def get_kind_list():
    """Display a list of all kinds."""
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)

@app.route("/pet/create", methods=["GET"])
def get_create():
    """Render the pet creation form with available kinds and owners."""
    kinds = database.get_kinds()
    owners = database.get_owners()
    return render_template("pet_create.html", kinds=kinds, owners=owners)

@app.route("/pet/create", methods=["POST"])
def post_create():
    """Handle submission of the pet creation form."""
    data = dict(request.form)
    database.create_pet(data)
    return redirect(url_for("get_list"))

@app.route("/pet/delete/<id>", methods=["GET"])
def get_delete(id):
    """Delete a pet by ID and redirect to the pet list."""
    database.delete_pet(id)
    return redirect(url_for("get_list"))

@app.route("/pet/update/<id>", methods=["GET"])
def get_update(id):
    """Render the pet update form with existing data and lists of kinds and owners."""
    data = database.get_pet(id)
    kinds = database.get_kinds()
    owners = database.get_owners()
    return render_template("pet_update.html", data=data, kinds=kinds, owners=owners)

@app.route("/pet/update/<id>", methods=["POST"])
def post_update(id):
    """Handle submission of the pet update form."""
    data = dict(request.form)
    database.update_pet(id, data)
    return redirect(url_for("get_list"))

@app.route("/kind/create", methods=["GET"])
def get_kind_create():
    """Render the kind creation form."""
    return render_template("kind_create.html")

@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    """Handle submission of the kind creation form."""
    data = dict(request.form)
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))

@app.route("/kind/delete/<id>", methods=["GET"])
def get_kind_delete(id):
    """Delete a kind by ID, handling any foreign-key restrictions gracefully."""
    try:
        database.delete_kind(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_kind_list"))

@app.route("/kind/update/<id>", methods=["GET"])
def get_kind_update(id):
    """Render the kind update form with existing data."""
    data = database.get_kind(id)
    return render_template("kind_update.html", data=data)

@app.route("/kind/update/<id>", methods=["POST"])
def post_kind_update(id):
    """Handle submission of the kind update form."""
    data = dict(request.form)
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))

@app.route("/owner/list", methods=["GET"])
def get_owner_list():
    """Display a list of all owners."""
    owners = database.get_owners()
    return render_template("owner_list.html", owners=owners)

@app.route("/owner/create", methods=["GET"])
def get_owner_create():
    """Render the owner creation form."""
    return render_template("owner_create.html")

@app.route("/owner/create", methods=["POST"])
def post_owner_create():
    """Handle submission of the owner creation form."""
    data = dict(request.form)
    database.create_owner(data)
    return redirect(url_for("get_owner_list"))

@app.route("/owner/update/<id>", methods=["GET"])
def get_owner_update(id):
    """Render the owner update form with existing data."""
    data = database.get_owner(id)
    return render_template("owner_update.html", data=data)

@app.route("/owner/update/<id>", methods=["POST"])
def post_owner_update(id):
    """Handle submission of the owner update form."""
    data = dict(request.form)
    database.update_owner(id, data)
    return redirect(url_for("get_owner_list"))

@app.route("/owner/delete/<id>", methods=["GET"])
def get_owner_delete(id):
    """Delete an owner by ID, handling any foreign-key restrictions gracefully."""
    try:
        database.delete_owner(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_owner_list"))

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True)
