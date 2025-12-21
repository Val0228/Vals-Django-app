from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.validators import FileExtensionValidator

# Create your models here.

class Issue(models.Model):
    type = models.CharField(max_length=100, choices=[('Hardware', 'Hardware'), ('Software', 'Software')])
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})


class Module(models.Model):
    AVAILABILITY_CHOICES = [
        ('open', 'Open for Registration'),
        ('closed', 'Closed for Registration'),
    ]
    
    CATEGORY_CHOICES = [
        ('Core', 'Core'),
        ('Optional', 'Optional'),
        ('Elective', 'Elective'),
        ('Foundation', 'Foundation'),
    ]
    
    name = models.CharField(max_length=200, help_text='Name of the module')
    code = models.CharField(max_length=20, unique=True, help_text='Module code (e.g., CS101)')
    credit = models.PositiveIntegerField(help_text='Number of credits')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, help_text='Module category')
    description = models.TextField(help_text='Module description')
    availability = models.CharField(
        max_length=10, 
        choices=AVAILABILITY_CHOICES, 
        default='open',
        help_text='Registration availability status'
    )
    courses_allowed = models.ManyToManyField(
        Group, 
        related_name='modules',
        blank=True,
        help_text='Courses (Groups) allowed to register for this module'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code', 'name']

    def __str__(self):
        return f'{self.code} - {self.name}'

    def get_absolute_url(self):
        return reverse('itreporting:module-detail', kwargs={'pk': self.pk})
    
    def is_available(self):
        return self.availability == 'open'


class StudentModuleRegistration(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='student_registrations')
    date_registered = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'module']
        ordering = ['-date_registered']
    
    def __str__(self):
        return f'{self.student.username} - {self.module.code}'
    
    def get_absolute_url(self):
        return reverse('itreporting:module-detail', kwargs={'pk': self.module.pk})


class ModuleSubmission(models.Model):
    registration = models.OneToOneField(
        StudentModuleRegistration, 
        on_delete=models.CASCADE, 
        related_name='submission'
    )
    file = models.FileField(
        upload_to='module_submissions/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'zip', 'rar', 'txt'])]
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, help_text='Additional notes or comments')
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f'Submission for {self.registration.module.code} by {self.registration.student.username}'


class ContactEnquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Contact Enquiries'
    
    def __str__(self):
        return f'Enquiry from {self.name} - {self.subject}'
