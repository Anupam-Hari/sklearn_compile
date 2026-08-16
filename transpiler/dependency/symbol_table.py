from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SymbolRecord:
    name: str
    symbol_type: str
    file_path: Path | str | None = None
    language: str = "python"
    parent: str | None = None
    base_class: str | None = None
    line_number: int = 0
    return_type: str | None = None
    parameters: dict[str, str] = field(default_factory=dict)
    members: dict[str, str] = field(default_factory=dict)
    methods: dict[str, str] = field(default_factory=dict)


@dataclass
class ClassRecord:
    name: str
    members: dict[str, str] = field(default_factory=dict)
    methods: dict[str, str] = field(default_factory=dict)
    base_class: str | None = None


class SymbolTable:
    def __init__(self):
        self.classes: dict[str, ClassRecord] = {}
        self.functions: dict[str, SymbolRecord] = {}
        self.variables: dict[str, SymbolRecord] = {}
        self.imports: list[str] = []

    def add_class(self, name: str, *, members: dict[str, str] | None = None, methods: dict[str, str] | None = None, base_class: str | None = None):
        record = self.classes.setdefault(name, ClassRecord(name=name, members={}, methods={}, base_class=base_class))
        if members:
            record.members.update(members)
        if methods:
            record.methods.update(methods)
        if base_class:
            record.base_class = base_class

    def add_method(self, class_name: str, method_name: str, *, return_type: str | None = None):
        class_record = self.classes.setdefault(class_name, ClassRecord(name=class_name, members={}, methods={}, base_class=None))
        class_record.methods[method_name] = return_type or "unknown"

    def add_function(self, name: str, *, return_type: str | None = None, parameters: dict[str, str] | None = None):
        self.functions[name] = SymbolRecord(
            name=name,
            symbol_type="function",
            file_path=None,
            language="python",
            return_type=return_type,
            parameters=parameters or {},
        )

    def add_variable(self, name: str, type_name: str):
        self.variables[name] = SymbolRecord(name=name, symbol_type="variable", file_path=None, language="python", return_type=type_name)

    def add_import(self, import_name: str):
        self.imports.append(import_name)
