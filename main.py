import asyncio
import logging

from aiogram_dialog import setup_dialogs

from loader import bot, dp

# this import is a must-have, because won't work otherwise, or not anymore?
# import dialogs
# from dialogs.main_menu_cmds import main_menu_cmds
# from dialogs.view_memes import test_send_photo
# from dialogs.setup_bot.dialogs import setup_bot_dialog
# from dialogs.view_memes.dialogs import view_memes_dialog

from dialogs import main_menu_cmds, remember_event, memorize_event
from dialogs import test_dialog


# logging formats
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


async def main():
    dp.include_routers(
        main_menu_cmds.main_menu_cmds.router,
        remember_event.dialogs.remember_event_dialog,
        memorize_event.dialogs.memorize_dialog,
        test_dialog.test.router     # clean up testing branch after completing work
        # view_memes_dialog
    )
    setup_dialogs(dp)  # aiogram_dialog thing
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, filename="chill_log.log", filemode="a", format=LOG_FORMAT)
    asyncio.run(main())
