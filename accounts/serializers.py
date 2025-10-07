from rest_framework import serializers
from .models import Organizer
from django.contrib.auth.password_validation import validate_password

class OrganizerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Organizer
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = Organizer.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
