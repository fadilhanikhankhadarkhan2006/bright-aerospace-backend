from django.urls import path
from .views import post_internship, apply_internship, view_applicants

urlpatterns = [
    path('post-internship/', post_internship),
    path('apply-internship/', apply_internship),
    path('view-applicants/<int:internship_id>/', view_applicants),
]