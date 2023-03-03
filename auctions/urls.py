from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("edit_listing/<int:item_id>", views.edit_listing_view, name="edit_listing"),
    path("see_listing/<int:item_id>", views.see_listing, name="see_listing"),
    path("watchlist", views.watchlist_view, name="watchlist")
]
