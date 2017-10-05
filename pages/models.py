# -*- coding: utf-8

import tempfile
import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from pages.forms import AddSaleForm, AddContactsForm, AddPurchasesForm, AddVacanciesForm
from pages.models import Vacancie, Product, PurchasesPrice

# Create your views here.

RECIPIENT = ['snabservis_llc@mail.ru']


def IndexView(request):
    return render(request, 'pages/index.html', context={}, content_type='text/html')


def SalesView(request):
    products = Product.objects.all()
    categories = []
    categories_check_list = []
    for product in products:
        if not (product.category in categories_check_list):
            categories_check_list.append(product.category)
            category = {
                'name': product.category,
                'products': Product.objects.filter(category=product.category).order_by('-shape')
            }
            categories.append(category)
    titles = []
    for product in products:
        if not (product.title in titles):
            titles.append(product.title)

    if request.method == 'POST':
        form_data = AddSaleForm(request.POST, request.FILES)

        if form_data.is_valid():
            subject = u'Заявка на покупку металлопроката: ' + form_data.cleaned_data['first_name'] + ' ' + \
                      form_data.cleaned_data['patronym'] + ' ' + form_data.cleaned_data['last_name']

            messageHTML = u'<html><head><meta charset="utf-8"></head><body>'
            message = u'Имя: ' + form_data.cleaned_data['first_name'] + '\n'
            messageHTML += u'<p><span style="font-weight:bold">Имя: </span>' + form_data.cleaned_data[
                'first_name'] + u'</p>'
            message += u'Отчество: ' + form_data.cleaned_data['patronym'] + '\n'
            messageHTML += u'<p><span style="font-weight:bold">Отчество: </span>' + form_data.cleaned_data[
                'patronym'] + u'</p>'
            message += u'Фамилия: ' + form_data.cleaned_data['last_name'] + '\n' + '\n'
            messageHTML += u'<p><span style="font-weight:bold">Фамилия: </span>' + form_data.cleaned_data[
                'last_name'] + u'</p><br>'
            message += u'Способ доставки: ' + form_data.cleaned_data['delivery_type'] + '\n'
            messageHTML += u'<p><span style="font-weight:bold">Способ доставки: </span>' + form_data.cleaned_data[
                'delivery_type'] + u'</p>'
            if form_data.cleaned_data['delivery_type'] == u'Железной дорогой':
                message += u'Станция: ' + form_data.cleaned_data['station'] + '\n' + '\n'
                messageHTML += u'<p><span style="font-weight:bold">Станция: </span>' + form_data.cleaned_data[
                    'station'] + u'</p><br>'
            elif form_data.cleaned_data['delivery_type'] == u'Автотранспортом':
                message += u'Адрес: ' + form_data.cleaned_data['address'] + '\n' + '\n'
                messageHTML += u'<p><span style="font-weight:bold">Адрес: </span>' + form_data.cleaned_data[
                    'address'] + u'</p><br>'
            else:
                message += '\n'
                messageHTML += u'<br>'
            if form_data.cleaned_data['message']:
                message += u'Сообщение: ' + form_data.cleaned_data['message'] + '\n' + '\n'
                messageHTML += u'<p><span style="font-weight:bold">Сообщение: </span>' + form_data.cleaned_data[
                    'message'] + u'</p><br>'
            message += u'Выбранные позиции:' + '\n' + '\n'
            i = 0
            for key in request.POST:
                if key.find('amount') != -1:
                    i += 1
                    message += unicode(i) + u'й продукт:' + '\n'
                    selected_product = Product.objects.filter(pk=int(key.split('_')[1])).values()[0]
                    if ('title' in selected_product):
                        message += u'Тип: ' + unicode(selected_product['title']) + '\n'
                    if ('category' in selected_product):
                        message += u'Категория: ' + unicode(selected_product['category']) + '\n'
                    if ('shape' in selected_product) and selected_product['shape']:
                        message += u'Форма: ' + unicode(selected_product['shape']) + '\n'
                    if ('diameter' in selected_product) and selected_product['diameter']:
                        message += u'Диаметр: ' + unicode(selected_product['diameter']) + '\n'
                    if ('length' in selected_product) and selected_product['length']:
                        message += u'Длина: ' + unicode(selected_product['length']) + '\n'
                    if ('price' in selected_product) and selected_product['price']:
                        message += u'Цена: ' + unicode(selected_product['price']) + '\n'
                    message += u'Количество: ' + request.POST[key] + '\n' + '\n'

            messageHTML += request.POST['cart']
            messageHTML += u'</body></html>'

            sender = 'snab-service.com@yandex.ru'
            recipient = RECIPIENT
            email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient)
            email.attach_alternative(messageHTML, 'text/html')

            for document in request.FILES:
                with tempfile.TemporaryFile(mode='wb+') as fp:
                    for chunk in request.FILES[document].chunks():
                        fp.write(chunk)
                    fp.seek(0)
                    email.attach(request.FILES[document].name, fp.read(), request.FILES[document].content_type)

            email.send(fail_silently=False)

            return HttpResponseRedirect('/sales/')
    else:
        form_data = AddSaleForm()

    return render(request, 'pages/services__sale.html',
                  context={'titles': titles, 'categories': categories, 'form': form_data}, content_type='text/html')


