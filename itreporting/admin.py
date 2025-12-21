from django.contrib import admin
from itreporting.models import Issue, Module, StudentModuleRegistration, ModuleSubmission, ContactEnquiry

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['type', 'room', 'author', 'date_submitted', 'urgent']
    list_filter = ['type', 'urgent', 'date_submitted']
    search_fields = ['room', 'details', 'author__username']
    date_hierarchy = 'date_submitted'

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credit', 'category', 'availability', 'created_at']
    list_filter = ['category', 'availability', 'created_at']
    search_fields = ['code', 'name', 'description']
    filter_horizontal = ['courses_allowed']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'credit', 'category')
        }),
        ('Details', {
            'fields': ('description', 'availability')
        }),
        ('Registration', {
            'fields': ('courses_allowed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StudentModuleRegistration)
class StudentModuleRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'date_registered', 'status']
    list_filter = ['status', 'date_registered', 'module__category']
    search_fields = ['student__username', 'module__code', 'module__name']
    date_hierarchy = 'date_registered'
    readonly_fields = ['date_registered']

@admin.register(ModuleSubmission)
class ModuleSubmissionAdmin(admin.ModelAdmin):
    list_display = ['registration', 'submitted_at', 'file']
    list_filter = ['submitted_at']
    search_fields = ['registration__student__username', 'registration__module__code']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']
    list_editable = ['is_read']

# Register your models here.
