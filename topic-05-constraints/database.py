from mongita import MongitaClientDisk

client = None
db = None
kind_col = None
owner_col = None
pet_col = None


def initialize(database_name: str):
    global client, db, kind_col, owner_col, pet_col

    client = MongitaClientDisk()
    db = client[database_name]

    # Collections 
    kind_col = db["kind"]
    owner_col = db["owner"]
    pet_col = db["pet"]

    setup_database()


def setup_database():
    global kind_col, owner_col, pet_col

    kind_col.create_index("id")
    owner_col.create_index("id")
    pet_col.create_index("id")


# Helper functions
def _get_next_id(collection, id_field: str = "id") -> int:
    last = collection.find_one(sort=[(id_field, -1)])
    if last is None:
        return 1
    return int(last.get(id_field, 0)) + 1



# Query / Read functions
def get_pets():
    global pet_col, kind_col, owner_col

    pet_docs = list(pet_col.find({}))
    kind_docs = list(kind_col.find({}))
    owner_docs = list(owner_col.find({}))

    kinds_by_id = {k["id"]: k for k in kind_docs}
    owners_by_id = {o["id"]: o for o in owner_docs}

    pets = []

    for p in pet_docs:
        kind = kinds_by_id.get(p.get("kind_id"))
        owner = owners_by_id.get(p.get("owner_id"))

        if not kind or not owner:
            continue

        pet_view = {
            "id": p["id"],
            "name": p.get("name"),
            "age": p.get("age"),
            "kind_name": kind.get("name"),
            "food": kind.get("food"),
            "sound": kind.get("sound"),
            "owner": owner.get("name"),
            "color": p.get("color", ""),
        }
        pets.append(pet_view)

    for pet in pets:
        print(pet)

    return pets


def get_kinds():
    global kind_col
    kinds = list(kind_col.find({}))
    for kind in kinds:
        kind.pop("_id", None)
        print(kind)
    return kinds


def get_owners():
    global owner_col
    owners = list(owner_col.find({}))
    for owner in owners:
        owner.pop("_id", None)
        print(owner)
    return owners

def get_kind(id):
    global kind_col
    try:
        _id = int(id)
    except Exception:
        return "Data not found."

    doc = kind_col.find_one({"id": _id})
    if not doc:
        return "Data not found."
    doc.pop("_id", None) 
    return doc


def get_owner(id):
    global owner_col
    try:
        _id = int(id)
    except Exception:
        return "Data not found"

    doc = owner_col.find_one({"id": _id})
    if not doc:
        return "Data not found"
    doc.pop("_id", None)
    return doc

def get_pet(id):
    global pet_col
    try:
        _id = int(id)
    except Exception:
        return "Data not found."

    doc = pet_col.find_one({"id": _id})
    if not doc:
        return "Data not found."
    doc.pop("_id", None) 
    return doc




# Create functions
def create_pet(data):
    global pet_col

    try:
        data["age"] = int(data.get("age", 0))
    except Exception:
        data["age"] = 0

    try:
        data["kind_id"] = int(data["kind_id"])
    except Exception:
        raise ValueError("kind_id must be convertible to int")

    try:
        data["owner_id"] = int(data["owner_id"])
    except Exception:
        raise ValueError("owner_id must be convertible to int")

    new_id = _get_next_id(pet_col)
    doc = {
        "id": new_id,
        "name": data["name"],
        "age": data["age"],
        "kind_id": data["kind_id"],
        "owner_id": data["owner_id"],
        # NEW FIELD
        "color": data.get("color", ""), 
    }
    pet_col.insert_one(doc)



def create_kind(data):
    global kind_col

    new_id = _get_next_id(kind_col)
    doc = {
        "id": new_id,
        "name": data["name"],
        "food": data.get("food"),
        "sound": data.get("sound"),
    }
    kind_col.insert_one(doc)


def create_owner(data):
    global owner_col

    new_id = _get_next_id(owner_col)
    doc = {
        "id": new_id,
        "name": data["name"],
        "address": data.get("address"),
    }
    owner_col.insert_one(doc)


