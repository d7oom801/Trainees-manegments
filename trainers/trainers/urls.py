from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [

]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('trainees_list.urls')),
)
