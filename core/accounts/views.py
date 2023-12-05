from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserCreationForm

# Create your views here.


class LoginUser(LoginView):
    """
    view class with parent LoginView in auth views
    rewrite Attributes :
    template_name , Fields,Redirect if user authenticated
    """

    template_name = "accounts/login.html"
    fields = "email", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        def to reverse urls name if login successful
        """
        return reverse_lazy("todo:tasks_todo")


class RegisterUser(FormView):
    """_summary_

    child class from parent class
    formview from django generic view
    with Attributes template name redirect
    style form_class comes from forms.py accounts app
    and success url is the tasks todo list
    """

    template_name = "accounts/register.html"
    redirect_authenticated_user = True
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks_todo")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)
