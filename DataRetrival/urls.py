from django.conf.urls import url

from DataRetrival.views import create_software, software_list, version_details, files_list, version_anomalies

urlpatterns = [
    url(regex='^create_software/$',
        view=create_software,
        name='test_software'),
    url(regex='^software/list/$',
        view=software_list,
        name='software_list'),
    url(regex='^version/(?P<pk>\d+)/details/$',
        view=version_details,
        name='version_details'),
    url(regex='^version/(?P<pk>\d+)/anomalies/$',
        view=version_anomalies,
        name='version_anomalies'),
    url(regex='^software/(?P<pk>\d+)/files/list/$',
        view=files_list,
        name='files_list'),
]
