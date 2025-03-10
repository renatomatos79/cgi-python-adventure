<p align="center">
  <img src="https://github.com/renatomatos79/cgi-python-adventure/blob/main/images/consoleapp.PNG" height="400px" width="400px" alt="consoleapp">
</p>


# Quick setup

## Starting with a fresh git project
```
git config --global init.defaultBranch main && git init --quiet
```

## Installing python
https://www.python.org/downloads/release/python-3132/

# Let´s build our first project

### Add a new folder "py-from-zero-to-hero-01"
```
mkdir py-from-zero-to-hero-01
cd py-from-zero-to-hero-01
```

### So, then let´s build a dynamic environment named "capp"
```
python -m venv capp (capp is just an alias for "Console Application")
```

### And activate our new dynamic env "capp"
```
.\capp\Scripts\activate
```

### Rather than installing packages one by one, let´s use our dependencies file :)
```
pip install -r .\requirements.txt
```

### Finally, we should confirm whether our packages were properly installed
```
pip list
```

### Please, don´t run this command right now! 
### This is just a minor note demoing how to "deactivate" a dyn env 
```
.\capp\Scripts\deactivate
```

## Time to play with Database

### (1) Create a file named database.py and paste the script below
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite Database
DATABASE_URL = "sqlite:///users_groups.db"

# Factory function to create a Database connection
# When echo=True is set, SQLAlchemy prints all SQL statements executed under the hood.
engine = create_engine(DATABASE_URL, echo=False)

# Creates a Session Factory to ensure that every database transaction occurs inside a session.
SessionLocal = sessionmaker(bind=engine)
```

The script above imports the create_engine and sessionmaker functions from the SQLAlchemy package to set up and map the users_groups.db database.
At the bottom, these two objects are now available for import:

- engine
- SessionLocal

This allows us to create a new isolated session to interact with the database.
```
session = SessionLocal()
user = session.query(User).first() 
```

And leveraging the engine object let´s provide our Entity Models
```
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Define a User Model
class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True)
name = Column(String, nullable=False)

# Create Tables
Base.metadata.create_all(engine)
```

### (2) Create a file named model.py and paste the script below
```
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from database import engine

Base = declarative_base()

# Many-to-Many Association Table (Group x User)
user_group_association = Table(
"user_group",
Base.metadata,
Column("user_id", Integer, ForeignKey("users.id")),
Column("group_id", Integer, ForeignKey("groups.id")),
)

# User Model
class User(Base):
__tablename__ = "users"

    # Fields defs
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Many-to-Many Relationship
    groups = relationship("Group", secondary=user_group_association, back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"

# Group Model
class Group(Base):
__tablename__ = "groups"

    # Fields defs
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Many-to-Many Relationship
    users = relationship("User", secondary=user_group_association, back_populates="groups")

    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}')"

# Create tables in the database
Base.metadata.create_all(engine)
```

### So, finally, let´s put everything together adding a new file named "app.py"
```
from sqlalchemy.orm import Session
from models import User, Group
from database import SessionLocal
import os

def create_user(session, name):
    """Creates a new user"""
    user = User(name=name)
    session.add(user)
    session.commit()
    print(f"User '{name}' created!")

def create_group(session, name):
    """Creates a new group"""
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Group '{name}' created!")

....

def main():
    session = SessionLocal()

    while True:
        print("\n Choose an option:")
        print("(1)  Add User")
        print("(2)  Add Group")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            create_user(session, name)

        elif choice == "2":
            name = input("Enter group name: ")
            create_group(session, name)

        ....

    session.close()

if __name__ == "__main__":
    main()

```

### Running the app
```
python app.py
```

# So, let's run a quick demo to showcase what we've accomplished so far.
![demo](https://github.com/user-attachments/assets/2dd2697b-fa14-4858-85bf-0d3c773d8e3c)


