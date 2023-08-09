'''Admin setup for budgetmanager app'''
from django.contrib import admin
from . import models


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=...):
        if obj is None:
            return tuple()
        return self.readonly_fields

    class Meta:
        abstract = True


@admin.register(models.Budget)
class BudgetAdmin(BaseAdmin):
    '''Settings for the Budget admin'''
    list_display = ('user', 'name', 'active')
    list_display_links = list_display
    list_filter = ('user', 'active')
    sortable_by = list_display
    search_fields = ('name',)
    search_help_text = 'Search by budget name'


@admin.register(models.Payee)
class PayeeAdmin(BaseAdmin):
    '''Settings form the Payee admin'''
    list_display = ('user', 'name')
    list_display_links = list_display
    list_filter = ('user',)
    sortable_by = list_display
    search_fields = ('name',)
    search_help_text = 'Search by payee name'


@admin.register(models.Payment)
class PaymentAdmin(BaseAdmin):
    '''Settings for the Payment admin'''
    date_hierarchy = 'date'
    list_display = ('user', 'budget', 'payee', 'date')
    list_display_links = list_display
    list_filter = ('user', 'budget', 'payee', 'date')
    sortable_by = list_display

    def get_form(self, request, obj=..., change=..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj is not None:
            form.base_fields['budget'].queryset = form.base_fields['budget'].queryset.filter(
                user=obj.user)
            form.base_fields['payee'].queryset = form.base_fields['payee'].queryset.filter(
                user=obj.user)
        return form
