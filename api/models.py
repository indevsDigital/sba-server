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



class Item(models.Model):
    name = models.CharField(max_length=20)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_item_profit(self):
        return 0.0

    def __str__(self):
        return str(self.name)


class Stock(models.Model):
    item =models.ForeignKey(Item)
    number = models.IntegerField()
    inital_price = models.DecimalField(max_digits=8, decimal_places=2)

    
    def get_total_income(self):
        return 0.0
