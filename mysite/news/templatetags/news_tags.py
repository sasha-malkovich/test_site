from django import template

from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()


# @register.simple_tag()
# def get_categories():
#     return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.filter().annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)
    # categories = cache.get_or_set('categories', Category.objects.filter().annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)

    categories = Category.objects.filter().annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {'categories': categories}
