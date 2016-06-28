# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.http.response import Http404
from django.views.generic import CreateView
from django.conf import settings
from django.contrib import messages
from qcf.models import Email, EMap
from qcf.forms import EmailForm
from qcf.conf import SAVE_TO_DB, RECIPIENTS_LIST, EMAIL_SENT_MESSAGE, REDIRECT_URL


class AddPostView(CreateView):
    model = Email
    form_class = EmailForm
    template_name = 'qcf/email_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(AddPostView, self).get_context_data(**kwargs)
        map = EMap.objects.get(name="Contact form")
        context['map'] = map
        return context
    
    def form_valid(self, form, **kwargs):
        if self.request.method == "POST":
            obj = form.save(commit=False)
            obj.email = form.cleaned_data['email']
            obj.subject = form.cleaned_data['subject']
            obj.content = form.cleaned_data['content']
            formated_request = ''
            for key in self.request.META.keys():
                formated_request += str(key)+' : '+str(self.request.META[key])+'\n'
            obj.request = formated_request
            #~ send mail
            send_mail(obj.subject, obj.content, obj.email, RECIPIENTS_LIST)
            messages.info(self.request, EMAIL_SENT_MESSAGE)
        else: 
            raise Http404
        if SAVE_TO_DB == True:
            return super(AddPostView, self).form_valid(form)
        else:
            return
            
    def get_success_url(self):
        return REDIRECT_URL
