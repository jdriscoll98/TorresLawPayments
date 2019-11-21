from .models import Reminder

def reminders(request):
    return {'reminding': Reminder.objects.get(pk=1).in_progress}
