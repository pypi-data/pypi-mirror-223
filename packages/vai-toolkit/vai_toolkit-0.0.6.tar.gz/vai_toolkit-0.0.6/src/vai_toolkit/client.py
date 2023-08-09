# TODO: finish get all payloads to work ()
# ASSUME: fromDate toDate (both empty means all, from date means all after, to date means all before)

import requests, json 

url = "https://dev-cloud-api.virtuousai.com/vai-toolkit"
# url = "http://localhost:1333/vai-toolkit"


url_upload = "https://dev-cloud-api.virtuousai.com/vai-toolkit/upload"
# url_upload = "http://localhost:1333/vai-toolkit/upload"



def login(email: str, password: str, pipeline_id="", location_id=""):
    """AUTHENTICATE

        args:

            * email: (string) users unique id
            * password: (string) users password

        :returns:
            * _id: (string) token
            * first_name: (string) users first name
            * last_name: (string) users last name
            * email: (string) users email
            * account_created: (string) user account creation date
            * last_login: (string) user's last login date

    """
    payload =json.dumps({
            "functionName":"login", 
            "email": email, 
            "password": password,
            "pipeline": pipeline_id,
            "location": location_id,
        })

    return validate_response(payload , {})


def update_password(conn, new_password):
    """UPDATE ACCOUNT PASSWORD"""
    headers=  check_connection(conn)
    if(headers):
        payload =json.dumps({
                "functionName":"update_password", 
                "password" : new_password
        })
        return validate_response(payload, headers=headers)
    else:
         return {"success": False , "message" :"Invalid Connection"}
    


def update_name(conn, new_first, new_last):
    """UPDATE ACCOUNT NAME"""
    try:
        headers= check_connection(conn)
        payload =json.dumps({
                "functionName":"update_name", 
                "firstName": new_first, 
                "lastName": new_last
        })
        return validate_response(payload, headers=headers)
    except Exception as e:
        return e


# def update_email(conn, new_email):
#     """UPDATE ACCOUNT EMAIL"""
#     check_connection(conn)
    
#     payload =json.dumps({
#             "func":"client.update_email", 
#             "data": {
#                 "newEmail": new_email, 
#             }
#         })
    
#     return validate_response(payload, headers=conn)


def create_account(conn, email ,password, firstname ,lastname):
    """CREATE A NEW ORGANIZATION"""
    headers= check_connection(conn)

    payload =json.dumps({
            "functionName":"create_account",
             "email" :email ,
             "password" :password , 
             "firstName" :firstname ,
             "lastName" :lastname
        })

    return validate_response(payload, headers=headers)



def create_organization(conn, name, users):
    """CREATE A NEW ORGANIZATION"""
    headers= check_connection(conn)

    payload =json.dumps({
            "functionName":"create_organization",
            "name": name,   
            "users": users, 
        })

    return validate_response(payload, headers=headers)


def check_connection(conn):
    """CHECKS FOR A VALID CONNECTION"""
    if (len(conn.split(":")) == 3) :
        return {  "user-secret" :conn.split(":")[0],  "pipeline":  conn.split(":")[1],  "location":  conn.split(":")[2]}
    else:
        return False

def validate_response(payload, headers):
    """IF 'message', THEN ERROR"""
    response = requests.post(url ,data= payload,headers= headers)
    response = json.loads(response.text)
    if ('message' in response):
        return  (response['message'])
    else :
        return response

def validate_response_download(payload, headers):
    """IF 'message', THEN ERROR"""
    response = requests.post(url ,data= payload,headers= headers)
    return response

def validate_response_upload(func, file,headers):
    files = {'file': open(file,'rb')}
    response = requests.post(url_upload+'?functionName='+ func, files=files,headers= headers)
    response = json.loads(response.text)
    if ('message' in response):
        return  (response['message'])
    else :
        return response
   


def create_connection(email: str, password: str, pipeline_id="", location_id=""):
    ## create connection to give token
    res= login(email, password, pipeline_id= pipeline_id, location_id=location_id)
    if not isinstance(res,str) and res['token'] :
        return res['token']
    else: 
        return res
