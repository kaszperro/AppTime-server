from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .forms import RegisterForm
from django.http import JsonResponse
from django.template.loader import render_to_string

def register_json(request):
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
