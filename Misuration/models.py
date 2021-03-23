import datetime
from _csv import Error

from django.db import models

import csv
import sys

csv.field_size_limit(sys.maxsize)

# Create your models here.
from DataRetrival.models import Software, Version


class Class(models.Model):
    name = models.CharField(max_length=128, null=True)
    software = models.ForeignKey(Software, on_delete=models.CASCADE, null=True)
    file_path = models.TextField()

    def __str__(self):
        return '%s' % self.name


class Measure(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True)
    commit_hash = models.CharField(max_length=40, null=True)
    total_insertions_for_bugs = models.IntegerField(default=0)
    total_deletions_for_bugs = models.IntegerField(default=0)
    total_deletions_for_other = models.IntegerField(default=0)
    total_insertions_for_other = models.IntegerField(default=0)
    days_for_resolution = models.IntegerField(default=0)
    days_for_resolution_avg = models.IntegerField(default=0)
    bug_identifier = models.IntegerField(default=0)
    wmc = models.FloatField(max_length=16)
    dit = models.FloatField(max_length=16)
    noc = models.FloatField(max_length=16)
    cbo = models.FloatField(max_length=16)
    rfc = models.FloatField(max_length=16)
    lcom = models.FloatField(max_length=16)
    loc = models.FloatField(max_length=16)
    cloc = models.FloatField(max_length=16)
    bloc = models.FloatField(max_length=16)
    ifanin = models.FloatField(max_length=16)
    nmethod = models.FloatField(max_length=16)
    bugged_files_occurrences = models.IntegerField(default=0)
    bugged_files_solved = models.IntegerField(default=0)
    bugs_solved = models.IntegerField(default=0)
    research_question = models.IntegerField(default=0)
    bugged = models.IntegerField(default=False)
    severity = models.CharField(max_length=128)

    def __str__(self):
        return '%s - %s' % (self.class_name, self.commit_hash)
