from typing import Any, Dict
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from chat.models import Chat


class ChatList(ListView, LoginRequiredMixin):
    """
    Chat List View
    """

    model = Chat


class ChatRoom(DetailView, LoginRequiredMixin):
    """
    Chat Detail View
    """

    model = Chat

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class CreateRoom(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ["name"]
    success_url = "/chat/"