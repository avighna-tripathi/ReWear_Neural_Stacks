from django.urls import path

from .views import (
    RewearLoginView,
    RewearLogoutView,
    add_item,
    browse,
    create_swap_request,
    dashboard,
    home,
    item_detail,
    my_orders,
    my_shipments,
    open_item_conversation,
    send_message,
    signup,
    submit_shipping_address,
    update_swap_status,
)


urlpatterns = [
    path("", home, name="home"),
    path("login/", RewearLoginView.as_view(), name="login"),
    path("logout/", RewearLogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("browse/", browse, name="browse"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/orders/", my_orders, name="my_orders"),
    path("dashboard/shipments/", my_shipments, name="my_shipments"),
    path("add-item/", add_item, name="add_item"),
    path("item/<int:pk>/", item_detail, name="item_detail"),
    path("item/<int:pk>/request-swap/", create_swap_request, name="create_swap_request"),
    path("item/<int:pk>/message/", open_item_conversation, name="open_item_conversation"),
    path("swap/<int:swap_id>/address/", submit_shipping_address, name="submit_shipping_address"),
    path("swap/<int:swap_id>/<str:action>/", update_swap_status, name="update_swap_status"),
    path("conversation/<int:conversation_id>/message/", send_message, name="send_message"),
]
