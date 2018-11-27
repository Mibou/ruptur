from django.urls import path
from .views import IdeaCreate, IdeaUpdate, IdeaDelete

urlpatterns = [
    path('idea/add/', IdeaCreate.as_view(), name='idea-add'),
    path('idea/<int:pk>/', IdeaUpdate.as_view(), name='idea-update'),
    path('idea/<int:pk>/delete/', IdeaDelete.as_view(), name='idea-delete')
]
