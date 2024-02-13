
import json


base_list = """
list ::= 
    "[" ws (
        object
        ("," ws object)*
        )? "]"
"""

object_base = """ "{{"({lines})"}}" """

base_gbnf_struct = """
root  ::= {option}

{list}

object ::= {object}

array  ::=
  \"[\" ws (
            string
    (\",\" ws string)*
  )? \"]\"

string  ::=
  \"\\"\" (
    [^\"\\] |
    "\\\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
  )* \"\\"\" ws

ws ::= ([ \\t\\n] ws)?
"""

def gbnf_from_json(base_json: str):
    """
    takes json string, convert it to json object, and convert this object
    to a valid gbnf grammar string
    """
    try:
        json_obj = json.loads(base_json)
        grammar = ""
        if type(json_obj) == type([]):
            lines = ""
            for label,dtype in json_obj[0].items():
                line = "\"\\\""+label+"\\\"\" \":\" "+ dtype + " \",\""
                lines += line
            derived_object = object_base.format(lines=lines)
            grammar = base_gbnf_struct.format(option="list", list=base_list, object=derived_object)
        elif type(json_obj) == type({}):
            lines = ""
            for label,dtype in json_obj.items():
                line = "\"\\\""+label+"\\\"\" \":\" "+ dtype + " \",\""
                lines += line
            derived_object = object_base.format(lines=lines)
            grammar = base_gbnf_struct.format(option="object", list="", object=derived_object)
        return grammar
    except Exception as e:
        print(e)
        return "---" 

if __name__ == "__main__":
    res = gbnf_from_json(json.dumps([{
        "firstname": "string",
        "lastname": "string",
        "phone": "number"
    }]))
    with open("test.gbnf","w+") as f:
        f.write(res)