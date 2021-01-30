import calendar
from django.utils import timezone


class Day:
    def __init__(self, day, month, year, is_past):
        self.day = day
        self.month = month
        self.year = year
        self.is_past = is_past

    def __str__(self):
        return str(self.day)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_of_week_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",)
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_month(self):
        return self.months[self.month - 1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day_number, day_of_the_week in week:
                now = timezone.now()
                today = now.day
                current_month = now.month
                is_past = False
                if current_month == self.month:
                    if day_number <= today:
                        is_past = True
                new_day = Day(day=day_number, month=self.month, year=self.year, is_past=is_past)
                days.append(new_day)
        return days
