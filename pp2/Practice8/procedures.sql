CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;

    ELSIF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE phone = p_phone
    ) THEN
        UPDATE phonebook
        SET name = p_name,
            surname = p_surname
        WHERE phone = p_phone;

    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names TEXT[],
    p_surnames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1)
    LOOP
        IF p_phones[i] ~ '^[0-9]{11,15}$' THEN
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE name = p_names[i] AND surname = p_surnames[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE name = p_names[i] AND surname = p_surnames[i];

            ELSIF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE phone = p_phones[i]
            ) THEN
                UPDATE phonebook
                SET name = p_names[i],
                    surname = p_surnames[i]
                WHERE phone = p_phones[i];

            ELSE
                INSERT INTO phonebook(name, surname, phone)
                VALUES (p_names[i], p_surnames[i], p_phones[i]);
            END IF;
        ELSE
            RAISE NOTICE 'Incorrect data: %, %, %',
                p_names[i], p_surnames[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR phone = p_value;
END;
$$;