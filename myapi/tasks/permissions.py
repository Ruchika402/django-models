from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.craeted_by == request.user

class IsAssignedOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.craeted_by == request.user or obj.assigned_to == request.user
        