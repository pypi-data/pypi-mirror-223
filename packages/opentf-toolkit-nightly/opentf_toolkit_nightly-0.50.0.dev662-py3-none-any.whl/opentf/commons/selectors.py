# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Selectors helpers"""

from typing import Any, Dict, List, Optional, Tuple, Union

import re

########################################################################
## Constants

Object = Dict[str, Any]
Selector = Tuple[
    int,
    Optional[Union[str, List[str]]],
    Optional[bool],
    Optional[Union[str, List[str]]],
]

NAME_PATTERN = r'^[0-9a-zA-Z]+([0-9A-Za-z-_.]*[0-9a-zA-Z])?$'
LABEL_PATTERN = r'^([^/]+/)?([0-9A-Za-z-_.]{1,63})$'
DNS_LABEL_PATTERN = r'^(?![0-9]+$)(?!-)[a-z0-9-]{1,63}(?<!-)$'

KEY = r'[a-z0-9A-Z-_./]+'
VALUE = r'[a-z0-9A-Z-_./@]+'
EQUAL_EXPR = re.compile(rf'^({KEY})\s*([=!]?=)\s*({VALUE})(?:,|$)')
SET_EXPR = re.compile(rf'^({KEY})\s+(in|notin)\s+\(({VALUE}(\s*,\s*{VALUE})*)\)(?:,|$)')
EXISTS_EXPR = re.compile(rf'^{KEY}(?:,|$)')
NEXISTS_EXPR = re.compile(rf'^!{KEY}(?:,|$)')


########################################################################
## Selectors helpers

OP_RESOLV = 0x01
OP_EQUAL = 0x10
OP_EQUAL_RESOLV = 0x11
OP_EXIST = 0x20
OP_EXIST_RESOLV = 0x21
OP_NEXIST = 0x40
OP_NEXIST_RESOLV = 0x41
OP_SET = 0x80
OP_SET_RESOLV = 0x81


def _split_exprs(exprs: str) -> List[str]:
    """Split a comma-separated list of expressions.

    # Required parameters

    - exprs: a string

    # Returned value

    A (possibly empty) list of _expressions_.  An expression is a
    string, stripped.
    """
    result = []
    while exprs:
        match = SET_EXPR.match(exprs)
        if not match:
            match = EQUAL_EXPR.match(exprs)
        if not match:
            match = EXISTS_EXPR.match(exprs)
        if not match:
            match = NEXISTS_EXPR.match(exprs)
        if not match:
            raise ValueError(f'Invalid expression {exprs}')
        result.append(exprs[: match.end()].strip(', '))
        exprs = exprs[match.end() :].strip(', ')

    return result


def compile_selector(selector: str, resolve_path: bool = True) -> List[Selector]:
    """Compile selector.

    # Required parameters

    - selector: a string, a comma-separated list of expressions

    # Optional parameters

    - resolve_path: a boolean, default True

    # Returned value

    A list of tuples, the 'compiled' selectors.

    # Raised exceptions

    A _ValueError_ exception is raised if at least one expression is
    invalid.
    """

    def _maybe_resolve(opcode, item):
        if resolve_path and '.' in item:
            return opcode | OP_RESOLV, item.split('.')
        return opcode, item

    compiled = []
    for expr in _split_exprs(selector):
        match = EQUAL_EXPR.match(expr)
        if match:
            key, ope, value = match.groups()
            code, key = _maybe_resolve(OP_EQUAL, key)
            compiled.append((code, key, ope in ('==', '='), value))
            continue
        if EXISTS_EXPR.match(expr):
            code, expr = _maybe_resolve(OP_EXIST, expr)
            compiled.append((code, expr, None, None))
            continue
        if NEXISTS_EXPR.match(expr):
            expr = expr[1:]
            code, expr = _maybe_resolve(OP_NEXIST, expr)
            compiled.append((code, expr, None, None))
            continue
        match = SET_EXPR.match(expr)
        if match is None:
            raise ValueError(f'Invalid expression {expr}.')
        key, ope, list_, _ = match.groups()
        code, key = _maybe_resolve(OP_SET, key)
        compiled.append((code, key, ope == 'in', [v.strip() for v in list_.split(',')]))

    return compiled


