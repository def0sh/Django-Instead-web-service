from django.contrib import admin
from users.models import Message
from .models import Project, Tag, Review


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title','created','project_owner')
    save_as = True


admin.site.register(Project, ProjectAdmin)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Message)
