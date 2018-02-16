from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import RegisterForm
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

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




