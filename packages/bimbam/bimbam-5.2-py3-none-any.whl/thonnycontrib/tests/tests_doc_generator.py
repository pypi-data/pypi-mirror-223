import unittest as ut
from thonnycontrib.docstring_generator.doc_generator import *

class MockDocGeneratorStrategy(DocGenerationStrategy):
    def __init__(self):
        super().__init__(text_widget=None)
        
    def can_generate(self) -> bool:
        pass
    
    def generate(self) -> None:
        pass
    
class TestDocGenerator(ut.TestCase):
    def setUp(self):
        self.docGenerationStrategy = MockDocGeneratorStrategy()
    
    def tearDown(self) -> None:
        del self.docGenerationStrategy
    
    def test_doc_generator_when_ok(self):
        signature = "def func():"
        generated = self.docGenerationStrategy._generate(signature)
        
        self.assertTrue(len(generated) > 0)
        
        expected_doc = \
'''\
    """x_résumé_x

    Paramètres :
    Valeur de retour () :
    Contraintes d'utilisation : 
    Exemples :
    $$$ 

    """
'''
        self.assertTrue(generated == expected_doc)
    
    def test_doc_generator_typing_support_case_1(self):
        arg_type, r_type = "str", "int"
        signature = "def func(a: %s) -> %s:" % (arg_type, r_type)
        generated = self.docGenerationStrategy._generate(signature)
        
        self.assertTrue(len(generated) > 0)
        self.assertTrue(arg_type in generated)
        self.assertTrue(r_type in generated)
    
    def test_doc_generator_typing_support_case_2(self):
        arg_type = "str"
        signature = "def func(a: %s):" % arg_type
        generated = self.docGenerationStrategy._generate(signature)
        
        self.assertTrue(len(generated) > 0)
        self.assertTrue(arg_type in generated)
    
    def test_doc_generator_when_syntax_error(self):
        signature = "def func):"
       
        with self.assertRaises(DocGeneratorParserException) as e:
            self.docGenerationStrategy._generate(signature)
        
        raised_exception = e.exception      
        self.assertTrue(SyntaxError.__name__ in str(raised_exception))
        
    def test_doc_generator_when_signature_doesnt_finish_with_colon(self):
        signature = "def func()"
        
        with self.assertRaises(DocGeneratorParserException) as e:
            self.docGenerationStrategy._generate(signature)
        
        raised_exception = e.exception      
        self.assertTrue(SyntaxError.__name__ in str(raised_exception))
        self.assertTrue(SyntaxError.__name__+": expected ':'" in str(raised_exception))
        
if __name__ == '__main__':
    ut.main(verbosity=2)   