import requests
from requests.structures import CaseInsensitiveDict

bateria = '{"bateria": 4.98}'
vazao = '{"vazao": 19}'
pressao = '{"pressao": 34}'
umidade = '{"umidade": 88}'
temperatura = '{"temperatura": 22}'

url4 = "http://localhost:8000/sensors/api/data/datalogger_014"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
resp4 = requests.post(url4, headers=headers, data=bateria)
print(resp4.status_code)

url3 = "http://localhost:8000/sensors/api/data/datalogger_013"
resp3 = requests.post(url3, headers=headers, data=vazao)
print(resp3.status_code)

url2 = "http://localhost:8000/sensors/api/data/datalogger_012"
resp2 = requests.post(url2, headers=headers, data=pressao)
print(resp2.status_code)

url1 = "http://localhost:8000/sensors/api/data/datalogger_011"
resp1 = requests.post(url1, headers=headers, data=umidade)
print(resp1.status_code)

url0 = "http://localhost:8000/sensors/api/data/datalogger_010"
resp0 = requests.post(url0, headers=headers, data=temperatura)
print(resp0.status_code)
