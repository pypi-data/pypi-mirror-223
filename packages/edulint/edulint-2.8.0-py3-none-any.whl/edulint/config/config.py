from edulint.config.arg import ProcessedArg, UnprocessedArg, ImmutableArg
from edulint.linters import Linter
from edulint.options import (
    UnionT,
    ImmutableT,
    Option,
    DEFAULT_CONFIG,
    BASE_CONFIG,
    TakesVal,
    OptionParse,
    get_option_parses,
    get_name_to_option,
)
from edulint.config.file_config import load_toml_file
from edulint.config.config_translations import (
    get_config_translations,
    get_ib111_translations,
    Translation,
)
from typing import Dict, List, Optional, Tuple, Iterator, Any
from dataclasses import dataclass
from argparse import Namespace
import re
import sys
import shlex


@dataclass(frozen=True)
class Config:
    config: Tuple[ImmutableArg]

    @staticmethod
    def to_immutable(v: UnionT) -> ImmutableT:
        return v if not isinstance(v, list) else tuple(v)

    def __init__(
        self,
        config: Optional[List[ProcessedArg]] = None,
        option_parses: Dict[Option, OptionParse] = get_option_parses(),
    ) -> None:
        config = config if config is not None else []
        wip_config: List[Optional[ImmutableArg]] = [None for _ in Option]

        for arg in config:
            assert wip_config[int(arg.option)] is None
            wip_config[int(arg.option)] = ImmutableArg(arg.option, self.to_immutable(arg.val))

        object.__setattr__(
            self,
            "config",
            tuple(
                [
                    arg
                    if arg is not None
                    else ImmutableArg(o, self.to_immutable(option_parses[o].default))
                    for o, arg in zip(Option, wip_config)
                ]
            ),
        )

    def __str__(self) -> str:
        return f"Config({', '.join(arg.option.name + '=' + str(arg.val) for arg in self.config)})"

    def __getitem__(self, option: Option) -> ImmutableT:
        return self.config[int(option)].val

    def __contains__(self, option: Option) -> bool:
        return self[option] is not None

    def __iter__(self) -> Iterator[ImmutableArg]:
        return filter(lambda x: x is not None, self.config.__iter__())


