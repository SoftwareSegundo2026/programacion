from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Tarea


DESIGN_SYSTEM_INPUT_ATTRS = {
    'class': 'form-input',
}


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(DESIGN_SYSTEM_INPUT_ATTRS)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'fecha_nacimiento']
        widgets = {
            'bio': forms.Textarea(attrs={
                **DESIGN_SYSTEM_INPUT_ATTRS,
                'class': 'form-input form-textarea',
                'rows': 4,
                'placeholder': 'Contanos sobre vos...',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                **DESIGN_SYSTEM_INPUT_ATTRS,
                'type': 'date',
            }),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha', 'prioridad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                **DESIGN_SYSTEM_INPUT_ATTRS,
                'placeholder': 'Nombre de la tarea',
            }),
            'descripcion': forms.Textarea(attrs={
                **DESIGN_SYSTEM_INPUT_ATTRS,
                'class': 'form-input form-textarea',
                'rows': 4,
                'placeholder': 'Descripcion (opcional)',
            }),
            'fecha': forms.DateInput(
                attrs={
                    **DESIGN_SYSTEM_INPUT_ATTRS,
                    'type': 'date',
                },
                format='%Y-%m-%d',
            ),
            'prioridad': forms.Select(attrs=DESIGN_SYSTEM_INPUT_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['fecha'].initial = date.today()

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < date.today():
            raise forms.ValidationError('No se pueden crear tareas con fechas pasadas.')
        return fecha
