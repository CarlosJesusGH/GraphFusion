from django.db import models


class Feature(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    position = models.IntegerField('Position', primary_key=True)
    image = models.ImageField('Image', upload_to="landing-page/features", blank=True)

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_image(self):
        return self.image


class Description(models.Model):
    description = models.TextField('Description')
    position = models.IntegerField('Position', primary_key=True, unique=True)

    def get_description(self):
        return self.description

    def get_position(self):
        return self.position


class SampleNetwork(models.Model):
    name = models.CharField("Network Name", max_length=100, blank=False)
    network_file = models.FileField("Network File", upload_to="sample-networks", blank=False)

    def get_name(self):
        return self.name

    def get_file(self):
        return self.network_file

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name