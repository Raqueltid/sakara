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
from sakara.jquery_validate import JqueryForm
from sakara.common.constants import *

import datetime


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


class ClientesForm(JqueryForm):

    nombres = forms.CharField(
        max_length=50,
        error_messages={
            'required': "Campo obligatorio.",
            'max_length': u"La longitud m\u00E1xima permitida es de 50 car\u00E1cteres.",
        },
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
    )

    apellidos = forms.CharField(
        max_length=100,
        error_messages={
            'required': "Campo obligatorio.",
            'max_length': u"La longitud m\u00E1xima permitida es de 100 car\u00E1cteres."
        },
        widget=forms.TextInput(attrs={'placeholder': 'Apellidos'})
    )

    fecha_nac = forms.DateField(
        input_formats=['%d/%m/%Y'],
        help_text='Formato: %s/%s/%s' % (str(datetime.date.today().day).zfill(2),
                                         str(datetime.date.today().month).zfill(2),
                                         datetime.date.today().year),
        error_messages={
            'required': "Campo obligatorio",
            'invalid': u"El formato no es v\u00E1lido."
        },
        widget=forms.DateInput(attrs={'placeholder': 'Fecha de nacimiento', 'autocomplete': 'off'})
    )

    direccion = forms.CharField(
        max_length=100,
        required=False,
        error_messages={
            'max_length': u"La longitud m\u00E1xima permitida es de 100 car\u00E1cteres."
        },
        widget=forms.TextInput(attrs={'placeholder': 'Dirección'})
    )

    email = forms.EmailField(
        required=False,
        error_messages={
            'invalid': "Email invalido."
        },
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )

    telefono = forms.RegexField(
        required=False,
        max_length=9,
        regex=CONST_PHONENUMBER,
        error_messages={
            'max_length': u"La longitud m\u00E1xima permitida es de 9 car\u00E1cteres.",
            'regex_pattern': u"El valor introducido no se corresponde a un tel\u00E9fono"
        },
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'})
    )

    movil = forms.RegexField(
        required=False,
        max_length=9,
        regex=CONST_PHONENUMBER,
        error_messages={
            'max_length': u"La longitud m\u00E1xima permitida es de 9 car\u00E1cteres.",
            'regex_pattern': u"El valor introducido no se corresponde a un tel\u00E9fono"
        },
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono Móvil'})
    )

    fecha_alta = forms.DateField(
        input_formats=['%d/%m/%Y'],
        help_text='Formato: %s/%s/%s' % (str(datetime.date.today().day).zfill(2),
                                         str(datetime.date.today().month).zfill(2),
                                         datetime.date.today().year),
        error_messages={
            'required': "Campo obligatorio",
            'invalid': u"El formato no es v\u00E1lido."
        },
        widget=forms.DateInput(attrs={'placeholder': 'Fecha de alta', 'autocomplete': 'off'})
    )

    observaciones = forms.CharField(
        max_length=200,
        required=False,
        error_messages={
            'max_length': u'La longitud m\u00E1xima permitida es de 200 car\u00E1cteres.'
        },
        widget=forms.Textarea(attrs={'placeholder': 'Observaciones', 'cols': 50, 'rows': 10})
    )

    class Meta:
        model = Clientes


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
                    return HttpResponseRedirect(CONST_URL_HOME)
                else:
                    messages.error(request, "Usuario no activo, contacta con el administrador.")
            else:
                messages.error(request, "Tu usuario/password es incorrecto")
        else:
            messages.error(request, 'Tu usuario/password es incorrecto')
        return self.render_to_response(v)


class AddClientView(TemplateView):
    template_name = "add_client.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddClientView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddClientView, self).get_context_data(**kwargs)
        context["form"] = ClientesForm()
        return context

    def post(self, request):
        v = {}
        form = v["form"] = ClientesForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, u"Cliente a\u00F1adido correctamente!")
            return HttpResponseRedirect('')
        else:
            messages.error(request, u"No se ha podido a\u00F1adir el Cliente.")
        return self.render_to_response(v)


class HomeView(TemplateView):
    template_name = "home.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        return context
