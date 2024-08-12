from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorMessageSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    error = ErrorSerializer()


class MessageResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = MessageSerializer()
