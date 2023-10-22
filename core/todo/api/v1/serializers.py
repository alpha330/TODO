from rest_framework import serializers
from todo.models import TaskTodo
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskTodoSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url",read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = TaskTodo
        fields = ["id","user","title","snippet","complete","relative_url","absolute_url","createdOn","updatedOn"]
        read_only_fields = ["title","user"]
        
    def get_absolute_url(self,obj):
        request= self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    def create(self, validate_date):
        validate_date["author"]=User.objects.get(user__id = self.context.get("request").user.id)
        return super().create(validate_date)
    
    def update(self, instance, validate_date):
        return super().update(instance, validate_date)