def PurchasesView(request):
    form_data = AddPurchasesForm()

    if request.method == 'POST':
        form_data = AddPurchasesForm(request.POST, request.FILES)

        if form_data.is_valid():
            subject = u'Заявка на поставку металлолома'
            sender = 'snab-service.com@yandex.ru'
            recipient = RECIPIENT

            message = u'Имя: ' + form_data.cleaned_data['first_name'] + '\n'
            message += u'Отчество: ' + form_data.cleaned_data['patronym'] + '\n'
            message += u'Фамилия: ' + form_data.cleaned_data['last_name'] + '\n' + '\n'

            message += u'Телефон: ' + form_data.cleaned_data['phone'] + '\n'
            message += u'E-mail: ' + form_data.cleaned_data['email'] + '\n' + '\n'

            if form_data.cleaned_data['city']:
                message += u'Город: ' + form_data.cleaned_data['city'] + '\n' + '\n'

            if form_data.cleaned_data['amount']:
                message += u'Количество: ' + form_data.cleaned_data['amount'] + '\n' + '\n'

            message += u'Категории: '
            for key in form_data.cleaned_data:
                if key.split('_')[0] == 'category' and form_data.cleaned_data[key]:
                    message += key.split('_')[1] + ', '
            message = message[0:-2] + '\n' + '\n'

            if form_data.cleaned_data['deliverable']:
                message += u'Возможность доставки: ' + form_data.cleaned_data['deliverable'] + '\n'
            if form_data.cleaned_data['delivery_type']:
                message += u'Способ доставки: ' + form_data.cleaned_data['delivery_type'] + '\n' + '\n'
            else:
                message += '\n'

            if form_data.cleaned_data['message']:
                message += u'Сообщение: ' + form_data.cleaned_data['message']

            messageHTML = u'<p><span style="font-weight:bold">Имя: </span>' + form_data.cleaned_data[
                'first_name'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">Отчество: </span>' + form_data.cleaned_data[
                'patronym'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">Фамилия: </span>' + form_data.cleaned_data[
                'last_name'] + '</p><br>'

            messageHTML += u'<p><span style="font-weight:bold">Телефон: </span>' + form_data.cleaned_data[
                'phone'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">E-mail: </span>' + form_data.cleaned_data[
                'email'] + '</p><br>'

            if form_data.cleaned_data['city']:
                messageHTML += u'<p><span style="font-weight:bold">Город: </span>' + form_data.cleaned_data[
                    'city'] + '</p><br>'

            if form_data.cleaned_data['amount']:
                messageHTML += u'<p><span style="font-weight:bold">Количество: </span>' + form_data.cleaned_data[
                    'amount'] + '</p><br>'

            messageHTML += u'<p><span style="font-weight:bold">Категории: </span>'
            for key in form_data.cleaned_data:
                if key.split('_')[0] == 'category' and form_data.cleaned_data[key]:
                    messageHTML += key.split('_')[1] + ', '
            messageHTML = messageHTML[0:-2] + '</p><br>'

            if form_data.cleaned_data['deliverable']:
                messageHTML += u'<p><span style="font-weight:bold">Возможность доставки: </span>' + \
                               form_data.cleaned_data['deliverable'] + '</p>'
            if form_data.cleaned_data['delivery_type']:
                messageHTML += u'<p><span style="font-weight:bold">Способ доставки: </span>' + form_data.cleaned_data[
                    'delivery_type'] + '</p><br>'
            else:
                messageHTML += '<br>'

            if form_data.cleaned_data['message']:
                messageHTML += u'<p><span style="font-weight:bold">Сообщение: </span>' + form_data.cleaned_data[
                    'message'] + '</p>'

            email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient)
            email.attach_alternative(messageHTML, 'text/html')

            for document in request.FILES:
                with tempfile.TemporaryFile(mode='wb+') as fp:
                    for chunk in request.FILES[document].chunks():
                        fp.write(chunk)
                    fp.seek(0)
                    email.attach(request.FILES[document].name, fp.read(), request.FILES[document].content_type)

            email.send(fail_silently=False)

            return HttpResponseRedirect('/purchases/')

    prices = {}
    prices['2A'] = PurchasesPrice.objects.filter(category='2A').values()[0]
    prices['3A_rails'] = PurchasesPrice.objects.filter(category='3A_rails').values()[0]
    prices['3A'] = PurchasesPrice.objects.filter(category='3A').values()[0]
    prices['5A'] = PurchasesPrice.objects.filter(category='5A').values()[0]
    prices['5A_rails'] = PurchasesPrice.objects.filter(category='5A_rails').values()[0]
    prices['3AH'] = PurchasesPrice.objects.filter(category='3AH').values()[0]
    prices['17A'] = PurchasesPrice.objects.filter(category='17A').values()[0]
    prices['20A'] = PurchasesPrice.objects.filter(category='20A').values()[0]

    return render(request, 'pages/services__purchase.html', context={'price': prices, 'form': form_data},
                  content_type='text/html')


