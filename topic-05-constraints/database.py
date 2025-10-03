import sqlite3

connection = None


def initialize(database_file):
    global connection
    connection = sqlite3.connect(database_file, check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row
    setup_database()

def setup_database():
    cursor = connection.cursor()
    cursor.execute(
        """
        create table if not exists kind (
            id integer primary key autoincrement not null,
            name text not null,
            food text,
            sound text
        )
        """
    )
    connection.commit()
    cursor = connection.cursor()
    cursor.execute(
        """
        create table if not exists owner (
            id integer primary key autoincrement not null,
            name text not null,
            address text
        )
        """
    )
    connection.commit()
    cursor = connection.cursor()
    cursor.execute(
        """
        create table if not exists pet (
            id integer primary key autoincrement,
            name text not null,
            age integer,
            kind_id integer not null,
            owner_id integer not null,
            foreign key (kind_id) references kind(id) on delete RESTRICT on update CASCADE,
            foreign key (owner_id) references owner(id) on delete RESTRICT on update CASCADE
        )
        """
    )
    connection.commit()

def get_pets():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT pet.id, pet.name, pet.age, kind.name as kind_name, kind.food, kind.sound, owner.name as owner
        FROM pet 
        JOIN kind ON pet.kind_id = kind.id
        JOIN owner ON pet.owner_id = owner.id
    """)
    pets = cursor.fetchall()
    pets = [dict(pet) for pet in pets]
    for pet in pets:
        print(pet)
    return pets

def get_kinds():
    cursor = connection.cursor()
    cursor.execute("""select * from kind""")
    kinds = cursor.fetchall()
    kinds = [dict(kind) for kind in kinds]
    for kind in kinds:
        print(kind)
    return kinds

def get_owners():
    cursor = connection.cursor()
    cursor.execute("""select * from owner""")
    owners = cursor.fetchall()
    owners = [dict(owner) for owner in owners]
    for owner in owners:
        print(owner)
    return owners

def get_pet(id):
    cursor = connection.cursor()
    cursor.execute(f"""select * from pet where id = ?""", (id,))
    rows = cursor.fetchall()
    try:
        (id, name, kind_id, age, owner_id) = rows[0]
        data = {"id": id, "name": name, "kind_id": kind_id, "age": age, "owner_id": owner_id}

        return data
    except:
        return "Data not found."

def get_kind(id):
    cursor = connection.cursor()
    cursor.execute(f"""select * from kind where id = ?""", (id,))
    rows = cursor.fetchall()
    try:
        (id, name, food, sound) = rows[0]
        data = {"id": id, "name": name, "food": food, "sound": sound}

        return data
    except:
        return "Data not found."

def get_owner(id):
    cursor = connection.cursor()
    cursor.execute(f"""select * from owner where id = ?""", (id,))
    rows = cursor.fetchall()
    try:
        (id, name, address) = rows[0]
        data = {"id": id, "name": name, "address": address}

        return data
    except:
        return "Data not found"

def create_pet(data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """insert into pet(name, age, kind_id, owner_id) values (?,?,?,?)""",
        (data["name"], data["age"], data["kind_id"], data["owner_id"]),
    )
    connection.commit()

def create_kind(data):
    cursor = connection.cursor()
    cursor.execute(
        """insert into kind(name, food, sound) values (?,?,?)""",
        (data["name"], data["food"], data["sound"]),
    )
    connection.commit()

def create_owner(data):
    cursor = connection.cursor()
    cursor.execute(
        """insert into owner(name, address) values (?,?)""",
        (data["name"], data["address"])
    )
    connection.commit()

def test_create_pet():
    pass

def update_pet(id, data):
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """update pet set name=?, age=?, kind_id=?, owner_id=? where id=?""",
        (data["name"], data["age"], data["kind_id"], data["owner_id"], id),
    )
    connection.commit()

def update_kind(id, data):
    cursor = connection.cursor()
    cursor.execute(
        """update kind set name=?, food=?, sound=? where id=?""",
        (data["name"], data["food"], data["sound"], id),
    )
    connection.commit()

def update_owner(id, data):
    cursor = connection.cursor()
    cursor.execute(
        """update owner set name=?, address=? where id=?""",
        (data["name"], data["address"], id)
    )
    connection.commit()

def delete_pet(id):
    cursor = connection.cursor()
    cursor.execute(f"""delete from pet where id = ?""", (id,))
    connection.commit()

def delete_kind(id):
    cursor = connection.cursor()
    cursor.execute(f"""delete from kind where id = ?""", (id,))
    connection.commit()

def delete_owner(id):
    cursor = connection.cursor()
    cursor.execute(f"""delete from owner where id = ?""", (id,))
    connection.commit()

def setup_test_database():
    initialize("test_pets.db")
    cursor = connection.cursor()
    cursor.execute("drop table if exists pet")
    cursor.execute("drop table if exists kind")
    cursor.execute("drop table if exists owner")
    cursor.execute(
            """
            create table if not exists kind (
                id integer primary key autoincrement not null,
                name text not null,
                food text,
                sound text
            )
            """
        )
    connection.commit()
    cursor.execute(
        """
            insert 
                into kind(name, food, sound) 
                values (?,?,?)
            """,
        ("dog", "dogfood", "bark"),
    )
    cursor.execute(
        """
            insert 
                into kind(name, food, sound) 
                values (?,?,?)
            """,
        ("cat", "catfood", "meow"),
    )
    connection.commit()
    cursor = connection.cursor()
    cursor.execute(
        """
        create table if not exists owner (
            id integer primary key autoincrement not null,
            name text not null,
            address text
        )
    """
    )
    connection.commit()
    cursor.executemany("""insert into owner(name, address) values (?,?)""",
                   [("Greg", "1365 Maple Ave."), ("David", "13 Elm St.")]
                   )
    connection.commit()
    cursor.connection.cursor()
    cursor.execute(
        """
        create table if not exists pet (
            id integer primary key autoincrement,
            name text not null,
            age integer,
            kind_id integer not null,
            owner_id integer not null,
            foreign key (kind_id) references kind(id) on delete RESTRICT on update CASCADE,
            foreign key (owner_id) references owner(id) on delete RESTRICT on update CASCADE
        )
    """
    )
    connection.commit()
    cursor.execute("select id from owner where name='Greg'")
    greg_id = cursor.fetchone()["id"]
    cursor.execute("select id from owner where name='David'")
    david_id = cursor.fetchone()["id"]
    pets = [
        {"name": "dorothy", "kind_id": 1, "age": 9, "owner_id": greg_id},
        {"name": "suzy", "kind_id": 1, "age": 9, "owner_id": greg_id}, 
        {"name": "casey", "kind_id": 2, "age": 9, "owner_id": greg_id},
        {"name": "heidi", "kind_id": 2, "age": 15, "owner_id": david_id},
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
    for field in ["id", "name", "age", "owner", "kind_name","food","sound"]:
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
    assert type(owner["address"]) is str

if __name__ == "__main__":
    setup_test_database()
    test_get_pets()
    test_get_kinds()
    test_get_owners()
    test_create_pet()
    print("done.")




    
    