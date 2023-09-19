from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
def custom404(request, exception):
    return render(request, "misc/custom404.html", status=404)

class MessageLoginRequiredMixin(LoginRequiredMixin):

    message = 'You have to be logged in to access that page'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            print(f"::{self.message}")
            messages.warning(request,self.message)
            return self.handle_no_permission()
        return super(MessageLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )