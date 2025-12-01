import logging
import re
from abc import abstractmethod


from django import template
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from mdeditor.fields import MDTextField
from uuslug import slugify

from djangooj.utils import cache_decorator, cache
from djangooj.utils import get_current_site

# Create your models here.
logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('onlinejudge/tags/entity_info.html')
def load_article_detail(article, isindex, user):
    """
    加载文章详情
    :param article:
    :param isindex:是否列表页，若是列表页只显示摘要
    :return:
    """

    return {
        'article': article,
        'isindex': isindex,
        'user': user,
    }


@register.simple_tag
def get_markdown_toc(content):
    from djangooj.utils import CommonMarkdown
    body, toc = CommonMarkdown.get_markdown_with_toc(content)
    return mark_safe(toc)


