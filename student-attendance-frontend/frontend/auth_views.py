from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Welcome back, {form.get_user().username}!"
        )
        return super().form_valid(form)

class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request,
            "You have been logged out successfully."
        )
        return super().dispatch(request, *args, **kwargs)