from django.contrib import admin

from .models import Posts, Comments, Likes

# Register your models here.
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
