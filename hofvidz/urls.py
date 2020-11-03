from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from themes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # User account creation and authorisation
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    # Theme view
    path('themes/create_theme', views.CreateTheme.as_view(), name='create_theme'),
    path('themes/<int:pk>', views.DetailTheme.as_view(), name='detail_theme'),
    # path('themes/<int:pk>/update', views.UpdateTheme.as_view(), name='update_theme'),
    # path('themes/<int:pk>/delete', views.DeleteTheme.as_view(), name='delete_theme'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
