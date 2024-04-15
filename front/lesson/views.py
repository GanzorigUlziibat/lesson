from django.shortcuts import render, redirect
import requests, json
import hashlib 
# Create your views here.
def dt_login(request):
    requestJSON = {}
    ctx = {}
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['passw']
        # print(username,passw)
        requestJSON["action"] = "login"
        requestJSON["email"] = username
        requestJSON["passw"] = hashlib.md5(hashlib.md5(passw.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
        
# mobicom.mn/mandakh/?phone=88121511&sms=Tanii burtgeliin dugaar: 8080
        r = requests.post('http://localhost:8001/users/',
                            data=json.dumps(requestJSON),
                            headers={'Content-Type': 'application/json'},
                            )

        # pled validation bolon busad exeption-uud shalgah
        # print(r)
        resultCode = r.json()['resultCode']
        resultMessage = r.json()['resultMessage']
        # print(resultCode, resultMessage)
        # ctx = r.json()
        ctx['resultCode'] = resultCode
        ctx['resultMessage'] = resultMessage

        if resultCode == 1002:
            ctx['email'] = r.json()["data"][0]["email"]
            ctx['firstname'] = r.json()["data"][0]["firstname"]
            ctx['lastname'] = r.json()["data"][0]["lastname"]
            # ctx = r.json()
            # print(r.json(), " aaaaaa ",r.json()["data"][0]["email"])
            return render(request,"dashboard.html", ctx)
        
    return render(request, "login.html",ctx)
# dt_login

def dt_dashboard(request):
    return render (request, "dashboard.html")
# dt_dashboard

def dt_register(request):
    requestJSON = {}
    ctx = {}
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['passw']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
       
        # print(username, passw, firstname,lastname) 
        requestJSON["action"] = "register"
        requestJSON["email"] = username
        requestJSON["firstname"] = firstname
        requestJSON["lastname"] = lastname
        requestJSON["passw"] = hashlib.md5(hashlib.md5(passw.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

        r = requests.post('http://localhost:8001/users/',
                            data=json.dumps(requestJSON),
                            headers={'Content-Type': 'application/json'},
                            )
        
        resultCode = r.json()['resultCode']
        resultMessage = r.json()['resultMessage']
        print(resultCode, resultMessage)
        # print(resultCode, resultMessage)
        # ctx = r.json()
        ctx['resultCode'] = resultCode
        ctx['resultMessage'] = resultMessage
        ctx['inputFirstname'] = firstname

        if resultCode == 1001:
            email = r.json()['data'][0]['email']
            lastname = r.json()['data'][0]['lastname']
            firstname = r.json()['data'][0]['firstname']
            ctx['username'] = email
            ctx['lastname'] = lastname
            ctx['firstname'] = firstname
            return render (request, "login.html", ctx)
        else:
            email = r.json()['data'][0]['email']
            ctx['username'] = email
       
            
            
    return render (request, "register.html", ctx)
# dt_register