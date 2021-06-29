from django.shortcuts import redirect, render
from django.contrib.auth import logout
from .forms import PasswordChangingForm, PasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Passwords


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def dashboard(request):
    return render(request, "user_side/dashboard.html")


@login_required(login_url='login')
def events(request):
    return render(request, "user_side/events.html")


@login_required(login_url='login')
def passwords(request):
    form = PasswordForm
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        if form.is_valid():
            form.save()
    passwords = Passwords.objects.filter(user=request.user)
    return render(request, "user_side/password_manager.html", {
        "passwords": passwords,
        'form': form
    })


@login_required(login_url='login')
def deletePassword(request, pk):
    item = Passwords.objects.get(id=pk)
    item.delete()
    return redirect("user-passwords")


# @login_required(login_url='login')
class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login')
