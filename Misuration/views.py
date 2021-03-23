from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from DataRetrival.models import Version, Bug
from Misuration.models import Measure
from djqscsv import write_csv


def create_measures_rq1(request):
    version = Version.objects.get(name='AllVersions', software__name='jdt')
    # Detailed dataset
    version.dataset_rq1('b035f7a4c467249c63cc869fd5f75e4bad8cf303')
    version.dataset_rq1('4e3d522e86b4dbde916017a602e046903b89c502', '2015-01-03', '2015-06-30')
    version.dataset_rq1('8bcd93659b03cef1840f96fe89a46264aadd1f45', '2015-07-01', '2015-12-31')
    version.dataset_rq1('f3bfae5dab0876c081285b39b99ee175c6789d5e', '2016-01-01', '2016-06-29')
    version.dataset_rq1('e5a7d0aa05379c4d2fc91287bfa03a7d5e0b029a', '2016-06-30', '2016-12-25')
    version.dataset_rq1('47a90e7b1de4688e7f32fe6fd2c477a26a451a47', '2016-12-26', '2017-06-30')
    version.dataset_rq1('5a2e5fc5d9901cc4ff9cc91a93aff365e80f9f94', '2017-07-01', '2017-12-26')
    version.dataset_rq1('63a9c515c209e6bf2abb66917b314514c45cc943', '2017-12-27', '2018-06-30')
    version.dataset_rq1('4cf7716d7704e6dde6cf2a66fd8b143cad9df805', '2018-07-01', '2018-12-29')
    version.dataset_rq1('ee8afd3f2611403b3beb75ba311eda4769a6da40', '2018-12-30', '2019-06-28')
    version.dataset_rq1('6a1b569cd8c1b29ac527dc139575b75c0ac810dc', '2019-06-29', '2019-12-29')
    version.dataset_rq1('03c0989a5bc07e20793e344c6ad788f76b8de370', '2019-12-30', '2020-06-30')
    version.dataset_rq1('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2020-07-01', '2020-12-24')
    qs = Measure.objects.filter(research_question=1, version=version).values('commit_hash', 'bugs_solved',
                                                                             'class_name__name',
                                                                             'class_name__file_path',
                                                                             'bugged_files_occurrences',
                                                                             'bugged_files_solved', 'wmc', 'dit', 'noc',
                                                                             'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod',
                                                                             'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs',
                                                                             'total_deletions_for_other',
                                                                             'total_insertions_for_other').order_by('id')
    with open('dataset_swt_rq1_detailed.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    # General dataset
    Measure.objects.filter(research_question=1, version=version).delete()
    version.dataset_rq1('b035f7a4c467249c63cc869fd5f75e4bad8cf303')
    version.dataset_rq1('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2015-01-03', '2020-12-24')
    qs = Measure.objects.filter(research_question=1, version=version).values('commit_hash', 'bugs_solved',
                                                                             'class_name__name',
                                                                             'class_name__file_path',
                                                                             'bugged_files_occurrences',
                                                                             'bugged_files_solved', 'wmc', 'dit', 'noc',
                                                                             'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod',
                                                                             'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs',
                                                                             'total_deletions_for_other',
                                                                             'total_insertions_for_other').order_by('id')
    with open('dataset_swt_rq1_detailed.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return HttpResponse('OK')


def create_measures_rq2(request):
    version = Version.objects.get(name='AllVersions', software__name='jdt')
    # Detailed dataset
    version.dataset_rq2('b035f7a4c467249c63cc869fd5f75e4bad8cf303')
    version.dataset_rq2('4e3d522e86b4dbde916017a602e046903b89c502', '2015-01-03', '2015-06-30')
    version.dataset_rq2('8bcd93659b03cef1840f96fe89a46264aadd1f45', '2015-07-01', '2015-12-31')
    version.dataset_rq2('f3bfae5dab0876c081285b39b99ee175c6789d5e', '2016-01-01', '2016-06-29')
    version.dataset_rq2('e5a7d0aa05379c4d2fc91287bfa03a7d5e0b029a', '2016-06-30', '2016-12-25')
    version.dataset_rq2('47a90e7b1de4688e7f32fe6fd2c477a26a451a47', '2016-12-26', '2017-06-30')
    version.dataset_rq2('5a2e5fc5d9901cc4ff9cc91a93aff365e80f9f94', '2017-07-01', '2017-12-26')
    version.dataset_rq2('63a9c515c209e6bf2abb66917b314514c45cc943', '2017-12-27', '2018-06-30')
    version.dataset_rq2('4cf7716d7704e6dde6cf2a66fd8b143cad9df805', '2018-07-01', '2018-12-29')
    version.dataset_rq2('ee8afd3f2611403b3beb75ba311eda4769a6da40', '2018-12-30', '2019-06-28')
    version.dataset_rq2('6a1b569cd8c1b29ac527dc139575b75c0ac810dc', '2019-06-29', '2019-12-29')
    version.dataset_rq2('03c0989a5bc07e20793e344c6ad788f76b8de370', '2019-12-30', '2020-06-30')
    version.dataset_rq2('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2020-07-01', '2020-12-24')
    qs = Measure.objects.filter(research_question=2, version=version).values('commit_hash', 'bugs_solved',
                                                                             'class_name__name',
                                                                             'class_name__file_path',
                                                                             'bugged_files_occurrences',
                                                                             'bugged_files_solved', 'wmc', 'dit', 'noc',
                                                                             'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod',
                                                                             'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs',
                                                                             'total_deletions_for_other',
                                                                             'total_insertions_for_other').order_by('id')
    with open('dataset_swt_rq2.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    # General analysis
    Measure.objects.filter(research_question=2, version=version).delete()
    version.dataset_rq2('b035f7a4c467249c63cc869fd5f75e4bad8cf303')
    version.dataset_rq2('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2015-01-03', '2020-12-24')
    qs = Measure.objects.filter(research_question=2, version=version).values('commit_hash', 'bugs_solved',
                                                                             'class_name__name',
                                                                             'class_name__file_path',
                                                                             'bugged_files_occurrences',
                                                                             'bugged_files_solved', 'wmc', 'dit', 'noc',
                                                                             'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod',
                                                                             'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs',
                                                                             'total_deletions_for_other',
                                                                             'total_insertions_for_other').order_by('id')
    with open('dataset_swt_rq2_general.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return HttpResponse('OK')

def create_measures_rq3(request):
    version = Version.objects.get(name='AllVersions', software__name='jdt')
    version.dataset_rq3('b035f7a4c467249c63cc869fd5f75e4bad8cf303', '2015-01-03', '2015-06-30')
    version.dataset_rq3('4e3d522e86b4dbde916017a602e046903b89c502', '2015-07-01', '2015-12-31')
    version.dataset_rq3('8bcd93659b03cef1840f96fe89a46264aadd1f45', '2016-01-01', '2016-06-29')
    version.dataset_rq3('f3bfae5dab0876c081285b39b99ee175c6789d5e', '2016-06-30', '2016-12-25')
    version.dataset_rq3('e5a7d0aa05379c4d2fc91287bfa03a7d5e0b029a', '2016-12-26', '2017-06-30')
    version.dataset_rq3('47a90e7b1de4688e7f32fe6fd2c477a26a451a47', '2017-07-01', '2017-12-26')
    version.dataset_rq3('5a2e5fc5d9901cc4ff9cc91a93aff365e80f9f94', '2017-12-27', '2018-06-30')
    version.dataset_rq3('63a9c515c209e6bf2abb66917b314514c45cc943', '2018-07-01', '2018-12-29')
    version.dataset_rq3('4cf7716d7704e6dde6cf2a66fd8b143cad9df805', '2018-12-30', '2019-06-28')
    version.dataset_rq3('ee8afd3f2611403b3beb75ba311eda4769a6da40', '2019-06-29', '2019-12-29')
    version.dataset_rq3('6a1b569cd8c1b29ac527dc139575b75c0ac810dc', '2019-12-30', '2020-06-30')
    version.dataset_rq3('03c0989a5bc07e20793e344c6ad788f76b8de370', '2020-07-01', '2020-12-24')
    # Deletion of bugs that are between two date ranges
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        double_measure = Measure.objects.filter(version=version, research_question=3, bug_identifier=ms.bug_identifier,
                                                class_name=ms.class_name,
                                                total_insertions_for_bugs=ms.total_insertions_for_bugs,
                                                total_deletions_for_bugs=ms.total_deletions_for_bugs,
                                                days_for_resolution=ms.days_for_resolution,
                                                days_for_resolution_avg=ms.days_for_resolution_avg).order_by('id')
        count = double_measure.count()
        if count > 1:
            to_keep = double_measure[0]
            double_measure.exclude(id=to_keep.id).delete()
            print('deleted %s double measures for bug %s' % (str(count - 1), str(to_keep.bug_identifier)))

    # Aggregation of classes with same metrics
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        measures = Measure.objects.filter(version=version, research_question=3, class_name=ms.class_name,
                                          wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc,
                                          lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin,
                                          nmethod=ms.nmethod)
        if measures.count() > 1:
            tot_ins = measures.aggregate(Sum('total_insertions_for_bugs'))['total_insertions_for_bugs__sum']
            tot_del = measures.aggregate(Sum('total_deletions_for_bugs'))['total_deletions_for_bugs__sum']
        else:
            tot_ins = ms.total_insertions_for_bugs
            tot_del = ms.total_deletions_for_bugs
        Measure.objects.get_or_create(version=version, research_question=33, bugs_solved=measures.count(), class_name=ms.class_name,
                                      wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc, commit_hash=ms.commit_hash,
                                      lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin, nmethod=ms.nmethod,
                                      total_insertions_for_bugs=tot_ins, total_deletions_for_bugs=tot_del)

    qs = Measure.objects.filter(research_question=33, version=version).values('class_name__name', 'class_name__file_path',
                                                                              'bugs_solved', 'wmc', 'dit', 'noc', 'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod', 'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs', 'commit_hash').order_by('id')
    with open('dataset_swt_rq3.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)

    return HttpResponse('OK')

def create_measures_rq6(request):
    version = Version.objects.get(name='AllVersions', software__name='jdt')
    # Detailed dataset
    version.dataset_rq3('4e3d522e86b4dbde916017a602e046903b89c502', '2015-01-03', '2015-06-30')
    version.dataset_rq3('8bcd93659b03cef1840f96fe89a46264aadd1f45', '2015-07-01', '2015-12-31')
    version.dataset_rq3('f3bfae5dab0876c081285b39b99ee175c6789d5e', '2016-01-01', '2016-06-29')
    version.dataset_rq3('e5a7d0aa05379c4d2fc91287bfa03a7d5e0b029a', '2016-06-30', '2016-12-25')
    version.dataset_rq3('47a90e7b1de4688e7f32fe6fd2c477a26a451a47', '2016-12-26', '2017-06-30')
    version.dataset_rq3('5a2e5fc5d9901cc4ff9cc91a93aff365e80f9f94', '2017-07-01', '2017-12-26')
    version.dataset_rq3('63a9c515c209e6bf2abb66917b314514c45cc943', '2017-12-27', '2018-06-30')
    version.dataset_rq3('4cf7716d7704e6dde6cf2a66fd8b143cad9df805', '2018-07-01', '2018-12-29')
    version.dataset_rq3('ee8afd3f2611403b3beb75ba311eda4769a6da40', '2018-12-30', '2019-06-28')
    version.dataset_rq3('6a1b569cd8c1b29ac527dc139575b75c0ac810dc', '2019-06-29', '2019-12-29')
    version.dataset_rq3('03c0989a5bc07e20793e344c6ad788f76b8de370', '2019-12-30', '2020-06-30')
    version.dataset_rq3('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2020-07-01', '2020-12-24')
    # Deletion of bugs that are between two date ranges
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        double_measure = Measure.objects.filter(version=version, research_question=3, bug_identifier=ms.bug_identifier,
                                                class_name=ms.class_name,
                                                total_insertions_for_bugs=ms.total_insertions_for_bugs,
                                                total_deletions_for_bugs=ms.total_deletions_for_bugs,
                                                days_for_resolution=ms.days_for_resolution,
                                                days_for_resolution_avg=ms.days_for_resolution_avg).order_by('id')
        count = double_measure.count()
        if count > 1:
            to_keep = double_measure[0]
            double_measure.exclude(id=to_keep.id).delete()
            print('deleted %s double measures for bug %s' % (str(count - 1), str(to_keep.bug_identifier)))

    # Aggregation of classes with same metrics
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        measures = Measure.objects.filter(version=version, research_question=3, class_name=ms.class_name, commit_hash=ms.commit_hash,
                                          wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc,
                                          lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin, nmethod=ms.nmethod)
        if measures.count() > 1:
            tot_ins = measures.aggregate(Sum('total_insertions_for_bugs'))['total_insertions_for_bugs__sum']
            tot_del = measures.aggregate(Sum('total_deletions_for_bugs'))['total_deletions_for_bugs__sum']
        else:
            tot_ins = ms.total_insertions_for_bugs
            tot_del = ms.total_deletions_for_bugs
        Measure.objects.get_or_create(version=version, research_question=33, bugs_solved=measures.count(), class_name=ms.class_name,
                                      wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc, commit_hash=ms.commit_hash,
                                      lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin, nmethod=ms.nmethod,
                                      total_insertions_for_bugs=tot_ins, total_deletions_for_bugs=tot_del)

    qs = Measure.objects.filter(research_question=33, version=version).values('class_name__name', 'class_name__file_path',
                                                                              'bugs_solved', 'wmc', 'dit', 'noc', 'cbo', 'rfc',
                                                                             'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                             'nmethod', 'total_insertions_for_bugs',
                                                                             'total_deletions_for_bugs', 'commit_hash').order_by('id')
    with open('dataset_swt_rq6_detailed.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)

    # General dataset
    # Reset measures
    Measure.objects.filter(research_question=3, version=version).delete()
    Measure.objects.filter(research_question=33, version=version).delete()
    version.dataset_rq3('7a7d8f1c3d71e40b54a57675cbf6d30b6721e7e9', '2015-01-03', '2020-12-24')

    # Cancello le doppie misurazioni per i bug che si trovano a cavallo tra i range di date
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        double_measure = Measure.objects.filter(version=version, research_question=3, bug_identifier=ms.bug_identifier,
                                                class_name=ms.class_name,
                                                total_insertions_for_bugs=ms.total_insertions_for_bugs,
                                                total_deletions_for_bugs=ms.total_deletions_for_bugs,
                                                days_for_resolution=ms.days_for_resolution,
                                                days_for_resolution_avg=ms.days_for_resolution_avg).order_by('id')
        count = double_measure.count()
        if count > 1:
            to_keep = double_measure[0]
            double_measure.exclude(id=to_keep.id).delete()
            print('deleted %s double measures for bug %s' % (str(count - 1), str(to_keep.bug_identifier)))

    # Aggregation of classes with same metrics
    for ms in Measure.objects.filter(version=version, research_question=3).order_by('id'):
        measures = Measure.objects.filter(version=version, research_question=3, class_name=ms.class_name,
                                          commit_hash=ms.commit_hash,
                                          wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc,
                                          lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin,
                                          nmethod=ms.nmethod)
        if measures.count() > 1:
            tot_ins = measures.aggregate(Sum('total_insertions_for_bugs'))['total_insertions_for_bugs__sum']
            tot_del = measures.aggregate(Sum('total_deletions_for_bugs'))['total_deletions_for_bugs__sum']
        else:
            tot_ins = ms.total_insertions_for_bugs
            tot_del = ms.total_deletions_for_bugs
        Measure.objects.get_or_create(version=version, research_question=33, bugs_solved=measures.count(),
                                      class_name=ms.class_name,
                                      wmc=ms.wmc, dit=ms.dit, noc=ms.noc, cbo=ms.cbo, rfc=ms.rfc,
                                      commit_hash=ms.commit_hash,
                                      lcom=ms.lcom, loc=ms.loc, cloc=ms.cloc, bloc=ms.bloc, ifanin=ms.ifanin,
                                      nmethod=ms.nmethod,
                                      total_insertions_for_bugs=tot_ins, total_deletions_for_bugs=tot_del)

    qs = Measure.objects.filter(research_question=33, version=version).values('class_name__name',
                                                                              'class_name__file_path',
                                                                              'bugs_solved', 'wmc', 'dit', 'noc', 'cbo',
                                                                              'rfc',
                                                                              'lcom', 'loc', 'cloc', 'bloc', 'ifanin',
                                                                              'nmethod', 'total_insertions_for_bugs',
                                                                              'total_deletions_for_bugs',
                                                                              'commit_hash').order_by('id')
    with open('dataset_swt_rq6_bis.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)

    return HttpResponse('OK')


def measures_list(request, pk, rq):
    rq = int(rq)
    if rq == 1:
        return render(request, 'Measurement/MeasuresListRQ1RQ2.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=1).order_by('id')})
    elif rq == 2:
        return render(request, 'Measurement/MeasuresListRQ1RQ2.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=2).order_by('id')})
    elif rq == 3:
        return render(request, 'Measurement/MeasuresListRQ3.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=3).order_by('id')})
    elif rq == 4:
        return render(request, 'Measurement/MeasuresListRQ4.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=1).order_by('id')})
    elif rq == 5:
        return render(request, 'Measurement/MeasuresListRQ5.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=2).order_by('id')})
    elif rq == 6:
        return render(request, 'Measurement/MeasuresListRQ6.html',
                      {'measures': Measure.objects.filter(version=pk, research_question=3).exclude(severity=Bug.ENHANCEMENT).order_by('id')})
