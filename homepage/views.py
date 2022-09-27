from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# Create your views here.
def index(request):
    titles = _('Kosamindo - Analisa Teknikal Saham menggunakan teknik Astro Trading')
    # member = MemberProfile.objects.filter(username=request.user).values_list('username', flat=True).first()
    # request.breadcrumbs(titles, request.path_info)

    get_memberusername = request.user.username

    if request.user.is_authenticated:
        # get_status_trial = Subscription.objects.filter(member=request.user, subscription=1).values_list('status', flat=True).first()
        # get_status_standar = Subscription.objects.filter(member=request.user, subscription=2).values_list('status', flat=True).first()
        # get_status_professional = Subscription.objects.filter(member=request.user, subscription=3).values_list('status', flat=True).first()
        # get_status_enterprise = Subscription.objects.filter(member=request.user, subscription=4).values_list('status', flat=True).first()

        dir_user = base_dir + "/upload/members/" + get_memberusername + "/"
        # print("dir_user", dir_user)
        # check_dir_user = os.path.isdir(dir_user)
        check_dir_user = os.path.exists(dir_user)

        # print("get_element_member", get_element_member)

        if check_dir_user is False:
            # os.makedirs(dir_user, exist_ok=True)
            os.makedirs(dir_user)
            os.chmod(dir_user, 0o777)
            # os.mkdir(dir_user)
            # print("check_dir_user")
        else:
            pass

        dir_user_forecast = dir_user + "forecast/"
        check_dir_user_forecast = os.path.isdir(dir_user_forecast)

        if check_dir_user_forecast is False:
            # os.mkdir(dir_user_forecast)
            os.makedirs(dir_user_forecast)
            os.chmod(dir_user_forecast, 0o777)
        # print("None")
        else:
            pass

        cache.set('dir_user_forecast', dir_user_forecast, None)


        get_now = Subscription.objects.filter(member=request.user, expired_date__lte=timezone.now())

        if get_now:
            for item in get_now.all():
                item.status = "expired"
                item.active = False
                item.save()

        # if get_status_trial == "expired":
        #   messages.warning(request, "You're Trial Package is expired. Please choose the package to continue.")
        # if get_status_standar == "expired":
        #   messages.warning(request, "You're Standar Package is expired. Please choose the package to continue.")
        # if get_status_professional == "expired":
        #   messages.warning(request, "You're Professional Package is expired. Please choose the package to continue.")
        # if get_status_enterprise == "expired":
        #   messages.warning(request, "You're Enterprise Package is expired. Please choose the package to continue.")

    else:
        pass

    context = {
        # 'member': member,
        'titles': titles,
    }
    return render(request, 'index.html', context)
