"""
Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from pathlib import Path

import yaml
from hydra.experimental import compose as hydra_compose

from nndet.io.paths import Pathlike, get_task


def load_dataset_info(task_dir: Pathlike) -> dict:
    """
    Load dataset information from a given task directory

    Args:
        task_dir: path to directory of specific task e.g. ../Task12_LIDC

    Returns:
        dict: loaded dataset info. Typically includes:
            `name` (str): name of dataset
            `target_class` (str)
    """
    task_dir = Path(task_dir)
    yaml_path = task_dir / "dataset.yaml"
    json_path = task_dir / "dataset.json"

    if yaml_path.is_file():
        with open(yaml_path, 'r') as f:
            data = yaml.full_load(f)
    elif json_path.is_file():
        with open(json_path, "r") as f:
            data = json.load(f)
    else:
        raise RuntimeError(f"Did not find dataset.json or dataset.yaml in {task_dir}")
    return data


def compose(task, *args, models: bool = False, **kwargs) -> dict:
    from omegaconf import OmegaConf
    cfg = hydra_compose(*args, **kwargs)
    OmegaConf.set_struct(cfg, False)
    task_name = get_task(task, name=True, models=models)
    cfg["task"] = task_name
    cfg["data"] = load_dataset_info(get_task(task_name))
    return cfg