# Update functions
def update_pet(id, data):
    global pet_col

    try:
        _id = int(id)
    except Exception:
        return

    try:
        data["age"] = int(data.get("age", 0))
    except Exception:
        data["age"] = 0

    try:
        kind_id = int(data["kind_id"])
        owner_id = int(data["owner_id"])
    except Exception:
        raise ValueError("kind_id and owner_id must be convertible to int")

    update_doc = {
        "name": data["name"],
        "age": data["age"],
        "kind_id": kind_id,
        "owner_id": owner_id,
        "color": data.get("color", ""),
    }

    pet_col.update_one({"id": _id}, {"$set": update_doc})



def update_kind(id, data):
    global kind_col

    try:
        _id = int(id)
    except Exception:
        return

    update_doc = {
        "name": data["name"],
        "food": data.get("food"),
        "sound": data.get("sound"),
    }

    kind_col.update_one({"id": _id}, {"$set": update_doc})


def update_owner(id, data):
    global owner_col

    try:
        _id = int(id)
    except Exception:
        return

    update_doc = {
        "name": data["name"],
        "address": data.get("address"),
    }

    owner_col.update_one({"id": _id}, {"$set": update_doc})



# Delete functions
def delete_pet(id):
    global pet_col
    try:
        _id = int(id)
    except Exception:
        return
    pet_col.delete_one({"id": _id})


def delete_kind(id):
    global kind_col
    try:
        _id = int(id)
    except Exception:
        return
    kind_col.delete_one({"id": _id})
    


def delete_owner(id):
    global owner_col
    try:
        _id = int(id)
    except Exception:
        return
    owner_col.delete_one({"id": _id})


# Test DB setup and tests
def setup_test_database():
    """
    Mongita version of the original setup_test_database.
    """
    global db, kind_col, owner_col, pet_col

    initialize("test_pets_mongita")

    # Drop old collections
    kind_col.drop()
    owner_col.drop()
    pet_col.drop()

    # Recreate indexes
    setup_database()

    # Insert kinds
    create_kind({"name": "dog", "food": "dogfood", "sound": "bark"})
    create_kind({"name": "cat", "food": "catfood", "sound": "meow"})

    # Insert owners
    create_owner({"name": "Greg", "address": "1365 Maple Ave."})
    create_owner({"name": "David", "address": "13 Elm St."})

    # Look up their ids
    greg = owner_col.find_one({"name": "Greg"})
    david = owner_col.find_one({"name": "David"})
    greg_id = greg["id"]
    david_id = david["id"]

    pets = [
    {"name": "dorothy", "kind_id": 1, "age": 9, "owner_id": greg_id, "color": "brown"},
    {"name": "suzy",    "kind_id": 1, "age": 9, "owner_id": greg_id, "color": "black"},
    {"name": "casey",   "kind_id": 2, "age": 9, "owner_id": greg_id, "color": "white"},
    {"name": "heidi",   "kind_id": 2, "age": 15, "owner_id": david_id, "color": "gray"},
    ]

    for pet in pets:
        create_pet(pet)

    pets = get_pets()
    assert len(pets) == 4


def test_get_pets():
    print("testing get_pets")
    pets = get_pets()
    assert type(pets) is list
    assert len(pets) > 0
    assert type(pets[0]) is dict
    pet = pets[0]
    print(pet)
    for field in ["id", "name", "age", "owner", "kind_name", "food", "sound", "color"]:
        assert field in pet, f"Field {field} missing from {pet}"
    assert type(pet["id"]) is int
    assert type(pet["name"]) is str



def test_get_kinds():
    print("testing get_kinds")
    kinds = get_kinds()
    assert type(kinds) is list
    assert len(kinds) > 0
    assert type(kinds[0]) is dict
    kind = kinds[0]
    for field in ["id", "name", "food", "sound"]:
        assert field in kind, f"Field {field} missing from {kind}"
    assert type(kind["id"]) is int
    assert type(kind["name"]) is str


def test_get_owners():
    print("testing get_owners")
    owners = get_owners()
    assert type(owners) is list
    assert len(owners) > 0
    assert type(owners[0]) is dict
    owner = owners[0]
    for field in ["id", "name", "address"]:
        assert field in owner, f"Field {field} missing from {owner}"
    assert type(owner["id"]) is int
    assert type(owner["name"]) is str
    assert isinstance(owner["address"], str) or owner["address"] is None


if __name__ == "__main__":
    setup_test_database()
    test_get_pets()
    test_get_kinds()
    test_get_owners()
    print("done.")
