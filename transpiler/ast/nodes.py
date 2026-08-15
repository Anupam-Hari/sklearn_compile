from dataclasses import dataclass, field


@dataclass
class ImportNode:
    module: str
    names: list[str] = field(default_factory=list)


@dataclass
class FunctionNode:
    name: str


@dataclass
class ClassNode:
    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionNode] = field(default_factory=list)


@dataclass
class ModuleNode:
    imports: list[ImportNode] = field(default_factory=list)
    classes: list[ClassNode] = field(default_factory=list)
    functions: list[FunctionNode] = field(default_factory=list)