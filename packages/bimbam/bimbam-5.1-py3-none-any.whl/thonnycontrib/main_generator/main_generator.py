from thonny.editors import EditorCodeViewText
import re
import tkinter as tk
from thonny import ui_utils
from thonnycontrib import utils

# The regex to check if the __main__ already exists
# The regex checks if a string already contains the __main__ and not commented.
_REGEX = re.compile(r"(?m)^\s*if\s+__name__\s*==\s*['\"]__main__['\"]\s*:\s*")

# The generated `__main__` function. 
# Leave a blank line before the `if __name__ == '__main__':` line, 
# so that the generated main function is separated from the rest of the code.
GENERATED_MAIN:str = (
"""
    
if __name__ == '__main__':
    # éxécuté qd ce module n'est pas initialisé par un import.
    pass
"""
)

# used to tell the user whether the __main_ is generated or not
MAIN_EXISTS_MSG = "`__main__` existe déjà"
MAIN_GENERATED_MSG = "`__main__` généré"

class MainGenerator(): 
    """
    This class is responsible for generating the __main__ function.
    It takes a source code as input and generates the __main__ function 
    at the bottom of the source code.
    
    Args:
        source (str, optional): The source code in which 
        the __main__ will be generated. Defaults to "".
    """         
    def __init__(self, source=""):
        self._source = source
     
    def generate(self, text_widget:EditorCodeViewText=None, show_tooltip_info=True) -> str: 
        """
        Generate the __main__ and insert it at the bottom of the given `text_widget`.

        Args:
            text_widget (EditorCodeViewText, optional): The text widget to insert 
            the generated __main__ into. Set to `None` to not insert the generated 
            main function, this is useful for testing.
            
            show_tooltip_info (bool, optional): Set to True to show a message on a tooltip 
            to tell the user whether the __main__ is generated or not. Defaults to True.
            
        Returns:
            str: The generated __main__ function or an empty string if the __main__ already exists.
        """        
        main_line = self.__find_main_lineno(self._source) # Check if a __main__ already exists
        if main_line:
            if show_tooltip_info:
                self.__show_info_on_tooltip(text_widget, main_line=main_line, msg=MAIN_EXISTS_MSG, is_success=False)
            return "" # __main__ already exists so return empty string.

        generated_main = self.__generate_main()
        if text_widget :  
            text_widget.insert("end", generated_main)
            if show_tooltip_info:
                last_line_number = int(text_widget.index('end').split('.')[0]) - generated_main.count("\n")
                self.__show_info_on_tooltip(text_widget, main_line=last_line_number, msg=MAIN_GENERATED_MSG, is_success=True)
        return generated_main
    
    def __find_main_lineno(self, text: str) -> int:
        """
        Returns the line numbers where the __main__ (and not commented) exists. Returns None if not found.
        """
        lines = text.splitlines()
        # use next() to get the first line number where the regex is found. Gets None if not found
        return next((i for i, line in enumerate(lines, 1) if re.search(_REGEX, line)), None)
    
    def __generate_main(self) -> str:
        """ Generate the main function """
        return GENERATED_MAIN
      
    def __show_info_on_tooltip(self, text_widget:EditorCodeViewText, main_line:int, msg:str, is_success:bool):
        """
        Show a message on a tooltip. A tooltip is a toplevel window. this method 
        customizes the style of the tooltip and it is destroyed after few seconds.

        Args:
            text_widget (EditorCodeViewText): The text widget where the tooltip will be displayed.
            main_line (int): The line where the existed __main__ is.
            msg (str): The message to display on the tooltip.
            is_success (bool): Set to True to set the colors of the tooltip to green, When set to False, 
            the colors are red.
        """
        wx, wy, _, _ = text_widget.bbox("insert")
        lineno, column = utils.get_selected_line(text_widget, only_lineno=False)
        
        tw = tk.Toplevel(text_widget)   
        tw.after(1500, tw.destroy) # destroy the tooltip after 1.5 seconds
        tw.wm_overrideredirect(1) # remove the title bar
        tw.wm_geometry("+%d+%d" % (column+wx+text_widget.winfo_rootx(), lineno+wy+text_widget.winfo_rooty()))

        options = ui_utils.get_style_configuration("Tooltip").copy()
        
        # (#facdcd, #850303) are the default colors for error messages
        # (#d4f4cd, #0b4f00) are the default colors for success messages
        options.setdefault("background", "#d4f4cd" if is_success else "#facdcd")
        options.setdefault("foreground", "#0b4f00" if is_success else "#850303")
        options.setdefault("relief", "flat") # remove the border
        options.setdefault("padx", 1)
        options.setdefault("pady", 0)

        msg = " %s, ligne %s " % (msg, main_line)
        label = tk.Label(tw, text=msg, **options)
        label.pack()

    def get_source(self) -> str:
        """ Returns the source code """
        return self._source
    
    def set_source(self, source: str):
        """ Sets the source code """
        self._source = source