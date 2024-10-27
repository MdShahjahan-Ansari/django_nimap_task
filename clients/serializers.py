from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User
from django.utils import timezone
import pytz


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    created_by_name = serializers.SerializerMethodField()
    created_at_ist = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_at_ist', 'created_by', 'created_by_name']

    def get_created_by_name(self, obj):

        return obj.created_by.username

    def get_created_at_ist(self, obj):

        ist = pytz.timezone('Asia/Kolkata')
        return obj.created_at.astimezone(ist).isoformat()


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'created_by_name', 'projects', 'updated_at']

    def get_created_by_name(self, obj):

        return obj.created_by.username
