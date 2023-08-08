import re
import sys
import textwrap
from typing import List

from .doc_template import DocTemplate
from ..backend.ast_parser import L1TestAstParser
from .doc_template import *
from ..properties import CANNOT_GENERATE_THE_DOCSTRING
from thonny.tktextext import *  
from ..exceptions import DocGeneratorParserException, FrontendException, NoFunctionSelectedToDocumentException
from ..utils import replace_error_line, get_last_exception
from thonny.editors import EditorCodeViewText
from ..ThonnyLogsGenerator import log_doc_in_thonny
from thonny import get_workbench
from .. l1test_frontend import get_l1test_runner
from thonnycontrib import docstring_generator

r""" Docstring Generator Module
Description:
------------
This module generates a docstring using the templates.

For a selected line the `DocGenerator` tries to verify if the selected line
corresponds to a function signature. If the selected line is a function 
signature so a the `DocGenerator` will build a custom function with the given
selected line and then it parses(with AST parser) this function. If the AST parser
fails so the error will be displayed in the ErrorView. otherwise, the docstring
will be generated.

About templates, the docstring generator invokes the `DefaultDocTemplate` by default. 
The `DocTemplate.DefaultDocTemplate` class contains an implementation 
of a default template. 

How to use the Generator in thonny IDE:
---------------------------------------
- Right click on a function or a class declaration(it's prototype) and choose 
in the `edit menu` ~Generate Docstring~ button. You can also select the short cut 
Alt+d after putting the cursor on the function(or a class) declaration.

- Just a return on a function declaration will generate its docstring.
"""

class DocParser:
    def __init__(self, filename="", source=""):
        self._filename = filename
        self._source = source
    
    def parse_source(self, error_line:int=None):
        """
        Parses the given `source` and returns a list of 
        AST nodes that may contains a doctsring.
        
        As the AST python module stated in its documentation, the AST nodes that can 
        contain a dosctring are reported at ~SourceParser.SUPPORTED_TYPES~.
        
        Args:
            error_line(int): Set it only if you want to change the error line in 
            the raised exception. If `None`, so the error line mentioned in the error will 
            be kept. 
        
        Raises:
            DocGeneratorParserException: if the ast parser is failed.
        """
        try :
            parsed = ast.parse(self._source, self._filename, mode="single").body
            return parsed[0] if len(parsed) == 1 else None
        except Exception as e: # if a compilation error occurs during the parsing
            error_info = sys.exc_info()
            last_exception = get_last_exception(error_info)
            if error_line:
                last_exception = replace_error_line(last_exception, error_line)
            raise DocGeneratorParserException(last_exception)    
    
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
    
    def set_source(self, source: str):
        self._source = source
        
    def get_source(self):
        return self._source 
    
    def set_ast_parser(self, parser) :
        self._ast_parser = parser

