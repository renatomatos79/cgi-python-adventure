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
