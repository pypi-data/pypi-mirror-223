from dataclasses import dataclass, field as dataclass_field
from typing import TypeVar, Optional

from model_connect import registry
from model_connect.constants import is_undefined, UNDEFINED
from model_connect.registry import get_model_field, get_model_fields

_T = TypeVar('_T')


class ProcessedFilters(list['ProcessedFilter']):
    def __init__(self, vars_: list = UNDEFINED, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_undefined(vars_):
            vars_ = []

        self.vars = vars_


class ProcessedSortingOptions(list['ProcessedSortingOption']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class ProcessedFilter:
    column: str
    operator: str
    value: str


@dataclass
class ProcessedSortingOption:
    column: str
    direction: str


@dataclass
class ProcessedPaginationOptions:
    limit: Optional[int] = None
    skip: Optional[int] = None


@dataclass
class ProcessedGroupByOptions(list[str]):
    pass


@dataclass
class ProcessedOnConflictOptions:
    do: str = None
    conflict_targets: list[str] = dataclass_field(default_factory=list)
    update_columns: list[str] = dataclass_field(default_factory=list)

    @property
    def do_nothing(self) -> bool:
        return self.do == 'NOTHING'

    @property
    def do_update(self) -> bool:
        return self.do == 'UPDATE'


def process_filter_options(
        dataclass_type: type[_T],
        filter_options: dict,
        vars_: list
) -> ProcessedFilters:
    result = ProcessedFilters(
        vars_
    )

    if not filter_options:
        return result

    for field, operators_object in filter_options.items():
        field = get_model_field(dataclass_type, field)

        if not field:
            continue

        if not field.can_filter:
            continue

        if isinstance(operators_object, (list, set, tuple)):
            values = operators_object
            operators_object = {
                'IN': tuple(values)
            }

        if not isinstance(operators_object, dict):
            value = operators_object
            operators_object = {
                '=': value
            }

        for operator, value in operators_object.items():
            operator = operator.upper()

            if operator in ('IN', 'NOT IN'):
                value = tuple(value)

                result.vars.append(value)
                result.append(
                    ProcessedFilter(
                        column=field.name,
                        operator=operator,
                        value='%s'
                    )
                )

                continue

            if not isinstance(value, (list, set, tuple)):
                value = [value]

            for value_ in value:
                if value_ is None and operator == '=':
                    operator = 'IS'
                if value_ is None and operator in ('!=', '<>'):
                    operator = 'IS NOT'

                result.vars.append(value_)
                result.append(
                    ProcessedFilter(
                        column=field.name,
                        operator=operator,
                        value='%s'
                    )
                )

    return result


def process_sort_options(
        dataclass_type: type[_T],
        sort_options: dict
):
    result = ProcessedSortingOptions()

    if not sort_options:
        return result

    for field, direction in sort_options.items():
        field = get_model_field(dataclass_type, field)

        if not field:
            continue

        if not field.can_sort:
            continue

        direction = direction.upper()

        if direction not in ('ASC', 'DESC'):
            continue

        result.append(
            ProcessedSortingOption(
                column=field.name,
                direction=direction
            )
        )

    return result


def process_pagination_options(
        pagination_options: dict,
        vars_: list
):
    result = ProcessedPaginationOptions()

    if not pagination_options:
        return result

    if 'limit' in pagination_options:
        result.limit = pagination_options['limit']
        vars_.append(result.limit)

    if 'skip' in pagination_options:
        result.skip = pagination_options['skip']
        vars_.append(result.skip)

    return result


def process_group_by_options(
        dataclass_type: type[_T],
        group_by_options: list
):
    result = ProcessedGroupByOptions()

    if not group_by_options:
        return result

    model_fields = registry.get(dataclass_type).model_fields

    for column in group_by_options:
        if column not in model_fields:
            continue

        model_field = model_fields[column]

        if not model_field.can_group:
            continue

        result.append(model_field.name)

    return result


def process_on_conflict_options(
        dataclass_type: type[_T],
        on_conflict_options: dict
):
    result = ProcessedOnConflictOptions()

    if not on_conflict_options:
        return result

    assert 'do' in on_conflict_options

    do: str
    do = on_conflict_options['do']
    do = do.upper()

    assert do in ('UPDATE', 'NOTHING')

    conflict_targets = on_conflict_options.get(
        'conflict_targets',
        ()
    )
    update_columns = on_conflict_options.get(
        'update_columns',
        ()
    )

    is_conflict_targets_specified = (
        'conflict_targets' in on_conflict_options
    )
    is_update_columns_specified = (
        'update_columns' in on_conflict_options
    )

    model_fields = get_model_fields(dataclass_type, 'psycopg2')
    model_fields = list(model_fields)

    for field in model_fields:
        if is_conflict_targets_specified:
            if field.column_name in conflict_targets:
                result.conflict_targets.append(field.column_name)
        else:
            if field.include_in_on_conflict_targets:
                result.conflict_targets.append(field.column_name)

    if do != 'NOTHING':
        for field in model_fields:
            if is_update_columns_specified:
                if field.column_name in update_columns:
                    result.update_columns.append(field.column_name)
            else:
                if field.include_in_on_conflict_update:
                    result.update_columns.append(field.column_name)

    result.do = do
    result.conflict_targets = tuple(result.conflict_targets)
    result.update_columns = tuple(result.update_columns)

    return result
