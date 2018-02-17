from datetime import datetime
from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import RegisterForm
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import (
    VerifyJSONWebTokenSerializer,
    JSONWebTokenSerializer
)
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework import status

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class JSONWebTokenAPIView(APIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True,
                                    secure=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer



@api_view(['POST'])
def validate_token(request):
    data = {'token': request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)}
    print(data)
    # return JsonResponse(data)
    valid_data = VerifyJSONWebTokenSerializer().validate(data)
    print(valid_data)
    return JsonResponse(data)


def register_html(request):
    data = dict()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = RegisterForm()

    context = {'form': form}
    data['html_form'] = render_to_string(
        'accounts/snippets/form.html',
        context,
        request=request
    )
    return JsonResponse(data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    data = dict()
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    data['form_errors'] = form.errors

    return JsonResponse(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': request.user.name,
        'status': 'request was permitted'
    }
    return Response(content)



