from django.http import HttpResponse
from django.db import transaction
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CSVUploadSerializer
from .models import EquipmentUpload

import pandas as pd

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_file = serializer.validated_data["file"]

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response(
                {"error": f"Failed to read CSV: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if df.empty:
            return Response(
                {"error": "CSV file is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_columns = {"Type", "Flowrate", "Pressure", "Temperature"}
        if not required_columns.issubset(df.columns):
            return Response(
                {
                    "error": "CSV must contain columns: Type, Flowrate, Pressure, Temperature"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            df["Flowrate"] = pd.to_numeric(df["Flowrate"], errors='coerce')
            df["Pressure"] = pd.to_numeric(df["Pressure"], errors='coerce')
            df["Temperature"] = pd.to_numeric(df["Temperature"], errors='coerce')
            
            if df[["Flowrate", "Pressure", "Temperature"]].isnull().any().any():
                return Response(
                    {"error": "CSV contains invalid numeric values"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": f"Data validation error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        summary = {
            "total_equipment": int(len(df)),
            "average_flowrate": float(df["Flowrate"].mean()),
            "average_pressure": float(df["Pressure"].mean()),
            "average_temperature": float(df["Temperature"].mean()),
            "equipment_type_distribution": df["Type"].value_counts().to_dict(),
        }

        with transaction.atomic():
            EquipmentUpload.objects.create(
                total_equipment=summary["total_equipment"],
                average_flowrate=summary["average_flowrate"],
                average_pressure=summary["average_pressure"],
                average_temperature=summary["average_temperature"],
                equipment_type_distribution=summary["equipment_type_distribution"],
            )

            uploads = EquipmentUpload.objects.order_by("-uploaded_at")
            if uploads.count() > 5:
                old_ids = list(uploads.values_list('id', flat=True)[5:])
                if old_ids:
                    EquipmentUpload.objects.filter(id__in=old_ids).delete()

        return Response(summary, status=status.HTTP_200_OK)


class UploadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = EquipmentUpload.objects.order_by("-uploaded_at")[:5]

        response = []
        for item in uploads:
            response.append(
                {
                    "uploaded_at": item.uploaded_at.strftime("%d %b %Y, %I:%M %p UTC"),
                    "total_equipment": item.total_equipment,
                    "average_flowrate": item.average_flowrate,
                    "average_pressure": item.average_pressure,
                    "average_temperature": item.average_temperature,
                    "equipment_type_distribution": item.equipment_type_distribution,
                }
            )

        return Response(response, status=status.HTTP_200_OK)


class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = EquipmentUpload.objects.order_by("-uploaded_at").first()

        if not latest:
            return Response(
                {"error": "No uploads found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="equipment_report.pdf"'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 50, "Chemical Equipment Report")

        uploaded_at = latest.uploaded_at.strftime("%d %b %Y, %I:%M %p UTC")

        c.setFont("Helvetica", 11)
        y = height - 100

        c.drawString(50, y, f"Uploaded At: {uploaded_at}")
        y -= 20
        c.drawString(50, y, f"Total Equipment: {latest.total_equipment}")
        y -= 20
        c.drawString(50, y, f"Average Flowrate: {latest.average_flowrate:.2f}")
        y -= 20
        c.drawString(50, y, f"Average Pressure: {latest.average_pressure:.2f}")
        y -= 20
        c.drawString(50, y, f"Average Temperature: {latest.average_temperature:.2f}")

        y -= 40
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "Equipment Type Distribution")

        table_data = [["Equipment Type", "Count"]]
        for key, value in latest.equipment_type_distribution.items():
            table_data.append([key, str(value)])

        table = Table(table_data, colWidths=[3 * inch, 2 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ]
            )
        )

        table.wrapOn(c, width, height)
        table.drawOn(c, 50, y - (25 * len(table_data)))

        c.showPage()
        c.save()

        return response

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )