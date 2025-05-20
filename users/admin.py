from django.contrib import admin
from users.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'password')
    search_fields = ('username', 'first_name', 'last_name', 'password')
    ordering = ('username',)
    list_per_page = 10

admin.site.register(User, UserAdmin)