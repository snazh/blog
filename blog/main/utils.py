from django.db.models import Count

from .models import *


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('post'))
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
