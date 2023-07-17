from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from tickets.models import Ticket, Message
from users.constants import Role


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.MANAGER


class RoleIsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.USER


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Ticket):
        return obj.user == request.user


class CanTakeTicket(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.MANAGER

    def has_object_permission(self, request, view, obj: Ticket):
        if obj.manager is not None:
            raise exceptions.PermissionDenied("Manager is already specified")
        return True
