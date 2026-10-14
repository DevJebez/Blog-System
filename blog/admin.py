from django.contrib import admin
from .models import Post, Comment, Tag


# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'short_content', 'toxicity', 'is_approved', 'date_posted')
    list_filter = ('is_approved',)
    actions = ['approve', 'reject']

    @admin.display(description='content')
    def short_content(self, obj):
        return obj.content[:60]

    @admin.action(description='Approve selected comments')
    def approve(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Hide selected comments')
    def reject(self, request, queryset):
        queryset.update(is_approved=False)
