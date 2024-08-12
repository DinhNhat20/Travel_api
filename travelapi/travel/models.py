from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)


class ServiceProvider(BaseModel):
    name = models.CharField(max_length=100, null=False)
    description = RichTextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=15, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.last_name} - {self.first_name}"


class ServiceType(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    image = CloudinaryField(null=True)
    price = models.FloatField(null=False, default=0)
    description = RichTextField(null=True, blank=True)
    require = RichTextField(null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Discount(BaseModel):
    discount = models.FloatField(null=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class ServiceSchedule(BaseModel):
    date = models.DateField(null=False)
    max_slot = models.IntegerField(null=False)
    available = models.IntegerField(null=True, default=0)
    start_time = models.IntegerField(null=False)
    end_time = models.IntegerField(null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Booking(BaseModel):
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_status = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_schedule = models.ForeignKey(ServiceSchedule, on_delete=models.PROTECT)


class Review(BaseModel):
    star = models.IntegerField(null=False)
    content = RichTextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
