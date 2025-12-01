import logging
import re
from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField
from uuslug import slugify

from djangooj.utils import cache_decorator, cache
from djangooj.utils import get_current_site

# Create your models here.
logger = logging.getLogger(__name__)

@register.inclusion_tag('onlinejudge/tags/entity_info.html')
def load_article_detail(article, isindex, user):
    """
    加载文章详情
    :param article:
    :param isindex:是否列表页，若是列表页只显示摘要
    :return:
    """
    from djangoblog.utils import get_blog_setting
    blogsetting = get_blog_setting()

    return {
        'article': article,
        'isindex': isindex,
        'user': user,
        'open_site_comment': blogsetting.open_site_comment,
    }


