from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from travel.models import Role, User, Provider, Customer, ServiceType, Province, Image, Service, Discount, \
    ServiceSchedule, Booking, Review


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url

        return rep


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'CCCD', 'phone', 'address', 'username', 'password', 'avatar',
                  'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['path'] = instance.path.url

        return rep

    class Meta:
        model = Image
        fields = ['path', 'service']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount']


class ServiceSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    discount = DiscountSerializer()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_images(self, obj):
        return [image.path.url for image in obj.get_images()]

    class Meta:
        model = Service
        fields = ['id', 'name', 'address', 'price', 'description', 'require', 'discount', 'service_type', 'provider',
                  'province', 'average_rating', 'images']


class ServiceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSchedule
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
