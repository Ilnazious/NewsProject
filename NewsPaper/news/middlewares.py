import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            try:
                tz = pytz.timezone(tzname)
                timezone.activate(tz)
            except (pytz.UnknownTimeZoneError, ValueError):
                timezone.activate(pytz.UTC)
                request.session['django_timezone'] = 'UTC'
        else:
            timezone.deactivate()
        return self.get_response(request)