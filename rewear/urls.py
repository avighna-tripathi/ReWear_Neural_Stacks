from django.urls import path

from .views import (
    RewearLoginView,
    RewearLogoutView,
    add_item,
    browse,
    dashboard,
    home,
    item_detail,
    signup,
)


urlpatterns = [
    path("", home, name="home"),
    path("login/", RewearLoginView.as_view(), name="login"),
    path("logout/", RewearLogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("browse/", browse, name="browse"),
    path("dashboard/", dashboard, name="dashboard"),
    path("add-item/", add_item, name="add_item"),
    path("item/<int:pk>/", item_detail, name="item_detail"),
]
