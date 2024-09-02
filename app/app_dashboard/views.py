from django.views import View
from django.shortcuts import render,redirect
from utils.redirect import rolebased_redirection

class DashboardView(View):

    def get(self,request):
        return rolebased_redirection(request._user,"dashboard/dashboard.html",request)


class AboutView(View):

    def get(self,request):
        return rolebased_redirection(request._user,"dashboard/about.html",request)
    

class ContactView(View):

    def get(self,request):
        return rolebased_redirection(request._user,"dashboard/contact.html",request)
    

class LoginView(View):

    def get(self,request):
        return rolebased_redirection(request._user,"dashboard/login.html",request)