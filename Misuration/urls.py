from django.conf.urls import url

from Misuration.views import create_measures_rq1, create_measures_rq2, create_measures_rq6,\
    measures_list, create_measures_rq3

urlpatterns = [
    url(regex='^create_measures_rq1/$',
        view=create_measures_rq1,
        name='create_measures'),
    url(regex='^create_measures_rq2/$',
        view=create_measures_rq2,
        name='create_measures_rq2'),
    url(regex='^create_measures_rq3/$',
        view=create_measures_rq3,
        name='create_measures_rq3'),
    url(regex='^create_measures_rq6/$',
        view=create_measures_rq6,
        name='create_measures_rq6'),
    url(regex='^version/(?P<pk>\d+)/(?P<rq>\d+)/list/$',
        view=measures_list,
        name='measures_list'),
]
