from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username',
                     'user__email',
                     'user__first_name',
                     'user__last_name',
                     'phone', ]


admin.site.register(Profile, ProfileAdmin)
