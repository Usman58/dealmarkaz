from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    bio= models.TextField(null=True, blank=True)
    image= models.ImageField(null=True, blank=True)
    phone_number=models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


Condition_type=(("New","New"),("Used","Used"))
class Product(models.Model):
    owner= models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand =models.ForeignKey('Brand',on_delete=models.SET_NULL,null=True,blank=True)
    condition = models.CharField(max_length=200, null=True, blank=True,choices=Condition_type)
    category =models.ForeignKey('Category',on_delete=models.SET_NULL,null=True,blank=True)
    price = models.DecimalField(max_digits=20,decimal_places=0, null=True, blank=True)
    likes=models.ManyToManyField(User,related_name='ad_likes',blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True, blank=True)
    slug=models.SlugField(null=True, blank=True)
    @property
    def total_likes(self):
        return self.likes.count()
    def save(self,*args,**kwargs):
        if not self.slug  and self.name:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name= models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name='Category'
        verbose_name_plural = 'Categories'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.category_name
class Brand(models.Model):
    brand_name=models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.brand_name
class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(null=True,blank=True)
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    def __str__(self):
        return str(self.product.id)
