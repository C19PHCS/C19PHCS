from database import get_conn
import datetime

def get_single(table, data):
    conn = get_conn()
    cursor = conn.cursor()
    
    temp = ""
    for k, v in data.items():
        if isinstance(v, str):
            temp += "{} = '{}' and ".format(k, v)
        else:
            temp += "{} = {} and ".format(k, v)
    temp = temp[:-5]

    query = ("SELECT * FROM {} WHERE {};").format(table, temp)

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

    temp = ""
    for k, v in data.items():
        if isinstance(v, str):
            temp += "{} = '{}' and ".format(k, v)
        else:
            temp += "{} = {} and ".format(k, v)
    temp = temp[:-5]

    query = ("DELETE FROM {} WHERE {};").format(table, temp)

    cursor.execute(query)

    cursor.close()
    conn.commit()
    conn.close()

    return True

primary_keys = {
    'person' : ['medicareNumber'],
    'publicHealthWorker' : ['workerID'],
    'publicHealthCenter' : ['id'],
    'region' : ['name'],
    'groupZone' : ['groupID'],
    'healthRecommendation' : ['id'],
    'healthRecommendationSecondary': ['id', 'recommendation']
}

def edit(table, data):
    ids = {}
    datas = {}

    for key, value in data.items():
        if key in primary_keys[table]:
            ids[key] = value
        else:
            datas[key] = value

    if not exists(table, ids):
        return False

    conn = get_conn()
    cursor = conn.cursor()

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
    
    cursor.execute(query)

    cursor.close()
    conn.commit()
    conn.close()

    return True

# 7- set new alert for a specific region
def set_region_alert(data):
    create('alert', data)

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
    conn = get_conn()
    cursor = conn.cursor()
    
    query = ("""
    SELECT P.firstName, P.lastName, P.dateOfBirth, P.phoneNumber, P.email, D.result
FROM
(SELECT medicareNumber, result
FROM diagnostic
WHERE testDate = '{}') as D, person as P
WHERE P.medicareNumber = D.medicareNumber
ORDER BY D.result DESC
;""").format(data['testDate'])

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    return rows

# 15- list of workers in specific facility
def get_workers_at_facility(data):
    conn = get_conn()
    cursor = conn.cursor()

    query = ("""SELECT P.firstName, P.lastName, PHW.workerID, PHW.medicareNumber, PHW.publicHealthCenterID
FROM publicHealthWorker as PHW, person as P
WHERE publicHealthCenterID = {} and PHW.medicareNumber = P.medicareNumber;""").format(data['publicHealthCenterID'])

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    return rows

def get_all_at_risk_workers(from_date, to_date, workerid):
    conn = get_conn()
    cursor = conn.cursor()

    query = ("""SELECT DISTINCT PHW2.workerID, P.firstName, P.lastName
FROM workerSchedule, publicHealthWorker as PHW1, publicHealthWorker as PHW2, person as P
WHERE 
	workerSchedule.workerID <> {} and 
    `date` between "{}" and "{}" and 
    PHW1.workerID = {} and
    PHW2.workerID = workerSchedule.workerID and
    PHW1.publicHealthCenterID = PHW2.publicHealthCenterID and
    PHW2.medicareNumber = P.medicareNumber;""").format(workerid, from_date, to_date, workerid)

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()
    return rows

# 16- list of all public health workers who tested positive on a specific date in a specific facility
def get_workers_positive_test_at_facility(data):
    date_formatted = datetime.datetime.strptime(data['testDate'], '%Y-%m-%d')
    date_before = date_formatted - datetime.timedelta(days=14)
    date_before_str = date_before.strftime("%Y-%m-%d")

    conn = get_conn()
    cursor = conn.cursor()

    query = ("""SELECT P.firstName, P.lastName, PHW.medicareNumber, PHW.workerID
FROM
(SELECT medicareNumber, workerID
FROM publicHealthWorker
WHERE publicHealthCenterID = {}) as PHW, diagnostic as D, person as P
WHERE D.result = true and 
D.testDate = '{}'and 
PHW.medicareNumber = D.medicareNumber and 
PHW.medicareNumber = P.medicareNumber;""").format(data['publicHealthCenterID'], data['testDate'])

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    res = []
    for worker in rows:
        temp = {}
        temp['sickWorker'] = worker
        workerid = worker['workerID']
        temp['atRiskWorkers'] = get_all_at_risk_workers(date_before_str, data['testDate'], workerid)
        res.append(temp)

    return res

# 17- report for each region
def get_all_region_reports():
    conn = get_conn()
    cursor = conn.cursor()

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
WHERE negative_count.regionName = positive_count.regionName;""")

    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.commit()
    conn.close()

    for report in rows:
        alerts = get_single('alert', {'regionName' : report['regionName']})
        report['alertHistory'] = alerts
        
        for alert in alerts:
            alert.pop('regionName', None)

    return rows

def perform_action(action, table, data):
    table_list = ['person', 'publicHealthWorker', 'publicHealthCenter', 'region', 'groupZone', 'groupZoneMapping', 'diagnostic', 'healthRecommendation', 'healthRecommendationSecondary', 'message']

    if table not in table_list:
        raise Exception('invalid table')

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
