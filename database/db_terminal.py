# little .py -file to do operate DataBase
#
#
from bot_db import BotDB, RickDB
#
#
rick_db = RickDB()
# rick_db.create_rick_quotes_table()
with rick_db:
    rick_db.update_pages("1 3 5 17 12")
#     pages = rick_db.get_pages()
#     print(pages)


# with RickDB() as rick_db:
#     pages = rick_db.get_pages()
#     if not pages:
#         print("Bubba is nomore")

