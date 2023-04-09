from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def runserver_page(request):
    return HttpResponse(
        "<ul><li><a href='admin/'>admin</a></li>"
        "<li><a href='api/'>api</a></li></ul>",
        content_type="text/html",
        charset="utf-8"
    )


urlpatterns = [
    path('', runserver_page),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
]
