from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserCreationForm
# Create your views here.

class LoginUser(LoginView):
    template_name = "accounts/login.html"
    fields = "email","password"
    redirect_authenticated_user = True

    def get_success_url(self):
          return reverse_lazy("tasks_todo")
    

class RegisterUser(FormView):
     template_name="accounts/register.html"
     redirect_authenticated_user = True
     form_class=UserCreationForm
     success_url =  reverse_lazy("tasks_todo")

     def form_valid(self, form):
        user = form.save()
        if user is not None:
             login(self.request, user)
        return super(RegisterUser, self).form_valid(form)
        

