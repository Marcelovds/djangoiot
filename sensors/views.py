import csv
import json
import os.path
import time
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from sensors.models import Sensor
from sensors.utils.fix_corrupted_files import fix_corrupted_file
from sensors.utils.SensorDataPoint import SensorDataPoint


def index(request):
    all_sensors = Sensor.objects.order_by('-creation_date')
    for sensor in all_sensors:
        sensor.last_data = load_last_data(sensor)
    context = {
        'sensors': all_sensors
    }
    return render(request, 'sensors/index.html', context)


def sensor_detail(request, slug):
    try:
        sensor = Sensor.objects.get(slug=slug)
    except Sensor.DoesNotExist:
        raise Http404("Sensor não existe")

    context = {
        'sensor': sensor
    }
    return render(request, 'sensors/' + sensor.type + '/detail.html', context)


# example POST body:
# {
#     "temperature": 12.3,
#     "humidity": 20.3
# }
# "temperature" and "humidity" must be defined on the 'format' field of the sensor
@csrf_exempt
def api_add_data(request, slug):
    try:
        sensor = Sensor.objects.get(slug=slug)
    except Sensor.DoesNotExist:
        return JsonResponse({'erro': 'Sensor não encontrado'}, status=404)

    if request.method == 'POST':
        try:
            sensor_data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'erro': 'Erro relacionado ao dado'}, status=400)

        save_sensor_data(sensor_data, sensor)
        return JsonResponse({'resultado': 'ok'})
    else:
        [from_date, to_date] = parse_date_range(request)
        return JsonResponse({
            'name': sensor.name,
            'format': sensor.format,
            'data': load_sensor_data(sensor, from_date, to_date)
        })


def parse_date_range(request):
    from_timestamp = request.GET.get('from', None)
    to_timestamp = request.GET.get('to', None)

    from_date = datetime.today()
    to_date = datetime.today()
    if from_timestamp is not None:
        from_date = datetime.utcfromtimestamp(int(from_timestamp))
    if to_timestamp is not None:
        to_date = datetime.utcfromtimestamp(int(to_timestamp))

    return [from_date, to_date]


def save_sensor_data(data, sensor):
    # automatic date if it is missing in the data
    if 'date' not in data:
        data['date'] = int(time.time() * 1000)

    csv_separator = ','

    column_names = sensor.format.split(csv_separator)
    values = []
    for i in range(len(column_names)):
        values.append(str(data[column_names[i]]))

    create_file_if_new(sensor)
    data_file = open(sensor_file_path(sensor), 'a+')
    data_file.write(csv_separator.join(values) + '\n')
    data_file.close()


def load_last_data(sensor):
    file_path = sensor_file_path(sensor)
    data = load_sensor_data_file(sensor, file_path)
    if len(data) == 0:
        return None
    return data[-1]


def load_sensor_data(sensor, from_date, to_date):
    return load_sensor_data_files(sensor, from_date, to_date)


def load_sensor_data_files(sensor, from_date, to_date):
    file_paths = sensor_file_paths(sensor, from_date, to_date)
    data = []
    for file_path in file_paths:
        daily_data = load_sensor_data_file(sensor, file_path)
        column_names = sensor.format.split(',')
        # if there are dates in the data, exclude points before from_date and after to_date
        if 'date' in column_names:
            for data_point in daily_data:
                date = datetime.utcfromtimestamp(
                    int(int(data_point['date'])/1000))
                if from_date <= date <= to_date:
                    data.append(data_point)
        # otherwise just add all daily data without filtering
        else:
            data = data + daily_data
    return data


def load_sensor_data_file(sensor, file_path):
    if not os.path.isfile(file_path):
        return []

    csv_separator = ','
    column_names = sensor.format.split(csv_separator)
    sensor_data = open(file_path, 'r')
    csv_reader = csv.reader(sensor_data, delimiter=csv_separator)
    line_count = 0
    data = []

    # for some reason when there is a blackout a file might get corrupted
    # a number of NULL bytes get written to the file and it no longer can be parsed
    # it would be better to avoid this corruption in the first place but this should work too, as a workaround
    fix_corrupted_file(file_path)

    for row in csv_reader:
        if line_count == 0:
            if not sensor.format == csv_separator.join(row):
                raise ValueError('File format does not match. '
                                 'Expected "%s" but found "%s"' % (sensor.format, csv_separator.join(row)))
            line_count += 1
        else:
            point = SensorDataPoint()
            for i in range(len(column_names)):
                point[column_names[i]] = row[i]
            data.append(point)
            line_count += 1
    return data


def create_file_if_new(sensor):
    file_path = sensor_file_path(sensor)
    if not os.path.isfile(file_path):
        try:
            f = open(file_path, 'w')
            f.write(sensor.format + '\n')
            f.close()
        except IOError:
            raise
        finally:
            f.close()


def sensor_file_path(sensor, date=None):
    if date is None:
        date = datetime.utcnow()

    day = date.strftime('%Y-%m-%d')
    project_path = os.path.abspath(os.path.dirname(__name__))
    return project_path + '/data/' + sensor.slug + '-' + day + '.csv'


def sensor_file_paths(sensor, from_date, to_date):
    from_day = from_date.replace(hour=0, minute=0, second=0, microsecond=0)
    to_day = to_date.replace(hour=0, minute=0, second=0, microsecond=0)

    files = []
    date = from_day
    while date <= to_day:
        files.append(sensor_file_path(sensor, date))
        date = date + timedelta(days=1)
    return files
