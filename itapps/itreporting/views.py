from django.shortcuts import render
from django.http import HttpResponse
from itreporting.models import Issue
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from itreporting.models import Issue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeleteView

def home(request):

    return render (request, 'itreporting/home.html', {'title':'Welcome'})

def aboutus(request):

    return render (request, 'itreporting/aboutus.html', {'title':'About Us'})

def contactus(request):

    return render (request, 'itreporting/contactus.html', {'title':'Contact Us'})

def report(request):
    issues = issues.objects.all()
    context = {'issues':issues}
    return render (request,'itreporting/report.html', context)

def report (request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request,'itreporting/report.html',daily_report)
# Create your views here.

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted'] #one "t" due to ordering issue < that was old, I remigrated everything 
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5 #Optinal pagination...??

    
class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Issue
    fields = ['type','room','urgent','details']

    def form_valid(self,form):
        
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

    success_url = '/report'

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Issue

    success_url = '/report'
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author

