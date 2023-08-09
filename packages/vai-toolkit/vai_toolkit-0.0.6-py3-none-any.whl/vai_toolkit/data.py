from vai_toolkit.client import *
import json



def upload_data(conn,data, date, time,  new_columns=False, duplicates=False, new_categories=False):
    """UPLOAD CSV TYPE DATA"""

    headers =check_connection(conn)  
    payload = json.dumps({ 
        "functionName": "upload_data",
        "date": date,
        "time" : time,
        "data" : data,
        "allowNewColumns" : new_columns,
        "allowDuplicate" : duplicates,
        "allowNewCategory" : new_categories
        })   
    return validate_response(payload,headers)


def upload_csv(conn, path):
    headers =check_connection(conn)  
    return validate_response_upload('upload_csv' ,path ,headers)


def download_csvs(conn, to_file, from_date="", to_date=""):
    """DOWNLOAD A ZIP OF CSV TYPE DATA"""

    headers =check_connection(conn)
    payload = json.dumps({
        "functionName": "download_csvs",
        "fromDate": from_date,
        "toDate": to_date
    })  
    response = validate_response_download(payload,headers )
    if(response.status_code == 200) :
        f = open(to_file, 'wb')
        f.write(response.content)
        f.close()
        return "File saved successfully"
    else :
        response = json.loads(response.text)
        if ('message' in response):
            return  (response['message'])
        else :
            return response



def list_labels(conn):
    """LIST ALL OF THE CURRENT DATA LABLES"""
    
    headers =check_connection(conn) 
    payload = json.dumps({ 
            "functionName": "list_labels"
        })
    return validate_response(payload,headers)


def set_labels(conn, labels, d_types):
    """LIST ALL OF THE CURRENT DATA LABLES"""
    
    headers =check_connection(conn) 
    payload = json.dumps({ 
            "functionName": "set_labels",
                "columnLabels": labels,
                "columnTypes": d_types,
        })
    return validate_response(payload,headers)
