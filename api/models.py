from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

def get_UserProfile_avatar_path(self,filename):
    return "files/users/profiles/%s/%s"%(str(self.user.username),filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    avatar = ResizedImageField(size =[500,500],upload_to=get_UserProfile_avatar_path)
    national_id = models.CharField(max_length=100)
    def profile_image(self):
        return '<a href="/media/%s"><img style="height:70px;width:70px;" alt="25" src="/media/%s"/></a>' % (self.avatar,self.avatar)
    profile_image.allow_tags = True

    def __str__(self):
        return str(self.user)
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name=("Product Category"))

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name=("Product Name"))
    product_category = models.ForeignKey(Category)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    shiping_price = models.DecimalField(max_digits=8,decimal_places=2)
    shiped_on = models.DateTimeField()
    end_on = models.DateTimeField(null=True, blank=True)

    def get_price(self,request):
        return self.unit_price

    def get_item_profit(self):
        return 0.0

    def __str__(self):
        return str(self.product_name)


class Business(models.Model):
    name = models.CharField(verbose_name="Business Name",max_length=200)
    products  = models.ManyToManyField(Product)
    county = models.CharField(max_length=200)
    owner = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)

    def get_products(self):
        return "\n".join([str(p) for p  in self.products.all()])

class Sales(models.Model):
    product  = models.ForeignKey(Product)
    units = models.DecimalField(max_digits=4,decimal_places=4)
    sold_at = models.DateTimeField()
    business = models.ForeignKey(Business)


