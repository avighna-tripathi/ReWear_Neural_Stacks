from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    points = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} profile"


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("tops", "Tops"),
        ("bottoms", "Bottoms"),
        ("dresses", "Dresses"),
        ("outerwear", "Outerwear"),
        ("shoes", "Shoes"),
        ("accessories", "Accessories"),
    ]
    CONDITION_CHOICES = [
        ("like-new", "Like New"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
    ]
    STATUS_CHOICES = [
        ("available", "Available"),
        ("pending", "Pending"),
        ("swapped", "Swapped"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    item_type = models.CharField(max_length=80, blank=True)
    size = models.CharField(max_length=20)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    tags = models.CharField(max_length=250, blank=True, help_text="Comma-separated tags")
    points = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    @property
    def tag_list(self) -> list[str]:
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
