import json
import os
import yaml
from yaml import SafeLoader

from easyecs.cloudformation.fetch import (
    fetch_account_id,
    fetch_availability_zones,
    fetch_container_subnet_ids,
    fetch_region,
    fetch_vpc_id,
)
from easyecs.helpers.color import Color
from easyecs.model.ecs import EcsFileModel


def read_ecs_file() -> EcsFileModel:
    with open("./ecs.yml") as f:
        data = yaml.load(f, Loader=SafeLoader)
    return EcsFileModel(**data)


def load_settings(aws_account):
    try:
        os.makedirs(".tmp", exist_ok=True)
        with open(".tmp/easyecs.tmp", "r") as f:
            cache_configuration = json.load(f)
    except FileNotFoundError:
        cache_configuration = {}

    account_cache_configuration = cache_configuration.get(aws_account, {})

    aws_region = account_cache_configuration.get("aws_region", None)
    if not aws_region:
        aws_region = fetch_region()
    azs = account_cache_configuration.get("azs", None)
    if not azs:
        azs = fetch_availability_zones(aws_region)
    aws_account_id = account_cache_configuration.get("aws_account_id", None)
    if not aws_account_id:
        aws_account_id = fetch_account_id()
    vpc_id = account_cache_configuration.get("vpc_id", None)
    if not vpc_id:
        vpc_id = fetch_vpc_id()
    subnet_ids = account_cache_configuration.get("subnet_ids", None)
    if not subnet_ids:
        subnet_ids = fetch_container_subnet_ids(vpc_id)

    cache_configuration[aws_account] = {
        "aws_region": aws_region,
        "aws_account_id": aws_account_id,
        "vpc_id": vpc_id,
        "subnet_ids": subnet_ids,
        "azs": azs,
    }

    print(
        "Selected aws account:"
        f" {Color.BOLD}{Color.GREEN}{aws_account}{Color.END} \u2705"
    )
    print(f"Selected region: {Color.BOLD}{Color.GREEN}{aws_region}{Color.END} \u2705")
    print(f"Selected vpc_id: {Color.BOLD}{Color.GREEN}{vpc_id}{Color.END} \u2705")
    print(
        "Selected subnet_ids:"
        f" {Color.BOLD}{Color.GREEN}{','.join(subnet_ids)}{Color.END} \u2705"
    )
    print(
        "Selected availability zones:"
        f" {Color.BOLD}{Color.GREEN}{','.join(azs)}{Color.END} \u2705"
    )

    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/easyecs.tmp", "w") as f:
        json.dump(cache_configuration, f)

    return cache_configuration[aws_account]
