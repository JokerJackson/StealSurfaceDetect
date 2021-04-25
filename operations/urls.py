from django.urls import path
from .views import login, uploadImg, detectImg

app_name = "operations"

urlpatterns = [
    path("login/", login, name="login"),
    path("uploadImg/<int:user_id>/", uploadImg, name="uploadImg"),
    path("detectImg/<int:user_id>", detectImg, name="detectImg")
]