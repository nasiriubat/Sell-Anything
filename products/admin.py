from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'categories', 'user',
                    'location', 'price', 'condition', 'quantity', 'is_published']
    search_fields = ['title']
    list_filter = ['user', 'created_at','categories','condition']
    list_per_page = 10
    date_hierarchy = 'created_at'
    actions = ['publish','notpublish' ]
    
    def publish(self, request, queryset):
        for product in queryset:
            product.is_published =True
            product.save()

    publish.short_description = 'Publish Product'

    def notpublish(self, request, queryset):
        for product in queryset:
            product.is_published =False
            product.save()

    notpublish.short_description = 'Hide Product'



