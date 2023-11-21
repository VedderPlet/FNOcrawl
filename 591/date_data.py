import datetime
import re


def fn(s: str, month_year_min):
    pattern = f'([\d]+)({month_year_min})'
    match = re.search(pattern, s)

    return match.group(1)


def string_to_datetime(s: str) -> datetime.datetime:
    creation_date = s
    if "月" in creation_date:
        apt_creation_date = datetime.datetime(
            int(datetime.datetime.now().strftime("%Y")), int(fn(creation_date, "月")), int(fn(creation_date, "日")))
        return apt_creation_date

    elif "此房屋在剛剛發佈" in s:

        apt_creation_date = (datetime.datetime.now()) - \
                            (datetime.timedelta(0,
                                                59, 0, 0,
                                                0, 0, 0))
        return apt_creation_date

    elif "天" in s:

        apt_creation_date = (datetime.datetime.now()) - \
                            (datetime.timedelta(int(fn(creation_date, "天")),
                                                0, 0, 0,
                                                0, 0, 0))

        return apt_creation_date

    elif "小時" in s:

        apt_creation_date = (datetime.datetime.now()) - \
                            (datetime.timedelta(0,
                                                0, 0, 0,
                                                0, int(fn(creation_date, "小時")), 0))
        return apt_creation_date

    elif "分鐘" in s:

        apt_creation_date = (datetime.datetime.now()) - \
                            (datetime.timedelta(0,
                                                0, 0, 0,
                                                int(fn(creation_date, "分鐘")), 0, 0))
        return apt_creation_date

    else:
        print(creation_date)
        raise Exception("Format not recognized, site changed date retrieval format")
        # now = datetime.datetime.now() - 6 days
        # caller
        # print out the string / write a log, raise exception
