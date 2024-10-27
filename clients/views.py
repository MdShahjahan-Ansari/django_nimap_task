from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer  # type: ignore
from django.contrib.auth.models import User
from django.http import HttpResponse


# List all clients and create a new client
def home(request):
    return HttpResponse("home")


@api_view(['GET', 'POST'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        client = Client(client_name=data['client_name'], created_by=request.user)
        client.save()
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Retrieve, update, or delete a client
@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        client.client_name = data['client_name']
        client.save()
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_project(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data
    project = Project(project_name=data['project_name'], client=client, created_by=request.user)
    project.save()

    users = User.objects.filter(id__in=[user['id'] for user in data['users']])
    project.users.set(users)
    project.save()

    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def user_projects(request):
    projects = request.user.projects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ClientCreateView(APIView):
    permission_classes = [IsAuthenticated]


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer


class ClientCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = ClientSerializer(data=request.data)


        if serializer.is_valid():
            client = serializer.save(created_by=request.user)
            response_data = {
                'id': client.id,
                'client_name': client.client_name,
                'created_at': client.created_at,
                'created_by': client.created_by.username,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)