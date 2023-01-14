from django.contrib import admin
from .models import Profile, Skill


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bio')
    save_as = True


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)


