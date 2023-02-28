"""defines patterns of addresses URL for app learning_logs."""
from django.urls import path
from . import views
app_name = 'learning_logs'
urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    # Showing all topics
    path('topics/', views.topics, name='topics'),
    # Detail page concerning one topic
    path('topics/(<int:topic_id>)/', views.topic, name='topic'),
    # Page for adding new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page to adding new post.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Page for editing posts.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
