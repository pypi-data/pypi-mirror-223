import os
from datetime import datetime
from enum import Enum
from typing import List, Union

from gcsa.calendar import Calendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import (DAILY, FR, MO, MONTHLY, SA, SU, TH, TU, WE,
                             WEEKLY, Recurrence)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class EventRecurrence(Enum):
    DAILY = DAILY
    WEEKLY = WEEKLY
    MONTHLY = MONTHLY


class EventDays(Enum):
    MONDAY = MO
    TUESDAY = TU
    WEDNESDAY = WE
    THURSDAY = TH
    FRIDAY = FR
    SATURDAY = SA
    SUNDAY = SU


class BotGoogleCalendarPlugin:
    def __init__(self, credentials_file_path: str, calendar: str = "primary") -> None:
        """
        BotGoogleCalendarPlugin.

        Args:
            credentials_file_path (str): The path of the credentials json file obtained at Google Cloud Platform.
            calendar (str, optional): The id of the calendar that will be used. Defaults to "primary".
                To see the id of a calendar, go to the Integrate Calendar tab in the calendar settings.
        """
        creds = None
        scopes = ['https://www.googleapis.com/auth/calendar']

        # The file token_calendar.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        credentials_dir = os.path.abspath(os.path.dirname(credentials_file_path))

        if os.path.exists(os.path.join(credentials_dir, 'token_calendar.json')):
            creds = Credentials.from_authorized_user_file(
                os.path.join(credentials_dir, 'token_calendar.json'), scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath(credentials_file_path), scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(credentials_dir, 'token_calendar.json'), 'w') as token:
                token.write(creds.to_json())

        self._calendar_service = GoogleCalendar(
            credentials=creds,
            default_calendar=calendar
        )

    @property
    def calendar_service(self) -> GoogleCalendar:
        """The Google Calendar account service."""
        return self._calendar_service

    def get_events(self, date_min: datetime = None, date_max: datetime = None) -> List[Event]:
        """
        Get all calendar events.

        Args:
            date_min (datetime, optional): Events date is within or later than the specified date.
                Set this value if you want to return events that have already happened.
            date_max (datetime, optional): Events date is earlier or equal than the specified date.

        Returns:
            List[Event]: The list containing all the calendar events.
        """
        return list(self.calendar_service.get_events(time_min=date_min, time_max=date_max))

    def create_calendar(self, title: str, description: str = None) -> None:
        """
        Create a new secondary calendar.

        Args:
            title (str): Title of the calendar.
            description (str, optional): Description of the calendar.
        """
        calendar = Calendar(
            summary=title,
            description=description
        )
        self.calendar_service.add_calendar(calendar=calendar)

    def get_calendar(self, calendar_id: str = None) -> Calendar:
        """
        Return the calendar with the corresponding calendar_id.

        Args:
            calendar_id (str, optional): Calendar identifier.
                To see the id of a calendar, go to the Integrate Calendar tab in the calendar settings.

        Returns:
            Calendar: The Calendar object.
        """
        return self.calendar_service.get_calendar(calendar_id=calendar_id)

    def get_calendars(self) -> List[Calendar]:
        """
        Return the calendars on the user's calendar list.

        Returns:
            List[Calendar]: The list containing all the Calendar objects.
        """
        return list(self.calendar_service.get_calendar_list())

    def delete_calendar(self, calendar: Union[Calendar, str]) -> None:
        """
        Delete a secondary calendar.

        Args:
            calendar (Calendar | str): The calendar identifier or the Calendar object.
                To see the id of a calendar, go to the Integrate Calendar tab in the calendar settings.
        """
        self.calendar_service.delete_calendar(calendar=calendar)

    def create_event(self, title: str, description: str, start_date: datetime,
                     end_date: datetime = None, attendees: List[str] = None) -> None:
        """
        Create a new event on the calendar.

        Args:
            title (str): The title of the event.
            description (str): The description of the event. The text can be in HTML format.
            start_date (datetime): The starting date of the event.
            end_date(datetime, optional): The ending date of the event. Defaults to 1 hour after the starting date.
            attendees (str, optional): The list of emails that are included in the event.
        """
        event = Event(
            summary=title,
            description=description,
            start=start_date,
            end=end_date,
            attendees=attendees
        )
        self.calendar_service.add_event(event)

    def create_recurring_event(
            self,
            title: str,
            description: str,
            start_date: datetime,
            end_date: datetime = None,
            attendees: List[str] = None,
            recurrence: EventRecurrence = EventRecurrence.DAILY,
            recurrence_freq: int = None,
            recurrence_count: int = None,
            recurrence_days: List[EventDays] = [],
            recurrence_until_date: datetime = None) -> None:
        """
        Create a new recurring event on the calendar.

        Args:
            title (str): The title of the event.
            description (str): The description of the event. The text can be in HTML format.
            start_date (datetime): The starting date of the event.
            end_date(datetime, optional): The ending date of the event. Defaults to 1 hour after the starting date.
            attendees (str, optional): The list of emails that are included in the event.
            recurrence (EventRecurrence): The recurrence period of the event. Usage: EventRecurrence.<PERIOD>
            recurrence_freq (int, optional): Positive integer representing how often the recurrence rule repeats.
            recurrence_count (int, optional): Maximum number of events created.
            recurrence_days (List[EventDays]): Specific days for event creation. Usage: EventDays.<DAY>
            recurrence_until_date (datetime, optional): The end date of the event recurrence.
        """
        recurrence_rule = Recurrence.rule(
            freq=recurrence.value,
            interval=recurrence_freq,
            count=recurrence_count,
            by_week_day=[day.value for day in recurrence_days],
            until=recurrence_until_date
        )

        event = Event(
            summary=title,
            description=description,
            start=start_date,
            end=end_date,
            attendees=attendees,
            recurrence=recurrence_rule
        )
        self.calendar_service.add_event(event)

    def move_event(self, event: Event, destination_calendar: str) -> None:
        """
        Move a event from the calendar to another calendar.

        Args:
            event (Event): The event to be moved.
            destination_calendar (str): The id of the destination calendar.
                To see the id of a calendar, go to the Integrate Calendar tab in the calendar settings.
        """
        self.calendar_service.move_event(event, destination_calendar)

    def delete_event(self, event: Event) -> None:
        """
        Delete a event from the calendar.

        Args:
            event (Event): The event to be deleted.
        """
        self.calendar_service.delete_event(event)
