from sqlalchemy.orm import Session
from models import User, Group
from database import SessionLocal
import os

def clear_screen():
    # For Windows, os.name returns 'nt', once Windows is based on the "Windows NT kernel"
    # For Linux/macOS, os.name returns 'posix'
    os.system('cls' if os.name == 'nt' else 'clear')

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

def assign_user_to_group_by_id(session, user_id, group_id):
    """Assigns a user to a group"""
    user = session.get(User, user_id)
    group = session.get(Group, group_id)

    if user and group:
        user.groups.append(group)
        session.commit()
        print(f"User '{user.name}' added to Group '{group.name}'")
    else:
        print("Invalid user or group ID.")

def assign_user_to_group_by_name(session, user_name, group_name):
    """Assigns a user to a group"""
    user = session.query(User).filter(User.name.like(f"%{user_name}%")).first()
    group = session.query(Group).filter(Group.name.like(f"%{group_name}%")).first()

    if user and group:
        user.groups.append(group)
        session.commit()
        print(f"User '{user.name}' added to Group '{group.name}'")
    else:
        print("Invalid user or group name.")

def list_users_and_groups(session):
    """Lists all users with their assigned groups"""
    users = session.query(User).all()
    for user in users:
        group_names = [obj.name for obj in user.groups]
        print(f"👤 {user.id}, {user.name}: Groups → {', '.join(group_names) if group_names else 'No Groups'}")

def list_groups_and_users(session):
    """Lists all groups with their assigned users"""
    groups = session.query(Group).all()
    for group in groups:
        user_names = [user.name for user in group.users]
        print(f"👤 {group.id}, {group.name}: Users → {', '.join(user_names) if user_names else 'No Users'}")

def main():
    session = SessionLocal()

    while True:
        print("\n Choose an option:")
        print("(1)  Add User")
        print("(2)  Add Group")
        print("(3)  Assign User to Group - BY ID")
        print("(31) Assign User to Group - BY Name")
        print("(4)  List Users & Groups")
        print("(5)  List Groups & Users")
        print("(9)  Exit")
        choice = input("Enter choice: ")

        # clean the whole screen before running any command
        clear_screen()

        if choice == "1":
            name = input("Enter user name: ")
            create_user(session, name)

        elif choice == "2":
            name = input("Enter group name: ")
            create_group(session, name)

        elif choice == "3":
            user_id = int(input("Enter User ID: "))
            group_id = int(input("Enter Group ID: "))
            assign_user_to_group_by_id(session, user_id, group_id)

        elif choice == "31":
            user_name = input("Enter User Name: ")
            group_name = input("Enter Group Name: ")
            assign_user_to_group_by_name(session, user_name, group_name)

        elif choice == "4":
            list_users_and_groups(session)

        elif choice == "5":
            list_groups_and_users(session)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

    session.close()

if __name__ == "__main__":
    main()
