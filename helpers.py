"""Functions that supplement what the app does, that probably shouldn't live on the server."""


def military_to_standard(num):
    """Converts a number from miliary time (0000) to standard time 12:00 AM"""
    biz_hours = int(num[0:2])
    biz_minutes = int(num[2:4])

    if biz_minutes < 10:
        biz_minutes = f'0{biz_minutes}'

    if biz_hours <= 12:
        return f"{biz_hours}:{biz_minutes} AM"

    else: 
        the_pms = biz_hours - 12
        return f"{the_pms}:{biz_minutes} PM"
        
def business_hours(yelp_hours_dict):
    """Takes in the yelp data for business hours,
    {'is_overnight': False, 'start': '1700', 'end': '2100', 'day': 2},
    and returns either '24 hours', standard/normal 
    time, or 'Closed' for any given day."""

    if yelp_hours_dict['is_overnight'] == True:
        return 'Open 24 Hours'
    
    elif yelp_hours_dict['is_overnight'] == False:
        return f"{military_to_standard(yelp_hours_dict['start'])} - {military_to_standard(yelp_hours_dict['end'])}"

def day_determiner(yelp_hours_list):
    """Takes in a list of dictionaries containing yelp hours dictionaries,
    [{'is_overnight': False, 'start': '1700', 'end': '2100', 'day': 2},...],
    and returns a dictionary containing a business's hours."""
    
    days_dict = {
        'Monday': 'Closed',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed'
    }
    # updates dictionary with provided times from dictionaries in the list
    # possibly need to index or have a counter because the day determines the hours
    # could make an array of days =
    for hours in yelp_hours_list:
        if hours['day'] == 0:
            days_dict['Monday'] = business_hours(hours)
        if hours['day'] == 1:
            days_dict['Tuesday'] = business_hours(hours)
        if hours['day'] == 2:
            days_dict['Wednesday'] = business_hours(hours)
        if hours['day'] == 3:
            days_dict['Thursday'] = business_hours(hours)
        if hours['day'] == 4:
            days_dict['Friday'] = business_hours(hours)
        if hours['day'] == 5:
            days_dict['Saturday'] = business_hours(hours)
        if hours['day'] == 6:
            days_dict['Sunday'] = business_hours(hours)

    return days_dict
