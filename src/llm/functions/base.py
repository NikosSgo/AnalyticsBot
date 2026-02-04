from typing import List, Dict, Any, Literal, TypedDict

JsonSchemaType = Literal["string", "integer", "number", "boolean"]

class ParamDef(TypedDict, total=False):
    type: JsonSchemaType
    description: str

class QueryDef(TypedDict, total=False):
    description: str
    sql: str
    parameters: Dict[str, ParamDef]
    required: List[str]

def generate_functions(query_definitions) -> List[Dict[str, Any]]:
    functions: List[Dict[str, Any]] = []

    for name, defn in query_definitions.items():
        params = defn.get("parameters", {})
        functions.append({
            "name": name,
            "description": defn["description"],
            "parameters": {
                "type": "object",
                "properties": params,
                "required": defn.get("required", list(params.keys())),
            },
        })

    return functions
