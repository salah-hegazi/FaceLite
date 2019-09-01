from django.urls import include, path

from .views import Registration, login, UpdateStatus


app_name = 'users'
urlpatterns = [
    # http://127.0.0.1:8000/users/register(First endpoint)
    path('register/', view=Registration.as_view(), name='registration'),
    # http://127.0.0.1:8000/users/login(Second endpoint)
    path('login/', view=login, name='login'),
    # http://127.0.0.1:8000/users/status(Third endpoint)
    path('status/', view=UpdateStatus.as_view(), name='status'),

]

