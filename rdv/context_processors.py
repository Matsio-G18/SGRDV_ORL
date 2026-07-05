from django.contrib.auth.models import AnonymousUser


def notifications(request):
    if isinstance(request.user, AnonymousUser):
        return {}

    unread_count = request.user.notifications.filter(is_read=False).count()
    return {
        'notification_unread_count': unread_count,
    }
