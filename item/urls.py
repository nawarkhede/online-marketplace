from django.urls import path

from . import views as item_views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', item_views.details, name='details'),
    path('new/', item_views.newitem, name="new_item"),
    path('<int:pk>/delete/', item_views.delete, name='delete'),
    path('<int:pk>/edit/', item_views.edit, name='edit'),
    path('', item_views.items, name="items")
]
