import calendar

class Calendar():
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",)
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
