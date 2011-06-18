from django.conf import settings

import commonware.log
from dateutil import parser
import feedparser

import cronjobs
from devhub.models import BlogPost

log = commonware.log.getLogger('z.cron')


@cronjobs.register
def update_blog_posts():
    """Update the blog post cache."""

    items = feedparser.parse(settings.DEVELOPER_BLOG_URL)['items']
    if not items:
        return

    BlogPost.objects.all().delete()

    for item in items[:5]:
        post = {}
        post['title'] = item.title
        post['date_posted'] = parser.parse(item.date)
        post['permalink'] = item.link
        BlogPost.objects.create(**post)

    log.info('Adding %d blog posts.' % BlogPost.objects.count())

