from rest_framework import permissions

class PatientApprovePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_superuser)

class isDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor
    
class ispatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient