from django.contrib.auth import get_user_model
from rest_framework import serializers

from tickets.models import Message, Ticket
from users.constants import Role

User = get_user_model()


class BaseTicketSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def validate_manager_tickets_limit(self, manager_id):
        has_ten_tickets = (
            Ticket.objects.filter(manager_id=manager_id)[:10].count() == 10
        )
        if has_ten_tickets:
            raise serializers.ValidationError(
                {"error": "A manager can be assigned to 10 tickets maximum"}
            )
        return manager_id


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ["id", "title", "text", "visibility", "status", "user", "manager"]
        read_only_fields = ["visibility", "manager"]


class TicketTakeSerializer(BaseTicketSerializer):
    manager_id = serializers.IntegerField()

    def take(self, ticket: Ticket) -> Ticket:
        manager_id = self.validated_data["manager_id"]
        self.validate_manager_tickets_limit(manager_id)

        ticket.manager_id = manager_id
        ticket.save()

        return ticket


class TicketAssignSerializer(BaseTicketSerializer):
    manager_id = serializers.IntegerField(required=True)

    def validate_manager_id(self, manager_id):
        user = User.objects.filter(id=manager_id).first()

        if not user:
            raise serializers.ValidationError(
                {"error": "User with given id does not exist"}
            )

        if user.role != Role.MANAGER:
            raise serializers.ValidationError({"error": "The user is not a manager"})

        return manager_id

    def assign(self, ticket: Ticket) -> Ticket:
        manager_id = self.validated_data["manager_id"]
        self.validate_manager_tickets_limit(manager_id)

        ticket.manager_id = manager_id
        ticket.save()

        return ticket


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "timestamp"]
