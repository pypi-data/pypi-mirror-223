# see https://pypi.org/project/setuptools-github
# copy of setuptools_github.tools
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any

from . import scm


class ToolsError(Exception):
    pass


class ValidationError(ToolsError):
    pass


class InvalidVersionError(ToolsError):
    pass


class MissingVariableError(ToolsError):
    pass


class AbortExecutionError(Exception):
    @staticmethod
    def _strip(txt):
        txt = txt or ""
        txt = txt[1:] if txt.startswith("\n") else txt
        txt = indent(txt, pre="")
        return txt[:-1] if txt.endswith("\n") else txt

    def __init__(
        self, message: str, explain: str | None = None, hint: str | None = None
    ):
        self.message = message.strip()
        self._explain = explain
        self._hint = hint

    @property
    def explain(self):
        return self._strip(self._explain)

    @property
    def hint(self):
        return self._strip(self._hint)

    def __str__(self):
        result = [self.message]
        if self.explain:
            result.append(indent("\n" + self.explain, pre=" " * 2)[2:])
        if self.hint:
            result.extend(["\nhint:", indent("\n" + self.hint, pre=" " * 2)[2:]])
        return "".join(result)


def urmtree(path: Path):
    "universal (win|*nix) rmtree"
    from os import name
    from shutil import rmtree
    from stat import S_IWUSR

    if name == "nt":
        for p in path.rglob("*"):
            p.chmod(S_IWUSR)
    rmtree(path, ignore_errors=True)
    if path.exists():
        raise RuntimeError(f"cannot remove {path=}")


def indent(txt: str, pre: str = " " * 2) -> str:
    "simple text indentation"

    from textwrap import dedent

    txt = dedent(txt)
    if txt.endswith("\n"):
        last_eol = "\n"
        txt = txt[:-1]
    else:
        last_eol = ""

    result = pre + txt.replace("\n", "\n" + pre) + last_eol
    return result if result.strip() else result.strip()


def list_of_paths(paths: str | Path | list[str | Path] | None) -> list[Path]:
    if not paths:
        return []
    return [Path(s) for s in ([paths] if isinstance(paths, (str, Path)) else paths)]


def lstrip(txt: str, left: str) -> str:
    return txt[len(left) :] if txt.startswith(left) else txt


def get_module_var(
    path: Path | str, var: str = "__version__", abort=True
) -> str | None:
    """extract from a python module in path the module level <var> variable

    Args:
        path (str,Path): python module file to parse using ast (no code-execution)
        var (str): module level variable name to extract
        abort (bool): raise MissingVariable if var is not present

    Returns:
        None or str: the variable value if found or None

    Raises:
        MissingVariable: if the var is not found and abort is True

    Notes:
        this uses ast to parse path, so it doesn't load the module
    """

    class V(ast.NodeVisitor):
        def __init__(self, keys):
            self.keys = keys
            self.result = {}

        def visit_Module(self, node):  # noqa: N802
            # we extract the module level variables
            for subnode in ast.iter_child_nodes(node):
                if not isinstance(subnode, ast.Assign):
                    continue
                for target in subnode.targets:
                    if target.id not in self.keys:
                        continue
                    if not isinstance(subnode.value, (ast.Num, ast.Str, ast.Constant)):
                        raise ValidationError(
                            f"cannot extract non Constant variable "
                            f"{target.id} ({type(subnode.value)})"
                        )
                    if isinstance(subnode.value, ast.Str):
                        value = subnode.value.s
                    elif isinstance(subnode.value, ast.Num):
                        value = subnode.value.n
                    else:
                        value = subnode.value.value
                    if target.id in self.result:
                        print(f">>> {path=}")  # noqa: T201
                        print(path.read_text())  # noqa: T201
                        raise ValidationError(
                            f"found multiple repeated variables {target.id}"
                        )
                    self.result[target.id] = value
            return self.generic_visit(node)

    v = V({var})
    path = Path(path)
    if path.exists():
        tree = ast.parse(Path(path).read_text())
        v.visit(tree)
    if var not in v.result and abort:
        raise MissingVariableError(f"cannot find {var} in {path}", path, var)
    return v.result.get(var, None)


def set_module_var(
    path: str | Path, var: str, value: Any, create: bool = True
) -> tuple[Any, str]:
    """replace var in path with value

    Args:
        path (str,Path): python module file to parse
        var (str): module level variable name to extract
        value (None or Any): if not None replace var in initfile
        create (bool): create path if not present

    Returns:
        (str, str) the (<previous-var-value|None>, <the new text>)
    """

    # validate the var
    get_module_var(path, var, abort=False)

    # module level var
    expr = re.compile(f"^{var}\\s*=\\s*['\\\"](?P<value>[^\\\"']*)['\\\"]")
    fixed = None
    lines = []

    src = Path(path)
    if not src.exists() and create:
        src.parent.mkdir(parents=True, exist_ok=True)
        src.touch()

    input_lines = src.read_text().split("\n")
    for line in input_lines:
        if fixed is not None:
            lines.append(line)
            continue
        match = expr.search(line)
        if match:
            fixed = match.group("value")
            if value is not None:
                x, y = match.span(1)
                line = line[:x] + value + line[y:]
        lines.append(line)
    txt = "\n".join(lines)
    if (fixed is None) and create:
        if txt and txt[-1] != "\n":
            txt += "\n"
        txt += f'{var} = "{value}"'

    with Path(path).open("w") as fp:
        fp.write(txt)
    return fixed, txt


