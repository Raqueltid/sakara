# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django import forms
from django.contrib import messages
from sakara.common.models import Clientes
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
            "invalid": "Contraseña invalida",
            "required": "El campo 'contraseña' es obligatorio",
        },
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce la contraseña', 'autocomplete': 'off'})
    )


class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        # Nota: Eliminando el atributo 'fields' anade por defecto todos los elemetnos
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            #TODO: Fecha de nacimiento con calendario // Por ahora acepta formato %m/%d%/%Y
            'fecha_nac': forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'Fecha'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Observaciones', 'cols': 50, 'rows': 10}),
        }


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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultaView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsultaView, self).get_context_data(**kwargs)
        context["form"] = ClientesForm()
        return context

    def post(self, request):
        v = {}
        form = v["form"] = ClientesForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Cliente anyadido correctamente!")
            return HttpResponseRedirect('')
        else:
            messages.error(request, "No se ha podido anyadir el Cliente.")
        return self.render_to_response(v)
