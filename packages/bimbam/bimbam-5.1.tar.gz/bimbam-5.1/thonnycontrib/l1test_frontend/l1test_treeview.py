from thonny import  tktextext, ui_utils
from thonny.ui_utils import scrollbar_style
from ..backend.verdicts.PassedVerdict import PassedVerdict
from ..backend.verdicts.PassedSetupVerdict import PassedSetupVerdict
from thonnycontrib.utils import get_font_size_option, get_font_family_option
from .l1test_error_view import L1TestErrorView
from ..properties import *
from ..backend.doctest_parser import Example
from ..backend.ast_parser import L1DocTest, L1DocTestFlag
from ..backend.verdicts.ExceptionVerdict import ExceptionVerdict
from ..backend.verdicts.FailedVerdict import FailedVerdict
from ..backend.verdicts.FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
from ..utils import *
from functools import partial
from ..l1test_configuration.l1test_options import *
import tkinter as tk, tkinter.font as tk_font, thonny
from collections import namedtuple
from thonny.codeview import *
from typing import Dict, List
from copy import deepcopy
from tkinter import ttk

# La hauteur, par défault, d'une ligne dans une Treeview
ROW_HEIGHT = 40

SMALL_MARGIN = 1.1
NORMAL_MARGIN = 1.17

CLICKABLE_TAG = "clickable"

# L'objet qui représente un summarize
Summarize = namedtuple('Summarize', ["total", "success", "failures", "errors", "empty"])

# Palette de couleurs utilisée par la treeview
COLORS:dict = { 'orange': '#e8770e',
                'red': 'red',
                'lightred': '#ffdddb',
                'darkred': '#f7140c',
                'green': 'darkgreen',
                'blue': '#0000cc',
                'gray': 'gray'
            }

## Binding events to shortcuts.  
ALT_I = "<Alt-i>" # to increase space between tree rows
ALT_D = "<Alt-d>" # to decrease space between tree rows
ALT_F = "<Alt-f>" # to update font size
ALT_U = "<Alt-u>" # to unfold tree rows
ALT_O = "<Alt-o>" # to fold tree rows
BINDINGS = {ALT_I: "Alt+i", ALT_D: "Alt+d", ALT_F: "Alt+f", ALT_U: "Alt+u", ALT_O: "Alt+o"}

