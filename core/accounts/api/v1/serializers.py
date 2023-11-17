from rest_framework import serializers
from accounts.models import Users
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
class RegistrationSerializer(serializers.ModelSerializer):
    password_1= serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model = Users
        fields = ["email","password","password_1"]
    def validate(self,attrs):
        if attrs.get("password") != attrs.get("password_1"):
            raise serializers.ValidationError({"detail":"Password dose not match"})
        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password":e.messages})
            
        return super().validate(attrs)
    def create(self,validated_data):
        validated_data.pop("password_1")
        return Users.objects.create_user(**validated_data)