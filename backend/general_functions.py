from flask import Flask, request, jsonify
import datetime

from database import conn

def get_single(table, data, **kwargs):
    conn.connect()
    
    temp = ""
    for k, v in data.items():
        if isinstance(v, str):
            temp += "{} = '{}' and ".format(k, v)
        else:
            temp += "{} = {} and ".format(k, v)
    temp = temp[:-5]

    query = ("SELECT * FROM {} WHERE {}").format(table, temp)

    conn.cursor.execute(query)
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


def get_all(table, **kwargs):
    conn.connect()

    query = (f"SELECT * FROM {table}")
    conn.cursor.execute(query)
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


def exists(table, data):
    res = get_single(table, data)
    return len(res) != 0


def action_create(table, data, **kwargs):
    conn.connect()

    temp = ""
    values = ""
    for k, v in data.items():
        temp += "{},".format(k)
        values += "'{}',".format(v)
    temp = temp[:-1]
    values = values[:-1]

    query = ("INSERT INTO {} ({}) VALUES ({});").format(table, temp, values)

    conn.cursor.execute(query)
    conn.cnx.commit()

    return conn.cursor.lastrowid


def action_delete(table, data, **kwargs):
    conn.connect()

    if not exists(table, data):
        return {"response": "failed", "reason": "data exists"}

    temp = ""
    for k, v in data.items():
        if isinstance(v, str):
            temp += "{} = '{}' and ".format(k, v)
        else:
            temp += "{} = {} and ".format(k, v)
    temp = temp[:-5]

    query = ("DELETE FROM {} WHERE {};").format(table, temp)
    conn.cursor.execute(query)
    conn.cnx.commit()

    return {"response": "sucess"}


primary_keys = {
    'person' : ['medicareNumber'],
    'publicHealthWorker' : ['workerID'],
    'publicHealthCenter' : ['id'],
    'region' : ['name'],
    'groupZone' : ['groupID'],
    'healthRecommendation' : ['id'],
    'healthRecommendationSecondary': ['id', 'recommendation']
}


def action_edit(table, data, **kwargs):
    conn.connect()

    ids = {}
    datas = {}

    for key, value in data.items():
        if key in primary_keys[table]:
            ids[key] = value
        else:
            datas[key] = value

    if not exists(table, ids):
        return {"response": "failed", "reason": "data doesn't exist"}

    temp = ""
    for k, v in datas.items():
        if isinstance(v, str):
            temp += "{} = '{}',".format(k, v)
        else:
            temp += "{} = {},".format(k, v)
    temp = temp[:-1]

    temp2 = ""
    for k, v in ids.items():
        if isinstance(v, str):
            temp2 += "{} = '{}' and ".format(k, v)
        else:
            temp2 += "{} = {} and ".format(k, v)
    temp2 = temp2[:-5]

    query = ("UPDATE {} SET {} WHERE {};").format(table, temp, temp2)
    
    conn.cursor.execute(query)
    conn.cnx.commit()

    return {"response": "success"}


# 7- set new alert for a specific region
def get_previous_alert(region_name):
    conn.connect()

    query = (
        f"""SELECT DISTINCT alertLevel, date
            FROM alert
            WHERE regionName = '{region_name}'
            ORDER BY date DESC
            LIMIT 1
        """)

    conn.cursor.execute(query)

    resp = conn.cursor.fetchall()
    if conn.cursor is not None:
        return conn.cursor['alertLevel']


def set_region_alert(data):
    conn.connect()

    previous_alert = get_previous_alert(data['regionName'])

    if data['alertLevel'] <= 0 or data['alertLevel'] > 4:
        raise Exception('invalid alert level')
    
    if (data['alertLevel'] + 1 is not previous_alert) and (data['alertLevel'] - 1 is not previous_alert):
        raise Exception('cannot set alert to this level')

    action_create('alert', data)


# 13- list of all regions
def get_regions():
    rows = get_all('region')
    for region in rows:
        cities = get_single('city', {'regionName' : region['name']})

        for city in cities:
            postal_codes = get_single('cityPostalCodeMapping', {'city' : city['name']})
            temp = list(map(lambda x: x['postalCodeRegion'], postal_codes))
            city['postalCodes'] = temp
            city.pop('regionName', None)

        region['cities'] = cities
        region.pop('alertLevel', None)

    return rows


# 14- list of people who got the result of the test on a specific date
def get_test_result_on_date(data):
    conn = conn.connect()
    conn.cursor = conn.conn.cursor()
    
    query = (
        f"""SELECT P.firstName, P.lastName, P.dateOfBirth, P.phoneNumber, P.email, D.result
                FROM
                (SELECT medicareNumber, result
                    FROM diagnostic
                    WHERE testDate = '{data['testDate']}') as D, person as P
                WHERE P.medicareNumber = D.medicareNumber
                ORDER BY D.result DESC
        """)

    conn.cursor.execute(query)

    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


