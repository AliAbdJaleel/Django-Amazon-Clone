from collections.abc import Iterable
from django.db import models
from taggit.managers import TaggableManager # pip install django-taggit
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify  # لتحويل اسم المنتج او المادة الى الرابط
from django.utils.translation import gettext_lazy as _     # يتم استدعاء هذه المكتبة في حال الموقع فيه اكثر من لغة
# Create your models here.

FLAG_TYPE = (

    ('NEW','NEW'),
    ('Sale','Sale'),
    ('Feature','Feature')
)

class Product(models.Model):
    name = models.CharField(max_length=120,verbose_name= _('name')) # لغرض ظهور اسم العمود مترجم امام المستخدم
    flag = models.CharField(_('flag'),max_length=10,choices=FLAG_TYPE)
    price = models.FloatField(_('price'))
    image = models.ImageField(_('image'),upload_to='product') # defult image that show on view product
    sku = models.IntegerField(_('sku'))
    subtitle = models.TextField(_('subtitle'),max_length=500)
    description = models.TextField(_('description'),max_length=50000)
    
    brand = models.ForeignKey('Brand',verbose_name=_('brand'),related_name='product_brand',on_delete=models.SET_NULL,null= True)
    tags = TaggableManager(_('tags'))
    slug = models.SlugField(blank=True,null=True,unique=True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args , **kwargs)

    def __str__(self):
        return self.name

        






class ProductImages(models.Model):
    product = models.ForeignKey(Product,verbose_name= _('product'),related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(_('image'),upload_to='productimages') # productimages is the Name of folder contains images
    slug = models.SlugField(blank=True,null=True)
 


class Brand(models.Model):
    name = models.CharField(_('name'),max_length=100)
    image = models.ImageField(_('image'),upload_to='brand')
    slug = models.SlugField(blank=True,null=True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(Brand,self).save(*args , **kwargs)
    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User,verbose_name= _('user'), related_name= 'review_user',on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,verbose_name= _('product'),related_name='review_product',on_delete=models.CASCADE)
    review = models.TextField(_('review'),max_length=500)
    rate = models.IntegerField(_('rate'),choices= [(i,i) for i in range(1,6)])
    created_at = models.DateTimeField(_('created_at'),default=timezone.now)
    def __str__(self):
        return f"{self.name} - {self.product} - {self.rate}"                        
