from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itreporting.models import Issue, Module, StudentModuleRegistration, ModuleSubmission, ContactEnquiry
from itreporting.forms import ModuleSubmissionForm, ContactForm
from itreporting.services import WeatherService, NewsService
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.db.models import Q
from datetime import datetime

def home(request):
    # Get statistics
    total_modules = Module.objects.count()
    open_modules = Module.objects.filter(availability='open').count()
    recent_modules = Module.objects.filter(availability='open').order_by('-created_at')[:6]
    
    context = {
        'title': 'Welcome',
        'total_modules': total_modules,
        'open_modules': open_modules,
        'recent_modules': recent_modules,
        'show_news_feed': True,  # Flag to show news feed only on home page
    }
    
    # Add user-specific data if logged in
    if request.user.is_authenticated:
        user_enrollments = StudentModuleRegistration.objects.filter(
            student=request.user,
            status='enrolled'
        ).select_related('module')[:5]
        
        completed_count = StudentModuleRegistration.objects.filter(
            student=request.user,
            status='completed'
        ).count()
        
        total_credits = sum(
            reg.module.credit 
            for reg in StudentModuleRegistration.objects.filter(
                student=request.user,
                status='completed'
            )
        )
        
        context.update({
            'user_enrollments': user_enrollments,
            'completed_count': completed_count,
            'total_credits': total_credits,
        })
    
    # Add weather data
    weather_service = WeatherService()
    weather_data = weather_service.get_weather_by_city("Sheffield", "GB")
    context['weather'] = weather_data
    
    return render(request, 'itreporting/home.html', context)

def aboutus(request):
    # Add weather data
    weather_service = WeatherService()
    weather_data = weather_service.get_weather_by_city("Sheffield", "GB")
    
    return render(request, 'itreporting/aboutus.html', {
        'title': 'About Us',
        'weather': weather_data
    })

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your enquiry! We will get back to you soon.')
            return redirect('itreporting:contactus')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    
    return render(request, 'itreporting/contactus.html', {
        'title': 'Contact Us',
        'form': form
    })

def weather(request):
    """Weather page view"""
    weather_service = WeatherService()
    city = request.GET.get('city', 'Sheffield')
    country = request.GET.get('country', 'GB')
    
    weather_data = weather_service.get_weather_by_city(city, country)
    forecast_data = weather_service.get_forecast(city, country, days=5)
    
    context = {
        'title': 'Campus Weather',
        'weather': weather_data,
        'forecast': forecast_data,
        'city': city,
        'country': country,
    }
    
    return render(request, 'itreporting/weather.html', context)

def weather_api(request):
    """API endpoint for weather data (JSON)"""
    weather_service = WeatherService()
    city = request.GET.get('city', 'Sheffield')
    country = request.GET.get('country', 'GB')
    
    weather_data = weather_service.get_weather_by_city(city, country)
    
    if weather_data:
        return JsonResponse(weather_data)
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def news_api(request):
    """API endpoint for news data (JSON)"""
    news_service = NewsService()
    
    # Clear cache if refresh parameter is present
    if request.GET.get('refresh'):
        from django.core.cache import cache
        # Clear all news cache keys
        for key in ['news_business,tech,sports_8_uk_en', 'news_business,tech,sports_5_uk_en']:
            cache.delete(key)
    
    # Fetch fresh news
    news_articles = news_service.get_latest_news(limit=5)
    
    # Format articles for JSON response
    articles = []
    for article in news_articles:
        articles.append({
            'title': article.get('title', 'No title'),
            'description': article.get('description', ''),
            'url': article.get('url', '#'),
            'source': article.get('source', 'Unknown'),
            'published_at': article.get('published_at', ''),
            'image_url': article.get('image_url', ''),
            'snippet': article.get('snippet', '')[:150] + '...' if article.get('snippet') else '',
        })
    
    return JsonResponse({'articles': articles})

