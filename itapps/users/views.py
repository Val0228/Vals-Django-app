from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm    
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from itreporting.models import StudentModuleRegistration, Module


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account has been created! Now you can login!')
            return redirect('login') 
        else:
           messages.warning(request, 'Unable to create account. Please check the form for errors.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})


   


@login_required 
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get enrollments and calculate credits
    enrollments = StudentModuleRegistration.objects.filter(
        student=request.user
    ).select_related('module').order_by('-date_registered')
    
    completed_modules = enrollments.filter(status='completed')
    enrolled_modules = enrollments.filter(status='enrolled')
    
    # Calculate total credits
    total_credits = sum(reg.module.credit for reg in completed_modules)
    
    # Determine degree classification
    all_modules = Module.objects.count()
    completed_count = completed_modules.count()
    credits_remaining = max(0, 50 - total_credits)
    
    if completed_count == all_modules and all_modules > 0:
        degree_classification = "1st Class"
        degree_color = "success"
    elif total_credits >= 65:
        degree_classification = "2:1 (Upper Second)"
        degree_color = "info"
    elif total_credits >= 50:
        degree_classification = "Pass"
        degree_color = "warning"
    else:
        degree_classification = "In Progress"
        degree_color = "secondary"
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Student Profile',
        'enrollments': enrollments,
        'completed_modules': completed_modules,
        'enrolled_modules': enrolled_modules,
        'total_credits': total_credits,
        'degree_classification': degree_classification,
        'degree_color': degree_color,
        'completed_count': completed_count,
        'total_modules': all_modules,
        'credits_remaining': credits_remaining,
    }
    return render(request, 'users/profile.html', context)

