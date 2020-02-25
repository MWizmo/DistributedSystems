from timeit import timeit
from tabulate import tabulate
import sys
import pickle
import json
import yaml
import dicttoxml
from io import BytesIO
import fastavro
import msgpack


message = {
    'words': """
    Lorem ipsum dolor sit amet, consectetur adipiscing
    elit. Mauris adipiscing adipiscing placerat.
    Vestibulum augue augue,
    pellentesque quis sollicitudin id, adipiscing.
    """,
    'list': [i for i in range(100)],
    'dict': dict((str(i),'a') for i in range(100)),
    'int': 100,
    'float': 100.123456
}


loops = 500
enc_table = []
dec_table = []


def native_test():
    src = pickle.dumps(message, 2)
    setup = 'd=%s; import pickle; src=pickle.dumps(d,2)' % message
    result = timeit(setup=setup, stmt='pickle.dumps(d, 2)', number=loops)
    enc_table.append(['Native serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='pickle.loads(src)', number=loops)
    dec_table.append(['Native deserialization', result])
    print("Native")


def json_test():
    src = json.dumps(message)
    setup = 'd=%s; import json; src=json.dumps(d)' % message
    result = timeit(setup=setup, stmt='json.dumps(d)', number=loops)
    enc_table.append(['JSON serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='json.loads(src)', number=loops)
    dec_table.append(['JSON deserialization', result])
    print("JSON")


def xml_test():
    src=dicttoxml.dicttoxml(message).decode()
    setup = 'd=%s; import dicttoxml; import xmltodict; src=dicttoxml.dicttoxml(d).decode()' % message
    result = timeit(setup=setup, stmt='dicttoxml.dicttoxml(d).decode()', number=loops)
    enc_table.append(['XML serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='xmltodict.parse(src)', number=loops)
    dec_table.append(['XML deserialization', result])
    print("XML")


def avro_test():
    schema = {
        'doc': 'test',
        'name': 'test',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'words', 'type': 'string'},
            {'name': 'list', 'type': {
                'type': 'array',
                'items': 'int'
            }},
            {'name': 'dict', "type": {
                "type": "map",
                "values": "string"
            }},
            {'name': 'int', 'type': 'int'},
            {'name': 'float', 'type': 'float'}
        ],
    }
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, message)
    src = bytes_writer.getvalue()
    setup = 'd={}; schema={}; import fastavro; from io import BytesIO; bytes_writer = BytesIO(); fastavro.schemaless_writer(bytes_writer, schema, d); src = bytes_writer.getvalue()'.format(message, schema)
    result = timeit(setup=setup, stmt='bytes_writer = BytesIO(); fastavro.schemaless_writer(bytes_writer, schema, d); bytes_writer.getvalue()', number=loops)
    enc_table.append(['Avro serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='bytes_writer = BytesIO(); bytes_writer.write(src); bytes_writer.seek(0); data = fastavro.schemaless_reader(bytes_writer, schema)', number=loops)
    dec_table.append(['Avro deserialization', result])
    print("Avro")


def yaml_test():
    src = yaml.dump(message)
    setup = 'd=%s; import yaml; src=yaml.dump(d)' % message
    result = timeit(setup=setup, stmt='yaml.dump(d)', number=loops)
    enc_table.append(['YAML serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='yaml.load(src)', number=loops)
    dec_table.append(['YAML deserialization', result])
    print("YAML")


def msgpack_test():
    src = msgpack.packb(message, use_bin_type=True)
    setup = 'd=%s; import msgpack; src=msgpack.packb(d, use_bin_type=True)' % message
    result = timeit(setup=setup, stmt='msgpack.packb(d, use_bin_type=True)', number=loops)
    enc_table.append(['MessagePack serialization', result, sys.getsizeof(src)])
    result = timeit(setup=setup, stmt='msgpack.unpackb(src, raw=False)', number=loops)
    dec_table.append(['MessagePack deserialization', result])
    print("MessagePack")


native_test()
json_test()
xml_test()
avro_test()
yaml_test()
msgpack_test()


enc_table.sort(key=lambda x: x[1])
enc_table.insert(0, ['Package', 'Seconds', 'Size'])
dec_table.sort(key=lambda x: x[1])
dec_table.insert(0, ['Package', 'Seconds'])

print("\nEncoding Test (%d loops)" % loops)
print(tabulate(enc_table, headers="firstrow"))
print("\nDecoding Test (%d loops)" % loops)
print(tabulate(dec_table, headers="firstrow"))