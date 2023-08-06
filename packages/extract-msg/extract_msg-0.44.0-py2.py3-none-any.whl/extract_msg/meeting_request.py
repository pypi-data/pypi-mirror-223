__all__ = [
    'MeetingRequest',
]


import datetime

from typing import List, Optional, Set

from . import constants
from .meeting_related import MeetingRelated
from .enums import BusyStatus, MeetingObjectChange, MeetingType, RecurCalendarType, RecurPatternType, ResponseStatus


class MeetingRequest(MeetingRelated):
    """
    Class for handling Meeting Request and Meeting Update objects.
    """

    @property
    def appointmentMessageClass(self) -> Optional[str]:
        """
        Indicates the value of the PidTagMessageClass property of the Meeting
        object that is to be generated from the Meeting Request object. MUST
        start with "IPM.Appointment".
        """
        return self._ensureSetNamed('_appointmentMessageClass', '0024', constants.PSETID_MEETING)

    @property
    def calendarType(self) -> Optional[RecurCalendarType]:
        """
        The value of the CalendarType field from the PidLidAppointmentRecur
        property if the Meeting Request object represents a recurring series or
        an exception.
        """
        return self._ensureSetNamed('_calendarType', '001C', constants.PSETID_MEETING, overrideClass = RecurCalendarType)

    @property
    def changeHighlight(self) -> Optional[Set[MeetingObjectChange]]:
        """
        Soecifies a bit field that indicates how the Meeting object has been
        changed.

        Returns a set of flags.
        """
        return self._ensureSetNamed('_changeHighlight', '8204', constants.PSETID_APPOINTMENT, overrideClass = MeetingObjectChange.fromBits)

    @property
    def forwardInstance(self) -> bool:
        """
        Indicates that the Meeting Request object represents an exception to a
        recurring series, and it was forwarded (even when forwarded by the
        organizer) rather than being an invitation sent by the organizer.
        """
        return self._ensureSetNamed('_forwardInstance', '820A', constants.PSETID_APPOINTMENT, overrideClass = bool, preserveNone = False)

    @property
    def headerFormatProperties(self) -> constants.HEADER_FORMAT_TYPE:
        """
        Returns a dictionary of properties, in order, to be formatted into the
        header. Keys are the names to use in the header while the values are one
        of the following:
        None: Signifies no data was found for the property and it should be
            omitted from the header.
        str: A string to be formatted into the header using the string encoding.
        Tuple[Union[str, None], bool]: A string should be formatted into the
            header. If the bool is True, then place an empty string if the value
            is None, otherwise follow the same behavior as regular None.

        Additional note: If the value is an empty string, it will be dropped as
        well by default.

        Additionally you can group members of a header together by placing them
        in an embedded dictionary. Groups will be spaced out using a second
        instance of the join string. If any member of a group is being printed,
        it will be spaced apart from the next group/item.

        If you class should not do *any* header injection, return None from this
        property.
        """
        meetingStatusString = {
            ResponseStatus.NONE: None,
            ResponseStatus.ORGANIZED: 'Meeting organizer',
            ResponseStatus.TENTATIVE: 'Tentatively accepted',
            ResponseStatus.ACCEPTED: 'Accepted',
            ResponseStatus.DECLINED: 'Declined',
            ResponseStatus.NOT_RESPONDED: 'Not yet responded',
        }[self.responseStatus]

        # Get the recurrence string.
        recur = '(none)'
        if self.appointmentRecur:
            recur = {
                RecurPatternType.DAY: 'Daily',
                RecurPatternType.WEEK: 'Weekly',
                RecurPatternType.MONTH: 'Monthly',
                RecurPatternType.MONTH_NTH: 'Monthly',
                RecurPatternType.MONTH_END: 'Monthly',
                RecurPatternType.HJ_MONTH: 'Monthly',
                RecurPatternType.HJ_MONTH_NTH: 'Monthly',
                RecurPatternType.HJ_MONTH_END: 'Monthly',
            }[self.appointmentRecur.patternType]

        showTime = None if self.appointmentNotAllowPropose else 'Tentative'

        return {
            '-main info-': {
                'Subject': self.subject,
                'Location': self.location,
            },
            '-date-': {
                'Start': self.startDate.__format__('%a, %d %b %Y %H:%M %z') if self.startDate else None,
                'End': self.endDate.__format__('%a, %d %b %Y %H:%M %z') if self.endDate else None,
                'Show Time As': showTime,
            },
            '-recurrence-': {
                'Recurrance': recur,
                'Recurrence Pattern': self.recurrencePattern,
            },
            '-status-': {
                'Meeting Status': meetingStatusString,
            },
            '-attendees-': {
                'Organizer': self.organizer,
                'Required Attendees': self.to,
                'Optional Attendees': self.cc,
                'Resources': self.bcc,
            },
            '-importance-': {
                'Importance': self.importanceString,
            },
        }


    @property
    def intendedBusyStatus(self) -> Optional[BusyStatus]:
        """
        The value of the busyStatus on the Meeting object in the organizer's
        calendar at the time the Meeting Request object or Meeting Update object
        was sent.
        """
        return self._ensureSetNamed('_intendedBusyStatus', '8224', constants.PSETID_APPOINTMENT, overrideClass = BusyStatus)

    @property
    def meetingType(self) -> Optional[MeetingType]:
        """
        The type of Meeting Request object or Meeting Update object.
        """
        return self._ensureSetNamed('_meetingType', '0026', constants.PSETID_MEETING, overrideClass = MeetingType)

    @property
    def oldLocation(self) -> Optional[str]:
        """
        The original value of the location property before a meeting update.
        """
        return self._ensureSetNamed('_oldLocation', '0028', constants.PSETID_MEETING)

    @property
    def oldWhenEndWhole(self) -> Optional[datetime.datetime]:
        """
        The original value of the appointmentEndWhole property before a meeting
        update.
        """
        return self._ensureSetNamed('_oldWhenEndWhole', '002A', constants.PSETID_MEETING)

    @property
    def oldWhenStartWhole(self) -> Optional[datetime.datetime]:
        """
        The original value of the appointmentStartWhole property before a
        meeting update.
        """
        return self._ensureSetNamed('_oldWhenStartWhole', '0029', constants.PSETID_MEETING)
