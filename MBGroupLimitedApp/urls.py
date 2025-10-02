from django.urls import path
from .views import (
    home ,service,
    
    #post function
    post_partner,post_client, post_certificate,
    
    #edit and delete
    partner_edit, partner_delete,client_edit, client_delete,certificate_edit, certificate_delete,
    
    #auth function
    register_admin ,login_admin, logout_admin,
    
    #account admin
    account, 
    
    #edit and delete users list
    admin_user_edit, admin_user_delete,
    
    #edit and delete adminaccount
    admin_superuser_edit, admin_superuser_delete,
)

urlpatterns = [
    path('', home, name='home'),
    path('service', service, name='service'),
    
    #post partner, client and certificates
    path('post_partner/', post_partner, name='post_partner'),
    path('post_client/', post_client, name='post_client'),
    path('post_certificate/', post_certificate, name='post_certificate'),
    
    # Partners
    path("partner_edit/<int:partner_id>/", partner_edit, name="partner_edit"),
    path("partner_delete/<int:partner_id>/", partner_delete, name="partner_delete"),

    # Clients
    path("client_edit/<int:client_id>/", client_edit, name="client_edit"),
    path("client_delete/<int:client_id>/", client_delete, name="client_delete"),

    # Certificates
    path("certificate_edit/<int:certificate_id>/", certificate_edit, name="certificate_edit"),
    path("certificate_delete/<int:certificate_id>/", certificate_delete, name="certificate_delete"),
    
    # # Auth
    path('register_admin/', register_admin, name='register_admin'),
    path('login_admin/', login_admin, name='login_admin'),
    path('logout_admin/', logout_admin, name='logout_admin'),
    
    ## account_admin
    path('account/', account, name='account'),
    
    #edit and delete admin account
    path("admin_superuser_edit/<int:user_id>/", admin_superuser_edit, name="admin_superuser_edit"),
    path("admin_superuser_delete/<int:user_id>/", admin_superuser_delete, name="admin_superuser_delete"),
    
    #edit and delete users
    path("admin_user_edit/<int:user_id>/", admin_user_edit, name="admin_user_edit"),
    path("admin_user_delete/<int:user_id>/", admin_user_delete ,name="admin_user_delete"),
]