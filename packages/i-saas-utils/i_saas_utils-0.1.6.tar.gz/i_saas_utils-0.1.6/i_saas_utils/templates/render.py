import os

from jinja2 import Template

from i_saas_utils.saas import get_list_files


def render_dir(source: str, dest: str, data: dict, exist_dir_ok: bool = False) -> None:
    for file in get_list_files(source, short_name=True):
        path = os.path.join(dest, file)
        os.makedirs(os.path.dirname(path), exist_ok=exist_dir_ok)
        render_file(os.path.join(source, file), path, data)


def render_file(source: str, dest: str, data: dict) -> None:
    with open(source, "r") as inp, open(render_text(dest, data), "w") as out:
        out.write(render_text(inp.read(), data))


def render_text(source: str, data: dict) -> str:
    return Template(source).render(**data)
