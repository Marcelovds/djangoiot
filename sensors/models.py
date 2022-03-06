from django.db import models


class Sensor(models.Model):
    TEMPERATURA = 'temperatura'
    UMIDADE = 'umidade'
    PRESSAO = 'pressao'
    VAZAO = 'vazao'
    BATERIA = 'bateria'

    SENSOR_TYPES = [
        (TEMPERATURA, 'Temperatura'),
        (UMIDADE, 'Umidade'),
        (PRESSAO, 'Pressao'),
        (VAZAO, 'Vazao'),
        (BATERIA, 'Bateria')
    ]
    SENSOR_FORMATS = dict([
        (TEMPERATURA, 'temperatura,date'),
        (UMIDADE, 'umidade,date'),
        (PRESSAO, 'pressao,date'),
        (VAZAO, 'vazao,date'),
        (BATERIA, 'bateria,date')
    ])

    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    type = models.CharField(
        max_length=20,
        choices=SENSOR_TYPES,
        default=PRESSAO,
    )
    format = models.CharField(blank=True, max_length=200,
                              help_text="Deixe em branco para deixar no formato padrão (recomendado).")
    creation_date = models.DateTimeField('creation date')

    def save(self, *args, **kwargs):
        if self.format == '':
            self.format = self.SENSOR_FORMATS[self.type]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