class L1TestTreeView(ttk.Frame):    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, borderwidth=0, relief="flat")
        self.workbench = thonny.get_workbench()
        self._origin_l1doctests: List[L1DocTest] = dict()
        self._copy_l1doctests = self._origin_l1doctests.copy()
        
        self.__init_treeview()
        self.__init_workbench_bindings()
        self.__init_special_attributes()
    
    def __init_workbench_bindings(self):
        """
        Binds the events to the workbench.
        """
        # Le binding est censé augmenter/diminuer automatiquement la taille de la treeview
        self.workbench.bind("<Control-plus>", self.observe_font_changing, True)
        self.workbench.bind("<Control-minus>", self.observe_font_changing, True)
        self.workbench.bind(ALT_I, self.increase_row_height, True)
        self.workbench.bind(ALT_D, self.decrease_row_height, True)
        self.workbench.bind(ALT_F, self.update_font, True)
        self.workbench.bind(ALT_U, self.expand_rows, True) 
        self.workbench.bind(ALT_O, self.fold_rows, True)
               
    def __init_treeview(self):
        """
        Creates the treeview widget.
        """
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=scrollbar_style("Vertical"))
        self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW, rowspan=3)
    
        self.treeview = ttk.Treeview(self,yscrollcommand=self.vert_scrollbar.set)
        rows, columns = 2, 0
        self.treeview.grid(row=rows, column=columns, sticky=tk.NSEW)
        self.vert_scrollbar["command"] = self.treeview.yview
        self.columnconfigure(columns, weight=1)
        self.rowconfigure(rows, weight=1)
        self.treeview.column("#0", anchor=tk.W, stretch=tk.YES) # configure the only tree column
        self.treeview["show"] = ("tree",)

        for color_name, color in COLORS.items():
            if color_name == "lightred": # lightred is used for background (highlighting)
                self.treeview.tag_configure(color_name, background=color)
            else:
                self.treeview.tag_configure(color_name, foreground=color)
        
        # définir un tag pour les tests en exception: il faut les souligner (underline)
        self.treeview.tag_configure(
            "exception_as_link", 
            foreground=COLORS["red"], 
            font=tk_font.Font(underline=True, weight="normal", family=get_font_family_option(), size=get_font_size_option())
        )
        # définir un tag pour les tests en exception survolé: il faut les souligner (underline) et les mettre en gras (bold)
        self.treeview.tag_configure(
            "exception_hovered", 
            foreground=COLORS["red"], 
            font=tk_font.Font(underline=True, weight="bold", family=get_font_family_option(), size=get_font_size_option())
        )

        # définir un style par défault pour la treeview
        self.style = ttk.Style()
        self.style_mapping = self.style.map('Treeview')
        self.__update_tree_font(get_font_family_option(), get_font_size_option())

        # All the icons used in the treeview should be loaded here to keep thier references.
        # Otherwise, they will be garbage collected and the treeview will not show them.
        self.image_references = {flag.get_image_basename(): get_photoImage(flag.get_image_basename()) for flag in L1DocTestFlag}
        self.image_references[PENDING_ICON] = get_photoImage(PENDING_ICON)
        self.image_references[ERROR_ICON] = get_photoImage(ERROR_ICON)
        self.image_references[RESTART_ICON] = get_photoImage(RESTART_ICON)
        self.image_references[FAILED_RED_CHIP] = get_photoImage(FAILED_RED_CHIP)
        self.image_references[EXCEPTION_RED_CHIP] = get_photoImage(EXCEPTION_RED_CHIP)
        self.image_references[SUCCESS_GREEN_CHIP] = get_photoImage(SUCCESS_GREEN_CHIP)
        
        self.treeview.tag_bind("clickable", "<<TreeviewSelect>>", self._on_select)
        self.treeview.tag_bind("nonClickable", "<<TreeviewSelect>>", self._remove_highlight_selection_effect)
        self.treeview.bind("<Motion>", self._on_hover_exception_test)
        self.treeview.bind("<Configure>", self.__wrap_tree_content) # Here we handle the motion event of the treeview 
        
        # add a menu to the treeview 
        self.menu = tk.Menu(self.treeview, name="menu", tearoff=False)        
        self.init_header(row=0, column=0)
        
    def __init_special_attributes(self):
        """
        Initializes the special attributes of the treeview.
        """
        self.__old_width = -1 # utilisé pour savoir si la hauteur de la treeview a changé
        self.__max_lines = 1 # le nombre de lignes du texte le plus long de la treeview
        self.__hovered_exception = None # l'exception test sur laquelle le curseur est en train de passer
     
    def _on_hover_exception_test(self, event):
        """
        Handles the motion event of the treeview. When the cursor is hovering over an exception test, 
        the font of the test is changed to bold and underlined. The cursor is also changed to "hand".
        """
        if not self.is_empty():
            item = self.treeview.identify('item', event.x, event.y)
            tags = self.treeview.item(item, "tags")
            if "exception_as_link" in tags:
                if self.__hovered_exception and self.__hovered_exception != item:
                    # If the cursor is hovering over a different item, revert the font and cursor to normal for the previously hovered item
                    prev_item = self.__hovered_exception
                    prev_tags = self.treeview.item(prev_item, "tags")
                    new_tags = tuple(tag for tag in prev_tags if tag not in ("exception_hovered", "exception_cursor"))
                    self.treeview.item(prev_item, tags=new_tags + ("exception_as_link",))
                    self.treeview.configure(cursor="")
                    self.__hovered_exception = None

                # Change the font to bold and underlined and set the cursor to "hand" when the cursor enters the row with the "exception_as_link" tag
                new_tags = tuple(tag for tag in tags if tag != "exception_as_link")
                self.treeview.item(item, tags=new_tags + ("exception_hovered", "exception_cursor"))
                self.treeview.configure(cursor="hand2")
                self.__hovered_exception = item
            elif self.__hovered_exception and self.__hovered_exception != item:
                # If the cursor is not over any "exception_as_link" item, revert the font and cursor to normal for the previously hovered item
                prev_item = self.__hovered_exception
                prev_tags = self.treeview.item(prev_item, "tags")
                new_tags = tuple(tag for tag in prev_tags if tag not in ("exception_hovered", "exception_cursor"))
                self.treeview.item(prev_item, tags=new_tags + ("exception_as_link",))
                self.treeview.configure(cursor="")
                self.__hovered_exception = None

    # ------------------------------------
    # Fonctions pour le Header du treeview
    # ------------------------------------
    
    def init_header(self, row=0, column=0):
        """
        Initialize the header of the treeview. Initially, the header contains 
        only a `menu button` at the top right of the treeview. The options of the 
        menu are created by `post_button_menu()` method.

        Args:
            row (int): Always set to 0. Defaults to 0.
            column (int): Always set to 0. Defaults to 0.
        """
        header_frame = ttk.Frame(self, style="ViewToolbar.TFrame")
        header_frame.grid(row=row, column=column, sticky="nsew")
        header_frame.columnconfigure(0, weight=1)
        
        self.header_bar = tktextext.TweakableText(
            header_frame,
            borderwidth=0,
            relief="flat",
            height=1,
            wrap="word",
            padx=ui_utils.ems_to_pixels(0.6),
            pady=ui_utils.ems_to_pixels(0.5),
            insertwidth=0,
            highlightthickness=0,
            background=ui_utils.lookup_style_option("ViewToolbar.TFrame", "background"),
        )
        
        for color_name, color in COLORS.items():
            self.header_bar.tag_configure(color_name, foreground=color)
        
        self.header_bar.grid(row=0, column=0, sticky="nsew")
        self.header_bar.set_read_only(True)
        self.menu_button = ttk.Button(
                                header_frame, 
                                text=" ≡ ", 
                                style="ViewToolbar.Toolbutton", 
                                width=3,
                                command=self.post_button_menu
                            )
        self.header_bar.bind("<Configure>", self.resize_header_bar, True)
        self.header_bar.configure(height=1)

        self.menu_button.place(anchor="ne", rely=0, relx=1)
        self.disable_menu()
     
    def post_button_menu(self):
        """
            The handler of the menu button located in the header of the treeview.
            When clicking the menu button a popoup is opened and shows several options.
        """
        self.add_menu_options()
        self.menu.tk_popup(
            self.menu_button.winfo_rootx(),
            self.menu_button.winfo_rooty() + self.menu_button.winfo_height(),
        )
    
    def add_menu_options(self):
        """
            Adds the options inside the menu button.
        """
        self.menu.delete(0, "end") 
         
        self.menu.add_command(label=PLACE_RED_TEST_ON_TOP_LABEL, command=self.sort_by_red_tests)
        self.menu.add_command(label=RESUME_ORIGINAL_ORDER, command=self.remove_sort_filter)
        self.menu.add_separator() 
        self.menu.add_command(label=SHOW_ONLY_RED_TESTS, command=self.show_only_red_tests)
        self.menu.add_command(label=SHOW_ALL_TESTS, command=self.show_all_tests)
        self.menu.add_separator()
        self.menu.add_command(label=GROUP_BY_VERDICTS, command=self.group_by_verdicts)
        self.menu.add_separator()    
        self.menu.add_command(label=EXPAND_ALL, command=self.expand_rows, accelerator=BINDINGS[ALT_U]) 
        self.menu.add_command(label=FOLD_ALL, command=self.fold_rows, accelerator=BINDINGS[ALT_O])
        self.menu.add_separator() 
        self.menu.add_command(label=UPDATE_FONT_LABEL, command=self.update_font, accelerator=BINDINGS[ALT_F])
        self.menu.add_command(label=INCREASE_SPACE_BETWEEN_ROWS, command=self.increase_row_height, accelerator=BINDINGS[ALT_I])
        self.menu.add_command(label=DECREASE_SPACE_BETWEEN_ROWS, command=self.decrease_row_height, accelerator=BINDINGS[ALT_D])
        self.menu.add_separator()
        self.menu.add_command(label=CLEAR_LABEL, command=partial(self.clear_tree, clear_verdicts_data=True))
          
    def resize_header_bar(self, event=None):
        """ 
        Resize the height of the header. 
        Always keep this method otherwise the header will take the whole treeview.
        """
        height = self.tk.call((self.header_bar, "count", "-update", "-displaylines", "1.0", "end"))
        self.header_bar.configure(height=height)

    def update_font(self, event=None):
        """
        This is the handler of the `Update the font` option.  
        
        It also update the font size of the treeview if and 
        only if the font is changed in thonny.
        """          
        self.resize_header_bar()
        # on applique la nouvelle police pour la treeview
        self.observe_font_changing()
     
    def sort_by_red_tests(self):
        
        # On filtre que les l1doctest qui ont un flag rouge.
        sorted_failed_nodes = [l1doctest for l1doctest in self._copy_l1doctests if l1doctest.get_flag() == L1DocTestFlag.FAILED_FLAG ]
        
        # On met les tests rouges en haut et cela pour tous les l1doctest qui ont au moins un test rouge.
        sorted_failed_tests = []
        for l1doctest in sorted_failed_nodes:
            new_l1doctest = deepcopy(l1doctest)
            new_l1doctest.sort_examples_by_verdicts((FailedVerdict, ExceptionVerdict))
            sorted_failed_tests.append(new_l1doctest)
           
        # On récupère les autres neouds AST 
        others = [l1doctest for l1doctest in self._copy_l1doctests if l1doctest.get_flag() != L1DocTestFlag.FAILED_FLAG]
         # l'addition de tous les noeuds
        sorted_failed_tests.extend(others)

        if not self.is_empty(): # on met à jour que si la treeview possède des éléments
            self._copy_l1doctests = sorted_failed_tests
            self.update_tree_contents(sorted_failed_tests, clear_header=False, clear_errorview=False)
    
    def remove_sort_filter(self):
        """
        When invoking this method the treeview will restore 
        the original order of its rows.
        """
        def __is_verdicts_copy_equals_to_original():
            if len(self._copy_l1doctests) != len(self._origin_l1doctests):
                return False
            c_names = [c_l1doctest.get_name() for c_l1doctest in self._copy_l1doctests]
            for o_l1doctest in self._origin_l1doctests:
                c_index = c_names.index(o_l1doctest.get_name())
                c_l1doctest = self._copy_l1doctests[c_index]
                if len(c_l1doctest.get_examples()) != len(o_l1doctest.get_examples()): 
                    return False 
            return True
        if not self.is_empty(): # on met à jour que si la treeview possède des éléments
            if __is_verdicts_copy_equals_to_original():
                self._copy_l1doctests = self._origin_l1doctests
            self.update_tree_contents(self._copy_l1doctests, clear_header=False, clear_errorview=False)
    
    def show_only_red_tests(self):
        from copy import deepcopy
        red_verdicts = (FailedVerdict, FailedWhenExceptionExpectedVerdict, ExceptionVerdict)
        
        only_reds = []
        for l1doctest in self._copy_l1doctests:
            if l1doctest.get_flag() == L1DocTestFlag.FAILED_FLAG:
                red_examples = l1doctest.filter_examples_by_verdicts(red_verdicts)
                new_l1doctest = deepcopy(l1doctest)
                new_l1doctest.set_examples(red_examples)
                only_reds.append(new_l1doctest)
                            
        if not self.is_empty(): # on met à jour que si la treeview possède des éléments
            self._copy_l1doctests = only_reds if only_reds else self._copy_l1doctests
            self.update_tree_contents(self._copy_l1doctests, clear_header=False, clear_errorview=False)
       
    def show_all_tests(self):
        self._copy_l1doctests = self._origin_l1doctests
        self.update_tree_contents(self._copy_l1doctests, clear_header=False, clear_errorview=False)
        
    
    def __group_by_verdicts(self, l1doctests: List[L1DocTest], status_order: List[L1DocTestFlag]=None) -> Dict[L1DocTestFlag, List[L1DocTest]]: 
        """
        Group l1doctests by status and order the statuses according to the provided 
        status order.
        
        :param status_order: A list of L1DocTestFlag that specifies the order in which 
        to group the verdicts by flag.
        :return: A dictionary of verdicts grouped by status.
        """
        status_groups:Dict[L1DocTestFlag, List[L1DocTest]] = {}
        for l1doctest in l1doctests:
            status = l1doctest.get_flag()
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(l1doctest)

        if status_order is None:
            status_order = L1DocTestFlag.get_priorities()
        
        # mettre en ordre les catégories selon l'ordre défini par le paramètre `status_order`
        ordered_groups = {}
        for status in status_order:
            if status in status_groups:
                ordered_groups[status] = status_groups[status]
        status_groups = ordered_groups
        
        return status_groups
    
    def group_by_verdicts(self):  
        grouped = self.__group_by_verdicts(self._origin_l1doctests)
        if not self.is_empty(): # on met à jour que si la treeview possède des éléments
            self.clear_tree(clear_all=False) 
            for status, l1doctests in grouped.items():
                row_id = self.treeview.insert(parent='', index="end", text=status.short_name(), open=status.is_failing(), 
                                         tags=(status.get_color(),))
                self.__add_verdicts_to_treeview(l1doctests, row_id)
        
    def expand_rows(self, event=None): 
        """ Spreads the function rows and the red tests. """
        self.__apply_row_change(False, get_option(OPEN_RED_TEST_ROWS))
    
    def fold_rows(self, event=None):
        """ Folds only the function rows """
        self.__apply_row_change(True, get_option(OPEN_RED_TEST_ROWS)) 
    
    def __apply_row_change(self, close_func_rows:bool, expand_red_tests:bool):
        """
        This function is used to expand or fold the rows of the treeview.
        It applies the new values of the args `close_rows` and `expand_red_tests` to
        the options `CLOSE_ALL_ROWS` and `OPEN_RED_ROWS` respectively. Then, it calls
        the method `update_tree_contents()` to update the treeview.

        Args:
            close_func_rows (bool): If True, the function rows will be folded. 
            expand_red_tests (bool): If True, the red tests will be expanded.
        """
        if not self.is_empty(): # on met à jour que si la treeview possède des éléments
            from copy import copy
            # on sauvegarde les valeurs initiales des options
            orig_red_tests = copy(get_option(OPEN_RED_TEST_ROWS))
            orig_close_rows = copy(get_option(CLOSE_FUNCTION_ROWS))
            
            # on applique les nouvelles valeurs aux options
            set_option(OPEN_RED_TEST_ROWS, expand_red_tests)
            set_option(CLOSE_FUNCTION_ROWS, close_func_rows)
            
            # update_tree invoque dynamiquement la valeur des options
            self.update_tree_contents(self._copy_l1doctests, clear_header=False, clear_errorview=False)
            
            # on restaure les valeurs initiales des options
            set_option(OPEN_RED_TEST_ROWS, orig_red_tests)
            set_option(CLOSE_FUNCTION_ROWS, orig_close_rows)
    
    def increase_row_height(self, event=None):
        if not self.is_empty():
            current_height = self.get_current_rowheight()
            self.update_row_height(current_height+1)
    
    def decrease_row_height(self, event=None):
        if not self.is_empty():
            current_height = self.get_current_rowheight()
            max_lines = self.get_max_lines()
            opt = self.__compute_optimal_height(max_lines, SMALL_MARGIN)
            if current_height > opt:
                self.update_row_height(current_height-1) 

    def update_row_height(self, rowheight:int=None):
        """
        Updates the height of a row in the treeview.
        """
        rowheight = rowheight if rowheight else self.get_current_rowheight()
        self.style.configure("Treeview", rowheight=rowheight) 
    
    def get_current_rowheight(self):
        """
        Returns the current height of a row in the treeview.
        """
        return self.style.lookup("Treeview", 'rowheight')    
    # -------------------------------------------
    # Fin des fonction pour le Header du treeview
    # ------------------------------------------
    
    def observe_font_changing(self, event=None):
        """
        Changes the font of the treeview.
        """
        self.__update_tree_font(get_font_family_option(), 
                                get_font_size_option())
        self.change_header_font() 
        self.__wrap_tree_content()
        error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
        error_view.update_font()
     
    def change_header_font(self, header_font_size=11):
        self.header_bar.config(font=(get_font_family_option(), header_font_size))
        self.resize_header_bar()
    
    def __update_tree_font(self, font_family, font_size):
        """
        Applies the new font to the treeview.
        """
        self.style.configure("Treeview", justify="left", font=(font_family, font_size), wrap=tk.WORD)  
        self.treeview.tag_configure("exception_as_link", font=tk_font.Font(underline=True, family=font_family, size=font_size))
    
    def __wrap_tree_content(self, event=None, margin=NORMAL_MARGIN):
        """
            This function wraps the text of treeview to follow its width.
        """
        widget = event.widget if event else self.treeview
        if (isinstance(widget, ttk.Treeview)): 
            view = self.workbench.get_view(self.__class__.__name__)
            if view.winfo_ismapped() :  
                if not self.is_empty():
                    width = view.winfo_width()
                    if self.__width_is_changed(width): # on ne met à jour que si la hauteur de la treeview n'a pas changé        
                        chars_per_pixels = width // get_font_size_option() 
                        visible_nodes = self.get_all_tree_childrens()
                        longest_length = self.__update_wrapped_texts(visible_nodes, chars_per_pixels)
                        new_rowheight = self.__compute_optimal_height(longest_length, margin)
                        self.update_row_height(new_rowheight)
                    self.__old_width = width
    
    def __width_is_changed(self, width):
        """
        Returns True if the height of the treeview hasn't changed.
        """
        return self.__old_width != width
    
    def get_all_tree_childrens(self):
        """
        Gets recursivly all the childrens of the given node of the treeview. 
        
        Note: This function is a generator. It yields the childrens of the given node 
        one by one. This is useful to not load all the childrens in memory at once after
        each update of the treeview.
        
        Keep this method as a generator to avoid performance issues on th GUI. 
        It's observed that thonny's IDE is more faster when the treeview is 
        updated with a generator.
        """
        def _all_childrens(treeview: ttk.Treeview, node: str = None):
            child = treeview.get_children(node)
            for sub_child in child: 
                if treeview.item(sub_child)["open"]:
                    yield from _all_childrens(self.treeview, sub_child)
                yield sub_child  

        yield from _all_childrens(self.treeview)

    def __update_wrapped_texts(self, nodes, chars_per_pixels:int) -> int:
        """
        Met à jour le wrapping des textes des nœuds spécifiés dans la Treeview.
        Return the longest wrapped line of the treeview.
        Returns the number of lines of the longest wrapped line of the treeview.
        """
        max_lines = 1
        for node in nodes:
            text = self.treeview.item(node, "text")
            wrapped_text = wrap(text, chars_per_pixels)
            
            num_lines = wrapped_text.count("\n") + 1
            if num_lines > max_lines:
                max_lines = num_lines
                
            self.treeview.item(node, text=wrapped_text)
        self.__max_lines = max_lines
        return self.__max_lines
    
    def __compute_optimal_height(self, max_lines:int=None, margin=NORMAL_MARGIN):
        """
            Uses the default font metrics to calculate the optimal row height.
            The default font metrics is multiplied by the given `max_lines`.
            
            Args:
                max_lines(int): The number of lines of the longest row in the treeview.
            Return:
                (int): The new height.
        """
        row_height = get_font_size_option() * 2     # multiply by 2 to handle the line spacing
        opt_height = max_lines * (row_height * margin) if max_lines else row_height
        return round(opt_height)
    
    def update_tree_contents(self, l1doctests:List[L1DocTest], parent="", clear_errorview=True, clear_header=True):
        """
            This function contructs and inserts the rows into the treeview.
        """
        self.__old_width = self.workbench.get_view("L1TestTreeView", False).winfo_width() if self.__old_width > 0 else -1
        
        self._restore_row_selection_effect() 
        self.clear_tree(clear_all=clear_header, clear_errorview=clear_errorview)
    
        if not self.__check_if_editor_is_open():
            return
        
        if not l1doctests:
            self.insert_in_header("No test found !", image="warning.png", clear=True, tags=("orange",))
            return
        
        self.enable_menu()
        self.__add_verdicts_to_treeview(l1doctests, parent)
        
        # on insère le summarize dans le header bar que si la treeview n'est pas vide
        if not self.is_empty() and clear_header:
            # We build the summarize object 
            summarize: Summarize = self.build_summarize_object(self._origin_l1doctests)
            # We insert the summarize infos into the header bar of the treeview
            self.insert_summarize_in_header_bar(summarize, self.header_bar)
            self.change_header_font() 
        
        self.update_row_height()
            
    def __add_verdicts_to_treeview(self, l1doctests:List[L1DocTest], parent=""):
        o_names = [c_l1doctest.get_name() for c_l1doctest in self._origin_l1doctests]
        
        for l1doctest in l1doctests:
            o_index = o_names.index(l1doctest.get_name())
            current_node = self._add_node_to_tree(self._origin_l1doctests[o_index], parent)
            if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG:
                self.treeview.insert(current_node, "end", values=l1doctest.get_node_lineno(), 
                                     text="No tests found", tags=("nonClickable", l1doctest.get_flag().get_color()))
            else:    
                self._add_verdicts_to_node(current_node, l1doctest.get_examples())
         
        self.__wrap_tree_content()
    
    def _add_node_to_tree(self, l1doctest: L1DocTest, parent=""):  
        flag: L1DocTestFlag = l1doctest.get_flag()
        open = get_option(OPEN_ONLY_RED_FUNCTIONS) and not get_option(CLOSE_FUNCTION_ROWS) \
                if get_option(OPEN_ONLY_RED_FUNCTIONS) and flag.is_failing() \
                else not get_option(OPEN_ONLY_RED_FUNCTIONS) and not get_option(CLOSE_FUNCTION_ROWS) 
        verdict_config = dict(text=self._get_l1doctest_stats(l1doctest),  
                              image=self.get_icon(flag.get_image_basename()), 
                              open=open)
        return self.treeview.insert(parent, "end", values=l1doctest.get_node_lineno(), tags=(CLICKABLE_TAG,), **verdict_config)
    
    def _add_verdicts_to_node(self, current_node:str, examples:list[Example]):
        """ 
        This function adds to the treeview all the rows that correspond 
        to the given ast node.
        """
        def __add_as_many_rows_as_text_lines(parent, text:str, lineno:int, tags:str):
            """
            Adds the necessary rows of each text to be inserted in the treeview.
            An exception message can be reported on several line, so we should 
            add as many rows as text lines. 
            """
            for line in text.splitlines():
                self.treeview.insert(parent, "end", text=line, values=lineno, tags=tags)

        verdicts_map = {
            FailedVerdict: (FAILED_RED_CHIP, False), # False means that the verdict is not an exception
            ExceptionVerdict: (EXCEPTION_RED_CHIP, True),
            PassedVerdict: (SUCCESS_GREEN_CHIP, False),
        }

        for example in examples:
            verdict = example.get_verdict()
            verdict_tags = (verdict.get_color(), CLICKABLE_TAG)
            item_text = str(verdict)

            for verdict_type, (icon, is_exception) in verdicts_map.items():
                if isinstance(verdict, verdict_type) and not isinstance(verdict, PassedSetupVerdict):                
                    if is_exception:
                        values = [verdict.get_lineno(), verdict.__class__.__name__, verdict.get_details()] 
                        verdict_tags += ("exception_as_link", "lightred" if get_option(HIGHLIGHT_EXCEPTIONS) else "")
                    else:
                        values = [verdict.get_lineno()]
                    # on insère le test dans la treeview   
                    current_test = self.insert_into_treeview(current_node, item_text, values, 
                                                        verdict_tags, icon, open=get_option(OPEN_RED_TEST_ROWS))
                    # on configure les tags pour insérer les détails de l'exception
                    if isinstance(verdict, FailedVerdict):
                        verdict_tags = (verdict_tags[0], "nonClickable")

                    if not is_exception:
                        __add_as_many_rows_as_text_lines(current_test, verdict.get_details(), verdict.get_lineno(), tags=verdict_tags)
                    break
    
    def insert_into_treeview(self, node="", text="", values=[], tags=(), image="", open=False):
        return self.treeview.insert(node, "end", text=text, values=values, 
                                    image=self.get_icon(image), tags=tags, open=open)
            
    def __check_if_editor_is_open(self) -> bool:
        """
            Returns True if an editor is already opened in thonny. 
            Otherwise, returns False 
        """
        return False if not self.workbench.get_editor_notebook().get_current_editor() else True
    
    def _get_l1doctest_stats(self, l1doctest: L1DocTest):
        """
        Get a string that represents how many tests are passed of the given l1doctest. 
        If the l1docstest is empty, returns only the name of the l1doctest.
        """
        # The first space is necessary so that all text will be aligned
        if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG:
            return " %s" % l1doctest.get_name()
        return " %s ~ %s/%s passed" %(l1doctest.get_name(), l1doctest.count_passed_tests(), l1doctest.count_tests())
        
    def insert_summarize_in_header_bar(self, summarize:Summarize, view: tktextext.TweakableText):
        """
        Builds the summarize test to be inserted in the header of the treeview.
        
        Args:
            summarize (Summarize): a named tuple that contains the summarize infos.
        """
        tests_run = "Tests run: %s\n" % summarize.total
        view.direct_insert("end", tests_run)
        
        insert_label = lambda label, color : view.direct_insert("end", label, tags=(color,)) 
        insert_how_many = lambda how_many, is_last=False: view.direct_insert("end", f"{how_many}" if is_last else f"{how_many}, ")
      
        insert_label("Success: ", "green")
        insert_how_many(summarize.success)
        
        insert_label("Failures: ", "darkred")
        insert_how_many(summarize.failures)
        
        insert_label("Errors: ", "darkred")
        insert_how_many(summarize.errors)
        
        insert_label("Empty: ", "orange")
        insert_how_many(summarize.empty, is_last=True)
            
    def build_summarize_object(self, l1doctests:List[L1DocTest]) -> Summarize:
        """
        Builds the summarize informations. 
        The summarize contains :
            - Total number of executed tests.
            - How many succeed tests, failed tests, error tests and empty tests.
        
        Args:
            results (List[L1DocTest]): all the l1doctests that have been evaluated.

        Returns:
            Summarize: a namedtuple that represents the summarize object.
        """       
        success = sum([l1doctest.count_passed_tests() for l1doctest in l1doctests])
        failures = sum([l1doctest.count_failed_tests() for l1doctest in l1doctests])
        errors = sum([l1doctest.count_error_tests() for l1doctest in l1doctests])
        empty = sum([1 for l1doctest in l1doctests if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG])
        total = success + failures + errors
        return Summarize(total, success, failures, errors, empty)
                   
    def clear_tree(self, clear_verdicts_data=False, clear_all=True, clear_errorview=False):
        """Clears the treeview by deleting all items. This method is called by
        the `update_tree_contents` method to clear the treeview before inserting
        the new rows.
        
        Note: this method is also called when the button `clear` is clicked. In 
        this case, the `event` is not None, then the original/copy lists of l1doctests
        will be cleared. Finally, the treeview or/and header or/and the errorview 
        will be cleared.
        
        Args:
            clear_verdicts_data: If true, the original and copy lists of l1doctests will be cleared.
            This argument is set to True when the button `clear` is clicked.
            clear_all: If True, the treeview and its header will be cleaned.
            clear_errorview: if True, the error view will be cleaned.            
        """
        if clear_verdicts_data: # si l'event est déclenché par le bouton `clear` alors on vide les listes
            from thonnycontrib.l1test_frontend import get_l1test_runner
            self._origin_l1doctests.clear()
            self._copy_l1doctests.clear()
            clear_errorview = True
            get_l1test_runner().set_has_exception(False)
        if clear_all:
            self.clear_header_bar()  # on supprime le contenu du header
        if clear_errorview:
            error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
            error_view.clear()
        self.treeview.delete(*self.treeview.get_children())
        self.__init_special_attributes()
        self.disable_menu()
        
    def clear_header_bar(self):
        """Clears the header of the treeview."""
        if self.header_bar:
            self.header_bar.direct_delete("1.0", "end")
            self.resize_header_bar()
    
    def _remove_highlight_selection_effect(self, event=None):
        """
        This function remove the selection effect. When a treeview's row is selected
        it removes the highlight effect on the selected row. So the selected row 
        will look like it is not selected.
        """
        self.style.map('Treeview', background=[], foreground=[])
    
    def _highlight_line_on_editor(self, lineno:int, editor: CodeView):
        """Highlights the line in the editor that corresponds to the selected row in the treeview.

        Args:
            lineno (int): the line number to highlight.
            editor (CodeView): the editor where the line will be highlighted.
        """
        index = editor.text.index(str(lineno) + ".0")
        editor.text.see(index)  # make sure that the double-clicked item is visible
        editor.text.select_lines(lineno, lineno)
    
    def _restore_row_selection_effect(self):
        """
        This function show the selection effect. When a treeview's row is selected
        it shows the highlight effect on the selected row. 
        """
        self.style.map('Treeview', 
                       background=[('selected', 'focus', '#ADD8E6'), ('selected', '!focus', '#D3D3D3')], 
                       foreground=[('selected', 'focus', 'black'), ('selected', '!focus', 'black')])

    
    def _on_select(self, event=None):
        """
        When a row is selected this function will be triggered. This function highlights 
        the line in the editor that corresponds to the seelcted row in the treeview. 
        """
        self._restore_row_selection_effect()
        editor = self.workbench.get_editor_notebook().get_current_editor()
        if editor:
            code_view = editor.get_code_view()
            focus = self.treeview.focus()
            if not focus: 
                return

            item = self.treeview.item(focus)
            values = item["values"]
            if not values:
                return
                
            if ExceptionVerdict.__name__ in values:
                # side_by_side=True means that the error view will be displayed side by side with the treeview
                self.workbench.event_generate(L1TREE_VIEW_EVENT, error_title=item["text"],
                                                error_msg=values[-1], side_by_side=True) 
                self.treeview.focus_set()
                        
            lineno = values[0]
            self._highlight_line_on_editor(lineno, code_view)
            self.workbench.event_generate(
                "OutlineDoubleClick", item_text=self.treeview.item(self.treeview.focus(), option="text")
            )

    def disable_menu(self):
        """disable the menu button of the treeview"""
        self.menu_button.state([tk.DISABLED])
        
    def enable_menu(self):
        """enable the menu button of the treeview"""
        self.menu_button.state(["!disabled"])
     
    def insert_in_header(self, text, image:str|tk.PhotoImage=None, clear=False, tags=tuple()):
        """ 
        Inserts text in the header of the treeview. 
        Args:
            text: the text to insert
            image: the basename with it's extension of an image to insert. 
            For example: "info.png". The image must be in the folder `docs/res`.
            clear: if True, the header will be cleared before inserting the text
            tags: the tags to apply to the text. For example: ("red",)
        """
        if clear:
            self.header_bar.direct_delete("1.0", tk.END)
        if image:
            if isinstance(image, str):
                image = self.get_icon(image)
            self.header_bar.image_create(tk.END, image=image)
            text = " " + text # add a space after the image
        self.header_bar.direct_insert(tk.END, text, tags=tags)
        self.resize_header_bar()
           
    def is_empty(self):
        return len(self.treeview.get_children()) == 0
    
    def is_header_bar_cleared(self): 
        return not self.header_bar.get("1.0", tk.END).strip("\n")    
    
    def hide_view(self):
        self.workbench.hide_view(self.__class__.__name__)
    
    def show_view(self):
        self.workbench.show_view(self.__class__.__name__)
        
    def set_verdicts(self, verdicts: List[L1DocTest]):
        self._origin_l1doctests = verdicts
        self._copy_l1doctests = self._origin_l1doctests.copy()
    
    def get_original_verdicts(self):
        """ Returns the original list of all l1doctests. """
        return self._origin_l1doctests
    
    def get_copy_verdicts(self):
        """ Returns the copy list of all l1doctests. """
        return self._copy_l1doctests
    
    def get_treeview(self):
        return self.treeview
    
    def get_icon(self, ref_name:str):
        """
        Returns the image reference saved in the treeview. Returns None if the 
        image reference is not found.
        """
        if ref_name in self.image_references:
            return self.image_references[ref_name]
        return None
    
    def get_max_lines(self):
        """Returns the maximum number of lines of the longest wrapped line of the treeview."""
        return self.__max_lines
