from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Tarea


TAILWIND_INPUT_ATTRS = {
    'class': 'w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200',
}


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(TAILWIND_INPUT_ATTRS)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'fecha_nacimiento']
        widgets = {
            'bio': forms.Textarea(attrs={
                **TAILWIND_INPUT_ATTRS,
                'rows': 4,
                'placeholder': 'Contanos sobre vos...',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                **TAILWIND_INPUT_ATTRS,
                'type': 'date',
            }),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha', 'prioridad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                **TAILWIND_INPUT_ATTRS,
                'placeholder': 'Nombre de la tarea',
            }),
            'descripcion': forms.Textarea(attrs={
                **TAILWIND_INPUT_ATTRS,
                'rows': 4,
                'placeholder': 'Descripcion (opcional)',
            }),
            'fecha': forms.DateInput(attrs={
                **TAILWIND_INPUT_ATTRS,
                'type': 'date',
            }),
            'prioridad': forms.Select(attrs=TAILWIND_INPUT_ATTRS),
        }
