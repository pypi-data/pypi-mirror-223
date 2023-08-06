import re
import os
from collections import namedtuple

ConfigItem = namedtuple("ConfigItem", "initfn default")


class ModelFilterException(Exception):
    pass


# Model list
# This list is sorted in priority order, with the best models first
# The best model that fits in the memory bounds and matches the model filter
# will be selected
models = [
    {
        "name": "flan-alpaca-xl",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "alpaca"],
        "params": 3e9,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",  # HF says apache-2.0, but alpaca is NC
    },
    {
        "name": "flan-alpaca-gpt4-xl",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "gpt4-alpaca"],
        "params": 3e9,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",  # HF says apache-2.0, but alpaca is NC
    },
    {
        "name": "flan-t5-xl",
        "tuning": "instruct",
        "datasets": ["c4", "flan"],
        "params": 3e9,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "apache-2.0",
    },
    {
        "name": "fastchat-t5-3b-v1.0",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "sharegpt"],
        "params": 3e9,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "apache-2.0",  # This does use OpenAI-generated data
    },
    {
        "name": "LaMini-Flan-T5-783M",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "lamini"],
        "params": 783e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",
    },
    {
        "name": "flan-t5-large",
        "tuning": "instruct",
        "datasets": ["c4", "flan"],
        "params": 783e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "apache-2.0",
    },
    {
        "name": "LaMini-Flan-T5-248M",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "lamini"],
        "params": 248e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",
    },
    {
        "name": "flan-alpaca-base",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "alpaca"],
        "params": 248e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",  # HF says apache-2.0, but alpaca is NC
    },
    {
        "name": "flan-t5-base",
        "tuning": "instruct",
        "datasets": ["c4", "flan"],
        "params": 248e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "apache-2.0",
    },
    {
        "name": "LaMini-Flan-T5-77M",
        "tuning": "instruct",
        "datasets": ["c4", "flan", "lamini"],
        "params": 77e6,
        "backend": "ct2",
        "quantization": "int8",
        "architecture": "encoder-decoder-transformer",
        "license": "cc-by-nc-4.0",
    },
    {
        "name": "flan-t5-small",
        "tuning": "instruct",
        "datasets": ["c4", "flan"],
        "params": 77e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "apache-2.0",
    },
    {
        "name": "LaMini-GPT-774M",
        "tuning": "instruct",
        "datasets": ["webtext", "lamini"],
        "params": 774e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "decoder-only-transformer",
        "license": "mit",
    },
    {
        "name": "LaMini-GPT-124M",
        "tuning": "instruct",
        "datasets": ["webtext", "lamini"],
        "params": 124e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "decoder-only-transformer",
        "license": "mit",
    },
    {
        "name": "codet5p-770m-py",
        "tuning": "code",
        "datasets": ["github-code"],
        "params": 770e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "bsd-3-clause",
    },
    {
        "name": "codet5p-220m-py",
        "tuning": "code",
        "datasets": ["github-code"],
        "params": 220e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-decoder-transformer",
        "license": "bsd-3-clause",
    },
    {
        "name": "all-MiniLM-L6-v2",
        "tuning": "embedding",
        "params": 22e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-only-transformer",
        "license": "apache-2.0",
    },
    {
        "name": "e5-small-v2",
        "tuning": "embedding",
        "params": 33e6,
        "quantization": "int8",
        "backend": "ct2",
        "architecture": "encoder-only-transformer",
        "license": "mit",
    },
]


