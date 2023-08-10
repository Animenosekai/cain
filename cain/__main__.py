"""
The Cain CLI

Copyright
---------
Animenosekai, 2023
    MIT License
"""
import argparse
import pathlib
import json
import sys
import contextlib
import importlib.util

import cain
from cain.types.types import Type


@contextlib.contextmanager
def add_to_path(path: pathlib.Path):
    """
    Parameters
    ----------
    path: pathlib.Path
        the parent path
    """
    old_path = sys.path
    sys.path = sys.path[:]
    sys.path.insert(0, str(path))
    try:
        yield
    finally:
        sys.path = old_path


def retrieve_schema(file: pathlib.Path, name: str):
    """Retrieves the schema `name` from the given file"""
    file = pathlib.Path(file).resolve().absolute()
    with add_to_path(file):
        spec = importlib.util.spec_from_file_location(file.stem, str(file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        try:
            return getattr(module, name)
        except AttributeError as err:
            raise ValueError(f"There is no schema {name} in the given file") from err


TRUST_WARNING = "\033[93;1m Warning\033[0m: This should only be used with trusted {entity}!"


def entry():
    """the CLI entrypoint"""
    parser = argparse.ArgumentParser("cain", description="A small yet powerful data format ✨")
    parser.add_argument("--version", "-v", action="version", version=cain.__version__)
    subparser = parser.add_subparsers(help='Actions', dest="action", required=True)

    encode_argparse = subparser.add_parser("encode", help="Encodes objects using the cain data format")
    decode_argparse = subparser.add_parser("decode", help="Decodes objects using the cain data format")
    schema_argparse = subparser.add_parser("schema", help="Manipulates cain schemas")

    # Encode
    encode_argparse.add_argument("input", action="store",
                                 help="The data to encode. By default, this should be JSON encoded (see --raw and --eval to change this behaviour)")
    encode_argparse.add_argument("--schema", "-s", action="store", required=True, help="The schema file or data encode the data with")

    encode_mutex_schema = encode_argparse.add_mutually_exclusive_group()
    encode_mutex_schema.add_argument("--schema-header", action="store_true",
                                     help="If provided, the `--schema` will be considered as a cain data input "
                                     "and the schema will be read from its header")
    encode_mutex_schema.add_argument("--schema-name", action="store", required=False,
                                     help="If provided, the `--schema` file will be considered as a Python file and this name will be considered as "
                                     "the variable name of the schema in the Python file." + TRUST_WARNING.format(entity="schemas"))
    encode_mutex_schema.add_argument("--schema-eval", action="store_true",
                                     help="If provided, the `--schema` will be treated as a Python expression and will be evaluated."
                                     + TRUST_WARNING.format(entity="schemas"))

    encode_argparse.add_argument("--output", "-o", action="store", required=False, default=None,
                                 help="The output destination for the encoded data (STDOUT if not specified)")

    encode_mutex_input = encode_argparse.add_mutually_exclusive_group()
    encode_mutex_input.add_argument("--raw", "-r", action="store_true", help="If the given input should be treated as raw bytes")
    encode_mutex_input.add_argument("--eval", "-e", action="store_true",
                                    help="If the given input is a Python expression which should be evaluated." + TRUST_WARNING.format(entity="inputs"))
    encode_mutex_input.add_argument("--include-header", "--header", action="store_true",
                                    help="This prepends a header containing the schema at the beginning of the content")

    def prepare_json_parser(parser: argparse.ArgumentParser):
        """Prepares parsers which can output to JSON"""
        # --eval, -e are here to mimick the encode parser behaviour
        parser.add_argument("--raw", "-r", "--eval", "-e", action="store_true", help="If the output should not be JSON parsed")

        parser.add_argument("--json-sort", action="store_true",
                            help="If the output is JSON parsed, if the encoder should sort the keys")
        parser.add_argument("--json-ascii", action="store_true",
                            help="If the output is JSON parsed, if the encoder should encode the strings using the ASCII character table")
        decode_mutex_json = parser.add_mutually_exclusive_group()
        decode_mutex_json.add_argument("--json-indent", action="store", type=int, required=False, default=4,
                                       help="If the output is JSON parsed, the indentation level of the JSON result")
        decode_mutex_json.add_argument("--json-minify", action="store_true",
                                       help="If the output is JSON parsed, if the output should be minified")

    # Decode
    decode_argparse.add_argument("input", action="store", help="The data to decode")
    decode_argparse.add_argument("--schema", "-s", action="store", required=False,
                                 help="The schema file or data encode the data with. "
                                 "If omitted, it will be assumed that `input` has the necessary headers.")

    decode_mutex_schema = decode_argparse.add_mutually_exclusive_group()
    decode_mutex_schema.add_argument("--schema-header", action="store_true",
                                     help="If provided, the `--schema` will be considered as a cain data input "
                                     "and the schema will be read from its header")
    decode_mutex_schema.add_argument("--schema-name", action="store", required=False,
                                     help="If provided, the `--schema` file will be considered as a Python file and this name will be considered as "
                                     "the variable name of the schema in the Python file." + TRUST_WARNING.format(entity="schemas"))
    decode_mutex_schema.add_argument("--schema-eval", action="store_true",
                                     help="If provided, the `--schema` will be treated as a Python expression and will be evaluated."
                                     + TRUST_WARNING.format(entity="schemas"))
    prepare_json_parser(decode_argparse)

    decode_argparse.add_argument("--output", "-o", action="store", required=False, default=None,
                                 help="The output destination for the decoded data (STDOUT if not specified)")

    # Schema

    def prepare_scheme_parser(parser: argparse.ArgumentParser):
        """Prepares the schema subparsers"""
        parser.add_argument("input", action="store", help="The schema to lookup")
        parser.add_argument("--output", "-o", action="store", required=False, default=None,
                            help="The output destination for the decoded data (STDOUT if not specified)")

        schema_mutex_schema = parser.add_mutually_exclusive_group()
        schema_mutex_schema.add_argument("--schema-header", action="store_true",
                                         help="If provided, the `input` will be considered as a cain data input "
                                         "and the schema will be read from its header")
        schema_mutex_schema.add_argument("--schema-name", action="store", required=False,
                                         help="If provided, the `input` file will be considered as a Python file and this name will be considered as "
                                         "the variable name of the schema in the Python file." + TRUST_WARNING.format(entity="schemas"))
        schema_mutex_schema.add_argument("--schema-eval", action="store_true",
                                         help="If provided, the `input` will be treated as a Python expression and will be evaluated."
                                         + TRUST_WARNING.format(entity="schemas"))

    schema_subparser = schema_argparse.add_subparsers(help='Actions', dest="schema_action", required=True)

    schema_lookup_argparse = schema_subparser.add_parser("lookup", help="Looks up what's inside the given schema")
    schema_export_argparse = schema_subparser.add_parser("export", help="Exports the given schema")

    # Schema Lookup
    prepare_scheme_parser(schema_lookup_argparse)
    prepare_json_parser(schema_lookup_argparse)

    # Schema Export
    prepare_scheme_parser(schema_export_argparse)

    args = parser.parse_args()

    def get_input(inp: str):
        if pathlib.Path(inp).is_file():
            return pathlib.Path(inp).read_bytes()
        else:
            return inp.encode("utf-8")

    def get_schema(schema: str, args):
        if args.schema_eval:
            if not schema:
                raise ValueError("You can't use `--schema-eval` without providing a schema")
            return eval(schema)
        elif args.schema_name:
            if not schema:
                raise ValueError("You can't use `--schema-name` without providing a schema")
            return retrieve_schema(pathlib.Path(schema), name=args.schema_name)
        elif args.schema_header:
            if not schema:
                raise ValueError("You can't use `--schema-header` without providing a schema")
            data = get_input(schema)
            result, _ = cain.types.Tuple[bytes, bytes].decode(data)
            return cain.decode_schema(result)
        elif schema:
            return cain.decode_schema(pathlib.Path(schema).read_bytes())
        return None

    if args.action == "encode":
        # Getting the input
        data = get_input(args.input)

        # Parsing the input
        if args.eval:
            parsed = eval(data)
        elif args.raw:
            parsed = data
        else:
            parsed = json.loads(data)

        # Getting the schema
        schema = get_schema(args.schema, args)

        # Encoding the input
        if args.output:
            output = pathlib.Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("wb") as handler:
                cain.dump(parsed, handler=handler, schema=schema, include_header=args.include_header)
        else:
            print(repr(cain.dumps(parsed, schema=schema, include_header=args.include_header))[2:-1])

    elif args.action == "decode":
        # Getting the schema
        schema = get_schema(args.schema, args)

        # Decoding the data
        if pathlib.Path(args.input).is_file():
            with pathlib.Path(args.input).open("rb") as handler:
                data = cain.load(handler, schema=schema)
        else:
            data = cain.loads(args.input.encode("utf-8"), schema=schema)

        # Parsing the data
        if not args.raw:
            if args.json_minify:
                data = json.dumps(data, separators=(",", ":"), ensure_ascii=args.json_ascii, sort_keys=args.json_sort)
            else:
                data = json.dumps(data, indent=args.json_indent, ensure_ascii=args.json_ascii, sort_keys=args.json_sort)

        # Outputting the data
        if args.output:
            output = pathlib.Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(data, bytes):
                output.write_bytes(data)
            else:
                output.write_text(data, encoding="utf-8")
        else:
            print(data)

    elif args.action == "schema":
        # Getting the schema
        schema = get_schema(args.input, args)

        if args.schema_action == "export":
            # Export
            data = cain.encode_schema(schema)
        else:
            # Lookup
            if not args.raw:
                data = Type.pack(schema, json=True)
                if args.json_minify:
                    data = json.dumps(data, separators=(",", ":"), ensure_ascii=args.json_ascii, sort_keys=args.json_sort)
                else:
                    data = json.dumps(data, indent=args.json_indent, ensure_ascii=args.json_ascii, sort_keys=args.json_sort)
            else:
                data = repr(schema)

        # Outputting the data
        if args.output:
            output = pathlib.Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(data, bytes):
                output.write_bytes(data)
            else:
                output.write_text(data, encoding="utf-8")
        else:
            if isinstance(data, bytes):
                print(str(data)[2:-1])
            else:
                print(data)
    else:
        raise ValueError(f"Couldn't recognize the given action `{args.action}`")


if __name__ == "__main__":
    entry()
