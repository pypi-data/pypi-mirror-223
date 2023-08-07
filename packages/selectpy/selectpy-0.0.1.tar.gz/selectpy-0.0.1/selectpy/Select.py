import rich
from rich.text import Text
from rich.live import Live
from yakh import get_key
from yakh.key import Keys
from typing import Union, Any
import re

selected_index = 0
selected_opt = ""
last_kp = ""

def select(opts: list = [],
           msg: str = "",
           c: str = ">",
           cursor_color: str = "#ffffff",
           cursor_index: int = 0,
           selected_color: str = "#ffffff",
           unselected_color: str = "#ffffff"
        ) -> Union[Any, None]:
    def menu():
        """A select menu that allows the user to select one option from a list of options

            Args:
                options (list): A list of options to select from
                c (str, optional): Cursor that is going to appear in front of currently selected option. Defaults to '>'.
                cursor_color (str, optional): Color of the cursor. Defaults to #ffffff.
                cursor_index (int, optional): Option can be preselected based on its list index. Defaults to 0.
                selected_color (str, optional): Color of the selected option. Defaults to #ffffff.
                unselected_color (str, optional): Color of the unselected options. Defaults to #ffffff.

            Raises:
                KeyboardInterrupt: Raised when keyboard interrupt is encountered and Config.raise_on_interrupt is True

            Returns:
                Union[str, None]: Selected value or `None`
        """


        global selected_index
        global selected_opt
        selected_index = cursor_index
        popts = []
        finalstr = Text()
        cursor = c + " "

        selected_opt = opts[selected_index]

        for i in range(0, len(opts)):
            unscolor = ""
            unsopt = ""
            styleinopt = bool(re.search('^(.*\[.*\].*)$', opts[i]))
            if bool(re.search('^(.*\[.*\].*)$', opts[i])):
                clr = opts[i].split('[')[1].split(']')[0]
                unscolor = clr
                unsopt = opts[i].split('[')[1].split(']')[1]
            else:
                unscolor = unselected_color

            (popts.append(Text(str("".ljust(len(cursor)) + unsopt), style=unscolor)) if styleinopt else popts.append(Text().assemble("".ljust(len(cursor)), (opts[i], unselected_color)))) if selected_index != i else popts.append(Text().assemble((cursor, cursor_color), (unsopt if styleinopt else opts[i], selected_color)))
        
        for opt in popts:
            finalstr.append(opt.append('\n'))

        return finalstr
    
    def up():
        global selected_index
        if selected_index == 0:
            selected_index = len(opts) - 1
        else:
            selected_index -= 1

    def down():
        global selected_index
        if selected_index == len(opts) - 1:
            selected_index = 0
        else:
            selected_index += 1

    with Live(menu(), refresh_per_second=4, transient=False, auto_refresh=False) as live:
        if msg != "":
            live.console.print(msg)

        while True:
            keypress = get_key()
            
            if keypress in [Keys.CTRL_C]:
                raise KeyboardInterrupt()

            if keypress in [Keys.UP_ARROW]:
                up()
                live.update(menu(), refresh=True)

            if keypress in [Keys.DOWN_ARROW]:
                down()
                live.update(menu(), refresh=True)

            if keypress in [Keys.ENTER]:
                return selected_opt
            
            if keypress in [Keys.ESC]:
                return None
            