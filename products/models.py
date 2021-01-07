from django.db import models
from Core.models import User
from django.utils.text import slugify
def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

class Product(models.Model):
    pCondition=[
        ('New','New'),
        ('Used','Used'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products/')
    categories = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    price = models.IntegerField()
    condition = models.CharField(max_length=10,choices=pCondition)
    quantity = models.PositiveIntegerField(default=1)
    details = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def get_categories(self):
        cats = self.categories.split(',')
        return cats

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        else:
            self.slug = generate_unique_slug(Product, self.title)
        super().save(*args, **kwargs)

    def delete(self,*args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:100]
