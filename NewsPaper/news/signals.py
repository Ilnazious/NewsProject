from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_subscribers_new_post(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        from .models import Category
        subscribers_notified = set()
        post_url = settings.SITE_URL + reverse('post_detail', args=[instance.id])

        for category in Category.objects.filter(pk__in=pk_set):
            for user in category.subscribers.exclude(id__in=[u.id for u in subscribers_notified]):
                if user.email:
                    send_mail(
                        subject=f'Новый материал в категории "{category.name}"',
                        message=(
                            f"Здравствуйте, {user.username}!\n\n"
                            f"Новый {instance.get_categoryType_display().lower()}:\n"
                            f"«{instance.title}»\n\n"
                            f"{instance.preview()}\n\n"
                            f"Читать полностью: {post_url}\n\n"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                    subscribers_notified.add(user)