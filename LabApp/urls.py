# created manually!
from django.urls import path
from . import views

urlpatterns = [
    path('test-upload', views.file_analysis_test, name='lab-app-test-upload'),
    path('sample-dataset-generator', views.sample_generator, name='lab-app-sample-dataset-generator'),
]