def _resolve_path(items: List[str], obj) -> Tuple[bool, Optional[Any]]:
    head, rest = items[0], items[1:]
    if head in obj:
        return (True, obj[head]) if not rest else _resolve_path(rest, obj[head])
    return False, None


def _op_equal_resolv(req, obj):
    key, ope, arg = req[1:]
    found, value = _resolve_path(key, obj)
    if found:
        return (value == arg) if ope else (value != arg)
    return not ope


def _op_exist(req, obj):
    key = req[1]
    return key in obj


def _op_exist_resolv(req, obj):
    key = req[1]
    return _resolve_path(key, obj)[0]


def _op_nexist(req, obj):
    key = req[1]
    return key not in obj


def _op_nexist_resolv(req, obj):
    key = req[1]
    return not _resolve_path(key, obj)[0]


def _op_set(req, obj):
    key, ope, arg = req[1:]
    if key in obj:
        return (obj[key] in arg) if ope else (obj[key] not in arg)
    return not ope


def _op_set_resolv(req, obj):
    key, ope, arg = req[1:]
    found, value = _resolve_path(key, obj)
    if found:
        return (value in arg) if ope else (value not in arg)
    return not ope


OP_HANDLERS = {
    OP_EQUAL_RESOLV: _op_equal_resolv,
    OP_EXIST: _op_exist,
    OP_EXIST_RESOLV: _op_exist_resolv,
    OP_NEXIST: _op_nexist,
    OP_NEXIST_RESOLV: _op_nexist_resolv,
    OP_SET: _op_set,
    OP_SET_RESOLV: _op_set_resolv,
}


def _evaluate(req, obj):
    """Evaluate whether req matches labels.

    # Required parameters

    - req: a tuple (a 'compiled' selector)
    - labels: a dictionary

    # Returned value

    A boolean.  True if `req` is satisfied by `labels`, False otherwise.

    # Raised exceptions

    A _ValueError_ exception is raised if `req` is not a valid
    expression.
    """
    opcode, key, ope, arg = req
    if opcode == OP_EQUAL:  # fast path
        if key in obj:
            if ope:
                return obj[key] == arg
            return obj[key] != arg
        return not ope

    handler = OP_HANDLERS.get(opcode)
    if not handler:
        raise ValueError(f'Invalid opcode {opcode}.')
    return handler(req, obj)


def match_field_compiledselector(obj: Object, selectors: List[Selector]) -> bool:
    return all(_evaluate(sel, obj) for sel in selectors)


def match_field_selector(obj: Object, selector: str) -> bool:
    """Return True if the object matches the selector."""
    return match_field_compiledselector(obj, compile_selector(selector))


def match_label_compiledselector(obj: Object, selectors: List[Selector]) -> bool:
    labels = obj.get('metadata', {}).get('labels', {})
    return all(_evaluate(sel, labels) for sel in selectors)


def match_label_selector(obj: Object, selector: str) -> bool:
    """Return True if the message's labels matches the selector.

    An empty selector always matches.

    The complete selector feature has been implemented.  `selector` is
    of form:

        expr[,expr]*

    where `expr` is one of `key`, `!key`, or `key op value`, with
    `op` being one of `=`, `==`, or `!=`.  The
    `key in (value[, value...])` and `key notin (value[, value...])`
    set-based requirements are also implemented.

    # Required parameters

    - obj: a message (a dictionary)
    - selector: a string

    # Returned value

    A boolean.
    """
    return match_label_compiledselector(
        obj, compile_selector(selector, resolve_path=False)
    )
