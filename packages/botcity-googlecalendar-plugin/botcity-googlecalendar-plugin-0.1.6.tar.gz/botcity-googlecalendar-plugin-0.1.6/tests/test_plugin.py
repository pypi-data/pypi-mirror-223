import datetime

import pytest

from botcity.plugins.googlecalendar import BotGoogleCalendarPlugin, EventRecurrence


def test_create_event(bot: BotGoogleCalendarPlugin, title: str, now: datetime.datetime):
    bot.create_event(title=title, description="testing", start_date=now)


def test_create_recurring_daily_event(bot: BotGoogleCalendarPlugin, title: str, now: datetime.datetime):
    now = now + datetime.timedelta(hours=1)
    bot.create_recurring_event(
        title=f"{title}_recurring_daily",
        start_date=now,
        description="testing recurring daily",
        recurrence=EventRecurrence.DAILY
    )


def test_create_recurring_weekly_event(bot: BotGoogleCalendarPlugin, title: str, now: datetime.datetime):
    now = now + datetime.timedelta(hours=3)
    bot.create_recurring_event(
        title=f"{title}_recurring_weekly",
        start_date=now,
        description="testing recurring weekly",
        recurrence=EventRecurrence.WEEKLY
    )


def test_create_recurring_monthly_event(bot: BotGoogleCalendarPlugin, title: str, now: datetime.datetime):
    now = now + datetime.timedelta(hours=4)
    bot.create_recurring_event(
        title=f"{title}_recurring_monthly",
        start_date=now,
        description="testing recurring monthly",
        recurrence=EventRecurrence.MONTHLY
    )


@pytest.mark.depends(name=["test_create_recurring_monthly_event", "test_create_recurring_weekly_event",
                           "test_create_recurring_daily_event", "test_create_event"])
def test_get_events(bot: BotGoogleCalendarPlugin):
    events = bot.get_events()
    assert len(events) == 4


def test_create_calendar(bot: BotGoogleCalendarPlugin, title: str):
    bot.create_calendar(title=title, description="Calendar test")


@pytest.mark.depends(name=["test_create_calendar"])
def test_move_event(bot: BotGoogleCalendarPlugin, title: str):
    calendars = bot.get_calendars()
    calendar = [calendar for calendar in calendars if calendar.summary == title][0]
    events = bot.get_events()
    for event in events:
        bot.move_event(event=event, destination_calendar=calendar.calendar_id)


@pytest.mark.depends(name=["test_move_event"])
def test_delete_events(bot: BotGoogleCalendarPlugin):
    events = bot.get_events()
    for event in events:
        bot.delete_event(event=event)


@pytest.mark.depends(name=["test_create_calendar"])
def test_get_calendars(bot: BotGoogleCalendarPlugin, title: str):
    calendars = bot.get_calendars()
    assert len([calendar for calendar in calendars if calendar.summary == title]) == 1


@pytest.mark.depends(name=["test_get_calendars"])
def test_get_calendar(bot: BotGoogleCalendarPlugin, title: str):
    calendars = bot.get_calendars()
    calendar = [calendar for calendar in calendars if calendar.summary == title][0]
    calendar = bot.get_calendar(calendar_id=calendar.calendar_id)
    assert calendar.summary == title


@pytest.mark.depends(name=["test_get_calendar"])
def test_delete_calendar(bot: BotGoogleCalendarPlugin, title: str):
    calendars = bot.get_calendars()
    calendar = [calendar for calendar in calendars if calendar.summary == title][0]
    calendar = bot.get_calendar(calendar_id=calendar.calendar_id)
    bot.delete_calendar(calendar=calendar)
