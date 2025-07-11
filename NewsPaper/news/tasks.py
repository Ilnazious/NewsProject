import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Category, Post

logger = logging.getLogger(__name__)


def send_weekly_digest():
    try:
        start_date = timezone.now() - timedelta(days=7)

        for category in Category.objects.all():
            new_posts = Post.objects.filter(
                postCategory=category,
                dataCreation__gte=start_date,
                categoryType=Post.ARTICLE
            )

            if new_posts.exists():
                subscribers = category.subscribers.all()

                for user in subscribers:
                    if user.email:
                        try:
                            html_content = render_to_string(
                                'email/weekly_digest.html',
                                {
                                    'category': category,
                                    'posts': new_posts,
                                    'user': user,
                                    'SITE_URL': settings.SITE_URL,
                                }
                            )

                            msg = EmailMultiAlternatives(
                                subject=f'Еженедельная подборка статей в категории "{category.name}"',
                                body='',
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[user.email],
                            )
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                            logger.info(f"Sent weekly digest to {user.email}")
                        except Exception as e:
                            logger.error(f"Error sending email to {user.email}: {str(e)}")
    except Exception as e:
        logger.error(f"Error in send_weekly_digest: {str(e)}")
        raise