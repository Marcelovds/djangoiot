import json
import time
import urllib

ENDPOINT = "http://localhost:8000/sensors/api/data/datalogger_014"


def send(bateria):
    unix_timestamp = int(time.time() * 1000)
    data = {
        'date': unix_timestamp,
        'bateria': bateria

    }

    req = urllib.Request(ENDPOINT)
    req.add_header('Content-Type', 'application/json')

    response = urllib.urlopen(req, json.dumps(data))


try:
    temperatura, umidade, pressao, vazao, bateria = (23, 80, 32, 4, 5)
    print('Temp= {0:0.1f} *C  Umidade= {1:0.1f} % Pressao= {2:0.1f} mca  Vazao= {3:0.1f} m3/min  Bateria= {4:0.1f} V'.format(
        temperatura, umidade, pressao, vazao, bateria))
    send(round(bateria, 1))
except:
    print('Erro ao enviar dado')
