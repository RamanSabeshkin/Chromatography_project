from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Eluent(models.Model):
    name = models.CharField(max_length=100, verbose_name="1-st solvent, 2-nd solvent", unique=True)
    description = models.TextField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100, unique_for_date='publish')

    publish = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_eluent')

    def __str__(self):
        return self.slug


class Column(models.Model):
    COLUMN_TYPE = [
        ('C18', 'C18-column'),
        ('C8', 'C8-column'),
    ]
    type = models.CharField(max_length=20, choices=COLUMN_TYPE, default='C18', )
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20, unique=True)
    manufacturer = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=50, blank=True, verbose_name="Dimensions, L×i.d.(mm×mm)")
    particle_size = models.DecimalField(blank=True,
                                        null=True, verbose_name="Particle size (µm)",
                                        max_digits=5, decimal_places=2, )
    pore_size = models.DecimalField(blank=True, null=True,
                                    verbose_name="Pore size (C)",
                                    max_digits=5, decimal_places=2, )
    pore_volume = models.DecimalField(blank=True, null=True,
                                      verbose_name="Pore volume (ml/g)",
                                      max_digits=5, decimal_places=2, )
    surface_area = models.DecimalField(blank=True, null=True,
                                       verbose_name="Surface area (m^2/g)",
                                       max_digits=6, decimal_places=2, )
    carbon_loading = models.CharField(max_length=50, blank=True, verbose_name="Carbon loading(%)", )
    surface_coverage = models.DecimalField(blank=True, null=True,
                                           verbose_name="Surface coverage (µmol/m^2)",
                                           max_digits=5, decimal_places=2, )
    bulk_density = models.DecimalField(blank=True, null=True,
                                       verbose_name="Bulk density (g/ml)",
                                       max_digits=5, decimal_places=2, )
    end_capping = models.CharField(max_length=50, blank=True, )
    silica = models.CharField(max_length=50, blank=True, )

    slug = models.SlugField(max_length=100, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_column', )
    eluents = models.ManyToManyField(Eluent, through='ChromatographicModel')

    def __str__(self):
        return self.abbreviation


class ChromatographicModel(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, to_field='abbreviation')
    eluent = models.ForeignKey(Eluent, on_delete=models.CASCADE, to_field='name')
    k1 = models.DecimalField(max_digits=7, decimal_places=4, )
    k2 = models.DecimalField(max_digits=7, decimal_places=4, )
    temperature = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Temperature of column (°C)", )
    flow_rate = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Flow rate (ml/min)", )
    injected_volume = models.DecimalField(max_digits=3, decimal_places=1,
                                          verbose_name="Injected volume (µl)", blank=True, )

    slug = models.SlugField(max_length=100, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_chromatographicmodel', )

    def __str__(self):
        return self.slug

