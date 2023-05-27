from django.db import models
from email.policy import default
from hashlib import blake2b
from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Avg,Count

from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django_countries.fields import CountryField


User = get_user_model()

# Create your models here.
class Category(MPTTModel):
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):

    VARIANT_CHOICE  = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True)
    keywords = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=False)
    amount= models.IntegerField(default=0)
    slug = models.SlugField(null=False, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    discount_price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    variant_choice = models.CharField(max_length=20, choices=VARIANT_CHOICE, default='None')
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse()

    def discount_percent(self):
        calculated = ((self.price - self.discount_price) / self.price) * 100

        return ("%.2f" % calculated)

 ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" width="50"/>'.format(self.image.url))
        else:
            return ""

    def average_review(self):
        reviews = Comment.objects.filter(product=self).aggregate(average=Avg('rate'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg

    def count_review(self):
        reviews = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count

    def get_display_price(self):
        return "{0:.2f}".format(self.price/100)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="70" width="60"/>'.format(self.image.url))
        else:
            return ""

    def id_tag(self):
        return self.pk


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300)
    content = models.TextField()
    ip = models.CharField(max_length=255)
    rate = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.subject

    

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = RichTextUploadingField()

    def __str__(self):
        return self.question


class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.name is not None:
            return mark_safe('<p style="background-color:{}">{} </p>'.format(self.name, self.name))
        else:
            return ""

class Size(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Variant(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_id = models.IntegerField(default=0, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    discount_price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.pk is not None:
            return mark_safe('<img src="{}" height="50" width="50"/>'.format(img.image.url))
        else:
            return ""

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage