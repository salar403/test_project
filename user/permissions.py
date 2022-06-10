from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request,"customer",None)
        if not user:
            raise NotAuthenticated()
        return True

class IsAuthenticatedLeader(BasePermission):
    def has_permission(self, request, view):
        leader = getattr(request,"leader",None)
        if not leader:
            raise NotAuthenticated()
        return True
