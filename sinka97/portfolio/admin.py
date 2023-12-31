from django.contrib import admin
from django.contrib.auth.models import User, Group

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(User, UserAdmin)