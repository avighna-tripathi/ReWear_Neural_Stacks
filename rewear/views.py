from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    ItemForm,
    MessageForm,
    ShippingAddressForm,
    SignUpForm,
    StyledAuthenticationForm,
)
from .models import Conversation, Item, Message, Swap, UserProfile


def _ordered_users(user_one, user_two):
    return (user_one, user_two) if user_one.id <= user_two.id else (user_two, user_one)


def _get_or_create_conversation(item, user_one, user_two, swap=None):
    participant_one, participant_two = _ordered_users(user_one, user_two)
    conversation, _ = Conversation.objects.get_or_create(
        item=item,
        participant_one=participant_one,
        participant_two=participant_two,
        defaults={"swap": swap},
    )
    if swap and conversation.swap_id != swap.id:
        conversation.swap = swap
        conversation.save(update_fields=["swap", "updated_at"])
    return conversation


def home(request):
    featured_items = Item.objects.select_related("owner")[:4]
    categories = [
        ("tops", "Tops"),
        ("bottoms", "Bottoms"),
        ("dresses", "Dresses"),
        ("outerwear", "Outerwear"),
        ("shoes", "Shoes"),
        ("accessories", "Accessories"),
    ]
    stats = {
        "items": Item.objects.count(),
        "members": UserProfile.objects.count(),
    }
    return render(
        request,
        "rewear/home.html",
        {
            "featured_items": featured_items,
            "categories": categories,
            "stats": stats,
        },
    )


class RewearLoginView(LoginView):
    template_name = "rewear/login.html"
    authentication_form = StyledAuthenticationForm


class RewearLogoutView(LogoutView):
    pass


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        UserProfile.objects.get_or_create(user=user)
        login(request, user)
        messages.success(request, "Welcome to ReWear. Your account is ready.")
        return redirect("dashboard")
    return render(request, "rewear/signup.html", {"form": form})


def browse(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "newest").strip()
    page_number = request.GET.get("page", 1)

    items = Item.objects.select_related("owner", "current_holder")
    if query:
        items = items.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
        )
    if category:
        items = items.filter(category=category)
    if sort == "points-low":
        items = items.order_by("points", "-created_at")
    elif sort == "points-high":
        items = items.order_by("-points", "-created_at")
    elif sort == "oldest":
        items = items.order_by("created_at")

    paginator = Paginator(items, 9)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "rewear/browse.html",
        {
            "items": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
            "selected_category": category,
            "selected_sort": sort,
            "categories": Item.CATEGORY_CHOICES,
        },
    )


def item_detail(request, pk):
    item = get_object_or_404(Item.objects.select_related("owner", "current_holder"), pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=item.pk)[:4]
    existing_pending_swap = None
    conversation = None
    if request.user.is_authenticated and request.user.id != item.owner_id:
        existing_pending_swap = Swap.objects.filter(item=item, initiator=request.user, status="pending").first()
        conversation = _get_or_create_conversation(item, request.user, item.owner)
    return render(
        request,
        "rewear/item_detail.html",
        {
            "item": item,
            "related_items": related_items,
            "existing_pending_swap": existing_pending_swap,
            "conversation": conversation,
        },
    )


