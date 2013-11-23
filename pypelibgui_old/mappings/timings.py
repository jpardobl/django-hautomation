from time import strftime, localtime, mktime


def current_day_of_week(mo=None):
    
    return strftime("%a", localtime())


def current_hour(mo=None):
    return "%f" % mktime(localtime())

mappings = [current_day_of_week, current_hour, ]
