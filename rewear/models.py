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
    current_holder = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="held_items",
    )
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

    @property
    def holder(self):
        return self.current_holder or self.owner

    def save(self, *args, **kwargs):
        if not self.current_holder_id:
            self.current_holder = self.owner
        super().save(*args, **kwargs)


class Swap(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    FULFILLMENT_CHOICES = [
        ("awaiting_address", "Awaiting Address"),
        ("ready_to_ship", "Ready to Ship"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name="swaps")
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiated_swaps")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_swaps")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    points_delta = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=255, blank=True)
    delivery_name = models.CharField(max_length=120, blank=True)
    delivery_phone = models.CharField(max_length=30, blank=True)
    delivery_line1 = models.CharField(max_length=255, blank=True)
    delivery_line2 = models.CharField(max_length=255, blank=True)
    delivery_city = models.CharField(max_length=120, blank=True)
    delivery_state = models.CharField(max_length=120, blank=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True)
    delivery_notes = models.TextField(blank=True)
    address_submitted_at = models.DateTimeField(null=True, blank=True)
    fulfillment_status = models.CharField(max_length=30, choices=FULFILLMENT_CHOICES, default="awaiting_address")
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        item_title = self.item.title if self.item else "Removed item"
        return f"{self.initiator.username} -> {self.recipient.username} ({item_title})"

    @property
    def has_shipping_address(self) -> bool:
        return bool(self.delivery_line1 and self.delivery_city and self.delivery_postal_code)


class Conversation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="conversations")
    swap = models.ForeignKey(Swap, on_delete=models.SET_NULL, null=True, blank=True, related_name="conversations")
    participant_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations_as_one")
    participant_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations_as_two")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "participant_one", "participant_two"],
                name="unique_item_conversation_pair",
            )
        ]

    def __str__(self) -> str:
        return f"Conversation: {self.participant_one.username} & {self.participant_two.username}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.sender.username}: {self.body[:30]}"
