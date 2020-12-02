from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect


# Verified User access
from django.shortcuts import render


class VerifiedRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified and not request.user.is_admin:
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # redirect same path
            return render(request,'my_Account/error_page.html',{"name":"Not Verified","details":"Your are not"
                    " Allow for this page Please Verify Your Email to Upload Items"})


        return super(VerifiedRequiredMixin, self).dispatch(
            request, *args, **kwargs)


# Admin access
class AdminRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # redirect same path

        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)

