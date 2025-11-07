from peewee import Model, CharField, IntegerField, ForeignKeyField, AutoField, SqliteDatabase

# Global database handle – initialized in `initialize`
db = None


class BaseModel(Model):
    """Base class that binds models to the database."""
    class Meta:
        database = db


class Kind(BaseModel):
    """Represents an animal type."""
    id = AutoField()
    name = CharField()
    food = CharField(null=True)
    sound = CharField(null=True)


class Owner(BaseModel):
    """Represents a pet owner."""
    id = AutoField()
    name = CharField()
    address = CharField(null=True)


class Pet(BaseModel):
    """Represents a pet with a foreign key to Kind and Owner."""
    id = AutoField()
    name = CharField()
    age = IntegerField(null=True)
    kind = ForeignKeyField(Kind, backref="pets", on_delete="RESTRICT", on_update="CASCADE")
    owner = ForeignKeyField(Owner, backref="pets", on_delete="RESTRICT", on_update="CASCADE")


def initialize(database_file: str) -> None:
    """
    Initialize the Peewee database connection, enable foreign keys,
    and ensure tables are created.
    """
    global db
    db = SqliteDatabase(database_file, check_same_thread=False)

    # Assign the database to model Meta after initialization
    Kind._meta.database = db
    Owner._meta.database = db
    Pet._meta.database = db

    db.connect(reuse_if_open=True)
    db.execute_sql("PRAGMA foreign_keys = 1")
    setup_database()


def setup_database() -> None:
    """Create tables for Kind, Owner, and Pet if they do not already exist."""
    db.create_tables([Kind, Owner, Pet])


def get_pets():
    """
    Retrieve all pets with their kind and owner information.
    Returns a list of dictionaries matching the original schema.
    """
    query = (
        Pet.select(
            Pet.id,
            Pet.name,
            Pet.age,
            Kind.name.alias("kind_name"),
            Kind.food,
            Kind.sound,
            Owner.name.alias("owner"),
        )
        .join(Kind)
        .switch(Pet)
        .join(Owner)
    )
    pets = [dict(pet) for pet in query.dicts()]
    for pet in pets:
        print(pet)
    return pets


def get_kinds():
    """
    Retrieve all kinds.
    Returns a list of dictionaries with keys: id, name, food, sound.
    """
    kinds = [dict(kind) for kind in Kind.select().dicts()]
    for kind in kinds:
        print(kind)
    return kinds


def get_owners():
    """
    Retrieve all owners.
    Returns a list of dictionaries with keys: id, name, address.
    """
    owners = [dict(owner) for owner in Owner.select().dicts()]
    for owner in owners:
        print(owner)
    return owners


def get_pet(id: int):
    """
    Retrieve a single pet by its ID.
    Returns a dictionary like {"id": ..., "name": ..., "kind_id": ..., "age": ..., "owner_id": ...}
    or a 'Data not found.' message if no pet is found.
    """
    pet = Pet.get_or_none(Pet.id == id)
    if pet:
        return {
            "id": pet.id,
            "name": pet.name,
            "kind_id": pet.kind.id,
            "age": pet.age,
            "owner_id": pet.owner.id,
        }
    return "Data not found."


def get_kind(id: int):
    """
    Retrieve a single kind by its ID.
    Returns a dictionary or a 'Data not found.' message if no kind is found.
    """
    kind = Kind.get_or_none(Kind.id == id)
    if kind:
        return {"id": kind.id, "name": kind.name, "food": kind.food, "sound": kind.sound}
    return "Data not found."


def get_owner(id: int):
    """
    Retrieve a single owner by its ID.
    Returns a dictionary or a 'Data not found' message if no owner is found.
    """
    owner = Owner.get_or_none(Owner.id == id)
    if owner:
        return {"id": owner.id, "name": owner.name, "address": owner.address}
    return "Data not found"


def create_pet(data: dict) -> None:
    """
    Insert a new pet record using the provided data dictionary.
    Keys expected: "name", "age", "kind_id", "owner_id".
    """
    try:
        data["age"] = int(data["age"])
    except Exception:
        data["age"] = 0
    Pet.create(name=data["name"], age=data["age"], kind=data["kind_id"], owner=data["owner_id"])


def create_kind(data: dict) -> None:
    """
    Insert a new kind record using the provided data dictionary.
    Keys expected: "name", "food", "sound".
    """
    Kind.create(name=data["name"], food=data["food"], sound=data["sound"])


