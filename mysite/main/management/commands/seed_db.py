from django.core.management.base import BaseCommand, CommandError
from main.models import Gender, DayOfWeek, WorkingHours, Rest


class Command(BaseCommand):
    def add_day_of_weeks(self):
        days=['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье',]
        if DayOfWeek.objects.all() != []:
            return
        for day in days:
            day = DayOfWeek(
                name = day
            )
            day.save()
    def add_working_hours(self):
        working_hours=['9.00-18.00','10.00-19.00','13.00-19.00','9.00-19.00','Выходной',]
        for working_hour in working_hours:
            working_hour = WorkingHours(
                name = working_hour
            )
            working_hour.save()
    def add_rest_hours(self):
        rest_hours=['12.00-13.00','13.00-14.00','Выходной']
        for rest_hour in rest_hours:
            rest_hour = Rest(
                name = rest_hour
            )
            rest_hour.save()

    def handle(self, *args, **options):
        self.add_day_of_weeks()
        self.add_working_hours()
        self.add_rest_hours()
        
        genders = ['f', 'm']
        for gender in genders:
            gender = Gender(
                name = gender
            )

            gender.save()
