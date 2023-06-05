from django.contrib import admin
import models

admin.site.register(models.Category)
admin.site.register(models.MenuItem)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
