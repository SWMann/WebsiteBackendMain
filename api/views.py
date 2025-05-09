from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class HomeAPIView(APIView):
    """
    A simple API view to demonstrate the API is working.
    This endpoint is publicly accessible.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'message': 'Welcome to the Community Platform API!',
            'status': 'online',
            'version': '0.1.0',
        })