def create_owner(data: dict) -> None:
    """
    Insert a new owner record using the provided data dictionary.
    Keys expected: "name", "address".
    """
    Owner.create(name=data["name"], address=data["address"])


def test_create_pet():
    """Placeholder for a pet creation test (not implemented)."""
    pass


def update_pet(id: int, data: dict) -> None:
    """
    Update an existing pet record identified by id with new data.
    Keys expected in data: "name", "age", "kind_id", "owner_id".
    """
    try:
        data["age"] = int(data["age"])
    except Exception:
        data["age"] = 0
    (
        Pet.update(
            name=data["name"],
            age=data["age"],
            kind=data["kind_id"],
            owner=data["owner_id"],
        )
        .where(Pet.id == id)
        .execute()
    )


def update_kind(id: int, data: dict) -> None:
    """
    Update an existing kind record identified by id with new data.
    Keys expected: "name", "food", "sound".
    """
    (
        Kind.update(name=data["name"], food=data["food"], sound=data["sound"])
        .where(Kind.id == id)
        .execute()
    )


def update_owner(id: int, data: dict) -> None:
    """
    Update an existing owner record identified by id with new data.
    Keys expected: "name", "address".
    """
    (
        Owner.update(name=data["name"], address=data["address"])
        .where(Owner.id == id)
        .execute()
    )


def delete_pet(id: int) -> None:
    """Delete a pet by its ID."""
    Pet.delete().where(Pet.id == id).execute()


def delete_kind(id: int) -> None:
    """Delete a kind by its ID."""
    Kind.delete().where(Kind.id == id).execute()


def delete_owner(id: int) -> None:
    """Delete an owner by its ID."""
    Owner.delete().where(Owner.id == id).execute()


def setup_test_database() -> None:
    """
    Set up a test database with sample data.
    Drops and recreates tables, inserts kinds, owners, pets, and asserts the number of pets.
    """
    initialize("test_pets.db")
    db.drop_tables([Pet, Kind, Owner])
    db.create_tables([Kind, Owner, Pet])

    # Insert sample kinds
    Kind.create(name="dog", food="dogfood", sound="bark")
    Kind.create(name="cat", food="catfood", sound="meow")

    # Insert sample owners
    greg = Owner.create(name="Greg", address="1365 Maple Ave.")
    david = Owner.create(name="David", address="13 Elm St.")

    # Insert sample pets
    pets = [
        {"name": "dorothy", "kind_id": 1, "age": 9, "owner_id": greg.id},
        {"name": "suzy", "kind_id": 1, "age": 9, "owner_id": greg.id},
        {"name": "casey", "kind_id": 2, "age": 9, "owner_id": greg.id},
        {"name": "heidi", "kind_id": 2, "age": 15, "owner_id": david.id},
    ]
    for pet_data in pets:
        create_pet(pet_data)

    # Verify that all four pets were added
    assert len(get_pets()) == 4


def test_get_pets():
    """Test the get_pets function for correct structure and types."""
    print("testing get_pets")
    pets = get_pets()
    assert isinstance(pets, list)
    assert len(pets) > 0
    assert isinstance(pets[0], dict)
    pet = pets[0]
    print(pet)
    for field in ["id", "name", "age", "owner", "kind_name", "food", "sound"]:
        assert field in pet, f"Field {field} missing from {pet}"
    assert isinstance(pet["id"], int)
    assert isinstance(pet["name"], str)


def test_get_kinds():
    """Test the get_kinds function for correct structure and types."""
    print("testing get_kinds")
    kinds = get_kinds()
    assert isinstance(kinds, list)
    assert len(kinds) > 0
    assert isinstance(kinds[0], dict)
    kind = kinds[0]
    for field in ["id", "name", "food", "sound"]:
        assert field in kind, f"Field {field} missing from {kind}"
    assert isinstance(kind["id"], int)
    assert isinstance(kind["name"], str)


def test_get_owners():
    """Test the get_owners function for correct structure and types."""
    print("testing get_owners")
    owners = get_owners()
    assert isinstance(owners, list)
    assert len(owners) > 0
    assert isinstance(owners[0], dict)
    owner = owners[0]
    for field in ["id", "name", "address"]:
        assert field in owner, f"Field {field} missing from {owner}"
    assert isinstance(owner["id"], int)
    assert isinstance(owner["name"], str)
    assert isinstance(owner["address"], str)


if __name__ == "__main__":
    # Run tests to ensure functionality matches the original API
    setup_test_database()
    test_get_pets()
    test_get_kinds()
    test_get_owners()
    test_create_pet()
    print("done.")
