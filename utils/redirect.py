from django.shortcuts import redirect,render
import json

def rolebased_redirection(user:str,page:str,request):
    if user:
        user=json.loads(user)
        if user.get('role')=='ADMIN':
            return redirect('/admins/')
    else:
        return render(request,page)