class DocGenerationStrategy(ABC):
    _SIGNATURE_REGEX = r"\s*(?P<id>def|class)\s*.*\s*$"
    
    def __init__(self, text_widget:EditorCodeViewText, parser:DocParser=DocParser()):
        self._parser = parser 
        self._text_widget = text_widget
    
    @abstractmethod
    def can_generate(self, selected_lineno:int) -> bool:
        pass
    
    @abstractmethod
    def generate(self) -> None:
        pass
    
    def _generate(self, signature:str, selected_lineno:int=None) -> str:   
        """Generate a docstring from a given signature (or prototype).
        
        Args:
            - signature(str): The signature for which the docstring will be generated.
            The signature should always be finished by a ":" caractere, otherwise the 
            docstring not will be generated. 
            - selected_lineno(int, Optional): This parameter is optional. It is the line number
            of the signature. This will be usefull for errors raised by the AST parser.
            If the ast parser raises an exception, the line number of the exception will be set to
            the given lineno.
            - text_widget(EditorCodeViewText, Optional): The view in which the generated docstring will 
            be inserted. Set to `None` if you want just to get the generated docstring. If `None` the
            generated docstring will not be inserted in any widget.
        
        Return:
            str: returns the generated docstring.
        
        Raises:
            - NoFunctionSelectedToDocument: When a selected line don't corresponds to 
            a function declaration. 
            - DocGeneratorParserException: when the ast parser fails.
        """
        if signature is None: signature = ""
        
        # We should check that the line is a function declaration and that ends with ':' character. 
        declaration_match = re.match(self._SIGNATURE_REGEX, signature)

        if not declaration_match:
            raise NoFunctionSelectedToDocumentException("No signature is selected to document!\n")
        else:   
            id_signature = declaration_match.group("id") # c'est le tag <id> dans l'expression régulière
            
            template:DocTemplate = DocTemplateFactory.create_template(id_signature) 
            
            generated_temp = self.__get_generated_template(template, signature, selected_lineno)
            
            indent = self.__compute_indent(signature)
            generated_doc = textwrap.indent(generated_temp, indent)
            if self._text_widget:
                # c'est içi que la docstring est ajoutée à l'éditeur
                self._text_widget.insert(str(selected_lineno + 1) + ".0", generated_doc)
            return generated_doc
    
    def __get_generated_template(self, template:DocTemplate, signature:str, selected_lineno:int) -> str:
        """
        Creates a custom function with the given `signature` then parses this function and if the
        AST parser success so the docstring will be generated. If the AST parser fails, so the 
        reported exception will be raised.

        Args:
            signature (str): the signature for which the docstring will be generated.
            selected_lineno (int): the line that corresponds to the selected line. This arg is used 
            to change the error line in the reported exception to the given `selected_line`. Remember
            that the error line will be always "1" if the ast parser fails, because the parsed source
            contains only the custom function.
            
        Returns:
            (str): The generated template.
            
        Raises: 
            DocGeneratorParserException: when the ast parser fails.
        """
        # The approach is to take the signature of the selected function then
        # adds a custom body to this function.
        custom_func = self._create_custom_body(signature)
        
        # don't forgot that the result of parsing is a list of supported nodes
        # -> see the doc
        self._parser.set_source(custom_func)
        node = self._parser.parse_source(selected_lineno)
        
        # Generate an event in Thonny with l1test/ThonnyLogsGenerator.log_doc_in_thonny
        log_doc_in_thonny(node)
        
        return template.get_template(node)

    def __compute_indent(self, signature:str) -> int:
        """
        Get the indentation based on the whitespaces located in the given `signature`.

        Args:
            signature (str): a signature of a function

        Returns:
            int: returns the indentation based on the whitespaces located in the given `signature`.
        """
        space_match = re.search("^(\s+)", signature)
        python_indent = 4
        sig_indent = len(space_match.group(1)) if space_match else 0
        return " " * (sig_indent + python_indent)
    
    def _create_custom_body(self, signature:str):
        signature = signature.strip()
        # on supprime tous ce qu'il vient après les ":" dans la signature. Car, on veut juste la signature.
        # En python on peut avoir une syntaxe comme : def foo(): pass, cela pose problème pour l'ast parser
        # il faut donc qu'on ait juste la signature sans le corps de la fonction.
        signature = re.sub(r"\s*(?P<id>def|class)(?P<signature>\s*.*\s*:)(?P<body>\s*.*)$", r"\g<id>\g<signature>", signature)
        indent = " " * 4
        return signature + "\n" + indent + "pass"
    
    def set_parser(self, parser: DocParser):
        self._parser = parser
        
    def get_parser(self):
        return self._parser
    
    def set_filename(self, filename):
        self._parser.set_filename(filename)
        
    def set_text_widget(self, text_widget:EditorCodeViewText):
        self._text_widget = text_widget
    
class AutoGenerationStrategy(DocGenerationStrategy):
    def __init__(self, text_widget:EditorCodeViewText=None, parser=DocParser()):
        super().__init__(text_widget, parser)
        self.__selected_sig = None
        self.__selected_lineno = None
    
    def can_generate(self, selected_lineno:int) -> bool:
        selected_sig = self._text_widget.get(str(selected_lineno)+".0", str(selected_lineno+1)+".0").strip().strip("\n")
        if selected_sig != "":
            self.__selected_sig = selected_sig
            self.__selected_lineno = selected_lineno
        return self.__selected_sig != ""
    
    def generate(self):
        return super()._generate(self.__selected_sig, self.__selected_lineno)
        