def bump_version(version: str, mode: str) -> str:
    """given a version str will bump it according to mode

    Arguments:
        version: text in the N.M.O form
        mode: major, minor or micro

    Returns:
        increased text

    >>> bump_version("1.0.3", "micro")
    "1.0.4"
    >>> bump_version("1.0.3", "minor")
    "1.1.0"
    """
    newver = [int(n) for n in version.split(".")]
    if mode == "major":
        newver[-3] += 1
        newver[-2] = 0
        newver[-1] = 0
    elif mode == "minor":
        newver[-2] += 1
        newver[-1] = 0
    elif mode == "micro":
        newver[-1] += 1
    return ".".join(str(v) for v in newver)


def get_data(
    initfile: str | Path, github_dump: str | None = None, abort: bool = True
) -> dict[str, str | None]:
    """extracts version information from github_dump and updates initfile in-place

    Args:
        initfile (str, Path): path to the __init__.py file with a __version__ variable
        github_dump (str): the os.getenv("GITHUB_DUMP") value

    Returns:
        dict[str,str|None]: a dict with the current config
    """
    result = {
        "version": get_module_var(initfile, "__version__"),
        "current": get_module_var(initfile, "__version__"),
        "branch": None,
        "hash": None,
        "build": None,
        "runid": None,
        "workflow": None,
    }

    path = Path(initfile)
    repo = scm.lookup(path)

    if not (repo or github_dump):
        if abort:
            raise scm.InvalidGitRepoError(f"cannot find a valid git repo for {path}")
        return result

    if not github_dump and repo:
        gdata = {
            "ref": repo.head.name,
            "sha": repo.head.target.hex[:7],
            "run_number": 0,
            "run_id": 0,
        }
        dirty = repo.dirty()
    else:
        gdata = json.loads(github_dump) if isinstance(github_dump, str) else github_dump
        dirty = False

    expr = re.compile(r"/(?P<what>beta|release)/(?P<version>\d+([.]\d+)*)$")
    expr1 = re.compile(r"(?P<version>\d+([.]\d+)*)(?P<num>b\d+)?$")

    result["branch"] = lstrip(gdata["ref"], "refs/heads/")
    result["hash"] = gdata["sha"] + ("*" if dirty else "")
    result["build"] = gdata["run_number"]
    result["runid"] = gdata["run_id"]
    result["workflow"] = result["branch"]

    current = result["current"]
    if match := expr.search(gdata["ref"]):
        # setuptools double calls the update_version,
        # this fixes the issue
        match1 = expr1.search(current or "")
        if not match1:
            raise InvalidVersionError(f"cannot parse current version '{current}'")
        if match1.group("version") != match.group("version"):
            raise InvalidVersionError(
                f"building package for {current} from '{gdata['ref']}' "
                f"branch ({match.groupdict()} mismatch {match1.groupdict()})"
            )
        if match.group("what") == "beta":
            result["version"] = f"{match1.group('version')}b{gdata['run_number']}"
            result["workflow"] = "beta"
        else:
            result["workflow"] = "tags"
    return result


def update_version(
    initfile: str | Path, github_dump: str | None = None, abort: bool = True
) -> str | None:
    """extracts version information from github_dump and updates initfile in-place

    Args:
        initfile (str, Path): path to the __init__.py file with a __version__ variable
        github_dump (str): the os.getenv("GITHUB_DUMP") value

    Returns:
        str: the new version for the package
    """

    data = get_data(initfile, github_dump, abort)
    set_module_var(initfile, "__version__", data["version"])
    set_module_var(initfile, "__hash__", data["hash"])
    return data["version"]


def process(
    initfile: str | Path,
    github_dump: str | None = None,
    paths: str | Path | list[str | Path] | None = None,
    fixers: dict[str, str] | None = None,
    abort: bool = True,
) -> dict[str, str | None]:
    """get version from github_dump and updates initfile/paths

    Args:
        paths (str, Path): path(s) to files jinja2 processeable
        initfile (str, Path): path to the __init__.py file with a __version__ variable
        github_dump (str): the os.getenv("GITHUB_DUMP") value

    Returns:
        str: the new version for the package

    Example:
        {'branch': 'beta/0.3.1',
         'build': 0,
         'current': '0.3.1',
         'hash': 'c9e484a*',
         'version': '0.3.1b0',
         'runid': 0
        }
    """
    from argparse import Namespace
    from functools import partial
    from urllib.parse import quote

    from jinja2 import Environment

    class Context(Namespace):
        def items(self):
            for name, value in self.__dict__.items():
                if name.startswith("_"):
                    continue
                yield (name, value)

    data = get_data(initfile, github_dump, abort)
    set_module_var(initfile, "__version__", data["version"])
    set_module_var(initfile, "__hash__", data["hash"])

    env = Environment(autoescape=True)
    env.filters["urlquote"] = partial(quote, safe="")
    for path in list_of_paths(paths):
        txt = path.read_text()
        for old, new in (fixers or {}).items():
            txt = txt.replace(old, new, 1)
        tmpl = env.from_string(txt)
        path.write_text(tmpl.render(ctx=Context(**data)))
    return data
