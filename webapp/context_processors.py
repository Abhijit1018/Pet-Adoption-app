from .models import Notification

def notifications_processor(request):
    """Add unread notification count to context for authenticated users."""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, unread=True).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
