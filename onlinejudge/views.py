import sys, logging, os

from django.conf import settings
from django.views.generic.list import ListView
from django.core.cache import cache


from onlinejudge.models import Problem, Article, ArticleTag, ProblemTag, LinkShowType


logger = logging.getLogger(__name__)

# Create your views here.

class EntityListView(ListView):
    template_name = 'EntityListView.html'
    context_object_name = 'article_list'

    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    link_type = LinkShowType.L

    def get_view_cache_key(self):
        return self.request.get['pages']

    @property
    def page_num(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset_cache_key(self):
        return NotImplementedError

    def get_queryset_data(self):
        return NotImplementedError

    def get_queryset_from_cache(self, cache_key):
        value = cache.get(cache_key)
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            entity_list = self.get_queryset_data()
            cache.set(cache_key, entity_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return entity_list

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value

class IndexView(EntityListView):

    def get_queryset_data(self):
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=self.page_num)
        return cache_key

# class ArticleListView(EntityListView):
