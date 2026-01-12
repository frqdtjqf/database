from backend.sql_api import DataBaseWrapper, Table, Attribute, Element, Record

DB_NAME = "testing.db"  # in-memory DB for testing

def test_db():

    # -------------------------------
    # 1️⃣ Define test tables
    # -------------------------------
    USER_ATTRIBUTES = [
        Attribute(name="id", type="TEXT", primary_key=True),
        Attribute(name="name", type="TEXT")
    ]
    POST_ATTRIBUTES = [
        Attribute(name="id", type="TEXT", primary_key=True),
        Attribute(name="user_id", type="TEXT", foreign_key=("users", "id")),
        Attribute(name="content", type="TEXT")
    ]

    USER_TABLE = Table(name="users", attributes=USER_ATTRIBUTES)
    POST_TABLE = Table(name="posts", attributes=POST_ATTRIBUTES)

    # -------------------------------
    # 2️⃣ Create wrapper
    # -------------------------------
    db = DataBaseWrapper(DB_NAME)
    db.create_table(USER_TABLE)
    db.create_table(POST_TABLE)

    # -------------------------------
    # 3️⃣ Insert test data
    # -------------------------------
    # insert user
    user_record = Record(elements=[
        Element(attribute=USER_ATTRIBUTES[0], value="u1"),
        Element(attribute=USER_ATTRIBUTES[1], value="Alice")
    ])
    db.insert_record(USER_TABLE, user_record)

    # insert a valid post (user exists)
    post_record = Record(elements=[
        Element(attribute=POST_ATTRIBUTES[0], value="p1"),
        Element(attribute=POST_ATTRIBUTES[1], value="u1"),  # FK to user
        Element(attribute=POST_ATTRIBUTES[2], value="Hello world")
    ])
    db.insert_record(POST_TABLE, post_record)

    # -------------------------------
    # 4️⃣ Try invalid post (should fail FK)
    # -------------------------------
    invalid_post = Record(elements=[
        Element(attribute=POST_ATTRIBUTES[0], value="p2"),
        Element(attribute=POST_ATTRIBUTES[1], value="u2"),  # non-existent user
        Element(attribute=POST_ATTRIBUTES[2], value="Bad post")
    ])

    try:
        db.insert_record(POST_TABLE, invalid_post)
    except Exception as e:
        print("Foreign key prevented insert:", e)

    # -------------------------------
    # 5️⃣ Fetch and print
    # -------------------------------
    print("Users:", db.get_records(USER_TABLE))
    print("Posts:", db.get_records(POST_TABLE))



