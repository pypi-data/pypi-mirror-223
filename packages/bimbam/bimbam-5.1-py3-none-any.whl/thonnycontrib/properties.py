PLUGIN_NAME = "L1Test"
DEBUG_NAME = "L1Test debugger"
ERROR_VIEW_LABEL = '%s errors' % PLUGIN_NAME

# ici vous pouvez changer la syntaxe du doctest. 
# version 2022 PJI : Actuellement on garde la syntaxe `$py`.
L1TEST_SYMBOL = "[$]py"
# version 2022 avant la rentrée
L1TEST_SYMBOL1 = "[$][$][$]"
L1TEST_SYMBOL2 = "[$]PY"
L1TEST_SYMBOL3 = "[$]py"
# L'invite des tests qui vérifient la levée d'exception
L1TEST_EXCEPTION_SYMBOL = "[$][$]e"


# ############################################################################################### #
#                       LES NOUVELLES VARIABLES VERSION 2023 PFE                                  #
# ############################################################################################### #

# Le nom de la commande magique pour l1test(doit toujours commencer par une majuscule)
BACKEND_COMMAND = "L1test"


# ############ Les noms des clés du dictionnaire renvoyé par le l1test_backend ############
# Le nom de l'attribut contenant les résulats des tests renvoyés par l1test_backend
VERDICTS = "verdicts"
# Le nom de l'attribut contenant une exception levée et renvoyée par l1test_backend
L1TEST_EXCEPTION = "l1test_exception"


# ############ Les labels des buttons du menu l1test treeview ############
PLACE_RED_TEST_ON_TOP_LABEL = "Place the red tests on the top"
RESUME_ORIGINAL_ORDER = "Resume original order"
SHOW_ONLY_RED_TESTS = "Show only red tests"
SHOW_ALL_TESTS = "Show all the tests"
GROUP_BY_VERDICTS = "Group by verdicts"
EXPAND_ALL = "Expand all"
FOLD_ALL = "Fold all"
UPDATE_FONT_LABEL = "Update the font"
INCREASE_SPACE_BETWEEN_ROWS = "Inrease row height"
DECREASE_SPACE_BETWEEN_ROWS = "Decrease row height"
CLEAR_LABEL = "Clear"

# Le message affiché sur la treeview quand `l1test` est en cours d'execution
L1TEST_IN_PROGRESS = "Executing tests in progress"

# the evaluation states
PENDING_STATE = "Pending" 
EXECUTED_STATE = "Executed" 
FINISHED_STATE = "Finished"

# The title of the error view when the docstring genertor shows the raised error
CANNOT_GENERATE_THE_DOCSTRING = "Cannot generate the docstring :"
# The title of the error view when the l1test shows the raised error
CANNOT_RUN_TESTS_MSG = "Cannot run %s :" %(PLUGIN_NAME)

# A special event that `L1TestTreeview` sends to `L1TestRunner` when clicking on an exception test
# The event transfers the details of the clicked exception to the `L1TestRunner` 
# which will show it in the error view.
L1TREE_VIEW_EVENT = "L1TreeviewEvent"

# Les images utilisées par la treeview
PENDING_ICON = "pending_icon.png"
ERROR_ICON = "error_icon.png"
RESTART_ICON = "restart_icon.png"
FAILED_RED_CHIP = "failed_red_chip.png" # le petit cercle rouge qui précède un test qui a échoué
EXCEPTION_RED_CHIP = "exception_red_chip.png" # le petit cercle rouge (avec un poitn d'exclamation) qui précède un test qui a échoué
SUCCESS_GREEN_CHIP = "success_green_chip.png" # le petit cercle vert qui précède un test qui a réussi