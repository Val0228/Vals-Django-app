from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm    
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account has been craetd! Now you can login!')
            return redirect('login') 
        else:
           messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})


   


@login_required 
def profile(request): 
    return render(request, 'users/profile.html', {'title':'Student Profile'})
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST, instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, insatnce=request.user.profile)

    if u_form.is_valid()and p_form.is_valid():
        u_form.save()
        p_form.save
        messages.success(request,'Your account has been successfully updated!')
        return redirect('profile')
    else:
       u_form = UserUpdateForm(instance=request.user)
       p_form = ProfileUpdateForm(instance=request.user.profile)
       context={'u_form':u_form,'p_form':p_form,'title':'Student Profile'}
       return render(request, 'user/profile.html', context)

