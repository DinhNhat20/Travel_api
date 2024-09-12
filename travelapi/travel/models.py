from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.db.models import Avg, Sum


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
    CCCD = models.CharField(max_length=12, null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)


class Provider(BaseModel):
    name = models.CharField(max_length=100, null=False)
    description = RichTextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def revenue_by_month(self, month, year):
        services = self.service_set.all()
        bookings = Booking.objects.filter(
            service_schedule__service__in=services,
            created_date__month=month,
            created_date__year=year,
            payment_status=True  # Lọc các booking đã thanh toán
        ).values('service_schedule__service__name').annotate(total_revenue=Sum('total_price'))

        return bookings

    def get_all_reviews(self):
        # Lấy tất cả các dịch vụ thuộc về Provider này
        services = self.service_set.all()
        # Lấy tất cả các đánh giá liên quan đến các dịch vụ này
        reviews = Review.objects.filter(service__in=services)
        return reviews

    def __str__(self):
        return self.name


class Customer(BaseModel):
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=15, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.full_name


class ServiceType(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    path = CloudinaryField(null=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)

    def __str__(self):
        return f"Hình của service {self.service}"


class Service(BaseModel):
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False, default=0)
    description = RichTextField(null=True, blank=True)
    require = RichTextField(null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    reviews = models.ManyToManyField('Customer', through='Review', null=True, blank=True)

    def __str__(self):
        return self.name

    def total_reviews(self):
        return self.review_set.count()

    def average_rating(self):
        avg_rating = self.review_set.aggregate(Avg('star'))['star__avg']
        return avg_rating or 0  # Return 0 if there are no reviews

    def get_images(self):
        return self.image_set.all()


class Discount(models.Model):
    discount = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.discount}%"


class ServiceSchedule(BaseModel):
    date = models.DateField(null=False)
    max_participants = models.IntegerField(null=False)
    available = models.IntegerField(null=True, default=0)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service} - {self.date}"


class Booking(BaseModel):
    full_name = models.CharField(max_length=50, null=False, default='')
    phone = models.CharField(max_length=10, null=False, default='')
    email = models.CharField(max_length=50, null=False, default='')
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_schedule = models.ForeignKey(ServiceSchedule, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.full_name} - {self.service_schedule}"


class Review(BaseModel):
    star = models.IntegerField(null=False)
    content = RichTextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.service}"