def VacanciesView(request):
    vacancies = Vacancie.objects.all()
    form_data = AddVacanciesForm()

    if request.method == 'POST':
        form_data = AddVacanciesForm(request.POST, request.FILES)
        if form_data.is_valid():
            subject = u'Отклик на вакансию ' + form_data.cleaned_data['vacancie']
            recipient = RECIPIENT
            sender = 'snab-service.com@yandex.ru'

            message = u'Имя: ' + form_data.cleaned_data['first_name'] + '\n'
            message += u'Отчество: ' + form_data.cleaned_data['patronym'] + '\n'
            message += u'Фамилия: ' + form_data.cleaned_data['last_name'] + '\n' + '\n'

            message += u'Телефон: ' + form_data.cleaned_data['phone'] + '\n'
            message += u'E-mail: ' + form_data.cleaned_data['email'] + '\n' + '\n'

            if form_data.cleaned_data['city']:
                message += u'Город: ' + form_data.cleaned_data['city'] + '\n'

            if form_data.cleaned_data['street']:
                message += u'Улица: ' + form_data.cleaned_data['street'] + '\n' + '\n'
            else:
                message += '\n'

            message += u'Вакансия: ' + form_data.cleaned_data['vacancie'] + '\n' + '\n'

            if form_data.cleaned_data['message']:
                message += u'Сообщение: ' + form_data.cleaned_data['message']

            messageHTML = u'<p><span style="font-weight:bold">Имя: </span>' + form_data.cleaned_data[
                'first_name'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">Отчество: </span>' + form_data.cleaned_data[
                'patronym'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">Фамилия: </span>' + form_data.cleaned_data[
                'last_name'] + '</p><br>'

            messageHTML += u'<p><span style="font-weight:bold">Телефон: </span>' + form_data.cleaned_data[
                'phone'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">E-mail: </span>' + form_data.cleaned_data[
                'email'] + '</p><br>'

            if form_data.cleaned_data['city']:
                messageHTML += u'<p><span style="font-weight:bold">Город: </span>' + form_data.cleaned_data[
                    'city'] + '</p>'

            if form_data.cleaned_data['street']:
                messageHTML += u'<p><span style="font-weight:bold">Улица: </span>' + form_data.cleaned_data[
                    'street'] + '</p><br>'
            else:
                messageHTML += '<br>'

            messageHTML += u'<p><span style="font-weight:bold">Вакансия: </span>' + form_data.cleaned_data[
                'vacancie'] + '</p><br>'

            if form_data.cleaned_data['message']:
                messageHTML += u'<p><span style="font-weight:bold">Сообщение: </span>' + form_data.cleaned_data[
                    'message'] + '</p>'

            email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient)
            email.attach_alternative(messageHTML, 'text/html')

            for document in request.FILES:
                with tempfile.TemporaryFile(mode='wb+') as fp:
                    for chunk in request.FILES[document].chunks():
                        fp.write(chunk)
                    fp.seek(0)
                    email.attach(request.FILES[document].name, fp.read(), request.FILES[document].content_type)

            email.send(fail_silently=False)

            return HttpResponseRedirect('/vacancies/')

    return render(request, 'pages/vacancies.html', context={'vacancies': vacancies, 'form': form_data},
                  content_type='text/html')


def ContactsView(request):
    form_data = AddContactsForm()

    if request.method == 'POST':
        form_data = AddContactsForm(request.POST)

        if form_data.is_valid():
            subject = u'Форма обратной связи: ' + form_data.cleaned_data['name']
            recipient = RECIPIENT
            sender = 'snab-service.com@yandex.ru'

            message = u'Имя: ' + form_data.cleaned_data['name'] + '\n'
            if form_data.cleaned_data['phone']:
                message += u'Телефон: ' + form_data.cleaned_data['phone'] + '\n'
            message += u'Email: ' + form_data.cleaned_data['email'] + '\n'
            if form_data.cleaned_data['message']:
                message += u'Сообщение: ' + form_data.cleaned_data['message']

            messageHTML = u'<p><span style="font-weight:bold">Имя: </span>' + form_data.cleaned_data['name'] + '</p>'
            if form_data.cleaned_data['phone']:
                messageHTML += u'<p><span style="font-weight:bold">Телефон: </span>' + form_data.cleaned_data[
                    'phone'] + '</p>'
            messageHTML += u'<p><span style="font-weight:bold">Email: </span>' + form_data.cleaned_data[
                'email'] + '</p>'
            if form_data.cleaned_data['message']:
                messageHTML += u'<p><span style="font-weight:bold">Сообщение: </span>' + form_data.cleaned_data[
                    'message'] + '</p>'

            email = EmailMultiAlternatives(subject=subject, body=message, from_email=sender, to=recipient)
            email.attach_alternative(messageHTML, 'text/html')
            email.send(fail_silently=False)

            return HttpResponseRedirect('/contacts/')

    return render(request, 'pages/contacts.html', context={'form': form_data}, content_type='text/html')
