import datetime
import calendar

class MeetingScheduler:
    def __init__(self, working_hours=(9, 17), holidays=None):
        """
        Initializes the Meeting Scheduler.

        Args:
            working_hours (tuple): Tuple representing the start and end of working hours (e.g., (9, 17) for 9 AM to 5 PM).
            holidays (list): List of datetime.date objects representing public holidays.
        """
        self.working_hours = working_hours
        self.holidays = holidays if holidays else []
        self.schedules = {}  # Dictionary to store user schedules

    def is_working_day(self, date):
        """
        Checks if a given date is a working day (not a weekend or holiday).

        Args:
            date (datetime.date): The date to check.

        Returns:
            bool: True if it's a working day, False otherwise.
        """
        if date.weekday() >= 5 or date in self.holidays:
            return False
        return True

    def is_time_slot_available(self, user, date, start_time, end_time):
        """
        Checks if a time slot is available for a given user.

        Args:
            user (str): The user's name.
            date (datetime.date): The date of the meeting.
            start_time (datetime.time): The start time of the meeting.
            end_time (datetime.time): The end time of the meeting.

        Returns:
            bool: True if the time slot is available, False otherwise.
        """
        if user not in self.schedules:
            return True

        for scheduled_start, scheduled_end, scheduled_date in self.schedules[user]:
            if scheduled_date == date:
                if (start_time < scheduled_end and scheduled_start < end_time):
                    return False
        return True

    def schedule_meeting(self, user, date, start_time, end_time):
        """
        Schedules a meeting for a user.

        Args:
            user (str): The user's name.
            date (datetime.date): The date of the meeting.
            start_time (datetime.time): The start time of the meeting.
            end_time (datetime.time): The end time of the meeting.

        Returns:
            str: A message indicating whether the meeting was scheduled successfully.
        """
        if not self.is_working_day(date):
            return "Cannot schedule meetings on weekends or holidays."

        if not (self.working_hours[0] <= start_time.hour < self.working_hours[1] and
                self.working_hours[0] < end_time.hour <= self.working_hours[1] and
                start_time < end_time):
            return "Meeting time is outside working hours or invalid."

        if not self.is_time_slot_available(user, date, start_time, end_time):
            return "Time slot is not available."

        if user not in self.schedules:
            self.schedules[user] = []

        self.schedules[user].append((start_time, end_time, date))
        self.schedules[user].sort(key=lambda x: (x[2], x[0])) #sort by date then start time.
        return "Meeting scheduled successfully."

    def get_available_slots(self, user, date):
        """
        Gets available time slots for a given user and date.

        Args:
            user (str): The user's name.
            date (datetime.date): The date to check for available slots.

        Returns:
            list: A list of available time slot strings.
        """
        if not self.is_working_day(date):
            return ["Cannot schedule meetings on weekends or holidays."]

        scheduled_slots = []
        if user in self.schedules:
            scheduled_slots = [(start, end) for start, end, scheduled_date in self.schedules[user] if scheduled_date == date]

        available_slots = []
        start_hour, end_hour = self.working_hours
        current_time = datetime.time(start_hour, 0)

        while current_time < datetime.time(end_hour, 0):
            next_slot = datetime.time(end_hour, 0)
            for start, end in scheduled_slots:
                if start > current_time:
                    next_slot = start
                    break
            if current_time < next_slot:
                available_slots.append(f"{current_time.strftime('%I:%M %p')} – {next_slot.strftime('%I:%M %p')}")
            current_time = next_slot

            found = False
            for start, end in scheduled_slots:
                if end > current_time:
                    current_time = end
                    found = True
                    break
            if not found:
                break

        return available_slots

    def view_scheduled_meetings(self, user):
        """
        Views scheduled meetings for a user.

        Args:
            user (str): The user's name.

        Returns:
            list: A list of scheduled meeting strings.
        """
        if user not in self.schedules:
            return ["No upcoming meetings."]

        meetings = []
        for start_time, end_time, date in self.schedules[user]:
            meetings.append(f"{date.strftime('%Y-%m-%d')}: {start_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}")
        return meetings

# Example Usage
scheduler = MeetingScheduler(
    holidays=[datetime.date(2025, 3, 21)]  # Example holiday
)

user = "Alice"
date = datetime.date(2025, 3, 18)
start_time = datetime.time(10, 0)
end_time = datetime.time(11, 0)

print(scheduler.schedule_meeting(user, date, start_time, end_time))

print("Available slots:")
for slot in scheduler.get_available_slots(user, date):
    print(slot)

print("Scheduled meetings:")
for meeting in scheduler.view_scheduled_meetings(user):
    print(meeting)

date2 = datetime.date(2025, 3, 18)
start_time2 = datetime.time(9, 0)
end_time2 = datetime.time(10, 0)
print(scheduler.schedule_meeting(user, date2, start_time2, end_time2))

print("Available slots:")
for slot in scheduler.get_available_slots(user, date):
    print(slot)

date3 = datetime.date(2025, 3, 21)
print(scheduler.schedule_meeting(user, date3, start_time2, end_time2))
