import os
from datetime import timezone, datetime

from django.test import TestCase

from .views import sensor_file_paths
from .models import Sensor


class SensorStorageTests(TestCase):

    def test_calculate_sensor_files_in_between_two_dates(self):
        """
        sensor_file_paths() returns a list of file paths, one for each day in between two dates, both dates included
        """
        sensor = Sensor(
            name='TestSensor',
            slug='test',
            format='temp,humidity,date'
        )
        from_date = datetime.strptime('2020-12-07', '%Y-%m-%d')
        to_date = datetime.strptime('2020-12-09', '%Y-%m-%d')

        paths = sensor_file_paths(sensor, from_date, to_date)

        project_path = os.path.abspath(os.path.dirname(__name__))
        expected_paths = [
            project_path + '/data/test-2020-12-07.csv',
            project_path + '/data/test-2020-12-08.csv',
            project_path + '/data/test-2020-12-09.csv'
        ]
        self.assertEquals(paths, expected_paths, 'sensor files between two dates do not match')

    def test_calculate_sensor_files_when_in_between_two_days(self):
        """
        sensor_file_paths() returns a list of file paths, one for each day in between two dates, both dates included
        """
        sensor = Sensor(
            name='TestSensor',
            slug='test',
            format='temp,humidity,date'
        )
        from_date = datetime.fromtimestamp(1608420600, timezone.utc)  # 2020-12-19 23:30
        to_date = datetime.fromtimestamp(1608424200, timezone.utc)  # 2020-12-20 00:30

        paths = sensor_file_paths(sensor, from_date, to_date)

        project_path = os.path.abspath(os.path.dirname(__name__))
        expected_paths = [
            project_path + '/data/test-2020-12-19.csv',
            project_path + '/data/test-2020-12-20.csv'
        ]
        self.assertEquals(paths, expected_paths, 'sensor files between two dates when in between days do not match')

