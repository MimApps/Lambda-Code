"""
Copyright (C) 2022 Lambda Code Organization.

This file is part of the Lambda Code programming language

Lambda Code is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Lambda Code is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see https://www.gnu.org/licenses/
"""

# with open('../test.lc', 'r') as c_target_file:  # c stands for class, a convention in this context
#     t_lines = c_target_file.readlines()  # t: target
#     h_cls_index = []
#     two_multiples = ['2', '4', '6', '8', '0']
#     for c_line in t_lines:
#         if 'class' in c_line:
#             h_cls_index.append(t_lines.index(c_line) + 1)
#     len_cls_index = str(len(h_cls_index))
#     if len_cls_index in two_multiples: pass
#     else:
#         raise Error("Incomplete class definition")

import sys
import string
from functions import parse_functions


class Error(Exception):
    __module__: str = 'builtins'


def parse_classes(ranges: list, file: str, flags: str = '') -> list:
    """
    Parse classes in the provided ranges of the file.

    :param ranges: ranges(start: end)
    :param file path pointing to the file to read from
    :param flags: Available flags, 'debug' for development purpose only
    :return: Abstract syntax tree
    """
    __ast__: list = []
    chars: list = [char for char in string.ascii_lowercase] \
        + ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    with open(file, 'r') as file:
        file = file.readlines()
        for _range in ranges:
            # Separating ranges from a string
            rvec_x: int = int(_range.split(':')[0]) - 1  # r = range
            rvec_y: int = int(_range.split(':')[-1])
            class_string: str = "".join(file[rvec_x: rvec_y])

            # Extracting the name
            name: str = ''.join(class_string.split('class')).split()[0]
            if '(' in name:
                name = name.split('(')[0]
            for n_char in name:
                if n_char.lower() not in chars:
                    raise Error(f"File {file}\ninvalid character '{n_char}' in class name {name}")
                if n_char.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    if name.index(n_char) < len(name):
                        raise Error(f"number {n_char} in between of a the class name {name}")

            # Extracting constructor parameters
            h_param0: str = class_string.split(name)[-1].split(')')[0]\
                .split('(')[-1]
            params_pairs: list = h_param0.split(',')
            final_params: list = []
            for _param in params_pairs:
                param_name: None
                default: None
                if '=' in _param:
                    # has default values
                    default: str = _param.split('=')[-1]
                if not default:
                    param_name = _param.split()[-1]
                else:
                    param_name = _param.split('=')
                final_params.append(
                    {
                        'name': param_name,
                        'default': default,
                        'type': _param.split()[0]
                    }
                )

            # Checking for and extracting super class(s)
            if 'inherits' in class_string:
                h_inheritance = class_string.split('inherits')[-1]\
                    .split('\n')[0].split(',')
                inheritance = []
                for super_class in h_inheritance:
                    inheritance.append(super_class.lstrip())

            # And finally appending everything into the syntax tree :)
            __ast__.append(
                {
                    "category": "class",
                    "name": name,
                    "supers": inheritance,
                    "constructor_params": final_params
                }
            )

            if 'debug' in flags:
                sys.stdout.write(
                    f"""
                    {name}(class)
                    |
                    |-------[INHERITANCE]
                    |              |
                    |              |
                    |             {inheritance}
                    |
                    |
                    |-------[CONSTRUCTOR]
                    |           |
                    |           |
                    |            {final_params}
                    |"""
                )

    return __ast__
