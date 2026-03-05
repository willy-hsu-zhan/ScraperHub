# backend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 前端登入頁面
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # 後台頁面
    path("dashboard/", views.dashboard_view, name="dashboard"), 
    # 各分類頁面
    path("gov-ojts/", views.gov_ojts_view, name="gov_ojts"),
    path("delivery-coupons/", views.delivery_coupons_view, name="delivery_coupons"),
    path("free-games-4gamers/", views.free_games_4gamers_view, name="free_games_4gamers"),
    path("birthday-discounts/", views.birthday_discounts_view, name="birthday_discounts"),
    path("rent-591/", views.rent_591_view, name="rent_591"),
    path("popular-video/", views.popular_video_view, name="popular_video"),
]