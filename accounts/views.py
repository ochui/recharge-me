#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.http import Http404
from allauth.account.models import EmailAddress
from .models import CustomUser
from .forms import EditProfileForm

class Dashboard(LoginRequiredMixin, TemplateView):
    
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #check user email status
        if not EmailAddress.objects.filter(user=self.request.user, verified=True).exists():
            context['verified_email'] = False
        else:
            context['verified_email'] = True
                
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = CustomUser
    template_name = "dashboard/profile.html"
    form_class = EditProfileForm
    model = CustomUser

    def get_object(self, queryset=None):
        """
        Returns a single user instance
        """
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(username=self.kwargs['username'])
        
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                        {'verbose_name': queryset.model._meta.verbose_name})
        return obj