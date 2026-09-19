from django.urls import path

from .views import (
    ChatView,
    ConversationDetailView,
    ConversationListView,
)


urlpatterns = [
    path(
        "",
        ChatView.as_view(),
        name="chat",
    ),

    path(
        "conversations/",
        ConversationListView.as_view(),
        name="conversation-list",
    ),

    path(
        "<int:conversation_id>/",
        ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
]