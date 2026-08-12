
from django.urls import path
from . import views

app_name="data1"
urlpatterns=[
    path('',views.home.as_view(),name="home"),
    path('info/<slug>/',views.info,name="info"),
    path('detail/<slug>/',views.detail,name="detail"),
    path('reference/<slug>/',views.reference_pdf,name="reference_pdf"),
    path('office/<slug>/',views.office_pdf,name="office_pdf"),
    path('one_time/',views.one_time,name="one_time"),
    path('all_user/',views.all_user.as_view(),name="all_user"),
    path('address_update',views.address_update,name="address_update")
]