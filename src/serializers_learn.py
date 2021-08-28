from rest_framework import serializers
from datetime import date


class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    birthdate = serializers.DateField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        delta = date.today() - obj.birthdate
        return int(delta.days / 365)

    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("The birthdate must be is date before today.")
        return value

    def validate(self, data):
        if not data['first_name'] and not data['last_name']:
            raise serializers.ValidationError("You must inform either the first name or last name.")
        return data