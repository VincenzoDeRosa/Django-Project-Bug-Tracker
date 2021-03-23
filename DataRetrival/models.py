import datetime
import re
from _csv import Error

from dateutil.relativedelta import relativedelta
from django.db import models

import csv
import sys


csv.field_size_limit(sys.maxsize)

import xml.etree.ElementTree as ET


# Create your models here.


class Software(models.Model):
    name = models.CharField(max_length=128)
    log_file_path = models.CharField(max_length=128)
    source_root_folder = models.CharField(max_length=512)

    def create_cleaned_log_instances(self):
        with open(self.log_file_path, mode='r', encoding='utf8') as csv_file:
            filtered = (line.replace('\r', '') for line in csv_file)
            csv_reader = csv.DictReader(filtered)
            iter = 0
            for row in csv_reader:
                try:
                    iter += 1
                    if row["commit hash"] and row["parent hash"]:
                        if row["date"]:
                            try:
                                date_time_obj = datetime.datetime.strptime(row["date"][:-15], '%Y-%m-%d').date()
                            except ValueError:
                                date_time_obj = datetime.datetime.strptime(row["date"], '%Y-%m-%d').date()
                        else:
                            date_time_obj = None
                        if ".java" in row["changed files"]:
                            Log.objects.get_or_create(commit_hash=row["commit hash"],
                                                      parent_hash=row["parent hash"],
                                                      author=row["author"],
                                                      date=date_time_obj,
                                                      subject=row["subject"],
                                                      changed_files=row["changed files"],
                                                      software=self)
                except Error:
                    print(Error)

    def get_versions(self):
        return Version.objects.filter(software=self).order_by('name')

    def get_logs(self):
        return Log.objects.filter(software=self)

    def __str__(self):
        return '%s' % self.name


