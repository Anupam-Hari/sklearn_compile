from transpiler.agent.tools.mapping_updater import (
    update_mapping_table,
)

from transpiler.llm.google import (
    GoogleLLM,
)


llm = GoogleLLM()

mapping = update_mapping_table(
    llm,
)

print(mapping)