from django.http import HttpResponse
from DataRetrival.models import Software, TrackedBug, File, Version, Bug
from django.shortcuts import render
from django.db.models import Sum
from dateutil.relativedelta import relativedelta


def create_software(request):
    # software creation
    software, created = Software.objects.get_or_create(name='swt',
                                                       log_file_path='media/swt/logs.csv',
                                                       source_root_folder='bundles')
    software.create_cleaned_log_instances()

    # version creation
    version, created = Version.objects.get_or_create(name='AllVersions',
                                                     bug_file_path='media/swt/AllVersions/bugs.csv',
                                                     software=software)
    version.create_bug_instances_from_csv()
    version.create_tracked_bugs()

    return HttpResponse('OK')


def software_list(request):
    return render(request, 'DataRetrival/SoftwareList.html', {'software': Software.objects.all().distinct('name')})


def version_details(request, pk):
    tracked_bugs = TrackedBug.objects.filter(version=pk)
    return render(request, 'DataRetrival/VersionDetails.html', {'tracked_bugs': tracked_bugs.order_by('log__date')})


def files_list(request, pk):
    files_dist = File.objects.filter(tracked_bug__version__software_id=pk).distinct('file_path')
    context = []
    for f in files_dist:
        files = File.objects.filter(file_path=f.file_path)
        n_occur = files.count()
        ins = files.aggregate(Sum('insertions'))
        dels = files.aggregate(Sum('deletions'))
        context.append((f.file_name, f.file_path, n_occur, ins['insertions__sum'], dels['deletions__sum']))
    return render(request, 'DataRetrival/FilesList.html', {'files': context})


def version_anomalies(request, pk):
    tracked_bugs = TrackedBug.objects.filter(version=pk)
    anomalies = list()
    for tb in tracked_bugs:
        anomaly = None
        r = relativedelta(tb.log.date, tb.bug.opened)
        if r.months + (12 * r.years) > 8 and TrackedBug.objects.filter(bug=tb.bug).count() > 1:
            anomaly = (tb, 'More than 12 months between bug and commit. More than 1 commit for this bug.')
        elif r.months + (12 * r.years) > 8:
            anomaly = (tb, 'More than 12 months between bug and commit.')
        elif TrackedBug.objects.filter(bug=tb.bug).count() > 1:
            anomaly = (tb, 'More than 1 commit for this bug.')
        if anomaly:
            anomalies.append(anomaly)
    return render(request, 'DataRetrival/VersionAnomalies.html', {'tracked_bugs': anomalies})
