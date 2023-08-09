from vai_toolkit.client import *
import json


url=""
def create(conn, title, p_type, org_id=""):
    """CREATE A NEW PIPELINE"""

    headers =check_connection(conn)
    
    payload =json.dumps({
            "functionName": "create_pipeline",
            "title": title,   
            "type": p_type, 
        })
    
    return validate_response(payload,headers)
    

def list_locations(conn):
    """ADD LOCATION TO AN EXISTING PIPELINE"""
    
    headers =check_connection(conn)
    payload =json.dumps({
        "functionName"  : "list_locations",
    })
    return validate_response(payload,headers)


def add_location(conn, title):
    """ADD LOCATION TO AN EXISTING PIPELINE"""
    
    headers =check_connection(conn)
    payload =json.dumps({
        "functionName"  : "add_location",
        "title": title
    })

    return validate_response(payload,headers)


def list_alerts(conn):
    """LIST ALERTS IN YOUR PIPELINE"""

    headers =check_connection(conn)

    payload = json.dumps({
            "functionName": "list_alerts",
        })

    return validate_response(payload,headers)


def create_alert(conn, settings):
    """LIST ALERTS IN YOUR PIPELINE"""

    headers =check_connection(conn)

    payload = json.dumps({
            "functionName": "create_alert",
            "data": settings
        })

    return validate_response(payload,headers)
