from django.contrib import admin
from django.utils.html import mark_safe

from travel.models import Role, User, Provider, Customer, ServiceType, Province, Image, Service, Discount, \
    ServiceSchedule, Booking, Review
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class RoleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Role
        fields = '__all__'


class MyRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'is_superuser', 'first_name', 'last_name', 'email', 'phone',
                    'address', 'is_staff',
                    'is_active', 'date_joined', 'role']
    search_fields = ['id', 'username', 'first_name', 'last_name']
    list_filter = ['is_superuser', 'is_staff', 'is_active', 'role']
    readonly_fields = ['my_avatar']

    def my_avatar(self, user):
        if user.avatar:
            return mark_safe(
                f"<img src='https://res.cloudinary.com/db1p2ugkn/image/upload/v1712623700/{user.avatar}' width='150' />")


# class MyThesisAdmin(admin.ModelAdmin):
#     list_display = ['id', 'code', 'name', 'start_date', 'complete_date', 'report_file', 'total_score', 'result',
#                     'council', 'major', 'school_year']
#     search_fields = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']
#     list_filter = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']


admin.site.register(Role, MyRoleAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Provider)
admin.site.register(Customer)
admin.site.register(ServiceType)
admin.site.register(Province)
admin.site.register(Image)
admin.site.register(Service)
admin.site.register(Discount)
admin.site.register(ServiceSchedule)
admin.site.register(Booking)
admin.site.register(Review)
