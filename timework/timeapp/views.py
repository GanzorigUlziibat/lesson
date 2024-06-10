from django.shortcuts import render
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from timework.settings import sendResponse, connectDB, disconnectDB

def gettime(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    today = datetime.now()
    data = [{'currenttime':today}]
    result = sendResponse(200, data, action)
    return result
# gettime

def getasuult(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    try:
        onn = jsons['onn']
        hicheelkod = jsons['hicheelkod']
        huvilbar = jsons['huvilbar']
        asuulttoo = jsons["asuulttoo"]
        username = jsons["username"]
    except Exception as e:
        action = action
        data = [{"error": str(e) + " key error"}]
        result = sendResponse(404, data, action)
        return result

    try: 
        myCon = connectDB()
        cursor = myCon.cursor()

        query = F"""INSERT INTO mttest.t_shalgalt(
                    username, onn, hicheelkod, huvilbar, asuulttoo, regdate)
                    VALUES ('{username}', {onn}, {hicheelkod}, '{huvilbar}', {asuulttoo}, NOW()) 
                    RETURNING shalgaltid;
            """
        cursor.execute(query)
        shalgaltid = cursor.fetchone()[0]
        myCon.commit()

        if onn == 0:
            onnQuery = " "
        else:
            onnQuery = F"AND onn = {onn}"
        if huvilbar == "":
            huvilbarQuery = " "
        else:
            huvilbarQuery = F"AND huvilbar = '{huvilbar}'"
        query = F"""SELECT t_asuult.aid, t_asuult.asuult, t_asuult.hicheelkod, t_asuult.onn, t_asuult.catkod, 
                            t_asuult.onoo, t_asuult.huvilbar, t_asuult.huvilbarid, t_asuult.minutes
                            FROM mttest.t_asuult
                            WHERE hicheelkod = {hicheelkod}  """ + huvilbarQuery + onnQuery + F""" 
                            ORDER BY random()
                            LIMIT {asuulttoo}"""
        cursor.execute(query)
        columns = cursor.description
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()]

        cursor.close()

        # print(respRow)
        desdugaar = 1
        for row in respRow:
            # print(row['aid'])
            cursor = myCon.cursor()
            
            query = F"""INSERT INTO mttest.t_userhariult(desdugaar,
                    shalgaltid, aid, shariult, regdate, updatedate)
                    VALUES ({desdugaar}, {shalgaltid}, {row['aid']}, 0, 
                            NOW(), '1900-01-01') RETURNING userhariultid
            """
            cursor.execute(query)
            userhariultid = cursor.fetchone()[0]
            myCon.commit()
            row['desdugaar'] = desdugaar
            desdugaar = desdugaar + 1
            
        
            query = F"""SELECT hid,aid,hariult, correctans, hariultid 
                        FROM mttest.t_hariult 
                        WHERE aid = {row['aid']} 
                        ORDER BY hariultid"""
            cursor.execute(query)
            columns = cursor.description
            respRowHariult = [{columns[index][0]:column for index, 
                column in enumerate(value)} for value in cursor.fetchall()]
            # print(respRowHariult)
            row["hariult"] = respRowHariult
            row["userhariultid"] = userhariultid

            # print(respRow)
            cursor.close()

        disconnectDB(myCon)
        
        data = respRow
        result = sendResponse(200, data, action)
        return result
    except Exception as e:
        action = action
        data = [{"error": str(e) + " database error" + query}]
        result = sendResponse(404, data, action)
        return result
#getasuult

def sethariult(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    try:
        userhariultid = jsons['userhariultid']
        shariult = jsons['shariult']
    except Exception as e:
        action = action
        data = [{"error": str(e) + " key error"}]
        result = sendResponse(404, data, action)
        return result

    try: 
        myCon = connectDB()
        cursor = myCon.cursor()

        query = F"""UPDATE mttest.t_userhariult
                        SET shariult={shariult}, updatedate=NOW()
                        WHERE userhariultid = {userhariultid};
            """
        cursor.execute(query)
        myCon.commit()
        cursor.close()

        disconnectDB(myCon)
        
        data = []
        result = sendResponse(200, data, action)
        return result
    except Exception as e:
        action = action
        data = [{"error": str(e) + " database error" + query}]
        result = sendResponse(404, data, action)
        return result
# sethariult


@csrf_exempt
def index(request):
    if request.method == "POST":
        try :
            jsons = json.loads(request.body)
        except json.JSONDecodeError:
            action = "wrong json"
            data = []
            result = sendResponse(404, data, action)
            return JsonResponse(json.loads(result))
        if 'action' in jsons:
            action = jsons['action']
            if action == 'gettime':
                result = gettime(request)
                return JsonResponse(json.loads(result))
            elif action == "getasuult":
                result = getasuult(request)
                return JsonResponse(json.loads(result))
            elif action == "sethariult":
                result = sethariult(request)
                return JsonResponse(json.loads(result))
            else:
                action = "action not found"
                data = []
                result = sendResponse(404, data, action)
                return JsonResponse(json.loads(result))
        else:
            action = "no action"
            data = []
            result = sendResponse(404, data, action)
            return JsonResponse(json.loads(result))
    else:
        action = "method buruu"
        data = []
        result = sendResponse(405, data, action)
        return JsonResponse(json.loads(result))
    
# gettime