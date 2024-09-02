from django.views import View
from django.shortcuts import render,redirect

class LoginView(View):

    def get(self,request):
        return render(request,'subadmin/login.html')