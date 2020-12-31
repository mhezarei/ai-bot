def find_calendar_types(string):
    """
    Gets whole input  string
    """
    calendar_types = ['هجری', 'شمسی', 'قمری']
    calendar_types = []
    for calendar in calendar_types:
        if calendar in string:
            calendar_types.append(calendar)
            break
    return calendar_types
