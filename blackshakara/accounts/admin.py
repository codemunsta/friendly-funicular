from django.contrib import admin

from .models import User, AccountSettings, Notification, FeedBack

admin.site.register(User)
admin.site.register(AccountSettings)
admin.site.register(Notification)
admin.site.register(FeedBack)

# Register your models here.
