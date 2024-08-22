import hashlib
import urllib

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage
from django.db.models import Avg, Count
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.template.response import TemplateResponse
from django.views import View
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import time
from datetime import datetime
import json
import requests
import hmac
import random
from django.views.decorators.csrf import csrf_exempt

from travelapi import settings
from travel.models import Role, User, Provider, Customer, ServiceType, Province, Image, Service, Discount, \
    ServiceSchedule, Booking, Review
from travel import serializers, paginators
from travel.serializers import RoleSerializer, ProviderSerializer, CustomerSerializer, ServiceTypeSerializer, \
    ProvinceSerializer, ImageSerializer, ServiceSerializer, DiscountSerializer, ServiceScheduleSerializer, \
    BookingSerializer, ReviewSerializer


class RoleViewSet(viewsets.ModelViewSet):  #ModelViewSet: lấy tất cả các action CRUD
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user', 'change-password']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            data = request.data.copy()  # Tạo một bản sao của dữ liệu để tránh ảnh hưởng đến dữ liệu gốc
            if 'password' in data:
                data['password'] = make_password(data['password'])  # Băm mật khẩu

            serializer = serializers.UserSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.UserSerializer(user).data)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            user = self.request.query_params.get('user')
            if user:
                queryset = queryset.filter(user=user)

        return queryset


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(first_name__icontains=q)

            user = self.request.query_params.get('user')
            if user:
                queryset = queryset.filter(user=user)

        return queryset


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = serializers.ServiceTypeSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = serializers.ProvinceSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = serializers.ImageSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    pagination_class = paginators.ServicePaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'list':
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            address = self.request.query_params.get('address')
            if address:
                queryset = queryset.filter(address__icontains=address)

            service_type = self.request.query_params.get('service_type')
            if service_type:
                queryset = queryset.filter(service_type=service_type)

            province = self.request.query_params.get('province')
            if province:
                queryset = queryset.filter(province=province)

            provider = self.request.query_params.get('provider')
            if provider:
                queryset = queryset.filter(provider=provider)

            sort = self.request.query_params.get('sort')
            if sort == '1':
                queryset = queryset.order_by('price')
            elif sort == '2':
                queryset = queryset.order_by('-price')

        return queryset


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer


class ServiceScheduleViewSet(viewsets.ModelViewSet):
    queryset = ServiceSchedule.objects.all()
    serializer_class = serializers.ServiceScheduleSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):

            service = self.request.query_params.get('service')
            if service:
                queryset = queryset.filter(service=service)

            # Sort the queryset by the 'date' field in ascending order
            queryset = queryset.order_by('date')

        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer


@csrf_exempt
def payment_view(request: HttpRequest):
    accessKey = 'F8BBA842ECF85'
    secretKey = 'K951B6PE1waDMi640xX08PD3vg6EkVlz'
    orderInfo = 'pay with MoMo'
    partnerCode = 'MOMO'
    redirectUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b'
    ipnUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b'
    requestType = "payWithMethod"
    amount = request.headers.get('amount', '')  # Lấy amount từ header
    orderId = partnerCode + str(int(time.time() * 1000))
    requestId = orderId
    extraData = ''
    orderGroupId = ''
    autoCapture = True
    autoCapture = True
    lang = 'vi'

    # Tạo chuỗi signature
    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
    signature = hmac.new(secretKey.encode(), rawSignature.encode(), hashlib.sha256).hexdigest()

    # Tạo request body
    data = {
        "partnerCode": partnerCode,
        "partnerName": "Test",
        "storeId": "MomoTestStore",
        "requestId": requestId,
        "amount": amount,
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "lang": lang,
        "requestType": requestType,
        "autoCapture": autoCapture,
        "extraData": extraData,
        "orderGroupId": orderGroupId,
        "signature": signature
    }

    # Gửi request đến MoMo
    response = requests.post('https://test-payment.momo.vn/v2/gateway/api/create', json=data)
    response_data = response.json()
    pay_url = response_data.get('payUrl')

    return JsonResponse(response_data)


config = {
    "app_id": 2553,
    "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
    "key2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
    "endpoint": "https://sb-openapi.zalopay.vn/v2/create"
}


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        # Lấy thông tin từ yêu cầu của người dùng
        amount = request.headers.get('amount', '')  # Lấy amount từ header
        transID = random.randrange(1000000)
        # Xây dựng yêu cầu thanh toán
        order = {
            "app_id": config["app_id"],
            "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),  # mã giao dich có định dạng yyMMdd_xxxx
            "app_user": "user123",
            "app_time": int(round(time.time() * 1000)),  # miliseconds
            "embed_data": json.dumps({}),
            "item": json.dumps([{}]),
            "amount": amount,
            "description": "Thanh Toán Vé Xe #" + str(transID),
            "bank_code": "",
        }

        # Tạo chuỗi dữ liệu và mã hóa HMAC
        data = "{}|{}|{}|{}|{}|{}|{}".format(order["app_id"], order["app_trans_id"], order["app_user"],
                                             order["amount"], order["app_time"], order["embed_data"], order["item"])
        order["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

        # Gửi yêu cầu đến ZaloPay API
        try:
            response = urllib.request.urlopen(url=config["endpoint"], data=urllib.parse.urlencode(order).encode())
            result = json.loads(response.read())
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})
