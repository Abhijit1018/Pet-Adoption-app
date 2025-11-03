class ChatRouter:
    """A router to control all database operations on models in the chat application.

    All chat app models go to the 'chat_db' database. Other apps use the default routing.
    """

    chat_app_labels = {'chat'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.chat_app_labels:
            return 'chat_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.chat_app_labels:
            return 'chat_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.chat_app_labels or
            obj2._meta.app_label in self.chat_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.chat_app_labels:
            return db == 'chat_db'
        # Ensure other apps don't get migrated to the chat_db
        if db == 'chat_db':
            return False
        return None
