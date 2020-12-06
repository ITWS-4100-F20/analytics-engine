import json

def flatten(data:list):
    res = []
    for row in data:
        rowdata = {}
        for point in row["fields"]:
            rowdata[point["field"]] = point["value"]
            if point["datatype"] == "int":
                rowdata[point["field"]] = int(point["value"])
        res.append(rowdata)
    return res
