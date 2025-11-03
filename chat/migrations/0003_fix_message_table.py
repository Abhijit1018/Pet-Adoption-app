from django.db import migrations


forward_sql = '''
CREATE TABLE IF NOT EXISTS chat_message_new (
    id integer primary key autoincrement,
    conversation_id integer NOT NULL,
    sender_id bigint NOT NULL,
    text text NOT NULL,
    created_at datetime,
    read bool DEFAULT 0
);
INSERT INTO chat_message_new (id, conversation_id, sender_id, text, created_at, read)
    SELECT id, conversation_id, sender_id, text, created_at, read FROM chat_message;
DROP TABLE chat_message;
ALTER TABLE chat_message_new RENAME TO chat_message;
'''

reverse_sql = '''
# Reverse migration: recreate original chat_message table with sender FK to auth_user
CREATE TABLE IF NOT EXISTS chat_message_old (
    id integer primary key autoincrement,
    text text NOT NULL,
    created_at datetime,
    read bool DEFAULT 0,
    conversation_id integer NOT NULL,
    sender_id integer NOT NULL,
    FOREIGN KEY(sender_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
INSERT INTO chat_message_old (id, text, created_at, read, conversation_id, sender_id)
    SELECT id, text, created_at, read, conversation_id, sender_id FROM chat_message;
DROP TABLE chat_message;
ALTER TABLE chat_message_old RENAME TO chat_message;
'''


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmember'),
    ]

    operations = [
        migrations.RunSQL(forward_sql, reverse_sql),
    ]
