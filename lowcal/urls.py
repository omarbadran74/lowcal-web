from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.urls import admin_panel_patterns, cashier_patterns

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', include(admin_panel_patterns)),
    path('cashier/', include(cashier_patterns)),
    path('s/<uuid:token>/', views.subscriber_page, name='subscriber_page'),
    path('s/<uuid:token>/select/', views.subscriber_select_meal, name='subscriber_select_meal'),
    path('s/<uuid:token>/submit/', views.subscriber_submit_day, name='subscriber_submit_day'),
    path('', views.login_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