class Config(dict):
    """
    Store configuration information for the package.

    This is a dictionary that provides data basic data validation.

    Only appropriate keys and values are allowed to be set.

    >>> c = Config({'max_ram': '4gb'})
    >>> c
    {...'max_ram': 4.0...}

    >>> c = Config({'instruct_model': 'flan-t5-small'})
    >>> c
    {...'instruct_model': 'flan-t5-small'...}

    >>> c = Config({'model_license': 'apache|mit|bsd'})
    >>> c
    {...'model_license': re.compile('apache|mit|bsd')...}

    >>> c = Config({'instruct_model': 'flan-t5-bad'})
    Traceback (most recent call last):
      ...
    KeyError: 'flan-t5-bad'

    >>> c = Config({'bad_value': 1})
    Traceback (most recent call last):
      ...
    KeyError: 'bad_value'

    >>> c = Config()
    >>> c.update({'bad_value': 1})
    Traceback (most recent call last):
      ...
    KeyError: 'bad_value'

    """

    model_names = {m["name"]: m for m in models}

    def __init__(self, config={}):
        # Defaults are loaded first
        for key in Config.schema:
            self[key] = self.schema[key].default

        # Environment variables override defaults
        for key in Config.schema:
            value = os.environ.get(f"LANGUAGEMODELS_{key.upper()}")
            if value:
                self[key] = value

        # Any values passed in the config dict override environment vars
        for key in config.keys():
            self[key] = config[key]

    def __setitem__(self, key, value):
        super().__setitem__(key, Config.schema[key].initfn(value))

        # Auto-adjust instruct_model when filters change
        if key == "max_ram" or key == "model_license":
            found = set()
            for model in models:
                if model["quantization"] == "int8":
                    memsize = model["params"] / 1e9
                elif model["quantization"] == "q3_k_m":
                    memsize = model["params"] * 0.48 / 1e9
                elif model["quantization"] == "q4_k_m":
                    memsize = model["params"] * 0.59 / 1e9

                sizefit = memsize < self["max_ram"]

                if "model_license" in self:
                    licensematch = self["model_license"].match(model["license"])
                else:
                    licensematch = True

                if model["tuning"] not in found and sizefit and licensematch:
                    self[model["tuning"] + "_model"] = model["name"]
                    found.add(model["tuning"])

            if len(found) < 3:
                raise ModelFilterException("Unable to find models to match filters")

    def update(self, other):
        for key in other:
            self[key] = other[key]

    @staticmethod
    def validate_model(model_name):
        return Config.model_names[model_name]["name"]

    @staticmethod
    def validate_device(device):
        assert device in ["auto", "cpu"]

        return device

    @staticmethod
    def convert_to_gb(space):
        """Convert max RAM string to int

        Output will be in gigabytes

        If not specified, input is assumed to be in gigabytes

        >>> Config.convert_to_gb("512")
        512.0

        >>> Config.convert_to_gb(".5")
        0.5

        >>> Config.convert_to_gb("4G")
        4.0

        >>> Config.convert_to_gb("256mb")
        0.25

        >>> Config.convert_to_gb("256M")
        0.25

        >>> Config.convert_to_gb("small")
        0.2

        >>> Config.convert_to_gb("base")
        0.48

        >>> Config.convert_to_gb("large")
        1.0

        >>> Config.convert_to_gb("xl")
        4.0

        >>> Config.convert_to_gb("xxl")
        16.0
        """

        if isinstance(space, int) or isinstance(space, float):
            return float(space)

        size_names = {
            "small": 0.2,
            "base": 0.48,
            "large": 1.0,
            "xl": 4.0,
            "xxl": 16.0,
        }

        if space.lower().strip() in size_names:
            return size_names[space.lower().strip()]

        multipliers = {
            "g": 1.0,
            "m": 2 ** -10,
        }

        space = space.lower()
        space = space.rstrip("b")

        if space[-1] in multipliers:
            return float(space[:-1]) * multipliers[space[-1]]
        else:
            return float(space)


Config.schema = {
    "max_ram": ConfigItem(Config.convert_to_gb, 0.48),
    "device": ConfigItem(Config.validate_device, "cpu"),
    "model_license": ConfigItem(re.compile, ".*"),
    "instruct_model": ConfigItem(Config.validate_model, "LaMini-Flan-T5-248M"),
    "embedding_model": ConfigItem(Config.validate_model, "all-MiniLM-L6-v2"),
    "code_model": ConfigItem(Config.validate_model, "codet5p-220m-py"),
}

config = Config()
