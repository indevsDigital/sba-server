from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

def get_UserProfile_avatar_path(self,filename):
    return "files/users/profiles/%s/%s"%(str(self.user.username),filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    avatar = ResizedImageField(size =[500,500],upload_to=get_UserProfile_avatar_path,blank=True, null=True)
    national_id = models.CharField(max_length=100,blank=True, null=True)#TODO: National id is required
    def profile_image(self):
        return '<a href="/media/%s"><img style="height:70px;width:70px;" alt="25" src="/media/%s"/></a>' % (self.avatar,self.avatar)
    profile_image.allow_tags = True

    def __str__(self):
        return str(self.user)
# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=255,verbose_name=("Product Category"))

    def __str__(self):
        return str(self.name)



class Business(models.Model):
    name = models.CharField(verbose_name="Business Name",max_length=200)
    county = models.CharField(max_length=200)
    owner = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)

    def get_products(self):
        return "\n".join([str(p) for p  in Product.objects.all().filter(business=self)])

    get_products.short_description = 'Products' 
    
    def __str__(self):
        return str(self.name)


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name=("Product Name"))
    product_code =  models.CharField(max_length=25)
    product_category = models.ForeignKey(Category,related_name="category")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    shiping_price = models.DecimalField(max_digits=8,decimal_places=2)#TODO: Remove it has no use
    purchase_date = models.DateTimeField()
    total_inital_units = models.PositiveIntegerField()
    business = models.ForeignKey(Business)
    end_on = models.DateTimeField(null=True, blank=True)
    expires_on = models.DateField()
    available_units = models.PositiveIntegerField()
    sold_unit = models.PositiveIntegerField(default=0)
    damaged_units = models.PositiveIntegerField(default=0)

    def get_price(self,request):
        return self.unit_price

    def get_item_profit(self):
        return (((self.unit_price-self.shiping_price)))

    def __str__(self):
        return str(self.product_name)+ " " +str(self.product_code)

class Receipt(models.Model):
    product  = models.ForeignKey(Product)
    units = models.DecimalField(max_digits=4,decimal_places=2)
    sold_at = models.DateTimeField()
    business = models.ForeignKey(Business)
    receipt_number = models.CharField(max_length=150)
    total_amount = models.DecimalField(max_digits=15,decimal_places=2)

    def __str__(self):
        return str(self.receipt_number)
    
