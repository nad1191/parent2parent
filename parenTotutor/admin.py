from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile
from .models import Info, Profile

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Info)