class Version(models.Model):
    name = models.CharField(max_length=128)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    bug_file_path = models.CharField(max_length=128)

    def create_bug_instances_from_xml(self):
        tree = ET.parse(self.bug_file_path)
        for bug in tree.getroot().findall('bug'):
            cc_list = ""
            delta_ts = bug.find('creation_ts').text
            date_time_obj = datetime.datetime.strptime(delta_ts[:-6], '%Y-%m-%d %H:%M:%S')
            b, created = Bug.objects.get_or_create(bug_identifier=bug.find('bug_id').text,
                                                   assignee=bug.find('assigned_to').get('name'),
                                                   status=bug.find('bug_status').text,
                                                   resolution=bug.find('resolution').text,
                                                   summary=bug.find('short_desc').text,
                                                   opened=date_time_obj,
                                                   severity=bug.find('bug_severity').text,
                                                   target_milestone=bug.find('target_milestone').text,
                                                   version=self)
            for cc in bug.iter('cc'):
                cc_list += cc.text + '%%'
            b.cc_list = cc_list[:-3]
            b.save()

    def create_bug_instances_from_csv(self):
        with open(self.bug_file_path, mode='r', encoding='utf8') as csv_file:
            filtered = (line.replace('\r', '') for line in csv_file)
            csv_reader = csv.DictReader(filtered)
            for row in csv_reader:
                try:
                    date_time_obj = datetime.datetime.strptime(row['Opened'], '%Y-%m-%d %H:%M:%S')
                    Bug.objects.get_or_create(bug_identifier=row['Bug ID'],
                                              assignee=row['Assignee'],
                                              status=row['Status'],
                                              resolution=row['Resolution'],
                                              summary=row['Summary'],
                                              opened=date_time_obj,
                                              severity=row['Severity'],
                                              target_milestone=row['Target Milestone'],
                                              version=self,
                                              cc_list='')
                except Error:
                    print(Error)


    def get_bugs(self):
        return Bug.objects.filter(version=self)

    def get_tracked_bugs(self):
        return TrackedBug.objects.filter(version=self).distinct('bug__bug_identifier')

    def create_tracked_bugs(self):
        for bug in Bug.objects.filter(version=self):
            for log in Log.objects.filter(software=self.software):
                if (' ' + str(bug.bug_identifier) + ' ' in ' ' + log.subject + ' ') or (' #' + str(bug.bug_identifier) + ' ' in ' ' + log.subject + ' '):
                    string_files = " ".join(log.changed_files.split())
                    files = re.findall(r'\d+\s\d+\s\w+/.*?\.\w+(?!\S)|\d+\s\d+\s[\w+?\.\w+]+/.*?\.\w+(?!\S)',
                                       string_files)
                    for f in files:
                        if ".java" in f and "=>" not in f:
                            filename = re.findall(r'\w+.java', f)
                            modifications = re.findall(r"\d+\s\d+", f)
                            path = re.findall(r'\s\w+/.*?\.\w+(?!\S)|\s[\w+?\.\w+]+/.*?\.\w+(?!\S)', f)
                            splitted = modifications[0].split(" ")
                            for root in bug.version.software.source_root_folder.split('@#'):
                                if root in path[0] and 'test' not in path[0]:
                                    tb, created = TrackedBug.objects.get_or_create(bug=bug, log=log, version=bug.version)
                                    File.objects.get_or_create(file_name=filename[0], file_path=path[0].strip(), tracked_bug=tb,
                                                               insertions=splitted[0], deletions=splitted[1])
        # delete bugs with resolution > 12 months
        tracked_bugs = TrackedBug.objects.filter(version=self)
        exclude = []
        for tb in tracked_bugs:
            r = relativedelta(tb.log.date, tb.bug.opened)
            if r.months + (12 * r.years) >= 12:
                exclude.append(tb.pk)
        tracked_bugs_without_anomalies = tracked_bugs.exclude(pk__in=exclude).order_by('log__date')
        diff = tracked_bugs.difference(tracked_bugs_without_anomalies)
        for x in diff:
            x.delete()

    def dataset_rq1(self, commit_hash, start_date=None, end_date=None):
        from Misuration.models import Class, Measure
        if self.name == 'AllVersions':
            path = 'media/%s/%s/%s/metrics.csv' % (self.software.name, self.name, commit_hash)
            tracked_bugs = TrackedBug.objects.filter(version=self).exclude(bug__severity=Bug.ENHANCEMENT)
            files_dist = File.objects.filter(tracked_bug__in=tracked_bugs, tracked_bug__version=self).values('file_name', 'file_path').distinct()
            if start_date and end_date:
                # bugs in the data range
                tracked_bugs_between_logs = TrackedBug.objects.filter(version=self, log__date__gte=start_date, log__date__lte=end_date).exclude(bug__severity=Bug.ENHANCEMENT)
                solved_bugs = tracked_bugs_between_logs.distinct('bug__bug_identifier').count()
                files_dist_2 = File.objects.filter(tracked_bug__in=tracked_bugs_between_logs, tracked_bug__version=self).values('tracked_bug__bug__bug_identifier', 'file_path', 'file_name').distinct()
            else:
                solved_bugs = 0
            context = []
            for f in files_dist:
                # I want the occurrences of the buggy files for each individual bug, so if I have two commits of the same bug with the same files, I only count one occurrence
                files = File.objects.filter(tracked_bug__version=self, tracked_bug__in=tracked_bugs, file_path=f['file_path'], file_name=f['file_name']).values('tracked_bug__bug__bug_identifier', 'file_path', 'file_name').distinct()
                n_occur = files.count()
                context.append((f['file_name'].strip(), f['file_path'].strip(), n_occur))
            with open(path, mode='r') as csv_file:
                filtered = (line.replace('\r', '') for line in csv_file)
                csv_reader = csv.DictReader(filtered)
                for row in csv_reader:
                    try:
                        if 'Class' in row['Kind'] and 'Anonymous' not in row['Kind']:
                            name = row['Name'].split('.')[-1] + '.java'
                            path = row['File'].replace("\\", "/").split('%s/' % commit_hash)[1].strip()
                            cl, created = Class.objects.get_or_create(name=name.strip(), file_path=path,
                                                                      software=self.software)
                            file = [item for item in context if path in item and name.strip() in item]
                            if file:
                                occurences = file[0][2]
                            else:
                                occurences = 0
                            if start_date and end_date:
                                solved_files_bugged = files_dist_2.filter(file_path=path, file_name=name.strip()).count()
                            else:
                                solved_files_bugged = 0
                            ms, created = Measure.objects.get_or_create(class_name=cl, version=self,
                                                                        commit_hash=commit_hash,
                                                                        research_question=1,
                                                                        bugged_files_occurrences=occurences,
                                                                        bugs_solved=solved_bugs,
                                                                        bugged_files_solved=solved_files_bugged,
                                                                        wmc=row['SumCyclomatic'],
                                                                        dit=row['MaxInheritanceTree'],
                                                                        noc=row['CountClassDerived'],
                                                                        cbo=row['CountClassCoupled'],
                                                                        rfc=row['CountDeclMethodAll'],
                                                                        lcom=row['PercentLackOfCohesion'],
                                                                        loc=row['CountLineCode'],
                                                                        cloc=row['CountLineComment'],
                                                                        bloc=row['CountLineBlank'],
                                                                        ifanin=row['CountClassBase'],
                                                                        nmethod=row['CountDeclMethod'])
                            if start_date and end_date:
                                for bug in tracked_bugs_between_logs:
                                    files = File.objects.filter(tracked_bug=bug, tracked_bug__version=self)
                                    for f in files:
                                        if f.file_path.strip() == cl.file_path.strip() and f.file_name.strip() == cl.name.strip():
                                            ms.total_insertions_for_bugs += f.insertions
                                            ms.total_deletions_for_bugs += f.deletions
                                            ms.save()
                    except Error:
                        print(Error)
            if start_date and end_date:
                logs = Log.objects.filter(software=self.software, date__gte=start_date, date__lte=end_date)
                for log in logs:
                    if 'restore head' not in log.subject:
                        string_files = " ".join(log.changed_files.split())
                        files = re.findall(r'\d+\s\d+\s\w+/.*?\.\w+(?!\S)|\d+\s\d+\s[\w+?\.\w+]+/.*?\.\w+(?!\S)',
                                           string_files)
                        for f in files:
                            if ".java" in f and "=>" not in f:
                                filename = re.findall(r'\w+.java', f)
                                modifications = re.findall(r"\d+\s\d+", f)
                                path = re.findall(r'\s\w+/.*?\.\w+(?!\S)|\s[\w+?\.\w+]+/.*?\.\w+(?!\S)', f)
                                splitted = modifications[0].split(" ")
                                if Measure.objects.filter(commit_hash=commit_hash, class_name__file_path=path[0].strip(), class_name__name=filename[0].strip(), research_question=1):
                                    ms = Measure.objects.get(commit_hash=commit_hash, class_name__file_path=path[0].strip(), class_name__name=filename[0].strip(), research_question=1)
                                    ms.total_insertions_for_other += int(splitted[0])
                                    ms.total_deletions_for_other += int(splitted[1])
                                    ms.save()

    def dataset_rq2(self, commit_hash, start_date=None, end_date=None):
        from Misuration.models import Class, Measure
        if self.name == 'AllVersions':
            path = 'media/%s/%s/%s/metrics.csv' % (self.software.name, self.name, commit_hash)
            tracked_bugs = TrackedBug.objects.filter(version=self, bug__severity=Bug.ENHANCEMENT)
            files_dist = File.objects.filter(tracked_bug__version=self, tracked_bug__in=tracked_bugs).values('file_name', 'file_path').distinct()
            if start_date and end_date:
                # bugs in the data range
                tracked_bugs_between_logs = TrackedBug.objects.filter(version=self, log__date__gte=start_date,
                                                                      log__date__lte=end_date, bug__severity=Bug.ENHANCEMENT)
                solved_bugs = tracked_bugs_between_logs.distinct('bug__bug_identifier').count()
                files_dist_2 = File.objects.filter(tracked_bug__version=self, tracked_bug__in=tracked_bugs_between_logs).values(
                    'tracked_bug__bug__bug_identifier', 'file_path', 'file_name').distinct()
            else:
                solved_bugs = 0
            context = []
            for f in files_dist:
                # I want the occurrences of the buggy files for each individual bug, so if I have two commits of the same bug with the same files, I only count one occurrence
                files = File.objects.filter(tracked_bug__version=self, tracked_bug__in=tracked_bugs, file_path=f['file_path'],
                                            file_name=f['file_name']).values('tracked_bug__bug__bug_identifier',
                                                                             'file_path', 'file_name').distinct()
                n_occur = files.count()
                context.append((f['file_name'].strip(), f['file_path'].strip(), n_occur))
            with open(path, mode='r') as csv_file:
                filtered = (line.replace('\r', '') for line in csv_file)
                csv_reader = csv.DictReader(filtered)
                for row in csv_reader:
                    try:
                        if 'Class' in row['Kind'] and 'Anonymous' not in row['Kind']:
                            name = row['Name'].split('.')[-1] + '.java'
                            path = row['File'].replace("\\", "/").split('%s/' % commit_hash)[1].strip()
                            cl, created = Class.objects.get_or_create(name=name.strip(), file_path=path,
                                                                      software=self.software)
                            file = [item for item in context if path in item and name.strip() in item]
                            if file:
                                occurences = file[0][2]
                            else:
                                occurences = 0
                            if start_date and end_date:
                                solved_files_bugged = files_dist_2.filter(file_path=path,
                                                                          file_name=name.strip()).count()
                            else:
                                solved_files_bugged = 0
                            ms, created = Measure.objects.get_or_create(class_name=cl, version=self,
                                                                        commit_hash=commit_hash,
                                                                        research_question=2,
                                                                        bugged_files_occurrences=occurences,
                                                                        bugs_solved=solved_bugs,
                                                                        bugged_files_solved=solved_files_bugged,
                                                                        wmc=row['SumCyclomatic'],
                                                                        dit=row['MaxInheritanceTree'],
                                                                        noc=row['CountClassDerived'],
                                                                        cbo=row['CountClassCoupled'],
                                                                        rfc=row['CountDeclMethodAll'],
                                                                        lcom=row['PercentLackOfCohesion'],
                                                                        loc=row['CountLineCode'],
                                                                        cloc=row['CountLineComment'],
                                                                        bloc=row['CountLineBlank'],
                                                                        ifanin=row['CountClassBase'],
                                                                        nmethod=row['CountDeclMethod'])
                            if start_date and end_date:
                                for bug in tracked_bugs_between_logs:
                                    files = File.objects.filter(tracked_bug__version=self, tracked_bug=bug)
                                    for f in files:
                                        if f.file_path.strip() == cl.file_path.strip() and f.file_name.strip() == cl.name.strip():
                                            ms.total_insertions_for_bugs += f.insertions
                                            ms.total_deletions_for_bugs += f.deletions
                                            ms.save()
                    except Error:
                        print(Error)
            if start_date and end_date:
                logs = Log.objects.filter(software=self.software, date__gte=start_date, date__lte=end_date)
                for log in logs:
                    if 'restore head' not in log.subject:
                        string_files = " ".join(log.changed_files.split())
                        files = re.findall(r'\d+\s\d+\s\w+/.*?\.\w+(?!\S)|\d+\s\d+\s[\w+?\.\w+]+/.*?\.\w+(?!\S)',
                                           string_files)
                        for f in files:
                            if ".java" in f and "=>" not in f:
                                filename = re.findall(r'\w+.java', f)
                                modifications = re.findall(r"\d+\s\d+", f)
                                path = re.findall(r'\s\w+/.*?\.\w+(?!\S)|\s[\w+?\.\w+]+/.*?\.\w+(?!\S)', f)
                                splitted = modifications[0].split(" ")
                                if Measure.objects.filter(commit_hash=commit_hash,
                                                          class_name__file_path=path[0].strip(),
                                                          class_name__name=filename[0].strip(), research_question=2):
                                    ms = Measure.objects.get(commit_hash=commit_hash,
                                                             class_name__file_path=path[0].strip(),
                                                             class_name__name=filename[0].strip(), research_question=2)
                                    ms.total_insertions_for_other += int(splitted[0])
                                    ms.total_deletions_for_other += int(splitted[1])
                                    ms.save()

    def dataset_rq3(self, commit_hash, start_date, end_date):
        from Misuration.models import Class, Measure
        if self.name == 'AllVersions':
            path = 'media/%s/%s/%s/metrics.csv' % (self.software.name, self.name, commit_hash)
            tracked_bugs_between_logs = TrackedBug.objects.filter(version=self, log__date__gte=start_date,
                                                                  log__date__lte=end_date).exclude(bug__severity=Bug.ENHANCEMENT).values('bug__bug_identifier').distinct()
            with open(path, mode='r') as csv_file:
                filtered = (line.replace('\r', '') for line in csv_file)
                csv_reader = csv.DictReader(filtered)
                for row in csv_reader:
                    try:
                        if 'Class' in row['Kind'] and 'Anonymous' not in row['Kind']:
                            name = row['Name'].split('.')[-1] + '.java'
                            path = row['File'].replace("\\", "/").split('%s/' % commit_hash)[1].strip()
                            cl, created = Class.objects.get_or_create(name=name.strip(), file_path=path,
                                                                      software=self.software)
                            for bug in tracked_bugs_between_logs:
                                files = File.objects.filter(tracked_bug__bug__bug_identifier=bug['bug__bug_identifier'],
                                                            tracked_bug__version=self)
                                for f in files:
                                    if f.file_path.strip() == cl.file_path.strip() and f.file_name.strip() == cl.name.strip():
                                        severity = Bug.objects.get(version=self, bug_identifier=bug['bug__bug_identifier']).severity
                                        ms, new = Measure.objects.get_or_create(class_name=cl, version=self,
                                                                                    commit_hash=commit_hash,
                                                                                    research_question=3,
                                                                                    bug_identifier=bug['bug__bug_identifier'],
                                                                                    wmc=row['SumCyclomatic'],
                                                                                    dit=row['MaxInheritanceTree'],
                                                                                    noc=row['CountClassDerived'],
                                                                                    cbo=row['CountClassCoupled'],
                                                                                    rfc=row['CountDeclMethodAll'],
                                                                                    lcom=row['PercentLackOfCohesion'],
                                                                                    loc=row['CountLineCode'],
                                                                                    cloc=row['CountLineComment'],
                                                                                    bloc=row['CountLineBlank'],
                                                                                    ifanin=row['CountClassBase'],
                                                                                    nmethod=row['CountDeclMethod'],
                                                                                    severity=severity)
                                        # If it is not created, it means that it already exists, so for the same bug id I will have the same file modified several times. So I aggregate the changes to that file.
                                        if new:
                                            ms.total_insertions_for_bugs = f.insertions
                                            ms.total_deletions_for_bugs = f.deletions
                                            ms.save()
                                        else:
                                            ms.total_insertions_for_bugs += f.insertions
                                            ms.total_deletions_for_bugs += f.deletions
                                            ms.save()
                    except Error:
                        print(Error)

