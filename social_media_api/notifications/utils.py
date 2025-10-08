from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    """
    Create a notification object.
    recipient: User instance to receive the notification
    actor: User instance who performed the action
    verb: short string like 'liked', 'commented', 'followed'
    target: optional model instance (Post, Comment, User, etc.)
    """
    target_ct = None
    target_id = None
    if target is not None:
        target_ct = ContentType.objects.get_for_model(target.__class__)
        target_id = str(getattr(target, 'pk', target))
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_ct,
        target_object_id=target_id
    )