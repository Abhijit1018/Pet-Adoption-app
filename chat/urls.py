from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('start/<int:pet_id>/', views.start_conversation, name='start_conversation'),
    path('select_admins/', views.start_with_admins, name='select_admins'),
    path('start_admins/', views.start_with_admins, name='start_with_admins'),
    path('', views.chat_index, name='index'),
    path('conversation/<int:convo_id>/', views.conversation_view, name='conversation'),
    path('conversation/<int:convo_id>/send/', views.send_message_ajax, name='send_message'),
    path('conversation/<int:convo_id>/fetch/', views.fetch_messages, name='fetch_messages'),
    path('conversation/<int:convo_id>/leave/', views.leave_conversation, name='leave_conversation'),
    path('conversation/<int:convo_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('conversation/<int:convo_id>/message/<int:msg_id>/delete/', views.delete_message, name='delete_message'),
    path('admin/', views.admin_conversations, name='admin_list'),
]
