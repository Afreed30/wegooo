from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views  # ✅ Import your new signup/login views

def home(request):
    return JsonResponse({
        "message": "🚍 Bus Booking API is running",
        "routes": [
            "/admin/",
            "/api/",
            "/api/signup/",
            "/api/login/",
            "/api/token/",
            "/api/token/refresh/",
            "/api/register-bus/",
            "/api/cities/",
            "/api/search_buses/"
        ]
    })


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # ✅ Main API endpoints
    path('api/', include('api.urls')),

    # ✅ User authentication routes
    path('api/signup/', views.signup_user, name='signup_user'),
    path('api/login/', views.login_user, name='login_user'),

    # ✅ JWT authentication (still available if needed)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
