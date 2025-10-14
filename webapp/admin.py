from django.contrib import admin
from django.utils import timezone
from .models import Pet, UserProfile, AdminProfile, AdoptionRequest, PetRegistrationRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'species', 'gender', 'age', 'location', 'owner', 'date_added')
    list_filter = ('status', 'species', 'gender', 'date_added')
    search_fields = ('name', 'location', 'description', 'breed')
    readonly_fields = ('date_added',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'species', 'breed', 'color', 'age', 'gender')
        }),
        ('Status & Location', {
            'fields': ('status', 'location', 'found_date', 'owner')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Details', {
            'fields': ('description', 'image', 'date_added')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'location', 'phone_number')
    list_filter = ('gender', 'age')
    search_fields = ('user__username', 'user__email', 'location', 'phone_number')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_super_admin', 'created_at')
    list_filter = ('is_super_admin', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'pet__name')
    readonly_fields = ('created_at',)

@admin.register(PetRegistrationRequest)
class PetRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'species', 'pet_status', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status', 'species', 'pet_status', 'created_at', 'reviewed_at')
    search_fields = ('user__username', 'name', 'location', 'description')
    readonly_fields = ('created_at', 'reviewed_at')
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'status', 'reviewed_by', 'reviewed_at', 'created_at')
        }),
        ('Pet Details', {
            'fields': ('name', 'species', 'breed', 'color', 'age', 'gender', 'pet_status', 'location')
        }),
        ('Contact & Description', {
            'fields': ('contact_email', 'contact_phone', 'description', 'image')
        }),
        ('Admin Review', {
            'fields': ('admin_notes', 'created_pet')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status in ['approved', 'rejected'] and not obj.reviewed_at:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

