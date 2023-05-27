from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages


from .forms import UserUpdate,UserProfileForm,UserProfile
# Create your views here.
# USER INFORMAATION
@login_required(login_url='accounts/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_info = UserUpdate(request.POST, instance=request.user)
        profile = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_info.is_valid() and profile.is_valid():
            user_info.save()
            profile.save()
            messages.success(request, 'Your account has been updated')
            return HttpResponseRedirect('/userprofile')
    
    else:
        user_info = UserUpdate(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'user_info': user_info,
            'profile_form': profile_form
        }
        return render(request, 'user/user_update.html', context)
    

@login_required(login_url='accounts/login') # Check login
def user_profile(request):
    profile_info = UserProfile.objects.get_or_create(user=request.user)

    profile_qs = UserProfile.objects.filter(user=request.user)
    if profile_qs.exists():
        profile = UserProfile.objects.get(user=request.user)
        context = {
            'profile': profile,
        }
        return render(request, 'user/user_profile.html', context)

    else:
        profile = UserProfile.objects.create(user=request.user)
        context = {
                    'profile': profile,
                }
        return render(request, 'user/user_profile.html', context)