from database import get_conn

def get_single(table, data):
    conn = get_conn()
    cursor = conn.cursor()
    query = ("SELECT * FROM {} WHERE id = {};").format(table, data['id'])

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    return rows


def exists(table, data):
    res = get_single(table, data)
    return len(res) != 0

def create(table, data):
    conn = get_conn()
    cursor = conn.cursor()

    temp = ""
    values = ""
    for k, v in data.items():
        temp += "{},".format(k)
        values += "'{}',".format(v)
    temp = temp[:-1]
    values = values[:-1]

    query = ("INSERT INTO {} ({}) VALUES ({});").format(table, temp, values)

    cursor.execute(query)
    res = cursor.lastrowid
    cursor.close()
    conn.commit()
    conn.close()

    return res

def get_all(table):
    conn = get_conn()
    cursor = conn.cursor()
    query = ("SELECT * FROM {};").format(table)

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    return rows

def delete(table, data):

    if not exists(table, data):
        return True

    conn = get_conn()
    cursor = conn.cursor()
    query = ("DELETE FROM {} WHERE id = {};").format(table, data['id'])

    cursor.execute(query)

    cursor.close()
    conn.commit()
    conn.close()

    return True

def edit(table, data):

    if not exists(table, data):
        return False

    conn = get_conn()
    cursor = conn.cursor()
    temp = ""

    for k, v in data.items():
        temp += "{} = '{}',".format(k, v)
    temp = temp[:-1]

    query = ("UPDATE {} SET {} WHERE id={}").format(table, temp, data["id"])

    cursor.execute(query)

    cursor.close()
    conn.commit()
    conn.close()

    return True

def perform_action(action, table, data):
    if action == 'get_single':
        return get_single(table, data)
    
    if action == 'get_all':
        return get_all(table)

    if action == 'create':
        return create(table, data)

    if action == 'delete':
        return delete(table, data)

    if action == 'edit':
        return edit(table, data) 