# Create your views here.

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by type
        issue_type = self.request.GET.get('type')
        if issue_type in ['Hardware', 'Software']:
            queryset = queryset.filter(type=issue_type)
        
        # Filter by urgent status
        urgent = self.request.GET.get('urgent')
        if urgent == 'true':
            queryset = queryset.filter(urgent=True)
        elif urgent == 'false':
            queryset = queryset.filter(urgent=False)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(room__icontains=search) |
                Q(details__icontains=search) |
                Q(description__icontains=search) |
                Q(author__username__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all issues for statistics
        all_issues = Issue.objects.all()
        
        # Statistics
        context['total_issues'] = all_issues.count()
        context['hardware_issues'] = all_issues.filter(type='Hardware').count()
        context['software_issues'] = all_issues.filter(type='Software').count()
        context['urgent_issues'] = all_issues.filter(urgent=True).count()
        context['recent_issues'] = all_issues.filter(
            date_submitted__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
        
        # Get current filter values
        context['current_type'] = self.request.GET.get('type', '')
        context['current_urgent'] = self.request.GET.get('urgent', '')
        context['current_search'] = self.request.GET.get('search', '')
        
        return context

    
class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Issue
    fields = ['type', 'room', 'details']

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = reverse_lazy('itreporting:report')
    
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author


# Module Views
class ModuleListView(ListView):
    model = Module
    template_name = 'itreporting/module_list.html'
    context_object_name = 'modules'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Module.objects.all()
        # Filter by availability if requested
        availability_filter = self.request.GET.get('availability')
        if availability_filter:
            queryset = queryset.filter(availability=availability_filter)
        # Filter by category if requested
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Module.CATEGORY_CHOICES
        context['availability_choices'] = Module.AVAILABILITY_CHOICES
        return context


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'itreporting/module_detail.html'
    context_object_name = 'module'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                registration = StudentModuleRegistration.objects.get(
                    student=self.request.user,
                    module=self.get_object()
                )
                context['registration'] = registration
                context['is_enrolled'] = True
                context['has_submission'] = hasattr(registration, 'submission')
            except StudentModuleRegistration.DoesNotExist:
                context['is_enrolled'] = False
        else:
            context['is_enrolled'] = False
        return context


# Enrollment Views
@login_required
def enroll_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    
    if not module.is_available():
        messages.error(request, 'This module is not available for registration.')
        return redirect('itreporting:module-detail', pk=pk)
    
    # Check if already enrolled
    if StudentModuleRegistration.objects.filter(student=request.user, module=module).exists():
        messages.warning(request, 'You are already enrolled in this module.')
        return redirect('itreporting:module-detail', pk=pk)
    
    # Create registration
    registration = StudentModuleRegistration.objects.create(
        student=request.user,
        module=module,
        status='enrolled'
    )
    messages.success(request, f'Successfully enrolled in {module.code} - {module.name}!')
    return redirect('itreporting:module-detail', pk=pk)


@login_required
def cancel_enrollment(request, pk):
    module = get_object_or_404(Module, pk=pk)
    
    try:
        registration = StudentModuleRegistration.objects.get(
            student=request.user,
            module=module
        )
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, f'Successfully cancelled enrollment in {module.code} - {module.name}.')
    except StudentModuleRegistration.DoesNotExist:
        messages.error(request, 'You are not enrolled in this module.')
    
    return redirect('itreporting:module-detail', pk=pk)


@login_required
def submit_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    
    try:
        registration = StudentModuleRegistration.objects.get(
            student=request.user,
            module=module,
            status='enrolled'
        )
    except StudentModuleRegistration.DoesNotExist:
        messages.error(request, 'You must be enrolled in this module to submit.')
        return redirect('itreporting:module-detail', pk=pk)
    
    if request.method == 'POST':
        form = ModuleSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if submission already exists
            if hasattr(registration, 'submission'):
                submission = registration.submission
                submission.file = form.cleaned_data['file']
                submission.notes = form.cleaned_data['notes']
                submission.submitted_at = timezone.now()
                submission.save()
                messages.success(request, 'Submission updated successfully!')
            else:
                submission = form.save(commit=False)
                submission.registration = registration
                submission.save()
                messages.success(request, 'Submission uploaded successfully!')
            return redirect('itreporting:module-detail', pk=pk)
    else:
        # Pre-fill form if submission exists
        if hasattr(registration, 'submission'):
            form = ModuleSubmissionForm(instance=registration.submission)
        else:
            form = ModuleSubmissionForm()
    
    return render(request, 'itreporting/module_submit.html', {
        'form': form,
        'module': module,
        'registration': registration
    })