class ManualGenerationStrategy(DocGenerationStrategy):
    _OUTLINER_REGEX = r"\s*(?P<type>def|class)[ ]+(?P<name>[\w]+)"
    
    def __init__(self, text_widget:EditorCodeViewText=None, parser=DocParser()):
        super().__init__(text_widget, parser)
        self.__nodes: List[SourceNode] = []
        self.__selected_node = None
    
    def can_generate(self, selected_lineno:int) -> bool:
        self.__nodes = self.__parse(self._text_widget.get("1.0", "end"))
        self.__selected_node = next((node for node in self.__nodes if node.get_starting_lineno() <= selected_lineno <= node.get_ending_lineno()), None)
        return self.__selected_node is not None
    
    def generate(self) -> str:
        return super()._generate(self.__selected_node.get_signature(), self.__selected_node.get_starting_lineno())
     
    def __parse(self, source:str) :
        """
        Parses a source and returns a list of the outlined nodes. 
        The outlined nodes are either a class or a function. For 
        each outlined node an object of type `OutlinedNode` is built 
        in which we store the type (class/function), the name and the lineno
        of the outlined node.
        """
        current_node = None
        lines = source.splitlines()
        lineno = 1
        last_non_empty_line = None
        for line in lines:
            match = re.match(self._OUTLINER_REGEX, line)
            if match:
                # If there was a previous outlined node, set its ending lineno.
                if current_node:
                    current_node.set_ending_lineno(last_non_empty_line or current_node.get_starting_lineno())
                    yield current_node

                # Create a new outlined node.
                current_node = SourceNode(line, lineno, None)
                last_non_empty_line = None  # Reset the last_non_empty_line for the new node.

            elif line.strip():
                last_non_empty_line = lineno  # Update last_non_empty_line.

            lineno += 1

        # Set the ending lineno for the last outlined node.
        if current_node:
            current_node.set_ending_lineno(last_non_empty_line or current_node.get_starting_lineno())
            yield current_node
    
    def get_nodes(self):
        return self.__nodes
        
class SourceNode():
    """
    This class represents an outlined node. An outlined node is either a class or a function.
    """ 
    def __init__(self, signature:str, starting_lineno:int, ending_lineno) -> None:
        self.__signature = signature
        self.__starting_lineno = starting_lineno
        self.__ending_lineno = ending_lineno
        
    def get_starting_lineno(self):
        return self.__starting_lineno  
    
    def get_ending_lineno(self):
        return self.__ending_lineno
    
    def set_ending_lineno(self, ending_lineno):
        self.__ending_lineno = ending_lineno
        
    def set_signature(self, signature):
        self.__signature = signature
    
    def get_signature(self):
        return self.__signature
    
    def __str__(self) -> str:
        return f"signature: {self.__signature}, s_lineno: {self.__starting_lineno}, e_lineno: {self.__ending_lineno}" 
    
    
class DocGenerator():
    def __init__(self, strategy:DocGenerationStrategy=AutoGenerationStrategy()):
        docstring_generator._doc_generator = self
        self._has_exception = False 
        self._strategy = strategy
   
    def run(self, selected_lineno:int, text_widget:EditorCodeViewText):
        try:
            self.__run(selected_lineno, text_widget)
        except NoFunctionSelectedToDocumentException as e:
            pass # do nothing
        except FrontendException as e: # parsing error
            self.set_has_exception(True)
            self._show_error(str(e))

    def __run(self, selected_lineno:int, text_widget:EditorCodeViewText):
        self._strategy.set_text_widget(text_widget)
        if self._strategy.can_generate(selected_lineno):
            filename = get_workbench().get_editor_notebook().get_current_editor().get_filename()
            if not filename:
                filename = "<unknown>" 
                    
            self._strategy.set_filename(filename)
            self._strategy.generate()   
            
            # après la génération (réussie) on vérifie si docgen avait rencontré une exception avant. Si oui, 
            # on supprime l'exception de docgen (car elle a été déja montrée).
            if get_l1test_runner().has_exception() or self.has_exception(): # si docgen avait lancé une exception avant
                # si les deux ont lancé une exception, on affiche l'exception de docgen
                if get_l1test_runner().has_exception() and self.has_exception(): 
                    get_l1test_runner().clean_error_view()
                    get_l1test_runner().get_reporter().get_error_view().hide_view()
                    get_l1test_runner().get_reporter().get_treeview().show_view()
                else:
                    self._show_treeview()
                
                self.set_has_exception(False) # success
    
    def _show_treeview(self):
        """
        Cleans the ErrorView and hides it. Retreives the Treeview and shows it.
        """
        get_l1test_runner().hide_errorview_and_show_treeview()
    
    def _show_error(self, error_msg:str, error_title:str=CANNOT_GENERATE_THE_DOCSTRING):
        """
        Shows the error in the ErrorView if the docstring generator raises an exception.
        """
        l1test_runner = get_l1test_runner()
        if self.has_exception():
            l1test_runner.show_errors(exception_msg=error_msg, title=error_title)
            l1test_runner.get_reporter().get_error_view().show_view() 
            l1test_runner.get_reporter().get_treeview().hide_view()     
        
    def has_exception(self):
        return self._has_exception
    
    def set_has_exception(self, has_exception: bool):
        self._has_exception = has_exception
        
    def get_strategy(self):
        return self._strategy
    
    def set_strategy(self, strategy: DocGenerationStrategy):
        self._strategy = strategy