class Log(models.Model):
    commit_hash = models.CharField(max_length=40, null=True)
    parent_hash = models.CharField(max_length=40, null=True)
    author = models.CharField(max_length=128, null=True)
    date = models.DateField(null=True)
    subject = models.TextField(null=True)
    changed_files = models.TextField(null=True)
    software = models.ForeignKey(Software, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s' % self.commit_hash

class Bug(models.Model):
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    NORMAL = "normal"
    MINOR = "minor"
    TRIVIAL = "trivial"
    ENHANCEMENT = "enhancement"

    bug_identifier = models.IntegerField()
    assignee = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    resolution = models.CharField(max_length=128)
    summary = models.TextField()
    opened = models.DateField()
    severity = models.CharField(max_length=128)
    target_milestone = models.CharField(max_length=128)
    version = models.ForeignKey(Version,
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return '%s' % self.bug_identifier


class TrackedBug(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    log = models.ForeignKey(Log, on_delete=models.CASCADE)

    def get_files(self):
        return File.objects.filter(tracked_bug=self)

    def __str__(self):
        return '%s' % self.id


class File(models.Model):
    file_name = models.CharField(max_length=128)
    file_path = models.TextField()
    tracked_bug = models.ForeignKey(TrackedBug, on_delete=models.CASCADE)
    insertions = models.IntegerField()
    deletions = models.IntegerField()

    def __str__(self):
        return '%s' % self.file_name