def extract_args(filename: str) -> List[str]:
    edulint_re = re.compile(r"\s*#[\s#]*edulint:\s*", re.IGNORECASE)
    ib111_re = re.compile(r"\s*from\s+ib111\s+import\s+week_(\d+)", re.IGNORECASE)

    result: List[str] = []
    with open(filename, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()

            edmatch = edulint_re.match(line)
            if edmatch:
                raw_args = line[edmatch.end() :]
                result.extend(shlex.split(raw_args))

            ibmatch = ib111_re.match(line)
            if ibmatch:
                result.append(f"{Option.IB111_WEEK.to_name()}={ibmatch.group(1)}")

    return result


def parse_option(
    option_parses: Dict[Option, OptionParse],
    name_to_option: Dict[str, Option],
    name: str,
    val: Optional[str],
) -> Optional[Option]:
    option = name_to_option.get(name)

    if option is None:
        print(f"edulint: unrecognized option {name}", file=sys.stderr)
    else:
        option_parse = option_parses[option]
        if option_parse.takes_val == TakesVal.YES and val is None:
            print(
                f"edulint: option {name} takes an argument but none was supplied",
                file=sys.stderr,
            )
        elif option_parse.takes_val == TakesVal.NO and val is not None:
            print(
                f"edulint: option {name} takes no argument but {val} was supplied",
                file=sys.stderr,
            )
        else:
            return option
    return None


def parse_args(
    args: List[str], option_parses: Dict[Option, OptionParse]
) -> Tuple[str, List[UnprocessedArg]]:
    name_to_option = get_name_to_option(option_parses)

    def get_name_val(arg: str) -> Tuple[str, Optional[str]]:
        if "=" in arg:
            name, val = arg.split("=", 1)
            return name, val
        return arg, None

    result: List[UnprocessedArg] = []
    config_path = DEFAULT_CONFIG
    for arg in args:
        name, val = get_name_val(arg)
        option = parse_option(option_parses, name_to_option, name, val)
        if option is not None:
            result.append(UnprocessedArg(option, val))
        if option == Option.CONFIG and val is not None:
            config_path = val

    return config_path, result


def parse_config_file(
    path: str, option_parses: Dict[Option, OptionParse]
) -> Optional[List[UnprocessedArg]]:
    def print_invalid_type_message(option: Option, val: Any) -> None:
        print(f"edulint: invalid value type {type(val)} of value {val} for option {Option.CONFIG}")

    def parse_base_config(config_dict: Dict[str, Any]) -> Optional[List[UnprocessedArg]]:
        rec_config = config_dict.get(Option.CONFIG.to_name(), BASE_CONFIG)
        if not isinstance(rec_config, str):
            print_invalid_type_message(Option.CONFIG, rec_config)
            rec_config = BASE_CONFIG
        return parse_config_file(rec_config, option_parses)

    def val_to_str(option: Option, val: Any) -> Optional[str]:
        if isinstance(val, str):
            return val
        if isinstance(val, list):
            return ",".join(val)
        if isinstance(val, tuple):
            key, value = val
            value = val_to_str(option, value)
            return f"--{key}={value}" if value is not None else None
        print_invalid_type_message(option, val)
        return None

    config_dict = load_toml_file(path)
    if config_dict is None:
        return None

    result = parse_base_config(config_dict) if path != BASE_CONFIG else []
    if result is None:
        return None

    name_to_option = get_name_to_option(option_parses)
    for name, val in config_dict.items():
        option = parse_option(option_parses, name_to_option, name, val)
        if option is None or option == Option.CONFIG:  # config is handled as the first option
            continue

        if not isinstance(val, dict):
            to_process = [val]
        elif option.to_name() not in {linter.to_name() for linter in Linter}:
            print_invalid_type_message(option, val)
            continue
        else:
            to_process = list(val.items())

        for val in to_process:
            str_val = val_to_str(option, val)
            if str_val is not None:
                result.append(UnprocessedArg(option, str_val))

    return result


def fill_in_val(arg: UnprocessedArg, translation: List[str]) -> List[str]:
    result = []
    for t in translation:
        if "<val>" in t:
            assert isinstance(arg.val, str)
            result.append(t.replace("<val>", arg.val))
        else:
            result.append(t)
    return result


def combine_and_translate(
    args: List[UnprocessedArg],
    option_parses: Dict[Option, OptionParse],
    config_translations: Dict[Option, Translation],
    ib111_translations: List[Translation],
) -> Config:
    def combine(option_vals: List[UnionT], option: Option, val: Optional[str]) -> None:
        parse = option_parses[option]
        old_val = option_vals[int(option)]
        option_vals[int(option)] = parse.combine(old_val, parse.convert(val))

    def apply_translation(option_vals: List[UnionT], translated: Translation) -> None:
        translated_option = translated.for_linter.to_option()
        for val in translated.vals:
            combine(option_vals, translated_option, val)

    option_vals = [option_parses[o].default for o in Option]

    for arg in args:
        combine(option_vals, arg.option, arg.val)

        translated = config_translations.get(arg.option)
        if translated is not None and option_vals[int(arg.option)] not in (False, None):
            apply_translation(option_vals, translated)

    ib111_week = option_vals[int(Option.IB111_WEEK)]
    if ib111_week is not None:
        assert isinstance(ib111_week, int)
        if 0 <= ib111_week < len(ib111_translations):
            apply_translation(option_vals, ib111_translations[ib111_week])
        else:
            print(
                f"edulint: option {Option.IB111_WEEK.to_name()} has value {ib111_week} which is invalid;"
                f"allowed values are 0 to {len(ib111_translations)}",
                file=sys.stderr,
            )

    return Config([ProcessedArg(o, v) for o, v in zip(Option, option_vals) if v is not None])


def get_config_one(
    filename: str,
    cmd_args: List[str],
    option_parses: Dict[Option, OptionParse] = get_option_parses(),
    config_translations: Dict[Option, Translation] = get_config_translations(),
    ib111_translation: List[Translation] = get_ib111_translations(),
) -> Optional[Config]:
    configs = get_config_many(
        [filename], cmd_args, option_parses, config_translations, ib111_translation
    )
    if len(configs) == 0:
        return None
    return configs[0][1]


def get_config_many(
    filenames: List[str],
    cmd_args_raw: List[str],
    option_parses: Dict[Option, OptionParse] = get_option_parses(),
    config_translations: Dict[Option, Translation] = get_config_translations(),
    ib111_translation: List[Translation] = get_ib111_translations(),
) -> List[Tuple[List[str], Config]]:
    def partition(
        configs: List[Tuple[str, List[UnprocessedArg]]]
    ) -> List[Tuple[List[str], Tuple[str, List[UnprocessedArg]]]]:
        immutable_configs = [(f, tuple(c)) for f, c in configs]

        dedup_configs = list(set(immutable_configs))
        indices = [dedup_configs.index(config) for config in immutable_configs]
        partitioned: List[List[str]] = [[] for _ in dedup_configs]

        for i, filename in enumerate(filenames):
            partitioned[indices[i]].append(filename)

        return list(zip(partitioned, [(f, list(c)) for f, c in dedup_configs]))

    cmd_config_path, cmd_args = parse_args(cmd_args_raw, option_parses)
    cmd_sets_config = any(arg.option == Option.CONFIG for arg in cmd_args)

    config_from_files = [
        parse_args(extract_args(filename), option_parses) for filename in filenames
    ]

    config_paths = {cmd_config_path} if cmd_sets_config else {c for c, _ in config_from_files}
    config_files_args = {
        config_path: parse_config_file(config_path, option_parses) for config_path in config_paths
    }

    result: List[Tuple[List[str], Config]] = []
    for files, (linted_config_path, linted_file_args) in partition(config_from_files):
        config_path = cmd_config_path if cmd_sets_config else linted_config_path
        config_file_args = config_files_args[config_path]
        if config_file_args is None:
            continue
        config = combine_and_translate(
            config_file_args + linted_file_args + cmd_args,
            option_parses,
            config_translations,
            ib111_translation,
        )
        result.append((files, config))
    return result


def get_cmd_args(args: Namespace) -> List[str]:
    return [s for arg in args.options for s in shlex.split(arg)]
