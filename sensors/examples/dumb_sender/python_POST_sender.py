import requests
from requests.structures import CaseInsensitiveDict

url = "http://localhost:8000/sensors/api/data/datalogger_014"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"bateria": 4.92}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
