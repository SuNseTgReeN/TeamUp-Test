from django.urls import path

from Tests.views import PollViewSet, PollSearch, PollAnswerView

app_name = 'Poll'

urlpatterns = [
    path('search/<str:secret_key>/', PollSearch.as_view(), name='poll-search'),
    path('poll_detail/<int:pk>/', PollViewSet.as_view(), name='poll-detail'),
    path('poll_detail/<int:pk>/go', PollAnswerView.as_view(), name='poll-go'),
]
