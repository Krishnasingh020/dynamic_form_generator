from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/')),         # <- redirect root to admin
    path('', include('formbuilder.urls')),                 # optional if you want form URLs at root too
]

