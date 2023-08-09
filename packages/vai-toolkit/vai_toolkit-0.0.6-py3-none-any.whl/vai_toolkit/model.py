# TODO: make predict_time and predict_link like "func", "data"

from vai_toolkit.client import *
import json


def train_mixed(conn, title,  from_date , to_date):
    """TRAIN A MIXED-MODAL MODEL"""

    headers=check_connection(conn)
    payload = json.dumps({ 
            "functionName": "train_mixed",
            "title": title,
            "fromDate": from_date,
            "toDate": to_date,
        })
    return validate_response( payload,headers)


def train_timeseries(conn, title,  from_date , to_date):
    """TRAIN A TIMESERIES MODEL"""

    headers=check_connection(conn)
    payload = json.dumps({ 
            "functionName":  "train_timeseries",
            "title": title,
            "fromDate": from_date,
            "toDate": to_date,
        })
    return validate_response( payload,headers)


def explain_mixed(conn, datasetData,modelId,dataset):
    """PERFORM SHAP ANAL. ON MIXED MODAL"""

    headers=check_connection(conn)    
    payload = json.dumps({         
        "functionName":  "explain",
        "datasetData": datasetData,
        "model": modelId,
        "dataset": dataset,
    })
    return validate_response( payload,headers)


def explain_timeseries(conn,panel, modelId ,from_date,to_date):
    """PERFORM SHAP ANAL. ON MIXED TIMESERIES DATA"""
    
    headers=check_connection(conn)
    payload = json.dumps({ 
        "functionName" :  "explain_timeseries",
        "modelId": modelId,
        "panel": panel,
        "fromDate":from_date,
        "toDate": to_date,    
    })
    return validate_response( payload,headers)

    
def predict_time(conn, panel, model, from_date, to_date):
    """PREDICT TIMESERIES DATA, W/O SHAP"""
    
    headers=check_connection(conn)
    payload = json.dumps({ 
        "functionName":  "predict_time",
        "panel": panel,
        "model": model,
        "fromDate" : from_date,
        "toDate" : to_date,
    })
    return validate_response( payload,headers)

    
def predict_link(conn, panel, model, from_date, to_date,guestcount, dimItem):
    """PREDICT TIMESERIES DATA, W/O SHAP"""
    
    headers=check_connection(conn)
    payload = json.dumps({ 
        "functionName": "predict_link",
        "panel": panel,
        "model": model,
        "fromDate" : from_date,
        "toDate" : to_date,
        "guestCount" : guestcount,
        "dimItems": dimItem
    })
    return validate_response( payload,headers)
    

# def explain(conn, d_params, model_id, dataset):
#     """EXPLAIN THE PREDICTION"""

#     headers=check_connection(conn)
#     payload = json.dumps({ 
#         "func" :  "explain",
#         "data": {
#             "datasetData": d_params,
#             "modelId": model_id,
#             "dataset" : dataset
#         }
#     })
#     return validate_response( payload,headers)


# def train_model(conn, title, from_date, to_date):
#     """EXPLAIN THE PREDICTION"""

#     headers=check_connection(conn)
#     payload = json.dumps({ 
#         "func" :  "train",
#         "data": {
#             "title": title,
#             "fromDate": from_date,
#             "toDate": to_date,
#         }
#     })
#     return validate_response( payload,headers)
