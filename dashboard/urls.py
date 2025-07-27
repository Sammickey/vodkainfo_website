from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_index, name='dashboard_index'),
    path('api_history/', views.APIHistoryAPIView.as_view(), name='api_history'),
    path('download_text_file/', views.download_text_file, name='download_text_file'),
    path('searchbase/status/<path:display_name>/<int:id>/', views.SearchBaseStatusView.as_view(), name='searchbase_status'),
    path('mickeyssndob/', views.dashboard_mickeyssndob, name='dashboard_mickeyssndob'),
    path('mickeyssndobnew/', views.dashboard_mickeyssndobnew, name='dashboard_mickeyssndobnew'),
    path('mickeydl/', views.dashboard_mickeydl, name='dashboard_mickeydl'),
    path('samssn/', views.dashboard_samssn, name='dashboard_samssn'),
    path('samssndob/', views.dashboard_samssndob, name='dashboard_samssndob'),
    path('samdlv2/', views.dashboard_samdlv2, name='dashboard_samdlv2'),
    path('samadvancedlookup/', views.dashboard_samadvancedlookup, name='dashboard_samadvancedlookup'),
    path('samdob/', views.dashboard_samdob, name='dashboard_samdob'),
    path('samphone/', views.dashboard_samphone, name='dashboard_samphone'),
    path('samreversephone/', views.dashboard_samreversephone, name='dashboard_samreversephone'),
    path('samreversessn/', views.dashboard_samreversessn, name='dashboard_samreversessn'),
    path('sergiossndob/', views.dashboard_sergiossndob, name='dashboard_sergiossndob'),
    path('sergiodl/', views.dashboard_sergiodl, name='dashboard_sergiodl'),
    path('alexssn/', views.dashboard_alexssn, name='dashboard_alexssn'),
]
