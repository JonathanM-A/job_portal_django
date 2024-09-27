from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework.exceptions import PermissionDenied
from .models import Job, User, Application
from .serializers import JobSerializer, UserSerializer, ApplicationSerializer
from .permissions import CanApplyForJob, CanPostJob


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ["create", "delete", "update"]:
            permission_classes = [CanPostJob]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"], permission_classes=[CanApplyForJob])
    def apply(self, request, pk=None):
        job = self.get_object()
        applicant = request.user

        cv = request.FILES.get("CV")
        filename = cv.name

        if "." in filename and filename.rsplit(".", 1)[1].lower() not in [
            "pdf",
            "doc",
            "docx",
        ]:
            return Response({"error": "Unsupported file type"}, status=415)

        if Application.objects.filter(applicant=applicant, listing=job).exists():
            return Response(
                {"message": "You have already applied for this job"}, status=400
            )

        application = Application.objects.create(
            applicant=applicant, listing=job, cv=cv
        )

        job.num_applicants += 1
        job.save()

        serialzer = ApplicationSerializer(application)
        return Response(serialzer.data, status=201)

    @action(detail=True, methods=["GET"], permission_classes=[CanPostJob])
    def applicants(self, request, pk=None):
        job = self.get_object()
        user = request.user

        if user.id == job.posted_by.id:

            applicants = Application.objects.filter(listing=job.id)

            if applicants:
                seralizer = ApplicationSerializer(applicants, many=True)
                return Response(seralizer.data, status=200)
            return Response({"message": "No applications found"}, status=404)

        return Response({"error": "Unauthorized access"}, status=403)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.action in ["delete", "update"]:
            raise PermissionDenied(
                detail="You don't have permission to delete or update and application."
            )
        if self.action == "create":
            permission_classes = [CanApplyForJob]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["GET"], permission_classes=[CanApplyForJob])
    def applications(self, request):
        applicant = request.user
        applications = Application.objects.filter(applicant=applicant)

        if applications:
            serializer = self.get_serializer(applications, many=True)
            return Response(serializer.data, status=200)
        return Response({"message": "No Applications Found"}, status=404)


class LogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = OutstandingToken.objects.get(token=refresh_token)
                BlacklistedToken.objects.create(token=token)
                return Response({"message": "Successfully logged out."}, status=200)
            except OutstandingToken.DoesNotExist:
                return Response({"message": "Invalid token."}, status=400)

        return Response({"message": "Refresh token required."}, status=400)
