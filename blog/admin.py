from django.contrib import admin

from blog.models import Post, Person, Feedback

admin.site.register(Post)
admin.site.register(Person)
admin.site.register(Feedback)
# Register your models here.
