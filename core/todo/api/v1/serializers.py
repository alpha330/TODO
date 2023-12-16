from rest_framework import serializers
from todo.models import TaskTodo
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskTodoSerializer(serializers.ModelSerializer):
    """_summary_
    Tasktodo serializer as modelserializer to get model from app Tasktodo class
    andr serialize values in table to learn views in api app
    """

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskTodo
        fields = [
            "id",
            "user",
            "title",
            "snippet",
            "complete",
            "relative_url",
            "absolute_url",
            "createdOn",
            "updatedOn",
        ]
        read_only_fields = ["id", "user"]

    def get_absolute_url(self, obj):
        """_summary_
        definition to build absolute Url from object with PK
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def create(self, validated_data):
        """_summary_
        to create Task by Api this def get requested data as validated_data
        and filter with logged in user to get permission to create task
        """
        user = self.context["request"].user
        validated_data["user"] = user

        task = TaskTodo.objects.create(**validated_data)
        return task

    def update(self, instance, validate_date):
        """_summary_

        update def in model serializer to update task attributes with instance and validated_data requested
        """
        return super().update(instance, validate_date)
