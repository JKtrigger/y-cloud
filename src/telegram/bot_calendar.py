from calendar import HTMLCalendar, month_abbr


class TelegramCalendar(HTMLCalendar):
    def formatday(self, day, weekday):
        """Return a day as a table cell.
        """
        if day == 0:
            return '_'
        return str(day)

    def formatweek(self, week):
        return [self.formatday(d, wd) for (d, wd) in week]

    def formatmonth(self, year, month, with_year=False):
        return [self.formatweek(week) for week in self.monthdays2calendar(year, month)]

    def to_telegram(self, year, month):
        month_names = [*month_abbr]
        result = {}
        days_in_month_to_end_of_year = [self.formatmonth(year, m) for m in range(month, 13)]
        for days_in_week in days_in_month_to_end_of_year:
            result[month_names[month].lower()] = days_in_week
            month += 1
        return result
