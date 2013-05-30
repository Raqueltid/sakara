# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django import forms
from django.contrib import messages
from sakara.common.models import Clientes, Servicios
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

class ServiciosForm(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        super(ServiciosForm, self).__init__(*args, **kwargs)
        self.fields['padre'] = forms.ChoiceField(
            label="prefix",
            required=False,
            choices=choices,
        )
        self.fields['servicio'] = forms.CharField(
            label="Servicio",
            required=True,
            widget=forms.TextInput(attrs={'placeholder': "Servicio", 'autocomplete': 'off'})
        )
        self.fields['descripcion'] = forms.CharField(
            label="Descripcion",
            required=False,
            widget=forms.Textarea(attrs={'placeholder': 'Descripcion del Servicio', 'cols': 50, 'rows': 10})
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


class CatalogoView(TemplateView):
    template_name = "catalogo.html"
    nivel = None
    catalogo = []

    def __init__(self):
        self.catalogo = []
        self.catalogo.append(('0', 'Sin categoría'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CatalogoView, self).dispatch(*args, **kwargs)

    def arbol_servicios(self, padre):
        result = Servicios.objects.filter(padre=padre)

        for key in result:
            self.nivel = key.__getattribute__('nivel')
            niv = ''
            for num in range(0, self.nivel):
                niv += '--'
            # Lista de tuplas para el combo de servicios
            self.catalogo.append((key.__getattribute__('id'), niv + key.__getattribute__('nombre')))
            # Llamada recursiva
            self.arbol_servicios(key.__getattribute__('id'))

    def get_context_data(self, **kwargs):
        context = super(CatalogoView, self).get_context_data(**kwargs)
        self.arbol_servicios(0)
        # Save in session categorias
        self.request.session['catalogo'] = self.catalogo
        context["form"] = ServiciosForm(choices=self.catalogo)
        return context

    def post(self, request):
        v = {}
        self.arbol_servicios(0)
        form = v["form"] = ServiciosForm(data=request.POST, choices=self.catalogo)
        if form.is_valid():
            if request.POST['padre'] == '0':
                nivel = 0
            else:
                padre_info = Servicios.objects.get(id=request.POST['padre'])
                nivel = padre_info.nivel+1
            serv = Servicios(
                padre=request.POST['padre'],
                nivel=nivel,
                nombre=request.POST['servicio'],
                descripcion=request.POST['descripcion']
            )
            serv.save()
            messages.success(request, "Servicio añadido correctamente!")
            return HttpResponseRedirect('')
        else:
            messages.error(request, "No se ha podido añadir el servicio.")

        return self.render_to_response(v)
