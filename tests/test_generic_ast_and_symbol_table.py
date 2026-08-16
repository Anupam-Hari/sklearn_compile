from transpiler.ast.nodes import ASTNode, ModuleNode, FunctionNode, ClassNode, VariableNode, ReturnNode
from transpiler.dependency.symbol_table import SymbolTable
from transpiler.parser.tokenizer import TokenType, tokenize


def test_generic_ast_nodes():
    fn = FunctionNode(name="foo", attributes={"return_type": "int"})
    assert isinstance(fn, ASTNode)
    assert fn.node_type == "function"
    assert fn.name == "foo"
    assert fn.attributes["return_type"] == "int"

    cls = ClassNode(name="Splitter", children=[fn])
    module = ModuleNode(children=[cls])

    assert module.node_type == "module"
    assert module.children[0].name == "Splitter"
    assert module.children[0].children[0].name == "foo"


def test_tokenizer_tracks_indentation():
    tokens = tokenize("def foo():\n    x = 1\n    return x\n")
    names = [token.type for token in tokens]
    assert TokenType.KEYWORD in names
    assert TokenType.INDENT in names
    assert TokenType.DEDENT in names


def test_symbol_table_tracks_members_and_methods():
    table = SymbolTable()
    table.add_class("Splitter", members={"criterion": "float", "n_features": "int"})
    table.add_method("Splitter", "node_split", return_type="void")

    assert table.classes["Splitter"].members["criterion"] == "float"
    assert table.classes["Splitter"].methods["node_split"] == "void"
