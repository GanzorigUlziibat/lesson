from django.shortcuts import render
from datetime import date
from django.http import HttpResponse
import json
from backlesson.settings import *

# Create your views here.

def gettime(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    today = date.today()
    data = [{"curtime" : today}]
    resp = sendResponse(request, 200, data,  action)
    return resp
# gettime

def userregister(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    email = str(jsons['email']).lower()
    firstname = str(jsons['firstname']).capitalize()
    lastname = str(jsons['lastname']).capitalize()
    passw = jsons['passw']
    
    myCon = connectDB()
    cursor = myCon.cursor()
    
    query = F"SELECT COUNT(*) as usercount FROM t_user WHERE email = '{email}' AND enabled = 1"

    cursor.execute(query)
    columns = cursor.description
    respRow = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

    for row in respRow: 
        if row["usercount"] == 1: # burtgeh bolomjgui
            data = [{'email':email }]
            resp = sendResponse(request, 1000, data, action  )
        else: # burtgeh bolomjtoi
            cursor1 = myCon.cursor()
            query = F"""INSERT INTO t_user(
                        email, lastname, firstname, passw, regdate, enabled, token, tokendate)
                        VALUES ('{email}', '{lastname}', '{firstname}', '{passw}'
                                , NOW(), 0, 'aisfhbaiwehbfuyebr2346728', NOW() + interval '24 hour');"""

            cursor1.execute(query)
            myCon.commit()
            cursor1.close()
            data = [{'email':email, 'lastname': lastname, 'firstname': firstname }]
            resp = sendResponse(request, 1001, respRow, action  )
            
    cursor.close()


    return resp
# userrequest


def checkService(request):
    jsons = json.loads(request.body)
    if jsons['action'] == 'gettime':
        result = gettime(request)
    elif jsons['action'] == 'register':
        result = userregister(request)
    else:
        result = "action buruu"

    return HttpResponse(result)
#checkService
    
 
    

#gettime
