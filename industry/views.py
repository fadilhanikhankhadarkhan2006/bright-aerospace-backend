from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import User
from .models import Internship, InternshipApplication


@api_view(['POST'])
def post_internship(request):

    company_id = request.data.get("company_id")

    try:
        company = User.objects.get(id=company_id, role="company")
    except User.DoesNotExist:
        return Response({"error": "Invalid company"}, status=400)

    internship = Internship.objects.create(
        company=company,
        title=request.data.get("title"),
        description=request.data.get("description"),
        location=request.data.get("location"),
        stipend=request.data.get("stipend")
    )

    return Response({
        "message": "Internship posted",
        "internship_id": internship.id
    })


@api_view(['POST'])
def apply_internship(request):

    student_id = request.data.get("student_id")
    internship_id = request.data.get("internship_id")

    try:
        student = User.objects.get(id=student_id, role="student")
        internship = Internship.objects.get(id=internship_id)
    except:
        return Response({"error": "Invalid data"}, status=400)

    InternshipApplication.objects.create(
        student=student,
        internship=internship
    )

    return Response({"message": "Application submitted"})


@api_view(['GET'])
def view_applicants(request, internship_id):

    applications = InternshipApplication.objects.filter(internship_id=internship_id)

    data = []

    for app in applications:
        data.append({
            "student": app.student.username,
            "email": app.student.email,
            "applied_at": app.applied_at
        })

    return Response(data)