# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 14:41:29 2021

@author: jnwag
"""
def GetGDCData(primarySite, race, gender,expStrat):
    import requests
    import json
    import re
    
    files_endpt = "https://api.gdc.cancer.gov/files"
    filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "cases.project.primary_site",
            "value": [primarySite]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "cases.demographic.race",
            "value": [race]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "cases.demographic.gender",
            "value": [gender]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "files.analysis.workflow_type",
            "value": ["HTSeq - FPKM"]
                    }
                },
        {
        "op": "in",
        "content":{
        "field": "files.experimental_strategy",
        "value": [expStrat]
        }
                    }
                
            ]
        }
        # Here a GET is used, so the filter parameters should be passed as a JSON string.
    
    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "1000"
        }
    response = requests.get(files_endpt, params = params)

    file_uuid_list = []

    # This step populates the download list with the file_ids from the previous query
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])
    
    data_endpt = "https://api.gdc.cancer.gov/data"
    
    params = {"ids": file_uuid_list}

    response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type": "application/json"})
    
    response_head_cd = response.headers["Content-Disposition"]
    
    file_name = re.findall("filename=(.+)", response_head_cd)[0]
    
    with open(file_name, "wb") as output_file:
        output_file.write(response.content)
        
    return(file_uuid_list)

GetGDCData("Brain", "white", "male","RNA-Seq")