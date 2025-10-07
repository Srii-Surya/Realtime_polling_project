from django.urls import path
from .views import CreatePollSessionView, start_stop_session, join_session, vote, poll_results

urlpatterns = [
    path('', CreatePollSessionView.as_view(), name='create_poll_session'),
    path('<int:pk>/start_stop/', start_stop_session, name='start_stop_session'),
    path('join/<str:join_code>/', join_session, name='join_session'),
    path('vote/', vote, name='vote'),
    path('<int:session_id>/results/', poll_results, name='poll_results'),
]
