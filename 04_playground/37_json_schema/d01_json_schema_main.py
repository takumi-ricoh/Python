import json
from jsonschema import validate, ValidationError

#%% jsonスキーマの読み込み
with open("j01_schema.json") as file_obj:
    json_schema = json.load(file_obj)


#%% チェック対象
item = {
    "kind":"cat",
    "name":"tame",
}

#%% チェック
try:
    validate(item,json_schema)
except ValidationError as e:
    print(e.message)

print("END")