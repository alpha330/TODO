from rest_framework import serializers
from accounts.models import Users

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["email","password"]
    def validate(self,attrs):
        return super().validate(attrs)
    def create(self,validated_data):
        return super().create(validated_data)