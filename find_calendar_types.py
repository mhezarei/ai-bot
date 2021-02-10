def find_calendar_types(string):
    """
    Gets whole input  string
    """
    calendar_types = ['هجری', 'شمسی', 'میلادی', 'قمری']
    myCalendar_types = []
    for calendar in calendar_types:
        if calendar in string:
            myCalendar_types.append(calendar)
            break
    return myCalendar_types