def _build_dashboard_context(user, selected_conversation_id=None):
    listed_items = user.items.select_related("current_holder")
    held_items = user.held_items.select_related("owner")
    received_items = held_items.exclude(owner=user)
    shared_items = listed_items.exclude(current_holder=user)

    item_count = listed_items.count()
    available_count = listed_items.filter(status="available").count()
    pending_items_count = listed_items.filter(status="pending").count()
    swapped_items_count = listed_items.filter(status="swapped").count()
    total_points = getattr(user, "profile", None).points if hasattr(user, "profile") else 0

    swap_qs = Swap.objects.filter(Q(initiator=user) | Q(recipient=user)).select_related(
        "item", "initiator", "recipient"
    )
    pending_swaps_count = swap_qs.filter(status="pending").count()
    completed_swaps_count = swap_qs.filter(status="completed").count()
    incoming_pending_count = swap_qs.filter(status="pending", recipient=user).count()
    recent_swaps = swap_qs[:6]
    incoming_swaps = swap_qs.filter(status="pending", recipient=user)[:6]
    outgoing_swaps = swap_qs.filter(status="pending", initiator=user)[:6]
    completed_swaps_needing_address = list(
        swap_qs.filter(
            status="completed",
            initiator=user,
            address_submitted_at__isnull=True,
        )[:6]
    )
    completed_swaps_with_address = swap_qs.filter(
        status="completed",
        recipient=user,
        address_submitted_at__isnull=False,
    )[:6]
    owner_shipping_actions = swap_qs.filter(
        status="completed",
        recipient=user,
        address_submitted_at__isnull=False,
    )[:6]
    buyer_delivery_actions = swap_qs.filter(
        status="completed",
        initiator=user,
        fulfillment_status="shipped",
    )[:6]

    conversations = list(
        Conversation.objects.filter(
            Q(participant_one=user) | Q(participant_two=user)
        ).select_related("item", "swap", "participant_one", "participant_two")
    )

    active_conversation = None
    active_messages = []
    if selected_conversation_id:
        active_conversation = next((c for c in conversations if str(c.pk) == selected_conversation_id), None)
    if not active_conversation and conversations:
        active_conversation = conversations[0]
    if active_conversation:
        active_messages = list(active_conversation.messages.select_related("sender"))
        if selected_conversation_id:
            unread_ids = [
                message.pk
                for message in active_messages
                if message.sender_id != user.id and message.read_at is None
            ]
            if unread_ids:
                read_time = timezone.now()
                Message.objects.filter(pk__in=unread_ids).update(read_at=read_time)
                for message in active_messages:
                    if message.pk in unread_ids:
                        message.read_at = read_time

    for conversation in conversations:
        other_user_id = conversation.participant_two_id if conversation.participant_one_id == user.id else conversation.participant_one_id
        conversation.other_user = conversation.participant_two if conversation.participant_one_id == user.id else conversation.participant_one
        conversation.unread_count = conversation.messages.filter(sender_id=other_user_id, read_at__isnull=True).count()
        conversation.last_message = conversation.messages.order_by("-created_at").first()

    for swap in completed_swaps_needing_address:
        swap.address_form = ShippingAddressForm(prefix=f"swap-{swap.pk}")

    return {
        "items": listed_items,
        "held_items": held_items,
        "received_items": received_items,
        "shared_items": shared_items,
        "item_count": item_count,
        "available_count": available_count,
        "pending_items_count": pending_items_count,
        "swapped_items_count": swapped_items_count,
        "total_points": total_points,
        "pending_swaps_count": pending_swaps_count,
        "completed_swaps_count": completed_swaps_count,
        "incoming_pending_count": incoming_pending_count,
        "recent_swaps": recent_swaps,
        "incoming_swaps": incoming_swaps,
        "outgoing_swaps": outgoing_swaps,
        "completed_swaps_needing_address": completed_swaps_needing_address,
        "completed_swaps_with_address": completed_swaps_with_address,
        "owner_shipping_actions": owner_shipping_actions,
        "buyer_delivery_actions": buyer_delivery_actions,
        "conversations": conversations,
        "active_conversation": active_conversation,
        "active_messages": active_messages,
        "message_form": MessageForm(),
    }


@login_required
def dashboard(request):
    context = _build_dashboard_context(request.user, request.GET.get("conversation"))
    return render(request, "rewear/dashboard.html", context)


@login_required
def my_orders(request):
    context = _build_dashboard_context(request.user, request.GET.get("conversation"))
    return render(request, "rewear/my_orders.html", context)


@login_required
def my_shipments(request):
    context = _build_dashboard_context(request.user, request.GET.get("conversation"))
    return render(request, "rewear/my_shipments.html", context)


