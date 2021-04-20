from flask import Flask, request, jsonify
import datetime

from database import conn


def get_single(table, data, json=False, **kwargs):
    if table is None or data is None:
        return {"response": "failed", "reason": "query failed"}

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
    if json:
        return (
            jsonify(conn.cursor.fetchall())
            if conn.cursor is not None
            else {"response": "failed", "reason": "query failed"}
        )
    else:
        return conn.cursor.fetchall()


def get_all(table, json=False, **kwargs):
    if table is None:
        return {"response": "failed", "reason": "query failed"}
    conn.connect()

    query = f"SELECT * FROM {table}"
    conn.cursor.execute(query)
    if json:
        return (
            jsonify(conn.cursor.fetchall())
            if conn.cursor is not None
            else {"response": "failed", "reason": "query failed"}
        )
    else:
        return conn.cursor.fetchall()


def exists(table, data):
    res = get_single(table, data)
    return len(res) != 0


def action_create(table, data,  **kwargs):
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

    return {"response": "success", "reason": "data exists"}


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
    "person": ["medicareNumber"],
    "publicHealthWorker": ["workerID"],
    "publicHealthCenter": ["id"],
    "region": ["name"],
    "groupZone": ["groupID"],
    "healthRecommendation": ["id"],
    "healthRecommendationSecondary": ["id", "recommendation"],
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


# 8 and 9. store or get survey
def survey(action):
    conn.connect()
    if action == "store":
        required = [
            "medicareNumber",
            "dateOfBirth",
            "temperature",
            "symptoms",
        ]

        data = request.get_json()

        if any(x not in data for x in required):
            return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

        query = f"""SELECT * FROM person
                WHERE medicareNumber = '{data["medicareNumber"]}'
                AND dateOfBirth = '{data["dateOfBirth"]}'
            """
        conn.cursor.execute(query)

        if len(conn.cursor.fetchall()):
            query = f"""INSERT INTO followUpForm
                    (
                        medicareNumber, temperature, fever, cough, shortnessOfBreath,
                        lossOfTaste, nausea, stomachAche, diarrhea, vomiting, headache, musclePain,
                        soreThroat, otherSymptoms
                    )
                    VALUES
                    (
                        '{data["medicareNumber"]}', {data["temperature"]}, {data["symptoms"]["fever"]},
                        {data["symptoms"]["cough"]}, {data["symptoms"]["shortnessOfBreath"]},
                        {data["symptoms"]["lossOfTaste"]}, {data["symptoms"]["nausea"]}, {data["symptoms"]["stomachAche"]},
                        {data["symptoms"]["diarrhea"]}, {data["symptoms"]["vomiting"]}, {data["symptoms"]["headache"]},
                        {data["symptoms"]["musclePain"]}, {data["symptoms"]["soreThroat"]}, '{data["symptoms"]["otherSymptoms"]}'
                    )
                """
            conn.cursor.execute(query)
            conn.cnx.commit()
            return {"response": "sucess"}
        else:
            return {"response": "fail", "reason": f"medicare + DoB don't match"}
    elif action == "get":
        required = [
            "medicareNumber",
            "date",
        ]

        data = request.get_json()

        if any(x not in data for x in required):
            return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

        query = (
            f"SELECT * FROM followUpForm "
            f"WHERE medicareNumber = \"{data['medicareNumber']}\" "
            f"AND dateTime >= '{data['date']}' "
        )

        conn.cursor.execute(query)
        return (
            jsonify(conn.cursor.fetchall())
            if conn.cursor is not None
            else {"response": "failed", "reason": "query failed"}
        )


