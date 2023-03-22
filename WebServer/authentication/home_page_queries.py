__author__ = 'varun'

from .models import Feature, SampleNetwork, Description


def get_all_features():
    features = Feature.objects.all().order_by('position')
    return [features[:3], features[3:]]


def get_all_sample_networks():
    return SampleNetwork.objects.all()


def get_all_descriptions():
    return Description.objects.all().order_by('position')