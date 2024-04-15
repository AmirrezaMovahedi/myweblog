from django.contrib import admin

from .models import Post, Ticket, Comment, Image, Account


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'publish']
    ordering = ['title', 'publish']
    list_filter = ['status', 'author', 'publish']
    search_fields = ['title', 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    list_editable = ['status']
    prepopulated_fields = {'slug': ['title']}
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Image)
class ImageAdminC(admin.ModelAdmin):
    list_display = ['post', 'title', 'description', 'created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'message', 'created', 'active']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'bio', 'birthday']
