from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Item, UserProfile


admin.site.site_header = "ReWear Admin"
admin.site.site_title = "ReWear Admin"
admin.site.index_title = "Marketplace management"


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


class RewearUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")


admin.site.unregister(User)
admin.site.register(User, RewearUserAdmin)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "category",
        "condition",
        "points",
        "status",
        "image_status",
        "created_at",
    )
    list_filter = ("category", "condition", "status")
    search_fields = ("title", "description", "owner__username", "owner__email")
    list_editable = ("status", "points")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    autocomplete_fields = ("owner",)
    fieldsets = (
        ("Listing", {"fields": ("owner", "title", "description", "category", "item_type")}),
        ("Condition", {"fields": ("size", "condition", "tags", "points", "status")}),
        ("Media", {"fields": ("image", "image_preview")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Image")
    def image_status(self, obj):
        return "Yes" if obj.image else "No"

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if not obj.image:
            return "No image uploaded"
        return format_html('<img src="{}" style="max-height: 180px; border-radius: 12px;" />', obj.image.url)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "points")
    search_fields = ("user__username", "user__email")
