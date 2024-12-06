from django.contrib import admin
from .models import Category, Product, Order

class CategoryAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CategoryAdmin, self).__init__(*args, **kwargs)
        self.model._meta.verbose_name_plural = "Categories"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Order)
