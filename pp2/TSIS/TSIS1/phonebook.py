# CSV файлдармен жұмыс істеу модулі / Модуль для работы с CSV файлами
import csv
# JSON файлдармен жұмыс істеу модулі / Модуль для работы с JSON файлами
import json
# Файлдық жүйемен жұмыс істеу модулі (файлдың бар-жоғын тексеру үшін) / Модуль для работы с ОС и путями
import os
# Біз жасаған деректер базасына қосылу функциясын импорттау / Импорт функции подключения к БД
from connect import connect

def setup_database():
    """
    Деректер базасын орнату (кестелер мен процедураларды құру)
    Настройка базы данных: создание таблиц из schema.sql и процедур из procedures.sql
    """
    conn = connect() # Базаға қосылу / Подключение к БД
    cur = conn.cursor() # SQL сұрауларды жіберу үшін курсор құру / Создание курсора для выполнения SQL
    try:
        # schema.sql файлын оқып, орындау / Читаем и выполняем файл со схемой БД (создание таблиц)
        with open("schema.sql", "r") as f:
            cur.execute(f.read())
        # procedures.sql файлын оқып, орындау / Читаем и выполняем файл с SQL-процедурами
        with open("procedures.sql", "r") as f:
            cur.execute(f.read())
        conn.commit() # Өзгерістерді сақтау / Подтверждаем и сохраняем изменения (commit)
        print("Database schema and procedures setup successfully.") # Табысты аяқталғанын хабарлау / Успех
    except Exception as e:
        conn.rollback() # Қате болса, өзгерістерді кері қайтару / Если ошибка - откатываем изменения (rollback)
        print("Error setting up database:", e)
    finally:
        cur.close() # Курсорды жабу / Закрываем курсор
        conn.close() # Қосылымды жабу / Закрываем соединение с БД

