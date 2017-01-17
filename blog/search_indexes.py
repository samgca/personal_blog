from django.utils import timezone
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    title = indexes.CharField(model_attr='title')
    # Remove this if you want your post go to draft.
    # pub_date = indexes.DateTimeField(model_attr='published_date')
    # We add this for autocomplete.
    # content_auto = indexes.EdgeNgramField(model_attr='body')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published_date__lte=timezone.now())
