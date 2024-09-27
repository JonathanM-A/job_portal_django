from rest_framework.permissions import BasePermission

class CanPostJob(BasePermission):
    """
    Custom permission to allow only Employers to post jobs
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm("api.post_a_job")
    

class CanApplyForJob(BasePermission):
    """
    Custom permission to allow only JobSeekers to apply for jobs
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm("api.apply_for_job")
    