from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('student_info/', views.student_info, name='student_info'),
    path('payments/', views.payments, name='payments'),
    path('reports/', views.reports, name= 'reports'),
    path('submit_payment/', views.make_payment, name='make_payment'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main, name='main'),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += staticfiles_urlpatterns()