from vai_toolkit.client import *
import json



## email group add, get

def get_email_groups(conn):
    """GET EMAIL LIST"""

    headers= check_connection(conn)

    payload = json.dumps({
            "functionName" : "get_email_groups",
        })

    return validate_response(payload, headers)


def create_email_groups(conn, group_name, email_list):
    """CREATE EMAIL LIST"""

    headers= check_connection(conn)

    payload = json.dumps({
            "functionName" : "create_email_groups",
            "groupName": group_name,
            "users": email_list ,
        })

    return validate_response(payload, headers)


## data tracker widget

def create_widget(conn, widget_title, controlPanel, columns):
    """CREATE WIDGET"""
    
    headers= check_connection(conn)

    payload = json.dumps({ 
            "functionName": "create_widget",
            "name": widget_title,
            "controlPanel": controlPanel,
            "dataSetFields": columns
        })

    return validate_response(payload, headers)


def create_timeseries_widget(conn, panel_id, name, type):
    """CREATE TIMESERIES"""
    
    headers= check_connection(conn)
    
    payload =json.dumps({
        "functionName": "create_timeseries",
        "panel" :panel_id,
        "name":name,
        "type" :type
        })

    return validate_response(payload, headers)



## survey widgets
 
def list_survey(conn):
    """LIST SURVEYS"""

    headers= check_connection(conn)  
        
    payload = json.dumps({ 
        "functionName": "list_survey",
    })    

    return validate_response(payload, headers)


def create_survey_panel(conn, panel_name):
    """CREATE TIMESERIES"""
    
    headers= check_connection(conn)

    payload =json.dumps({
            "functionName": "create_survey_panel",
            "name": panel_name,
        })

    return validate_response(payload, headers)


def create_survey(conn, panel_id, widget_title, questions):
    """CREATE SURVEY"""
    
    headers= check_connection(conn)

    payload= json.dumps({
            "functionName": "create_survey",
            "panel" :panel_id,
            "widgetName": widget_title,
            "questions" :questions
        })

    return validate_response(payload, headers)


def update_survey(conn, old_survey_name, new_survey_name):
    """UPDATE SURVEYS"""

    headers= check_connection(conn)  

    payload =json.dumps({
        "functionName": "update_survey",
        "surveyName": old_survey_name,
        "newSurveyName": new_survey_name,
    })

    return validate_response(payload, headers)
