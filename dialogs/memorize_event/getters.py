import datetime


# All getters should return a dict for aiogram-dialog library

async def date_getter(**kwargs) -> dict:
    """Function for getting date and sending it to the Date part (1st part) of Memo-dialog"""
    today = datetime.date.today()
    yesterday = (today - datetime.timedelta(days=1))

    dates_dict = {"date_today": today.strftime('%d-%m-%y'),
                  "date_yesterday": yesterday.strftime('%d-%m-%y')}

    return dates_dict


async def places_getter(**kwargs) -> dict:
    """
    Function to get places for the second window of Memorizing Dialog (place's part (2))
    :param kwargs: Usually no input
    :return: dict. The dictionary is a tuple (place - id) -> (items in web-docs)
             Though 'count' can be deleted, it used in web-docs for... counting items. Should leave it this way
    """
    places = [("CyberFactory 🏭", "CyberFactory 🏭"),
              ("Shaman shack 🛖", "Shaman shack 🛖"),
              ("le Garage 🏴‍☠", " le Garage 🏴‍☠"),
              ("Po-Lounge ⚙", "Po-Lounge ⚙"),
              ("Olympus ⚡️🏔", "Olympus ⚡️🏔"),
              ("Cat Kingdom 🐈🐈‍⬛🐈", "Cat Kingdom 🐈🐈‍⬛🐈"),
              ("The Forest 🌳", "The Forest 🌳"),
              ]

    places_dict = {
        "places": places,
        "count": len(places)
    }

    return places_dict


async def get_friends(**kwargs) -> dict:
    """
    Function to get dictionary of friends for the Friends part (3) of Memo-dialog
    :param kwargs: Usually no input
    :return: dict. The dictionary is a tuple (place - id) -> (items in web-docs)
    """
    friends = [("Иля 🧙‍♂", "Иля 🧙‍♂"),
               ("Кирилл 🧑‍🚀️", "Кирилл 🧑‍🚀"),
               ("Потап 👨‍🏭", "Потап 👨‍🏭"),
               ("Лёха 👨‍🌾", "Лёха 👨‍🌾"),
               ("Миша 👨‍💻", "Миша 👨‍💻"),
               ("Паша 🧛", "Паша 🧛"),
               ("Лёня 👷🏻‍♂️", "Лёня 🏻‍♂️"),
               ("Даша ☄️", "Даша ☄️"),
               ("Лёха Т. 💂‍♂️", "Лёха Т. 💂‍♂"),
               ("Мари 🙇‍♀️", "Мари 🙇‍♀️"),
               ("Варя 🧝‍♀️", "Варя 🧝‍♀️"),
               ("Настя 🧚‍♀️️", "Настя 🧚‍♀️️"),
               ("Паша К 😎", "Паша К 😎"),
               ("Али 🥷", "Али 🥷"),
               ("Mutter 👩‍👦", "Mutter 👩‍👦")
               ]

    out_dict = {
        "friends": friends,
        "count": len(friends)
    }

    return out_dict
