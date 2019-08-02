from haystack import indexes
from drf_haystack.serializers import HaystackSerializer

from .models import SKU
class SKUIndex(indexes.SearchIndex,indexes.Indexable):
    text=indexes.CharField(document=True,use_template=True)
    id=indexes.IntegerField(model_attr='id')
    name=indexes.CharField(model_attr='name')
    price=indexes.DecimalField(model_attr='price')
    default_image_url=indexes.CharField(model_attr='default_image_url')
    comments=indexes.IntegerField(model_attr='comments')

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_launched=True)

