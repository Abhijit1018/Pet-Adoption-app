from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """A conversation between two or more users."""
    subject = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject or f"Conversation {self.id}"


class ChatParticipant(models.Model):
    """Represents a participant in a conversation.

    This is intentionally an integer-backed user reference (user_id) so the chat
    DB remains decoupled from the auth.User table. The model maps to the existing
    through table created by the original M2M so we mark it unmanaged to avoid
    migrations trying to recreate the table.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()

    class Meta:
        db_table = 'chat_conversation_participants'
        unique_together = (('conversation', 'user_id'),)
        # The table already exists in chat_db.sqlite3; don't try to manage it here
        managed = False


class ChatMember(models.Model):
    """A simple, managed participants table stored in the chat DB that does
    not impose foreign-key constraints to auth.User. We use this for runtime
    writes/reads to avoid cross-database FK/triggers on the original through
    table.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()

    class Meta:
        db_table = 'chat_members'
        unique_together = (('conversation', 'user_id'),)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='chat_messages')
    # Allow null temporarily to avoid forcing a one-off default when creating
    # migrations; this keeps the chat DB decoupled from auth.User. A follow-up
    # data migration could set existing rows and make this non-nullable if
    # desired.
    sender_id = models.BigIntegerField(null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message {self.id} in {self.conversation_id}"
