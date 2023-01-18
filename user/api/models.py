from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.state import token_backend
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        #refresh = self.get_token(self.user)

        # Add extra responses here
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenObtainRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        # add filter query
        user = User.objects.get(pk=user_uid)
        data['username'] = user.username
        data['email'] = user.email
        #data.update({'': 'custom_data'})
        return data

class MyTokenObtainRefreshView(TokenRefreshView):
    serializer_class = MyTokenObtainRefreshSerializer