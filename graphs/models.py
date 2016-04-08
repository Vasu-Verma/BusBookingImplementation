from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from django.db import models

class Edges(models.Model):
	Vertex1 = models.CharField(max_length=150)
	Vertex2 = models.CharField(max_length=150)
	Weight = models.BigIntegerField()
	


class Vertices(models.Model):
	name = models.CharField(max_length=150)

class Bus(models.Model):
	Number = models.CharField(max_length=150)
	Path = models.TextField(max_length=400000)
	def __unicode__(self):
		return smart_unicode(self.Number)
	def Path_as_list(self):
		return self.Path.split(",")
# Create your models here.
