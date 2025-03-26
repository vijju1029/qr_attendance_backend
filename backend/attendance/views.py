import os
import json
import qrcode
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Attendance
from datetime import datetime

def home(request):
    """Render the home page."""
    return render(request, "attendance/home.html")

@csrf_exempt
def register_employee(request):
    """Register an employee and generate a QR code."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            name = data.get("name")
            department = data.get("department")

            if not (employee_id and name and department):
                return JsonResponse({"error": "Missing fields"}, status=400)
            
            # ✅ Check if employee already exists
            employee, created = Employee.objects.get_or_create(
                employee_id=employee_id,
                defaults={"name": name, "department": department},
            )

            if not created:
                return JsonResponse({"message": "Employee already exists", "qr_code": employee.qr_code})

            # ✅ Generate QR Code
            img = qrcode.make(employee_id)
            qr_directory = os.path.join(settings.MEDIA_ROOT, "qrcodes")
            os.makedirs(qr_directory, exist_ok=True)  # Ensure directory exists
            qr_path = os.path.join(qr_directory, f"{employee_id}.png")
            img.save(qr_path)

            # ✅ Save QR path to Employee
            employee.qr_code = f"qrcodes/{employee_id}.png"
            employee.save()

            # ✅ Return the full URL of the QR code
            qr_url = f"{settings.MEDIA_URL}{employee.qr_code}"

            return JsonResponse({
                "message": "Employee registered successfully",
                "employee_id": employee_id,
                "qr_code": qr_url
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def mark_attendance(request):
    """Mark attendance when an employee scans a QR code."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_id = data.get("employee_id")

            if not employee_id:
                return JsonResponse({"error": "Missing employee ID"}, status=400)

            try:
                employee = Employee.objects.get(employee_id=employee_id)
            except Employee.DoesNotExist:
                return JsonResponse({"error": "Employee not found"}, status=404)

            # ✅ Mark attendance
            attendance, created = Attendance.objects.get_or_create(
                employee=employee, date=datetime.today().date()
            )

            if not created:
                return JsonResponse({"message": "Attendance already marked for today"})

            return JsonResponse({"message": "Attendance marked successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def generate_qr(request):
    """Generate and return a QR Code for an employee."""
    if request.method == "GET":
        employee_id = request.GET.get("employee_id")
        if not employee_id:
            return HttpResponse("Missing employee ID", status=400)

        qr_path = os.path.join(settings.MEDIA_ROOT, "qrcodes", f"{employee_id}.png")

        if not os.path.exists(qr_path):
            return HttpResponse("QR Code not found", status=404)

        # Serve the image as an HTTP response
        with open(qr_path, "rb") as qr_file:
            return HttpResponse(qr_file.read(), content_type="image/png")

    return HttpResponse("Invalid request", status=400)

def employee_list(request):
    """Display a list of all employees."""
    employees = Employee.objects.all()
    return render(request, "attendance/employee_list.html", {"employees": employees})