# 10. get messages within time period
def messages():
    conn.connect()

    required = [
        "startDateTime",
        "endDateTime",
    ]

    data = request.get_json()

    if any(x not in data for x in required):
        return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

    query = (
        f"SELECT * FROM message "
        f"WHERE dateTime >= \"{data['startDateTime']}\" "
        f"AND dateTime <= \"{data['endDateTime']}\" "
    )
    conn.cursor.execute(query)

    return (
        jsonify(conn.cursor.fetchall())
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


# 7- set new alert for a specific region
def get_previous_alert(region_name):
    conn.connect()

    query = f"""SELECT DISTINCT alertLevel, date
            FROM alert
            WHERE regionName = '{region_name}'
            ORDER BY date DESC
            LIMIT 1
        """

    conn.cursor.execute(query)

    resp = conn.cursor.fetchall()[0]
    if conn.cursor is not None:
        return resp["alertLevel"]


# 11. People at address
def people_at_address():
    conn.connect()

    required = [
        "address",
        "city",
        "province",
        "postalCode",
        "country",
    ]

    data = request.get_json()

    if any(x not in data for x in required):
        return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

    query = (
        (
            """ SELECT child.firstName, child.lastName, child.dateOfBirth,
                        child.medicareNumber, child.phoneNumber, child.citizenship,
                        child.email, father.firstName as fatherFirstName,
                        father.lastName as fatherLastName,
                        mother.firstName motherFirstName, mother.lastName motherLastName
                FROM person as child
                JOIN (SELECT medicareNumber, firstName, lastName FROM person) as father on child.fatherMedicare = father.medicareNumber
                JOIN (SELECT medicareNumber, firstName, lastName FROM person) as mother on child.motherMedicare = mother.medicareNumber
                WHERE 
            """
        )
        + " AND ".join([f"{key}='{data[key]}'" for key in required])
    )

    print(query)
    # get people at address
    conn.cursor.execute(query)

    return (
        jsonify(conn.cursor.fetchall())
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


# 12. get all facility details
def facilities():
    conn.connect()
    query = "SELECT * FROM publicHealthCenter"
    conn.cursor.execute(query)
    return (
        jsonify(conn.cursor.fetchall())
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


# set alert for a given region
def set_alert_for_region():
    conn.connect()

    data = request.get_json()
    previous_alert = get_previous_alert(data["regionName"])

    if not (0 <= data["alertLevel"] < 4):
        raise Exception("invalid alert level")

    if (data["alertLevel"] + 1 is not previous_alert) and (
        data["alertLevel"] - 1 is not previous_alert
    ):
        raise Exception("cannot set alert to this level")

    action_create("alert", data)

    query = f"""SELECT email FROM person p
                WHERE p.city IN (
                    SELECT name FROM city 
                        WHERE regionName = '{data["regionName"]}'
                )
        """
    conn.cursor.execute(query)
    peopleInRegion = conn.cursor.fetchall()

    query = f"""SELECT prompt FROM alertDetails
                WHERE alertLevel = '{data["alertLevel"]}'
        """
    conn.cursor.execute(query)
    alertPrompt = conn.cursor.fetchall()[0]["prompt"]

    messages = ""

    for person in peopleInRegion:
        messages += f'(\'{person["email"]}\', {previous_alert}, {data["alertLevel"]}, \'{alertPrompt}\'),'

    messages = messages[:-1]

    query = f"""INSERT INTO message 
            (
                email, oldAlertLevel, newAlertLevel, description
            )
            VALUES
            {messages}
        """
    conn.cursor.execute(query)
    conn.cnx.commit()

    return {"response": "success"}


# 13- list of all regions
def get_all_regions():
    rows = get_all("region")
    for region in rows:
        cities = get_single("city", {"regionName": region["name"]})

        for city in cities:
            postal_codes = get_single("cityPostalCodeMapping", {"city": city["name"]})
            temp = list(map(lambda x: x["postalCodeRegion"], postal_codes))
            city["postalCodes"] = temp
            city.pop("regionName", None)

        region["cities"] = cities
        region.pop("alertLevel", None)

    return jsonify(rows)


# 14- list of people who got the result of the test on a specific date
def get_all_test_results_on_specific_date():
    conn = conn.connect()
    conn.cursor = conn.conn.cursor()

    data = request.get_json()
    query = f"""SELECT P.firstName, P.lastName, P.dateOfBirth, P.phoneNumber, P.email, D.result
                FROM
                (SELECT medicareNumber, result
                    FROM diagnostic
                    WHERE testDate = '{data['testDate']}') as D, person as P
                WHERE P.medicareNumber = D.medicareNumber
                ORDER BY D.result DESC
        """

    conn.cursor.execute(query)

    return (
        jsonify(conn.cursor.fetchall())
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


# 15- list of workers in specific facility
def get_all_workers_at_facility(facilityID):
    conn.connect()

    query = f"""SELECT P.firstName, P.lastName, WHCM.healthWorkerID, P.medicareNumber, WHCM.healthCenterID, P.email, P.phoneNumber, P.dateOfBirth
            FROM pfc353_4.workerHealthCenterMapping as WHCM, pfc353_4.publicHealthWorker as PHW, pfc353_4.person as P
            WHERE
                healthCenterID = {facilityID} and
                WHCM.healthWorkerID = PHW.workerID and
                PHW.medicareNumber = P.medicareNumber and
                WHCM.endDate is null
        """

    conn.cursor.execute(query)
    return (
        jsonify(conn.cursor.fetchall())
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


# 16- list of all public health workers who tested positive on a specific date in a specific facility
def get_all_at_risk_workers(from_date, to_date, workerId):
    conn.connect()
    query = f"""SELECT DISTINCT PHW2.workerID, P.firstName, P.lastName
            FROM workerSchedule as WS1, workerSchedule as WS2, publicHealthWorker as PHW2, person as P
            WHERE
                WS2.workerID <> {workerId} and
                WS2.date between '{from_date}' and '{to_date}' and
                WS1.workerID = {workerId} and
                WS1.healthCenterID = WS2.healthCenterID and
                WS2.workerID = PHW2.workerID and
                PHW2.medicareNumber = P.medicareNumber;
        """

    conn.cursor.execute(query)
    return (
        conn.cursor.fetchall()
        if conn.cursor is not None
        else {"response": "failed", "reason": "query failed"}
    )


def get_workers_positive_at_facility():
    conn.connect()

    data = request.get_json()
    date_formatted = datetime.datetime.strptime(data["testDate"], "%Y-%m-%d")
    date_before = date_formatted - datetime.timedelta(days=14)
    date_before_str = date_before.strftime("%Y-%m-%d")
    query = f"""SELECT workerID, P.firstName, P.lastName
                FROM
                (SELECT healthWorkerID
                FROM workerHealthCenterMapping
                WHERE healthCenterID = {data['healthCenterID']}) as WHCM, publicHealthWorker as PHW, diagnostic as D, person as P
                WHERE 
                    WHCM.healthWorkerID = PHW.workerID and
                    D.testDate = '{data['testDate']}' and
                    PHW.medicareNumber = P.medicareNumber
        """

    conn.cursor.execute(query)

    resp = conn.cursor.fetchall()

    if resp is None:
        return {"response": "failed", "reason": "query failed"}

    res = []
    for worker in resp:
        temp = {}
        temp["sickWorker"] = worker
        workerid = worker["workerID"]
        temp["atRiskWorkers"] = get_all_at_risk_workers(
            date_before_str, data["testDate"], workerid
        )
        res.append(temp)

    return jsonify(res)


# 17- report for each region
def get_region_reports():
    conn.connect()

    query = """SELECT negative_count.regionName, positive_count.count as positiveCount, negative_count.count as negativeCount
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
        """

    conn.cursor.execute(query)

    columns = [col[0] for col in conn.cursor.description]
    rows = [dict(zip(columns, row)) for row in conn.cursor.fetchall()]

    for report in rows:
        alerts = get_single("alert", {"regionName": report["regionName"]})
        report["alertHistory"] = alerts

        for alert in alerts:
            alert.pop("regionName", None)

    return jsonify(rows)


actions = {
    "POST": {
        "create": action_create,
        "delete": action_delete,
        "edit": action_edit,
        "get_single": get_single,
    },
    "GET": {
        "get_all": get_all,
    },
}


def perform_action(action, table):
    table_list = [
        "alert",
        "person",
        "publicHealthWorker",
        "publicHealthCenter",
        "region",
        "groupZone",
        "groupZoneMapping",
        "diagnostic",
        "healthRecommendation",
        "healthRecommendationSecondary",
        "message",
    ]

    if table not in table_list:
        return {"response": "failed", "reason": "table does not exist"}

    try:
        return actions[request.method][action](
            table=table, data=request.get_json(), json=True
        )
    except Exception as e:
        return {"response": "failed", "reason": str(e)}


def get_date(json=True):
    conn.connect()

    query = """
    SELECT MAX(date) FROM currentDate;
    """

    conn.cursor.execute(query)
    date = conn.cursor.fetchall()[0]

    if json:
        return (
            conn.cursor.fetchall()
            if conn.cursor is not None
            else {"response": "failed", "reason": "query failed"}
        )
    else:
        return date["MAX(date)"]


def increment_date():
    conn.connect()

    # get date
    current_date = get_date(json=False)

    # add next date
    next_date = current_date + datetime.timedelta(days=1)

    query = f"""
    INSERT INTO currentDate
    VALUES (DATE '{next_date}')
    """

    conn.cursor.execute(query)
    conn.cnx.commit()

    new_date = get_date(json=False)
    if new_date == next_date:
        return jsonify({"response": "success", "date": next_date})
    else:
        return {"response": "failed", "reason": "unknown"}
