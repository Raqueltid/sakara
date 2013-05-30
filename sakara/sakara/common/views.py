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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict

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
    def __init__(self, client=None, *args, **kwargs):
        self.base_fields['nombres'] = forms.CharField(
            max_length=50,
            initial=client["nombres"] if "nombres" in client and client["nombres"] else '',
            error_messages={
                'required': "Campo obligatorio.",
                'max_length': u"La longitud m\u00E1xima permitida es de 50 car\u00E1cteres.",
            },
            widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
        )

        self.base_fields['apellidos'] = forms.CharField(
            max_length=100,
            initial=client["apellidos"] if "apellidos" in client and client["apellidos"] else '',
            error_messages={
                'required': "Campo obligatorio.",
                'max_length': u"La longitud m\u00E1xima permitida es de 100 car\u00E1cteres."
            },
            widget=forms.TextInput(attrs={'placeholder': 'Apellidos'})
        )

        if "fecha_nac" in client and type(client["fecha_nac"]) is datetime.date:
            valid_datetime = datetime.datetime.strftime(client["fecha_nac"], '%d/%m/%Y')
        else:
            valid_datetime = client["fecha_nac"] if "fecha_nac" in client and client["fecha_nac"] else ''

        self.base_fields['fecha_nac'] = forms.DateField(
            input_formats=['%d/%m/%Y'],
            help_text='Formato: %s/%s/%s' % (str(datetime.date.today().day).zfill(2),
                                             str(datetime.date.today().month).zfill(2),
                                             datetime.date.today().year),
            initial=valid_datetime,
            error_messages={
                'required': "Campo obligatorio",
                'invalid': u"El formato no es v\u00E1lido."
            },
            widget=forms.DateInput(attrs={'placeholder': 'Fecha de nacimiento', 'autocomplete': 'off'})
        )

        self.base_fields['direccion'] = forms.CharField(
            max_length=100,
            required=False,
            initial=client["direccion"] if "direccion" in client and client["direccion"] else '',
            error_messages={
                'max_length': u"La longitud m\u00E1xima permitida es de 100 car\u00E1cteres."
            },
            widget=forms.TextInput(attrs={'placeholder': 'Dirección'})
        )

        self.base_fields['email'] = forms.EmailField(
            required=False,
            initial=client["email"] if "email" in client and client["email"] else '',
            error_messages={
                'invalid': "Email invalido."
            },
            widget=forms.TextInput(attrs={'placeholder': 'Email'})
        )

        self.base_fields['telefono'] = forms.RegexField(
            required=False,
            max_length=9,
            regex=CONST_PHONENUMBER,
            initial=client["telefono"] if "telefono" in client and client["telefono"] else '',
            error_messages={
                'max_length': u"La longitud m\u00E1xima permitida es de 9 car\u00E1cteres.",
                'regex_pattern': u"El valor introducido no se corresponde a un tel\u00E9fono"
            },
            widget=forms.TextInput(attrs={'placeholder': 'Teléfono'})
        )

        self.base_fields['movil'] = forms.RegexField(
            required=False,
            max_length=9,
            regex=CONST_PHONENUMBER,
            initial=client["movil"] if "movil" in client and client["movil"] else '',
            error_messages={
                'max_length': u"La longitud m\u00E1xima permitida es de 9 car\u00E1cteres.",
                'regex_pattern': u"El valor introducido no se corresponde a un tel\u00E9fono"
            },
            widget=forms.TextInput(attrs={'placeholder': 'Teléfono Móvil'})
        )

        if "fecha_alta" in client and type(client["fecha_alta"]) is datetime.date:
            valid_datetime = datetime.datetime.strftime(client["fecha_alta"], '%d/%m/%Y')
        else:
            valid_datetime = client["fecha_alta"] if "fecha_alta" in client and client["fecha_alta"] else ''

        self.base_fields['fecha_alta'] = forms.DateField(
            input_formats=['%d/%m/%Y'],
            help_text='Formato: %s/%s/%s' % (str(datetime.date.today().day).zfill(2),
                                             str(datetime.date.today().month).zfill(2),
                                             datetime.date.today().year),
            initial=valid_datetime,
            error_messages={
                'required': "Campo obligatorio",
                'invalid': u"El formato no es v\u00E1lido."
            },
            widget=forms.DateInput(attrs={'placeholder': 'Fecha de alta', 'autocomplete': 'off'})
        )

        self.base_fields['observaciones'] = forms.CharField(
            max_length=200,
            required=False,
            initial=client["observaciones"] if "observaciones" in client and client["observaciones"] else '',
            error_messages={
                'max_length': u'La longitud m\u00E1xima permitida es de 200 car\u00E1cteres.'
            },
            widget=forms.Textarea(attrs={'placeholder': 'Observaciones', 'cols': 50, 'rows': 10})
        )
        super(ClientesForm, self).__init__(*args, **kwargs)

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


class ClientView(TemplateView):
    template_name = "client.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClientView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        c = Clientes.objects.all().order_by('nombres')
        client_list = list()
        for e in c:
            txt = dict({"id": e.id, "full_name": e.full_name, "birthdate": e.fecha_nac, "date": e.fecha_alta})
            client_list.append(txt)

        paginator = Paginator(client_list, 3)  # Show 25 contacts per page

        page = self.request.GET.get('page')
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            clients = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            clients = paginator.page(paginator.num_pages)
        context["clients"] = clients

        return context


class AddClientView(TemplateView):
    template_name = "client_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddClientView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddClientView, self).get_context_data(**kwargs)
        if "id" in context["params"]:
            item = Clientes.objects.get(id=context["params"]["id"])
            context["form"] = ClientesForm(client=model_to_dict(item, fields=[], exclude=[]))
        else:
            item = Clientes.objects._copy_to_model(Clientes)
            context["form"] = ClientesForm(client={})

        return context

    def post(self, request, id=None):
        v = {}
        if id is not None:
            client = Clientes.objects.get(id=id)
        form = v["form"] = ClientesForm(data=request.POST, client=request.POST)

        if form.is_valid():
            if id is not None:
                client.copy_model_instance(form.instance, id)
                client.save()
                messages.success(request, u"Cliente guardado correctamente!")
            else:
                form.save()
                messages.success(request, u"Cliente a\u00F1adido correctamente!")
            return HttpResponseRedirect('')
        else:
            if id is not None:
                messages.error(request, u"No se ha podido guardar el Cliente.")
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
