from transpiler.parser.splitter_parser import parse_file

graph = parse_file(
    "examples/sample.py"
)

graph.dump()