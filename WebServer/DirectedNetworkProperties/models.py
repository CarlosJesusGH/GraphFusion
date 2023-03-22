from django.db import models


class DirectedNetworkPropertiesResult(models.Model):
    avg_path_length =  models.FloatField(blank=False, null=False)
    clustering_coeff =  models.FloatField(blank=False, null=False)
    degree_distribution = models.One


class DegreeDistributionPoint(models.Model):
    number_of_nodes = models.IntegerField(blank=False, null=False)
    degree = models.IntegerField(blank=False, null=False)
