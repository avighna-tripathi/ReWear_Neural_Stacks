from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, SignUpForm, StyledAuthenticationForm
from .models import Item, UserProfile


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

    items = Item.objects.select_related("owner")
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

    return render(
        request,
        "rewear/browse.html",
        {
            "items": items,
            "query": query,
            "selected_category": category,
            "selected_sort": sort,
            "categories": Item.CATEGORY_CHOICES,
        },
    )


def item_detail(request, pk):
    item = get_object_or_404(Item.objects.select_related("owner"), pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=item.pk)[:4]
    return render(
        request,
        "rewear/item_detail.html",
        {
            "item": item,
            "related_items": related_items,
        },
    )


@login_required
def dashboard(request):
    items = request.user.items.all()
    item_count = items.count()
    available_count = items.filter(status="available").count()
    total_points = getattr(request.user, "profile", None).points if hasattr(request.user, "profile") else 0
    return render(
        request,
        "rewear/dashboard.html",
        {
            "items": items,
            "item_count": item_count,
            "available_count": available_count,
            "total_points": total_points,
        },
    )


@login_required
def add_item(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        messages.success(request, "Your item has been listed successfully.")
        return redirect("item_detail", pk=item.pk)

    return render(request, "rewear/add_item.html", {"form": form})
