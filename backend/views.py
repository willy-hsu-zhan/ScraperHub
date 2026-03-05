# backend/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from .models import BirthdayDiscount,DeliveryCoupon,FreeGames4Gamers,GovOJTs,YoutubeVideos,Rent591
from .forms import BirthdayDiscountForm,DeliveryCouponForm,FreeGames4GamersForm,GovOJTsForm,YoutubeVideosForm,Rent591Form

#測試 API
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 限定必須驗證
def profile_view(request):
    """
    回傳登入使用者資訊
    """
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
    })

@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)  # 建立 session
            
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "帳號或密碼錯誤"})
    return render(request, "login.html")
    
@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)  # 清除 session
        return redirect("login")  # 登出後跳回登入頁
    
@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")

# 各分類頁面
@login_required
def gov_ojts_view(request):
    edit_id = request.GET.get("edit_id")
    delete_id = request.GET.get("delete_id")

    # 刪除
    if delete_id:
        obj = get_object_or_404(GovOJTs, id=delete_id)
        obj.delete()
        return redirect("gov_ojts")

    # 編輯
    if edit_id:
        instance = get_object_or_404(GovOJTs, id=edit_id)
    else:
        instance = None

    # 表單處理
    if request.method == "POST":
        form = GovOJTsForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_at = timezone.now()
            if not instance:
                obj.created_at = timezone.now()
            obj.save()
            return redirect("gov_ojts")
    else:
        form = GovOJTsForm(instance=instance)

    # 分頁
    objs = GovOJTs.objects.all()
    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "gov_ojts.html",
        {
            "form": form,
            "page_obj": page_obj,
            "edit_id": edit_id,
        },
    )

@login_required
def delivery_coupons_view(request):
    # 刪除
    delete_id = request.GET.get("delete_id")
    if delete_id:
        obj = get_object_or_404(DeliveryCoupon, pk=delete_id)
        obj.delete()
        return redirect("delivery_coupons")

    # 編輯
    edit_id = request.GET.get("edit_id")
    if edit_id:
        instance = get_object_or_404(DeliveryCoupon, pk=edit_id)
    else:
        instance = None

    # 新增 / 更新
    if request.method == "POST":
        form = DeliveryCouponForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("delivery_coupons")
    else:
        form = DeliveryCouponForm(instance=instance)

    # 列表 + 分頁
    coupons_list = DeliveryCoupon.objects.all().order_by("-id")
    paginator = Paginator(coupons_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "delivery_coupons.html",
        {
            "form": form,
            "page_obj": page_obj,
            "edit_id": edit_id
        }
    )

@login_required
def free_games_4gamers_view(request):
    edit_id = request.GET.get("edit_id")
    delete_id = request.GET.get("delete_id")

    # 刪除
    if delete_id:
        game = get_object_or_404(FreeGames4Gamers, id=delete_id)
        game.delete()
        return redirect("free_games_4gamers")

    # 編輯
    if edit_id:
        instance = get_object_or_404(FreeGames4Gamers, id=edit_id)
    else:
        instance = None

    # 表單處理
    if request.method == "POST":
        form = FreeGames4GamersForm(request.POST, instance=instance)

        if form.is_valid():
            game = form.save(commit=False)

            # 新增時產生 title_hash
            if not instance:
                game.title_hash = md5(game.title.encode()).hexdigest()

            game.updated_at = timezone.now()

            if not instance:
                game.created_at = timezone.now()

            game.save()
            return redirect("free_games_4gamers")
    else:
        form = FreeGames4GamersForm(instance=instance)

    # 分頁
    games = FreeGames4Gamers.objects.all()
    paginator = Paginator(games, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "free_games_4gamers.html",
        {
            "form": form,
            "page_obj": page_obj,
            "edit_id": edit_id,
        },
    )

@login_required
def birthday_discounts_view(request):
    """
    單一頁面管理生日優惠
    - 顯示列表
    - 分頁
    - 新增 / 編輯
    - 刪除
    """

    # 如果有 delete_id，刪除該筆
    delete_id = request.GET.get("delete_id")
    if delete_id:
        obj = get_object_or_404(BirthdayDiscount, pk=delete_id)
        obj.delete()
        return redirect("birthday_discounts")

    # 如果有 edit_id，讀取該筆資料
    edit_id = request.GET.get("edit_id")
    if edit_id:
        instance = get_object_or_404(BirthdayDiscount, pk=edit_id)
    else:
        instance = None

    if request.method == "POST":
        # 新增或編輯
        form = BirthdayDiscountForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("birthday_discounts")
    else:
        form = BirthdayDiscountForm(instance=instance)

    # 列表 + 分頁
    discounts_list = BirthdayDiscount.objects.all().order_by("-id")
    paginator = Paginator(discounts_list, 20)  # 每頁 20 筆
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "birthday_discounts.html",
        {"form": form, "page_obj": page_obj, "edit_id": edit_id}
    )

@login_required
def rent_591_view(request):
    edit_id = request.GET.get('edit_id')
    delete_id = request.GET.get('delete_id')

    if delete_id:
        Rent591.objects.filter(id=delete_id).delete()
        return redirect('rent_591')

    if request.method == 'POST':
        if edit_id:
            obj = Rent591.objects.get(id=edit_id)
            form = Rent591Form(request.POST, instance=obj)
        else:
            form = Rent591Form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('rent_591')
    else:
        if edit_id:
            obj = Rent591.objects.get(id=edit_id)
            form = Rent591Form(instance=obj)
        else:
            form = Rent591Form()

    queryset = Rent591.objects.all().order_by('-created_at')
    paginator = Paginator(queryset, 20)  # 每頁 20 筆
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'edit_id': edit_id,
    }
    return render(request, 'rent_591.html', context)

def popular_video_view(request):
    edit_id = request.GET.get("edit_id")
    delete_id = request.GET.get("delete_id")

    # 刪除
    if delete_id:
        obj = get_object_or_404(YoutubeVideos, id=delete_id)
        obj.delete()
        return redirect("popular_video")

    # 編輯
    if edit_id:
        instance = get_object_or_404(YoutubeVideos, id=edit_id)
    else:
        instance = None

    # 表單處理
    if request.method == "POST":
        form = YoutubeVideosForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_at = timezone.now()
            if not instance:
                obj.created_at = timezone.now()
            obj.save()
            return redirect("popular_video")
    else:
        form = YoutubeVideosForm(instance=instance)

    # 分頁
    objs = YoutubeVideos.objects.all()
    paginator = Paginator(objs, 20) # 每頁 20 筆
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "popular_video.html",
        {
            "form": form,
            "page_obj": page_obj,
            "edit_id": edit_id,
        },
    )