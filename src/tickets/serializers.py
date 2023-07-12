from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ["id", "title", "text", "visibility", "status", "user", "manager"]
        read_only_fields = ["visibility", "manager"]


class TicketTakeSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def validate_manager_id(self, manager_id):
        return manager_id

    def assign(self, ticket: Ticket) -> Ticket:
        manager_id = self.validated_data["manager_id"]
        tickets_count = Ticket.objects.filter(manager_id=manager_id).count()
        if tickets_count >= 10:
            raise ValidationError(
                {"error": "A manager can be assigned to 10 tickets maximum"}
            )

        ticket.manager_id = self.validated_data["manager_id"]
        ticket.save()

        return ticket
