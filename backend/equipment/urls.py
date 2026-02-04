from django.urls import path
from .views import CSVUploadView, UploadHistoryView, PDFReportView, SignupView

urlpatterns = [
    path("upload/", CSVUploadView.as_view(), name="upload_csv"),
    path("history/", UploadHistoryView.as_view(), name="upload_history"),
    path("report/", PDFReportView.as_view(), name="pdf_report"),
    path("signup/", SignupView.as_view(), name="signup"),
]
