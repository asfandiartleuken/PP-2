import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def insert_from_console():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_csv(filename="contacts.csv"):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["name"].strip()
                phone = row["phone"].strip()

                cur.execute("""
                    INSERT INTO phonebook (name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                """, (name, phone))

        conn.commit()
        print("CSV data imported successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def update_contact():
    print("1. Update name by phone")
    print("2. Update phone by name")
    choice = input("Choose option: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            phone = input("Enter current phone: ").strip()
            new_name = input("Enter new name: ").strip()
            cur.execute(
                "UPDATE phonebook SET name = %s WHERE phone = %s",
                (new_name, phone)
            )
        elif choice == "2":
            name = input("Enter current name: ").strip()
            new_phone = input("Enter new phone: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE name = %s",
                (new_phone, name)
            )
        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()
        print("Contact updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def query_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, name, phone FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def query_by_name():
    name = input("Enter name to search: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s",
        (f"%{name}%",)
    )
    rows = cur.fetchall()

    if not rows:
        print("No matching contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def query_by_phone_prefix():
    prefix = input("Enter phone prefix: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s",
        (f"{prefix}%",)
    )
    rows = cur.fetchall()

    if not rows:
        print("No matching contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose option: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter name: ").strip()
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ").strip()
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            cur.close()
            conn.close()
            return

        conn.commit()
        print("Contact deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact from console")
        print("3. Import contacts from CSV")
        print("4. Update contact")
        print("5. Show all contacts")
        print("6. Search by name")
        print("7. Search by phone prefix")
        print("8. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_all_contacts()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_phone_prefix()
        elif choice == "8":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()