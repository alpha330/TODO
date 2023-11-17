from rest_framework import serializers
from accounts.models import Users
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
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
    




class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs