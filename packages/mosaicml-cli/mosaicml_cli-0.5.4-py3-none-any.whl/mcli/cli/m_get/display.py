"""Helpers for `mcli get` displays"""
import datetime
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple

import yaml
from rich.table import Table

from mcli.utils.utils_logging import console, err_console
from mcli.utils.utils_rich import create_table

logger = logging.getLogger(__name__)


class OutputDisplay(Enum):
    TABLE = 'table'
    NAME = 'name'
    JSON = 'json'

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


@dataclass
class MCLIDisplayItem():
    """Item for display in an `mcli get` list of items
    """

    def to_dict(self) -> Dict[str, Any]:
        """Get the current object as a dictionary

        Returns:
            Dict[str, Any]: Dictionary representation of the object
        """

        def process_field_value(field_value: Any) -> Optional[Any]:
            """ Function that processes a field value based on its type into serializable form
            If a field value is an enum, it'll unpack it back to its serializable json value
            If a field is a list, it'll recursively process all elements
            """

            if isinstance(field_value, Enum):
                return str(field_value.value)
            elif isinstance(field_value, datetime.datetime):
                return field_value.isoformat()
            elif isinstance(field_value, (dict, list)):
                return field_value
            elif field_value is not None:
                return str(field_value)

        data = {}
        for class_field in fields(self):
            field_value = getattr(self, class_field.name)
            field_value = process_field_value(field_value)
            data[class_field.name] = field_value
        return data


class MCLIGetDisplay(ABC):
    """ABC for all `mcli get` lists
    """

    @property
    def override_column_ordering(self) -> Optional[List[str]]:
        """Override to enforce column ordering for display output. Otherwise, columns
        will be ordered by the default item ordering as returned by get_list
        """
        return None

    @property
    def index_label(self) -> str:
        return "name"

    def create_custom_table(self, columns: List[str], data: List[Any], names: List[str]) -> Optional[Table]:  # pylint: disable=unused-argument
        """Override for custom create display table formatting"""
        return None

    @property
    def custom_column_names(self) -> Optional[List[str]]:
        """Override column names for display"""
        return None

    def print(self, output: OutputDisplay):
        items = self.get_list()
        if output == OutputDisplay.TABLE:
            if not items:
                err_console.print('No items found.')
                return
            disp = self.to_table(items)
        elif output == OutputDisplay.NAME:
            names = self.to_name(items)
            disp = '\n'.join(names)
        elif output == OutputDisplay.JSON:
            json_list = self.to_json(items)
            disp = json.dumps(json_list)
        else:
            raise ValueError(f'output is not a known display type. It must be one of {list(OutputDisplay)}')
        console.print(disp)

    def get_list(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self]

    def to_table(self, items: List[Dict[str, Any]]) -> Table:

        def _to_str(obj: Any) -> str:
            return yaml.safe_dump(obj, default_flow_style=None).strip() if not isinstance(obj, str) else obj

        column_names = self.override_column_ordering or [
            key for key, val in items[0].items() if val is not None and key != self.index_label
        ]
        columns, names = [], []
        for item in items:
            if self.index_label:
                names.append(item[self.index_label])
            columns.append(tuple(_to_str(item[key]) for key in column_names))

        column_names = self.custom_column_names or column_names

        # pylint: disable-next=assignment-from-none
        custom_table = self.create_custom_table(columns=column_names, data=columns, names=names)
        return custom_table if custom_table else create_display_table(names, columns, column_names,
                                                                      self.index_label.upper())

    def to_name(self, items: List[Dict[str, Any]]) -> List[str]:
        return [item[self.index_label] for item in items]

    def to_json(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return items

    @abstractmethod
    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        ...


def create_vertical_display_table(data: List[Tuple[str]],
                                  columns: List[str],
                                  padding: Optional[Tuple[int, int]] = None) -> Table:
    final_padding = (0, 5) if not padding else padding
    grid = Table.grid(expand=False, padding=final_padding)
    # left column is header, right column is data
    grid.add_column(justify="left")
    grid.add_column(justify="left")
    for d in data:
        for col, val in zip(columns, d):
            grid.add_row(col, val)
    return grid


def create_display_table(names: List[str],
                         columns: List[Tuple[str]],
                         column_names: List[str],
                         index_label: str = 'NAME') -> Table:
    return create_table(data=columns,
                        indices=names,
                        index_label=index_label,
                        columns=[ss.upper() for ss in column_names],
                        table_kwargs={
                            'box': None,
                            'pad_edge': False
                        },
                        index_kwargs={
                            'justify': 'left',
                            'no_wrap': True
                        })


def format_timestamp(timestamp: Optional[datetime.datetime], default='-') -> str:
    """Format timestamps for printing
    """

    if not timestamp:
        return default
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    dt_format = '%Y-%m-%d %I:%M %p'
    try:
        return timestamp.astimezone(tz).strftime(dt_format)
    except (OverflowError, ValueError) as _:
        return default
