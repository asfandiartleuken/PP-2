from connect import connect


def call_upsert():
    name = input("Enter name: ").strip()
    surname = input("Enter surname: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL upsert_contact(%s, %s, %s)", (name, surname, phone))
        conn.commit()
        print("Contact inserted or updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def search_by_pattern():
    pattern = input("Enter pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def bulk_insert():
    n = int(input("How many contacts do you want to insert? "))

    names = []
    surnames = []
    phones = []

    for i in range(n):
        print(f"\nContact {i + 1}")
        names.append(input("Name: ").strip())
        surnames.append(input("Surname: ").strip())
        phones.append(input("Phone: ").strip())

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL insert_many_contacts(%s, %s, %s)", (names, surnames, phones))
        conn.commit()
        print("Bulk insert completed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def paginate_contacts():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Contact deleted if it existed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1. Upsert contact")
        print("2. Search by pattern")
        print("3. Bulk insert contacts")
        print("4. Show contacts with pagination")
        print("5. Delete by name or phone")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            call_upsert()
        elif choice == "2":
            search_by_pattern()
        elif choice == "3":
            bulk_insert()
        elif choice == "4":
            paginate_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()