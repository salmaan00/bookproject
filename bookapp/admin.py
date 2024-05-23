from django.contrib import admin

# Register your models here.
from .models import Book, Author

from .models import UserProfile,loginTable


admin.site.register(Book)
admin.site.register(Author)


admin.site.register(UserProfile)
admin.site.register(loginTable)
