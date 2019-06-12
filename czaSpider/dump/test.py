import requests
import json

formData = {
    "access_token": "",
    "local_province_id": "42",
    "local_type_id": "1",
    "page": "2",
    "school_id": "42",
    "signsafe": "3afd39c07ce14810eabd8a65944e05fc",
    "size": "20",
    "uri": "apidata/api/gk/score/special",
    "year": "2018",
}
header = {
    'Content-Type':'"application/json;charset=UTF-8"'
}