def add_contact_console():
    """
    Консоль арқылы жаңа контакт қосу
    Добавление нового контакта через консольный ввод
    """
    # Пайдаланушыдан мәліметтерді сұрау және бос орындарды алып тастау / Запрашиваем данные и удаляем лишние пробелы (strip)
    name = input("Enter name: ").strip()
    surname = input("Enter surname: ").strip()
    email = input("Enter email: ").strip()
    birthday = input("Enter birthday (YYYY-MM-DD) or leave empty: ").strip()
    
    # Егер туған күн бос болса, оны None (SQL-де NULL) қыламыз / Если дата рождения не введена, ставим None (NULL в БД)
    if not birthday:
        birthday = None
        
    conn = connect()
    cur = conn.cursor()
    try:
        # Жаңа контактіні contacts кестесіне қосу / Вставляем контакт в таблицу contacts
        # RETURNING id арқылы жаңа құрылған ID-ді қайтарады / RETURNING id позволяет получить ID новой записи
        cur.execute(
            "INSERT INTO contacts (name, surname, email, birthday) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, surname, email, birthday)
        )
        conn.commit()
        print("Contact added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def add_phone():
    """
    Бар контактіге телефон нөмірін қосу
    Добавление телефонного номера существующему контакту
    """
    contact_name = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()
    p_type = input("Enter phone type (home/work/mobile): ").strip() # Тип номера
    
    conn = connect()
    cur = conn.cursor()
    try:
        # Арнайы SQL процедурасын (add_phone) шақыру / Вызов SQL-процедуры add_phone
        cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, p_type))
        conn.commit()
        print("Phone added if contact exists (check notices).")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def move_to_group():
    """
    Контактіні белгілі бір топқа (Group) көшіру
    Перемещение (привязка) контакта к определенной группе
    """
    contact_name = input("Enter contact name: ").strip()
    group_name = input("Enter group name: ").strip()
    
    conn = connect()
    cur = conn.cursor()
    try:
        # move_to_group процедурасын шақыру / Вызов хранимой процедуры move_to_group
        cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        conn.commit()
        print("Contact moved to group successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def search_by_pattern():
    """
    Паттерн бойынша іздеу (аты, почтасы немесе телефоны бойынша)
    Поиск контактов по паттерну (имя, email или номер телефона)
    """
    pattern = input("Enter search pattern (name/email/phone): ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        # search_contacts функциясын орындап, нәтижелерін алу / Вызов SQL-функции search_contacts
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall() # Барлық табылған жолдарды алу / Извлекаем все строки результата
        if not rows:
            print("No contacts found.")
        else:
            for row in rows:
                print(row) # Әр нәтижені экранға шығару / Печать каждого найденного контакта
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def filter_by_group():
    """
    Топ атауы бойынша контактілерді сүзу
    Фильтрация и вывод контактов по названию группы
    """
    group_name = input("Enter group name to filter: ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        # contacts және groups кестелерін JOIN арқылы біріктіріп, топ аты бойынша іздеу
        # SQL-запрос с JOIN для получения контактов, принадлежащих к заданной группе
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, g.name 
            FROM contacts c 
            JOIN groups g ON c.group_id = g.id 
            WHERE g.name = %s
        """, (group_name,))
        rows = cur.fetchall()
        if not rows:
            print("No contacts found in this group.")
        else:
            for row in rows:
                print(row)
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def paginate_contacts():
    """
    Контактілерді парақтап (бет-бетке бөліп) шығару (Pagination)
    Пагинация контактов (вывод по страницам с сортировкой)
    """
    limit = int(input("Enter limit per page: ")) # Бір беттегі максималды контактілер саны / Лимит на странице
    
    # Сұрыптау (сортировка) критерийлерін ұсыну / Выбор поля для сортировки
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date Added (created_at)")
    sort_choice = input("Choice: ").strip()
    
    # Таңдауға сәйкес баған (колонна) атауын алу / Словарь для преобразования выбора в имя колонки
    sort_map = {"1": "name", "2": "birthday", "3": "created_at"}
    sort_column = sort_map.get(sort_choice, "name") # По умолчанию 'name'
    
    offset = 0 # Бастапқы нүкте (ығысу) / Смещение для пагинации
    conn = connect()
    cur = conn.cursor()
    
    while True:
        try:
            # get_contacts_paginated SQL функциясын шақыру / Вызов функции пагинации
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s, %s)", (limit, offset, sort_column))
            rows = cur.fetchall()
            print(f"\n--- Page {offset // limit + 1} ---") # Бет нөмірі / Номер страницы
            
            if not rows:
                print("No more contacts.")
            else:
                for row in rows:
                    print(row)
            
            # Келесі/алдыңғы бетке өту немесе шығу / Управление страницами
            cmd = input("\nEnter 'next', 'prev', or 'quit': ").strip().lower()
            if cmd == 'next':
                offset += limit # Келесі бетке өту / Переход на следующую страницу (увеличиваем offset)
            elif cmd == 'prev':
                offset = max(0, offset - limit) # Алдыңғы бетке өту (0-ден төмен болмауы тиіс) / Переход назад
            elif cmd == 'quit':
                break # Циклді тоқтату / Выход из режима пагинации
            else:
                print("Invalid command.")
        except Exception as e:
            print("Error:", e)
            break
            
    cur.close()
    conn.close()

def import_csv():
    """
    CSV файлынан контактілерді жүктеу (импорттау)
    Импорт контактов из CSV файла
    """
    filename = input("Enter CSV filename (default contacts.csv): ").strip()
    if not filename:
        filename = "contacts.csv" # Үнсіз келісім бойынша файл атауы / Имя по умолчанию
        
    conn = connect()
    cur = conn.cursor()
    try:
        # CSV файлын ашу / Открытие файла в режиме чтения с кодировкой utf-8
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file) # Сөздік ретінде оқу / Чтение файла как словаря (на основе заголовков)
            for row in reader:
                # Мәліметтерді қауіпсіз алу (бос болса "" қоямыз) / Безопасное извлечение данных
                name = row.get("name", "").strip()
                surname = row.get("surname", "").strip()
                email = row.get("email", "").strip()
                birthday = row.get("birthday", "").strip() or None
                group_name = row.get("group_name", "").strip()
                phone = row.get("phone", "").strip()
                p_type = row.get("type", "").strip()
                
                # Insert contact / Вставка контакта в базу и получение его сгенерированного ID
                cur.execute("""
                    INSERT INTO contacts (name, surname, email, birthday)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (name, surname, email, birthday))
                contact_id = cur.fetchone()[0] # Алынған ID-ді сақтау / Сохраняем ID нового контакта
                
                # Move to group if provided / Если указана группа, привязываем контакт к группе
                if group_name:
                    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
                
                # Add phone if provided / Если указан номер телефона, добавляем его в таблицу phones
                if phone and p_type:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (contact_id, phone, p_type))
                    
        conn.commit() # CSV-дағы барлық өзгерістерді сақтау / Фиксируем все вставки
        print("CSV imported successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def export_json():
    """
    Деректерді JSON форматына экспорттау
    Экспорт всех контактов с их телефонами и группами в JSON файл
    """
    filename = input("Enter JSON filename (default contacts.json): ").strip()
    if not filename:
        filename = "contacts.json"
        
    conn = connect()
    cur = conn.cursor()
    try:
        # SQL сұрау арқылы барлық мәліметті (телефондарды JSON массивіне жинақтап) алу
        # Сложный запрос с использованием json_agg для агрегации телефонов в JSON массив прямо на стороне СУБД
        cur.execute("""
            SELECT 
                c.id, c.name, c.surname, c.email, c.birthday, g.name AS group_name,
                (SELECT json_agg(json_build_object('phone', p.phone, 'type', p.type)) 
                 FROM phones p WHERE p.contact_id = c.id) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
        """)
        rows = cur.fetchall()
        
        data = []
        for row in rows:
            # Әр жолды Python сөздігіне (Dictionary) айналдыру / Преобразование строки результата в словарь
            data.append({
                "id": row[0],
                "name": row[1],
                "surname": row[2],
                "email": row[3],
                "birthday": str(row[4]) if row[4] else None, # Күнді жолға (string) айналдыру / Форматируем дату
                "group_name": row[5],
                "phones": row[6] or [] # Егер телефон болмаса, бос массив [] қоямыз / Если телефонов нет - пустой список
            })
            
        # Сөздікті JSON файлына жазу / Запись списка словарей в JSON файл с красивыми отступами (indent=4)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Exported successfully to JSON.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def import_json():
    """
    JSON файлынан деректерді деректер базасына жүктеу
    Импорт контактов из JSON файла с обработкой дубликатов
    """
    filename = input("Enter JSON filename (default contacts.json): ").strip()
    if not filename:
        filename = "contacts.json"
        
    # Файлдың бар-жоғын тексеру / Проверка существования файла
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
        
    # JSON файлын оқу / Чтение JSON файла в переменную data (будет списком словарей)
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    conn = connect()
    cur = conn.cursor()
    
    # Әр контактіні жеке-жеке өңдеу / Перебираем каждый контакт из JSON
    for item in data:
        name = item.get("name")
        surname = item.get("surname")
        email = item.get("email")
        birthday = item.get("birthday")
        group_name = item.get("group_name")
        phones = item.get("phones", [])
        
        # Check if exists: Осындай атпен контакт бар-жоғын тексеру / Проверяем, существует ли контакт с таким именем
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        
        # Егер бар болса, пайдаланушыдан не істеу керектігін сұрау / Если контакт существует, спрашиваем: пропустить или перезаписать
        if existing:
            action = input(f"Contact '{name}' already exists. Skip or Overwrite? (s/o): ").strip().lower()
            if action == 's':
                print(f"Skipping '{name}'...")
                continue # Келесіге өту / Пропускаем и идем к следующему контакту
            elif action == 'o':
                print(f"Overwriting '{name}'...")
                # Ескіні өшіреміз / Удаляем старый контакт (каскадное удаление должно удалить и телефоны, если настроено БД)
                cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
        
        try:
            # Жаңа контактіні енгізу / Вставка нового контакта
            cur.execute("""
                INSERT INTO contacts (name, surname, email, birthday)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (name, surname, email, birthday))
            contact_id = cur.fetchone()[0] # Получаем ID
            
            # Топқа қосу / Перемещение в группу
            if group_name:
                cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
                
            # Телефондарын қосу / Вставка всех телефонов, привязанных к контакту
            for p in phones:
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                            (contact_id, p.get("phone"), p.get("type")))
                            
            conn.commit() # Әр сәтті контактіден кейін сақтау / Фиксация изменений для текущего контакта
        except Exception as e:
            conn.rollback()
            print("Error importing contact:", e)
            
    cur.close()
    conn.close()
    print("JSON import finished.")

def menu():
    """
    Бағдарламаның негізгі мәзірі
    Главное меню консольного приложения
    """
    while True:
        # Пайдаланушыға мүмкіндіктер тізімін көрсету / Вывод опций меню на экран
        print("\n--- EXTENDED PHONEBOOK MENU ---")
        print("1. Setup Database (creates tables & procedures)")
        print("2. Add Contact (Console)")
        print("3. Add Phone to Contact")
        print("4. Move Contact to Group")
        print("5. Search Contacts by Pattern")
        print("6. Filter Contacts by Group")
        print("7. Paginated Contacts Navigation")
        print("8. Import from CSV")
        print("9. Export to JSON")
        print("10. Import from JSON")
        print("0. Exit")
        
        # Таңдауды қабылдау / Чтение выбора пользователя
        choice = input("Enter choice: ").strip()
        
        # Таңдау бойынша сәйкес функцияны шақыру / Вызов соответствующей функции в зависимости от выбора
        if choice == "1": setup_database()
        elif choice == "2": add_contact_console()
        elif choice == "3": add_phone()
        elif choice == "4": move_to_group()
        elif choice == "5": search_by_pattern()
        elif choice == "6": filter_by_group()
        elif choice == "7": paginate_contacts()
        elif choice == "8": import_csv()
        elif choice == "9": export_json()
        elif choice == "10": import_json()
        elif choice == "0":
            print("Goodbye!")
            break # Циклді тоқтату, бағдарламадан шығу / Выход из бесконечного цикла
        else:
            print("Invalid choice.") # Қате енгізу / Неверный ввод

# Если скрипт запускается напрямую, а не импортируется, вызываем функцию menu()
if __name__ == "__main__":
    menu()
