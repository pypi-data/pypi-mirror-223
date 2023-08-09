from thonny.config_ui import ConfigurationPage
from ..properties import PLUGIN_NAME
from thonny import get_workbench
from ..i18n.languages import tr

# Default config
DEFAULT_DOC_GENERATION_AFTER_RETURN = True
DEFAULT_IMPORT_MODULE_IN_SHELL = True
DEFAULT_CLOSE_FUNCTION_ROWS = False
DEFAULT_OPEN_RED_TESTS = False
DEFAULT_OPEN_ONLY_RED_FUNCTIONS = True
DEFAULT_HIGHLIGHT_EXCEPTIONS = False
DEFAULT_REPORT_EXCEPTION_DETAIL = True 
DEFAULT_MOVE_ERRORVIEW_TO_BOTTOM = False

# Option names
AUTO_GENERATON_DOC = "auto_generaton_doc"
IMPORT_MODULE = "import_module"
OPEN_RED_TEST_ROWS = "open_red_rows"
CLOSE_FUNCTION_ROWS = "close_function_rows"
OPEN_ONLY_RED_FUNCTIONS = "open_only_red_functions"
HIGHLIGHT_EXCEPTIONS = "highlight_exceptions"
REPORT_EXCEPTION_DETAIL = "exception_detail"
MOVE_ERRORVIEW_TO_BOTTOM = "move_errorview_to_bottom"

# Dict of options name and default value
OPTIONS = {
    AUTO_GENERATON_DOC : DEFAULT_DOC_GENERATION_AFTER_RETURN,
    IMPORT_MODULE : DEFAULT_IMPORT_MODULE_IN_SHELL,
    CLOSE_FUNCTION_ROWS: DEFAULT_CLOSE_FUNCTION_ROWS,
    OPEN_RED_TEST_ROWS : DEFAULT_OPEN_RED_TESTS,
    OPEN_ONLY_RED_FUNCTIONS : DEFAULT_OPEN_ONLY_RED_FUNCTIONS,
    HIGHLIGHT_EXCEPTIONS: DEFAULT_HIGHLIGHT_EXCEPTIONS,
    REPORT_EXCEPTION_DETAIL: DEFAULT_REPORT_EXCEPTION_DETAIL,
    MOVE_ERRORVIEW_TO_BOTTOM: DEFAULT_MOVE_ERRORVIEW_TO_BOTTOM
}

def init_options():
    """
    Initialise dans le workbench les options du plugin.
    """
    for opt in OPTIONS :
        if not get_workbench().get_option(opt) :
            get_workbench().set_default("%s." % PLUGIN_NAME + opt, OPTIONS[opt])

def get_option(name: str): 
    """
    Renvoie la valeur dans le workbench de l'option passée en paramètre.

    Paramètres:
    - name : le nom de l'option, tel que définie ds globals.py 
    """
    return get_workbench().get_option("%s." % PLUGIN_NAME + name)

def set_option(name, value):
    get_workbench().set_option("%s." % PLUGIN_NAME + name, value)

class L1TestConfigurationPage(ConfigurationPage):
    def __init__(self, master):
        ConfigurationPage.__init__(self, master)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, AUTO_GENERATON_DOC), 
                          tr("Generate the docstring automatically after a line break at a function name."))

        self.add_checkbox("%s.%s" % (PLUGIN_NAME, IMPORT_MODULE), 
                          tr("Import the module executed in the shell."))
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, CLOSE_FUNCTION_ROWS),
                          tr("Close all function lines in %s view.") % PLUGIN_NAME)
         
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, OPEN_ONLY_RED_FUNCTIONS),
                          tr("Open only red function lines in %s view.") % PLUGIN_NAME)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, OPEN_RED_TEST_ROWS), 
                          tr("Open failed tests in %s view.") % PLUGIN_NAME)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, HIGHLIGHT_EXCEPTIONS), 
                          tr("Highlight failed tests (only those that throw an exception)."))
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, MOVE_ERRORVIEW_TO_BOTTOM), 
                          tr("Place the error view at the bottom of the Thonny IDE (next to the `Shell` view). " + 
                             "By default, the error view is placed below the `L1Test` view."))
