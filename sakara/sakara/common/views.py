from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django import forms
from django.contrib import messages


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        required=True,
        error_messages={
            "invalid": "Usuario invalido",
            "required": "El campo 'Usuario' es obligatorio"
        },
        widget=forms.TextInput(attrs={'placeholder': "Introduce nombre de usuario", 'autocomplete': 'off'})
    )

    password = forms.CharField(
        label="password",
        required=True,
        error_messages={
            "invalid": "Contrasea invalida",
            "required": "El campo 'contrasea' es obligatorio",
        },
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce la contrasea', 'autocomplete': 'off'})
    )


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context

    def post(self, request):
        v = {}
        form = v["form"] = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/consulta/')
                else:
                    messages.error(request, "Usuario no activo, contacta con el administrador.")
            else:
                messages.error(request, "Tu usuario/password es incorrecto")
        else:
            messages.error(request, 'Tu usuario/password es incorrecto')
        return self.render_to_response(v)


class ConsultaView(TemplateView):
    template_name = "consulta.html"

    def get_context_data(self, **kwargs):
        context = {}
        return context
