from .models import Booking
from datetime import datetime, timedelta
from django.http import JsonResponse

def is_room_available(room, check_in, check_out):
    from dateutil.parser import parse

    try:
        check_in_date = parse(str(check_in)).date()
        check_out_date = parse(str(check_out)).date()
    except Exception:
        return JsonResponse({'error': 'Invalid date format'}, status=400)


    buffer = timedelta(hours=3)

    overlapping = Booking.objects.filter(
        room=room,
        check_in__lt=check_out + buffer,
        check_out__gt=check_in
    )
    return not overlapping.exists()