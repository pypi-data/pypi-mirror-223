import colorama
import logging
from colorama import Fore, Style

colorama.init()

_logger = logging.getLogger('OwO.client')
_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

Formatter = logging.Formatter(f'{Fore.LIGHTBLUE_EX}[%(asctime)s] {Fore.WHITE}[{Fore.BLUE}%(levelname)s    {Fore.WHITE}] {Fore.MAGENTA}%(name)s {Fore.WHITE}%(message)s' + Style.RESET_ALL,datefmt='%Y-%m-%d %H:%M:%S')

_logger.addHandler(console_handler)

console_handler.setFormatter(Formatter)


class logger():
    def info(txt:str):
        _logger.info(txt)
    def warn(txt:str):
        _logger.warning(txt)
    def error(txt:str):
        _logger.error(txt)
    def critical(txt:str):
        _logger.critical(txt) 


def _format(message_content:str,message_channel_id:int,message_guild_id:int):
    if "sent" in message_content:
        item = message_content
        item = item.replace("💳 | ", "")
        item = item.replace("**", "")
        item = item.replace("!", "")
        item = item.replace(",", "")
        item = item.replace("cowoncy ", "")
        item = item.replace("to ", "")
        item = item.replace(" sent", "")

        words = item.split()

        sender_name = words[0]
        amount = int(words[1])
        receiver_name = "".join(words[2])
        
        sender_id = int((sender_name.replace("<@","")).replace(">",""))
        receiver_id = int((receiver_name.replace("<@","")).replace(">","")) 

        
        result = {"sender_id": sender_id, "amount": amount, "receiver_id": receiver_id,"channel_id":message_channel_id,"guild_id":message_guild_id}

        logger.info("A new user sent money.")

        return result
    elif "declined the transaction" in message_content:
        return None
    else:
        return None 

def process(payload):
    message_content = payload.data["content"]
    message_author_id = int(payload.data["author"]["id"])
    message_channel_id = int(payload.data["channel_id"])
    message_guild_id = int(payload.data["guild_id"])
    if message_content:
        if message_author_id == 408785106942164992:
            result = _format(message_content=message_content,message_channel_id=message_channel_id,message_guild_id=message_guild_id)
            if result:
                return result        
