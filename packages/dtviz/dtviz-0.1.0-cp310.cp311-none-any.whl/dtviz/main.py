from pathlib import Path
import argparse
import itertools
import sys

from hat import json

from dtviz import common
from dtviz import decoder
from dtviz import encoder


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', metavar='PATH', type=Path,
                        default=Path('-'))
    parser.add_argument('conf', metavar='PATH', type=Path, default=Path('-'))
    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    conf = (json.decode_stream(sys.stdin, json.Format.JSON)
            if args.conf == Path('-')
            else json.decode_file(args.conf))

    common.json_schema_repo.validate(common.conf_schema_id, conf)

    projects = {}
    aliases = {}
    data = {}

    for project_conf in conf['projects']:
        path = Path(project_conf['path'])
        project_type = common.ProjectType(project_conf['type']
                                          if 'type' in project_conf
                                          else path.name)
        project_data = json.decode_file(path)

        project = decoder.get_project(project_type,
                                      project_conf.get('name'), project_data)

        projects[project.name] = project
        data[project.name] = data
        for alias in project_conf.get('aliases', []):
            aliases[alias] = project

    externals = set()
    name_ids = {name: i for i, name in enumerate(projects.keys())}
    next_name_ids = itertools.count(len(name_ids))

    for alias, project in aliases.items():
        name_ids[alias] = name_ids[project.name]

    for project in projects.values():
        for ref in project.refs:
            if ref.project in projects or ref.project in aliases:
                continue

            if ref.project in externals:
                continue

            externals.add(ref.project)
            name_ids[ref.project] = next(next_name_ids)

    output_stream = (open(args.output, 'w', encoding='utf-8')
                     if args.output != Path('-') else sys.stdout)
    try:
        encoder.write_header(output_stream)

        for project in projects.values():
            encoder.write_node(stream=output_stream,
                               node_id=name_ids[project.name],
                               name=project.name,
                               version=project.version,
                               is_external=False)

        for name in externals:
            encoder.write_node(stream=output_stream,
                               node_id=name_ids[name],
                               name=name,
                               version=None,
                               is_external=True)

        for project in projects.values():
            for ref in project.refs:
                encoder.write_edge(stream=output_stream,
                                   src_id=name_ids[project.name],
                                   dst_id=name_ids[ref.project],
                                   version=ref.version,
                                   is_dev=ref.dev)

        encoder.write_footer(output_stream)

    finally:
        if output_stream != sys.stdout:
            output_stream.close()


if __name__ == '__main__':
    sys.argv[0] = 'dtviz'
    sys.exit(main())
