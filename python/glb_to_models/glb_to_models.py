#!/usr/bin/env python3

import argparse
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import sys


def create_model_directory(model_dir: str) -> bool:
    if os.path.isdir(model_dir) or os.path.exists(model_dir):
        print(f'Model directory already exists: {model_dir}')
        return False

    os.mkdir(model_dir)
    return True


def create_model_config(model_name: str, model_dir: str, args: argparse.Namespace) -> bool:
    config_file_path = os.path.join(model_dir, 'model.config')
    if os.path.exists(config_file_path):
        print(f'Config file already exists: {config_file_path}')
        return False

    environment = Environment(loader=FileSystemLoader(args.templates))
    template = environment.get_template('model.config')
    config_content = template.render(
        name=model_name,
        sdf_version=args.sdf_version,
        author=args.author,
        email=args.email,
        description=args.description)

    with open(config_file_path, mode='w', encoding='utf-8') as message:
        message.write(config_content)

    print(f'{model_name}/model.config written')
    return True


def create_model_sdf(model_name: str, model_dir:str, args: argparse.Namespace) -> bool:
    sdf_file_path = os.path.join(model_dir, 'model.sdf')
    if os.path.exists(sdf_file_path):
        print(f'SDF file already exists: {sdf_file_path}')
        return False

    environment = Environment(loader=FileSystemLoader(args.templates))
    template = environment.get_template('model.sdf')
    sdf_content = template.render(
        name=model_name,
        sdf_version=args.sdf_version)

    with open(sdf_file_path, mode='w', encoding='utf-8') as message:
        message.write(sdf_content)

    print(f'{model_name}/model.sdf written')
    return True


def create_meshes_directory(model_dir: str) -> bool:
    meshes_dir_path = os.path.join(model_dir, 'meshes')
    if os.path.isdir(meshes_dir_path) or os.path.exists(meshes_dir_path):
        print(f'meshes directory already exists: {meshes_dir_path}')
        return False

    os.mkdir(meshes_dir_path)
    return True


def copy_mesh(mesh_path: str, model_dir: str) -> bool:
    mesh_filename = os.path.basename(mesh_path)
    output_mesh_path = os.path.join(model_dir, 'meshes', mesh_filename)
    if os.path.exists(output_mesh_path):
        print(f'mesh already exists: {output_mesh_path}')
        return False

    shutil.copyfile(mesh_path, output_mesh_path)
    return True


def generate_model(mesh_filename: str, args: argparse.Namespace) -> bool:
    mesh_path = os.path.join(args.input, mesh_filename)
    model_name = os.path.splitext(mesh_filename)[0]
    model_dir = os.path.join(args.output, model_name)

    if create_model_directory(model_dir) and \
            create_model_config(model_name, model_dir, args) and \
            create_model_sdf(model_name, model_dir, args) and \
            create_meshes_directory(model_dir) and \
            copy_mesh(mesh_path, model_dir):
        print(f'Created model for {mesh_filename}')
        return True

    print(f'Failed creating model for {mesh_filename}')
    return False


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Path to directory holding all the glb files')
    parser.add_argument('-o', '--output', help='Where to create the model')
    parser.add_argument('-s', '--sdf-version', default='1.9')
    parser.add_argument('-a', '--author', default='')
    parser.add_argument('-e', '--email', default='')
    parser.add_argument('-d', '--description', default='')
    parser.add_argument('-t', '--templates', default='templates/')
    args = parser.parse_args(argv[1:])

    if not os.path.isdir(args.input):
        print(f'Input directory does not exist: {args.input}')
        exit(1)

    if not os.path.isdir(args.output):
        print(f'Output directory does not exist: {args.output}')
        exit(1)

    mesh_filenames = os.listdir(args.input)
    for mesh_filename in mesh_filenames:
        if mesh_filename[-4:] != '.glb':
            print(f'Skipping non .glb file: {mesh_filename}')
            continue
        print(mesh_filename)
        if not generate_model(mesh_filename, args):
            exit(1)


if __name__ == '__main__':
    main(sys.argv)
