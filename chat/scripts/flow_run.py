from django.contrib.auth import get_user_model
from django.test import Client
from webapp.models import Pet
from chat.models import Conversation, ChatMember, Message

User = get_user_model()
# create users
own = User.objects.filter(username='flow_owner').first()
if not own:
    own = User.objects.create_user(username='flow_owner', password='pass')
req = User.objects.filter(username='flow_requester').first()
if not req:
    req = User.objects.create_user(username='flow_requester', password='pass')
# create pet
pet = Pet.objects.create(name='FlowBuddy', species='dog', location='Here', owner=own)
print('Users created:', own.id, req.id)
# client for requester
client_req = Client()
client_req.force_login(req)
# start conversation
resp = client_req.get(f'/chat/start/{pet.id}/')
print('start conversation response:', resp.status_code, getattr(resp, 'url', None))
# list conversations in chat_db
convos = list(Conversation.objects.using('chat_db').all())
print('Conversations in chat_db (count):', len(convos))
for c in convos:
    print('  convo', c.id, c.subject)
# list ChatMember rows
parts = list(ChatMember.objects.using('chat_db').filter(conversation_id__in=[c.id for c in convos]).values_list('conversation_id','user_id'))
print('ChatMember rows:', parts)
# requester posts a message via conversation view POST
if convos:
    # find the conversation about our pet (newest match)
    convo = Conversation.objects.using('chat_db').filter(subject__contains=pet.name).order_by('-id').first()
    if not convo:
        convo = convos[0]
    post = client_req.post(f'/chat/conversation/{convo.id}/', {'text':'Hello owner, this is requester'})
    print('post message status:', post.status_code)
    msgs = list(Message.objects.using('chat_db').filter(conversation_id=convo.id).values('id','sender_id','text','created_at'))
    print('Messages after requester post:', msgs)
    # now owner views and posts
    client_own = Client()
    client_own.force_login(own)
    view = client_own.get(f'/chat/conversation/{convo.id}/')
    print('owner view status:', view.status_code)
    # owner posts reply
    post2 = client_own.post(f'/chat/conversation/{convo.id}/', {'text':'Thanks, received your message'})
    print('owner post status:', post2.status_code)
    msgs2 = list(Message.objects.using('chat_db').filter(conversation_id=convo.id).values('id','sender_id','text','created_at'))
    print('Messages after owner reply:', msgs2)
else:
    print('No conversation found after start.')
