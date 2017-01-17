from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Tag(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Tag name')

    def __str__(self):
        return self.slug

    def get_post_from_tag(self):
        results = Post.objects.filter(tags=self, published_date__lte=timezone.now()).order_by('-published_date')
        return results


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=False)
    body = models.TextField(verbose_name='Text')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        new_slug = slugify(self.title)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
