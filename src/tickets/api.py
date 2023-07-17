from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated

from tickets.models import Ticket, Message

from tickets.permissions import (
    CanTakeTicket,
    IsOwner,
    RoleIsAdmin,
    RoleIsManager,
    RoleIsUser,
)
from tickets.serializers import (
    TicketAssignSerializer,
    TicketSerializer,
    TicketTakeSerializer, MessageSerializer,
)
from users.constants import Role


User = get_user_model()


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        all_tickets = Ticket.objects.all()

        if user.role == Role.ADMIN:
            return all_tickets
        elif user.role == Role.MANAGER:
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        else:
            # User's role fallback solution
            return all_tickets.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "destroy":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "take":
            permission_classes = [CanTakeTicket]
        elif self.action == "assign":
            permission_classes = [RoleIsAdmin]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["put"])
    def take(self, request, pk):
        ticket = self.get_object()

        serializer = TicketTakeSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.take(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def assign(self, request, pk):
        ticket = self.get_object()
        new_manager_id = request.data.get("manager_id")

        serializer = TicketAssignSerializer(data={"manager_id": new_manager_id})
        if serializer.is_valid(raise_exception=True):
            ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        ticket_id = self.kwargs[self.lookup_field]
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if not (ticket.user == self.request.user or (
                self.request.user.role in [Role.MANAGER, Role.ADMIN] and ticket.manager == self.request.user)):
            raise exceptions.PermissionDenied(
                "Only the owner, the assigned manager or an admin can view messages for this ticket.")

        return ticket.messages.all()

    def post(self, request, ticket_id: int):
        ticket = self.get_object()

        if request.user.role == Role.ADMIN:
            raise exceptions.PermissionDenied("Admins are not allowed to create messages.")

        payload = {
            "text": request.data["text"],
            "ticket": ticket.id,
        }
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
