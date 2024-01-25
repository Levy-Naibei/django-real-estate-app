from django.urls import path

from .views import (AgentsListView, GetProfileView, TopAgentListView,
                    UpdateProfileView)

urlpatterns = [
    path("me/", GetProfileView.as_view(), name="get_profile"),
    path("edit/<str:username>/", UpdateProfileView.as_view(), name="update_profile"),
    path("agents/all/", AgentsListView.as_view(), name="fetch-agents"),
    path("top-agents/all/", TopAgentListView.as_view(), name="top-agents"),
]
