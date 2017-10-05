# -*- coding: utf-8
from django import forms

import magic
import tempfile


# Create the form class.
class AddSaleForm(forms.Form):
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    patronym = forms.CharField(max_length=30)
    delivery_type = forms.ChoiceField(choices=(
    ('none', 'none'), (u'Самовывозом', u'Самовывозом'), (u'Железной дорогой', u'Железной дорогой'),
    (u'Автотранспортом', u'Автотранспортом')))
    station = forms.CharField(max_length=30, required=False)
    address = forms.CharField(max_length=100, widget=forms.Textarea, required=False)
    message = forms.CharField(max_length=200, widget=forms.Textarea, required=False)
    document1 = forms.FileField(required=False)
    document2 = forms.FileField(required=False)
    is_accepted = forms.BooleanField(required=True)

    def clean_is_accepted(self, value):
        if not value:
            raise forms.ValidationError(u'Необходимо дать согласие на обработку персональных данных.')
        else:
            return value

    def clean(self):
        cleaned_data = super(AddSaleForm, self).clean()
        if 'delivery_type' in cleaned_data and cleaned_data['delivery_type'] != 'none':
            if cleaned_data['delivery_type'] == u'Железной дорогой' and not cleaned_data['station']:
                raise forms.ValidationError(u'Укажите станцию')
            elif cleaned_data['delivery_type'] == u'Автотранспортом' and not cleaned_data['address']:
                raise forms.ValidationError(u'Укажите адрес')
        else:
            raise forms.ValidationError(u'Укажите способ доставки')

        cleaned_files = []
        for key in cleaned_data:
            if key.find('document') != -1 and cleaned_data[key]:
                cleaned_files.append(cleaned_data[key])

        VALID_MIME_TYPES = {
            'application/pdf': 1,
            'image/jpeg': 1,
            'image/png': 1,
            'application/msword': 1,
            'application/zip': 1
        }

        for document in cleaned_files:
            with tempfile.TemporaryFile(mode='wb+') as fp:
                for chunk in document.chunks():
                    fp.write(chunk)
                fp.seek(0)
                file_mime_type = magic.from_buffer(fp.read(), mime=True)
            if document.name[-3:] == 'doc' or document.name[-4:] == 'docx':
                file_mime_type = 'application/msword'
            if not (file_mime_type in VALID_MIME_TYPES):
                raise forms.ValidationError(u'Допустимые форматы файлов: pdf, doc, docx, zip, jpg, png.')
            if document.size > 2097152:
                raise forms.ValidationError(u'Максимальный размер файла: 2МБ.')


class AddContactsForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=200, widget=forms.Textarea, required=False)
    is_accepted = forms.BooleanField(required=True)

    def clean_is_accepted(self, value):
        if not value:
            raise forms.ValidationError(u'Необходимо дать согласие на обработку персональных данных.')
        else:
            return value


class AddPurchasesForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    patronym = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField()
    city = forms.CharField(max_length=30, required=False)
    amount = forms.CharField(max_length=30, required=False)
    category_2A = forms.BooleanField(required=False)
    category_3A = forms.BooleanField(required=False)
    category_3Arails = forms.BooleanField(required=False)
    category_5A = forms.BooleanField(required=False)
    category_5Arails = forms.BooleanField(required=False)
    category_26A = forms.BooleanField(required=False)
    category_6A = forms.BooleanField(required=False)
    deliverable = forms.ChoiceField(choices=(
    ('none', 'none'), (u'Могу доставить', u'Могу доставить'), (u'Не могу доставить', u'Не могу доставить')),
                                    required=False)
    delivery_type = forms.ChoiceField(choices=(
    ('none', 'none'), (u'Автотранспортом', u'Автотранспортом'), (u'Железной дорогой', u'Железной дорогой')),
                                      required=False)
    message = forms.CharField(max_length=200, widget=forms.Textarea, required=False)
    document1 = forms.FileField(required=False)
    document2 = forms.FileField(required=False)
    is_accepted = forms.BooleanField(required=True)

    def clean_is_accepted(self, value):
        if not value:
            raise forms.ValidationError(u'Необходимо дать согласие на обработку персональных данных.')
        else:
            return value

    def clean(self):
        cleaned_data = super(AddPurchasesForm, self).clean()

        cleaned_files = []
        for key in cleaned_data:
            if key.find('document') != -1 and cleaned_data[key]:
                cleaned_files.append(cleaned_data[key])

        VALID_MIME_TYPES = {
            'application/pdf': 1,
            'image/jpeg': 1,
            'image/png': 1,
            'application/msword': 1,
            'application/zip': 1,
            'video/mp4': 1,
            'video/3gpp': 1,
            'video/avi': 1,
            'video/x-flv': 1,
            'video/ogg': 1
        }

        for document in cleaned_files:
            with tempfile.TemporaryFile(mode='wb+') as fp:
                for chunk in document.chunks():
                    fp.write(chunk)
                fp.seek(0)
                file_mime_type = magic.from_buffer(fp.read(), mime=True)
            if document.name[-3:] == 'doc' or document.name[-4:] == 'docx':
                file_mime_type = 'application/msword'
            if not (file_mime_type in VALID_MIME_TYPES):
                raise forms.ValidationError(
                    u'Допустимые форматы файлов: pdf, doc, docx, zip, jpg, png, mp4, 3gp, avi, flv, ogg.')
            if document.size > 10485760:
                raise forms.ValidationError(u'Максимальный размер файла: 10МБ.')


class AddVacanciesForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    patronym = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField()
    city = forms.CharField(max_length=30, required=False)
    street = forms.CharField(max_length=30, required=False)
    vacancie = forms.CharField(max_length=100)
    message = forms.CharField(max_length=200, widget=forms.Textarea, required=False)
    document1 = forms.FileField(required=False)
    document2 = forms.FileField(required=False)
    is_accepted = forms.BooleanField(required=True)

    def clean_is_accepted(self, value):
        if not value:
            raise forms.ValidationError(u'Необходимо дать согласие на обработку персональных данных.')
        else:
            return value

    def clean(self):
        cleaned_data = super(AddVacanciesForm, self).clean()

        if 'vacancie' in cleaned_data and cleaned_data['vacancie'] == 'none':
            raise forms.ValidationError(u'Укажите вакансию')

        cleaned_files = []
        for key in cleaned_data:
            if key.find('document') != -1 and cleaned_data[key]:
                cleaned_files.append(cleaned_data[key])

        VALID_MIME_TYPES = {
            'application/pdf': 1,
            'image/jpeg': 1,
            'image/png': 1,
            'application/msword': 1,
            'application/zip': 1
        }

        for document in cleaned_files:
            with tempfile.TemporaryFile(mode='wb+') as fp:
                for chunk in document.chunks():
                    fp.write(chunk)
                fp.seek(0)
                file_mime_type = magic.from_buffer(fp.read(), mime=True)
            if document.name[-3:] == 'doc' or document.name[-4:] == 'docx':
                file_mime_type = 'application/msword'
            if not (file_mime_type in VALID_MIME_TYPES):
                raise forms.ValidationError(u'Допустимые форматы файлов: pdf, doc, docx, zip, jpg, png.')
            if document.size > 2097152:
                raise forms.ValidationError(u'Максимальный размер файла: 2МБ.')