# 15- list of workers in specific facility
def get_workers_at_facility(data):
    conn.connect()

    query = (
        f"""SELECT P.firstName, P.lastName, PHW.workerID, PHW.medicareNumber, PHW.publicHealthCenterID
                FROM publicHealthWorker as PHW, person as P
                WHERE publicHealthCenterID = {data['publicHealthCenterID']} and PHW.medicareNumber = P.medicareNumber
        """)

    conn.cursor.execute(query)
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


# 16- list of all public health workers who tested positive on a specific date in a specific facility
def get_all_at_risk_workers(from_date, to_date, workerid):
    conn.connect()

    query = (
        f"""SELECT DISTINCT PHW2.workerID, P.firstName, P.lastName
        FROM workerSchedule, publicHealthWorker as PHW1, publicHealthWorker as PHW2, person as P
            WHERE 
                workerSchedule.workerID <> {workerid} and 
                `date` between "{from_date}" and "{to_date}" and 
                PHW1.workerID = {workerid} and
                PHW2.workerID = workerSchedule.workerID and
                PHW1.publicHealthCenterID = PHW2.publicHealthCenterID and
                PHW2.medicareNumber = P.medicareNumber;
        """)

    conn.cursor.execute(query)
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


def get_workers_positive_test_at_facility(data):
    conn.connect()

    date_formatted = datetime.datetime.strptime(data['testDate'], '%Y-%m-%d')
    date_before = date_formatted - datetime.timedelta(days=14)
    date_before_str = date_before.strftime("%Y-%m-%d")

    query = (
        f"""SELECT P.firstName, P.lastName, PHW.medicareNumber, PHW.workerID
        FROM
            (SELECT medicareNumber, workerID
                FROM publicHealthWorker
                WHERE publicHealthCenterID = {data['publicHealthCenterID']}) as PHW, diagnostic as D, person as P
            WHERE D.result = true and 
            D.testDate = '{data['testDate']}'and 
            PHW.medicareNumber = D.medicareNumber and 
            PHW.medicareNumber = P.medicareNumber;
        """)

    breakpoint()
    conn.cursor.execute(query)

    resp = conn.cursor.fetchall()
    breakpoint()
    if resp is None:
        return {"response": "failed", "reason": "query failed"}

    res = []
    for worker in resp:
        temp = {}
        temp['sickWorker'] = worker
        workerid = worker['workerID']
        temp['atRiskWorkers'] = get_all_at_risk_workers(date_before_str, data['testDate'], workerid)
        res.append(temp)

    return res

# 17- report for each region
def get_all_region_reports():
    conn.connect()

    query = ("""SELECT negative_count.regionName, positive_count.count as positiveCount, negative_count.count as negativeCount
                FROM 
                (SELECT count(P.medicareNumber) as count, D.result, C.regionName
                FROM diagnostic as D, person as P, city as C
                WHERE 
                    D.result = true and
                    D.medicareNumber = P.medicareNumber and
                    P.city = C.`name`
                GROUP BY D.result, C.regionName) as positive_count,
                (SELECT count(P.medicareNumber) as count, D.result, C.regionName
                FROM diagnostic as D, person as P, city as C
                WHERE 
                    D.result = false and
                    D.medicareNumber = P.medicareNumber and
                    P.city = C.`name`
                GROUP BY D.result, C.regionName) as negative_count
                WHERE negative_count.regionName = positive_count.regionName;
             """)

    conn.cursor.execute(query)

    columns = [col[0] for col in conn.cursor.description]
    rows = [dict(zip(columns, row)) for row in conn.cursor.fetchall()]

    for report in rows:
        alerts = get_single('alert', {'regionName' : report['regionName']})
        report['alertHistory'] = alerts
        
        for alert in alerts:
            alert.pop('regionName', None)

    return rows


actions = {
    "POST": {
        "action_create": action_create,
        "action_delete": action_delete,
        "action_edit": action_edit,
    },
    "GET": {
        "get_single": get_single,
        "get_all": get_all,
    },
}


def perform_action(action, table, data):
    table_list = ['person', 'publicHealthWorker', 'publicHealthCenter', 'region', 'groupZone', 'groupZoneMapping', 'diagnostic', 'healthRecommendation', 'healthRecommendationSecondary', 'message']

    if table not in table_list:
        raise Exception('invalid table')

    try:
        return actions[request.method][action](table=table, data=data)
    except Exception as e:
        return str(e)