@login_required
def add_item(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.current_holder = request.user
        item.save()
        messages.success(request, "Your item has been listed successfully.")
        return redirect("item_detail", pk=item.pk)

    return render(request, "rewear/add_item.html", {"form": form})


@login_required
def create_swap_request(request, pk):
    if request.method != "POST":
        return redirect("item_detail", pk=pk)

    item = get_object_or_404(Item.objects.select_related("owner", "current_holder"), pk=pk)
    action_type = request.POST.get("action_type", "swap")

    if item.owner_id == request.user.id:
        messages.error(request, "You cannot request a swap for your own item.")
        return redirect("item_detail", pk=pk)

    if item.status != "available":
        messages.error(request, "This item is not currently available for new swap requests.")
        return redirect("item_detail", pk=pk)

    existing_pending = Swap.objects.filter(item=item, initiator=request.user, status="pending").first()
    if existing_pending:
        messages.info(request, "You already have a pending request for this item.")
        return redirect("item_detail", pk=pk)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if action_type == "redeem" and profile.points < item.points:
        messages.error(request, "You do not have enough points to redeem this item yet.")
        return redirect("item_detail", pk=pk)

    note = (
        f"{request.user.first_name or request.user.username} requested a direct swap."
        if action_type == "swap"
        else f"{request.user.first_name or request.user.username} requested a points redemption."
    )
    swap = Swap.objects.create(
        item=item,
        initiator=request.user,
        recipient=item.owner,
        status="pending",
        points_delta=item.points,
        note=note,
    )
    _get_or_create_conversation(item, request.user, item.owner, swap=swap)
    item.status = "pending"
    item.save(update_fields=["status"])
    messages.success(request, "Your request was sent to the item owner.")
    return redirect("dashboard")


@login_required
def update_swap_status(request, swap_id, action):
    if request.method != "POST":
        return redirect("dashboard")

    swap = get_object_or_404(Swap.objects.select_related("item", "initiator", "recipient"), pk=swap_id)
    item = swap.item

    if action == "complete":
        if swap.recipient_id != request.user.id:
            messages.error(request, "Only the item owner can complete this swap.")
            return redirect("dashboard")
        if swap.status != "pending":
            messages.info(request, "This swap is already closed.")
            return redirect("dashboard")

        initiator_profile, _ = UserProfile.objects.get_or_create(user=swap.initiator)
        recipient_profile, _ = UserProfile.objects.get_or_create(user=swap.recipient)
        if initiator_profile.points < swap.points_delta:
            messages.error(request, "The requester no longer has enough points to complete this swap.")
            return redirect("dashboard")

        initiator_profile.points -= swap.points_delta
        recipient_profile.points += swap.points_delta
        initiator_profile.save(update_fields=["points"])
        recipient_profile.save(update_fields=["points"])

        swap.status = "completed"
        swap.completed_at = timezone.now()
        swap.fulfillment_status = "awaiting_address"
        swap.save(update_fields=["status", "completed_at", "fulfillment_status"])
        if item:
            item.status = "swapped"
            item.current_holder = swap.initiator
            item.save(update_fields=["status", "current_holder"])
        _get_or_create_conversation(item, swap.initiator, swap.recipient, swap=swap)
        messages.success(request, "Swap marked as completed. The requester can now privately submit their shipping address.")
        return redirect("dashboard")

    if action == "cancel":
        if request.user.id not in {swap.initiator_id, swap.recipient_id}:
            messages.error(request, "You do not have permission to update this swap.")
            return redirect("dashboard")
        if swap.status != "pending":
            messages.info(request, "This swap is already closed.")
            return redirect("dashboard")

        swap.status = "cancelled"
        swap.save(update_fields=["status"])
        if item and not Swap.objects.filter(item=item, status="pending").exclude(pk=swap.pk).exists():
            item.status = "available"
            item.save(update_fields=["status"])
        messages.success(request, "Swap request cancelled.")
        return redirect("dashboard")

    if action == "ship":
        if swap.recipient_id != request.user.id:
            messages.error(request, "Only the original owner can mark the parcel as shipped.")
            return redirect("dashboard")
        if swap.status != "completed" or not swap.has_shipping_address:
            messages.error(request, "Shipping can start only after completion and address exchange.")
            return redirect("dashboard")
        swap.fulfillment_status = "shipped"
        swap.shipped_at = timezone.now()
        swap.save(update_fields=["fulfillment_status", "shipped_at"])
        messages.success(request, "Swap marked as shipped.")
        return redirect("dashboard")

    if action == "deliver":
        if swap.initiator_id != request.user.id:
            messages.error(request, "Only the requester can confirm delivery.")
            return redirect("dashboard")
        if swap.fulfillment_status != "shipped":
            messages.error(request, "Only shipped swaps can be marked as delivered.")
            return redirect("dashboard")
        swap.fulfillment_status = "delivered"
        swap.delivered_at = timezone.now()
        swap.save(update_fields=["fulfillment_status", "delivered_at"])
        messages.success(request, "Delivery confirmed. Enjoy the swap.")
        return redirect("dashboard")

    messages.error(request, "Unsupported swap action.")
    return redirect("dashboard")


@login_required
def submit_shipping_address(request, swap_id):
    swap = get_object_or_404(Swap.objects.select_related("item", "initiator", "recipient"), pk=swap_id)
    if swap.initiator_id != request.user.id:
        messages.error(request, "Only the requester can submit delivery details.")
        return redirect("dashboard")
    if swap.status != "completed":
        messages.error(request, "Address details can only be added after the swap is completed.")
        return redirect("dashboard")

    form = ShippingAddressForm(request.POST, prefix=f"swap-{swap.pk}")
    if form.is_valid():
        for field, value in form.cleaned_data.items():
            setattr(swap, field, value)
        swap.address_submitted_at = timezone.now()
        swap.fulfillment_status = "ready_to_ship"
        swap.save()
        messages.success(request, "Your delivery details were shared privately with the item owner.")
    else:
        messages.error(request, "Please complete all required address fields.")
    return redirect("dashboard")


@login_required
def open_item_conversation(request, pk):
    item = get_object_or_404(Item.objects.select_related("owner"), pk=pk)
    if item.owner_id == request.user.id:
        messages.info(request, "You already own this listing conversation thread.")
        return redirect("item_detail", pk=pk)
    conversation = _get_or_create_conversation(item, request.user, item.owner)
    return redirect(f"/dashboard/?conversation={conversation.pk}")


@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.select_related("item", "participant_one", "participant_two"),
        pk=conversation_id,
    )
    if request.user.id not in {conversation.participant_one_id, conversation.participant_two_id}:
        messages.error(request, "You do not have access to this conversation.")
        return redirect("dashboard")
    if request.method != "POST":
        return redirect(f"/dashboard/?conversation={conversation.pk}")

    form = MessageForm(request.POST)
    if form.is_valid():
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=form.cleaned_data["body"].strip(),
        )
        conversation.save(update_fields=["updated_at"])
        messages.success(request, "Message sent.")
    else:
        messages.error(request, "Please enter a message before sending.")
    return redirect(f"/dashboard/?conversation={conversation.pk}")
