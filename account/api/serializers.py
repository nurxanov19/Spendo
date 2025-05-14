

from rest_framework import serializers


from account.models import OneTimePasswordModel, CustomUser
import random
from .helper import run_thread, sent_to_email, send_sms_to_user
import re


class AuthOneSerializers(serializers.Serializer):

    identifier = serializers.CharField(max_length=200)

    def validate_identifier(self, value):
        for_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for_phone = r"^[+]{1}(?:[0-9\\-\\(\\)\\/" \
                    "\\.]\\s?){6,15}[0-9]{1}$"

        if re.match(for_email, value):
            self.is_email = True
        elif re.match(for_phone, value):
            self.is_email = False
        else:
            raise serializers.ValidationError("Invalid phone or email format.")

        return value

    # def validate_phone(self, phone):
    #     if len(str(phone)) != 12 or not phone.isdigit() \
    #         or str(phone)[:3] != '998':
    #         raise serializers.ValidationError('Phone is invalid (serializer)')
    #     return phone


class AuthTwoSerializer(serializers.Serializer):

    key = serializers.CharField(max_length=300)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        key = attrs.get('key')
        code = attrs.get('code')

        if not key or not code:
            raise serializers.ValidationError('Key or code missing (serializer)')

        if len(code) != 6 or not code.isdigit():
            raise serializers.ValidationError("Code must be a 6-digit number.")

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        read_only_fields = ['username']