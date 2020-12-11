import json

def flatten(data:list):
    res = []
    for row in data:
        rowdata = {}
        for point in row["fields"]:
            rowdata[point["field"]] = point["value"]
            if point["datatype"] == "int":
                rowdata[point["field"]] = int(point["value"])
            if point["datatype"] == "float":
                rowdata[point["field"]] = float(point["value"])
            if point["datatype"] == "bool":
                rowdata[point["field"]] = True if point["value"] == "TRUE" else False
        res.append(rowdata)
    return res
