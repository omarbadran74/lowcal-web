from django.urls import path
from . import views

# Admin panel URLs
admin_panel_patterns = ([
    path('', views.admin_dashboard, name='dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/new/', views.plan_create, name='plan_create'),
    path('plans/<int:pk>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('subscribers/', views.admin_subscribers, name='subscribers'),
    path('subscribers/<int:pk>/edit/', views.subscriber_edit, name='subscriber_edit'),
    path('subscribers/<int:pk>/delete/', views.subscriber_delete, name='subscriber_delete'),
    path('subscribers/<int:pk>/reset/<int:day_number>/', views.reset_day, name='reset_day'),
    path('subscribers/<int:pk>/absent/', views.add_absent_day, name='add_absent_day'),
], 'admin_panel')

# Cashier URLs
cashier_patterns = ([
    path('', views.cashier_dashboard, name='dashboard'),
    path('subscribers/new/', views.subscriber_create, name='subscriber_create'),
    path('subscribers/<int:pk>/', views.subscriber_detail, name='subscriber_detail'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/export/', views.orders_export_excel, name='orders_export'),
    path('orders/<int:subscriber_id>/<int:day_number>/deliver/', views.toggle_delivery, name='toggle_delivery'),
], 'cashier')
