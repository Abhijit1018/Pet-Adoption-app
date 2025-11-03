from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from webapp.models import Pet

from chat.models import Conversation, ChatMember, Message


class ChatFlowIntegrationTest(TestCase):
    databases = {'default', 'chat_db'}

    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username='owner2', password='pass')
        self.user = User.objects.create_user(username='requester2', password='pass')
        self.pet = Pet.objects.create(name='Buddy2', species='dog', location='Here', owner=self.owner)
        self.client = Client()

    def test_start_conversation_and_send_message(self):
        # login as requester and start a conversation
        self.client.force_login(self.user)
        resp = self.client.get(reverse('chat:start_conversation', args=[self.pet.id]))
        # should redirect to conversation
        self.assertIn(resp.status_code, (302, 301))

        # Conversation should exist in chat_db
        convo_qs = Conversation.objects.using('chat_db').filter(subject__contains=self.pet.name)
        self.assertTrue(convo_qs.exists(), 'Conversation not created in chat_db')
        convo = convo_qs.first()

        # Participants (ChatMember) should be present in chat_db
        parts = ChatMember.objects.using('chat_db').filter(conversation_id=convo.id).values_list('user_id', flat=True)
        self.assertEqual(set(parts), {self.owner.id, self.user.id})

        # Send a message via POST to conversation view
        post_resp = self.client.post(reverse('chat:conversation', args=[convo.id]), {'text': 'Hello owner'})
        self.assertIn(post_resp.status_code, (302, 301))

        # Message should be saved in chat_db with sender_id of requester
        msg_qs = Message.objects.using('chat_db').filter(conversation_id=convo.id, sender_id=self.user.id, text__contains='Hello')
        self.assertTrue(msg_qs.exists(), 'Message not saved in chat_db')
