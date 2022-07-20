import io
from fastavro import schemaless_writer, schemaless_reader, parse_schema

schema = {
    "type": "array", 
    "items": {
        "type": "record", 
        "name": "Tag", 
        "fields": [
            {"name": "name", "type": "string"}, 
            {"name": "value", "type": "string"}
        ]
    }
}

parsed_schema = parse_schema(schema)

def serialize_tags(tags):
    if len(tags) == 0:
        return 
    fo = io.BytesIO()
    schemaless_writer(fo, parsed_schema, tags)
    return fo.getvalue()

def deserialize_tags(tags_serialized):
    tags = []
    fo = io.BytesIO(tags_serialized)
    for tag in schemaless_reader(fo, parsed_schema):
        tags.append(tag)
    return tags