import pytz
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured


class DeadlineViewMixin:
    """
    For use with Django generic views.
    Define deadline as a naive datetime.datetime object.
    Define zone as the timezone you want the deadline to apply to.
    Define deadline_url as the url that should be redirected to if the timezone-aware deadline has been passed.
    """
    zone = "America/Toronto"
    deadline = None
    deadline_url = None

    def is_past_deadline(self):
        tz = pytz.timezone(self.zone)
        deadline = tz.localize(self.deadline)
        now = timezone.now()
        return now > deadline

    def dispatch(self, request, *args, **kwargs):
        if self.deadline is None:
            raise ImproperlyConfigured(
                "Deadline datetime object is not set. Set deadline as an instance of datetime.datetime.")
        if self.deadline_url is None:
            raise ImproperlyConfigured("Deadline redirect url needs to be specified. Set deadline_url.")
        if self.is_past_deadline():
            return HttpResponseRedirect(str(self.deadline_url))
        return super(DeadlineMixin, self).dispatch(request, *args, **kwargs)
