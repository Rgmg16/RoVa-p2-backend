from rest_framework import generics, status, serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import login, logout as auth_logout, authenticate, get_user_model
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Volunteer
from .serializers import UserSerializer, UserUpdateSerializer, VolunteerSerializer, UserProfileSerializer
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user


    def create(self, request, *args, **kwargs):
        logger.debug("Received data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            logger.error("Validation error: %s", e.detail)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {
            'username': user.username,
            'email': user.email,
            'name': user.name,
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

User = get_user_model()

@csrf_protect
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]   

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.context['request'] = self.request
        serializer.save()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Update request data: {request.data}")
        response = super().update(request, *args, **kwargs)
        logger.info(f"Response data: {response.data}")
        return response

class AuthStatusView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'status': 'Authenticated'}, status=status.HTTP_200_OK)
        return Response({'status': 'Not authenticated'}, status=status.HTTP_200_OK)

class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})
    
class VolunteerCreateView(generics.CreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        # Link the volunteer to the authenticated user
        serializer.save(user=self.request.user)

class VolunteerListView(generics.ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter based on user if needed
        return Volunteer.objects.all()

class VolunteerDetailView(generics.RetrieveUpdateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Volunteer.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.context['request'] = self.request
        serializer.save()
    


   
