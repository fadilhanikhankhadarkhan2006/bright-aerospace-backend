from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsCompany, IsStudent
from .models import Internship, InternshipApplication


@api_view(['POST'])
@permission_classes([IsCompany])
def post_internship(request):
    """Company users post internships."""

    # Use the authenticated user (must be a company account)
    company = request.user

    internship = Internship.objects.create(
        company=company,
        title=request.data.get("title"),
        description=request.data.get("description"),
        location=request.data.get("location"),
        stipend=request.data.get("stipend", "")
    )

    return Response(
        {
            "message": "Internship posted",
            "internship_id": internship.id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([IsStudent])
def apply_internship(request):
    """Students apply to an internship."""

    student = request.user
    internship_id = request.data.get("internship_id")

    if not internship_id:
        return Response(
            {"error": "internship_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        internship = Internship.objects.get(id=internship_id)
    except Internship.DoesNotExist:
        return Response(
            {"error": "Internship not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    InternshipApplication.objects.create(
        student=student,
        internship=internship,
    )

    return Response(
        {"message": "Application submitted"},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([IsCompany])
def view_applicants(request, internship_id):
    """Companies can view applicants to their own internships."""

    company = request.user

    try:
        internship = Internship.objects.get(id=internship_id, company=company)
    except Internship.DoesNotExist:
        return Response(
            {"error": "Internship not found or access denied"},
            status=status.HTTP_404_NOT_FOUND,
        )

    applications = internship.applications.select_related("student").all()

    data = [
        {
            "student": app.student.username,
            "email": app.student.email,
            "applied_at": app.applied_at,
        }
        for app in applications
    ]

    return Response(data)
