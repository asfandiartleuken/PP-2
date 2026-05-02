CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name LIMIT 1;
    IF FOUND THEN
        INSERT INTO phones(contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE NOTICE 'Contact % not found', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- create group if not exists
    INSERT INTO groups(name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;


DROP FUNCTION IF EXISTS search_contacts(TEXT);
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, c.name, c.surname, c.email, c.birthday, g.name::VARCHAR AS group_name,
        string_agg(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.surname ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR EXISTS (
           SELECT 1 FROM phones p2 WHERE p2.contact_id = c.id AND p2.phone ILIKE '%' || p_query || '%'
       )
    GROUP BY c.id, g.name
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT, TEXT);
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT, sort_column TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    email VARCHAR,
    birthday DATE,
    created_at TIMESTAMP,
    group_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT c.id, c.name, c.surname, c.email, c.birthday, c.created_at, g.name::VARCHAR AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY %I
        LIMIT $1 OFFSET $2
    ', sort_column) USING lim, off;
END;
$$ LANGUAGE plpgsql;
