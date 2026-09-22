from django import forms


def mask(value: str) -> str:
    if not value:
        return ''

    if len(value) <= 8:
        return '*' * 8

    return value[:4] + '*' * 8 + value[-4:]


class SSOConfigForm(forms.ModelForm):
    """Form for any UserDefinedSSOConfig subclass"""
    secret_fields = ('secret',)

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.secret_fields:
            if name not in self.fields:
                continue

            field = self.fields[name]
            field.widget = forms.PasswordInput(render_value=False)

            if self.instance.pk:
                masked_name = mask(getattr(self.instance, name))
                field.required = False
                field.help_text = f'Currently {masked_name}. Leave blank to keep it.'

    def clean(self):
        cleaned_data = super().clean()

        if not self.instance.pk:
            return cleaned_data

        # A blank secret on an existing config means unchanged, not empty
        for name in self.secret_fields:
            if name in self.fields and not cleaned_data.get(name):
                cleaned_data[name] = getattr(self.instance, name)

        return cleaned_data
