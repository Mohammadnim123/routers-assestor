import pandas as pd
import numpy as np


class PublicMapperService:

    file_paths = {
        "commands_router":"com_and_conf/static/commands_router.csv",
        "commands_switch":"com_and_conf/static/commands_switch.csv",
        "configurations":"com_and_conf/static/configurations.csv",
    }

    types = [
        'commands_router',
        'commands_switch',
        'configurations',
    ]

    all_companies = [
        'cisco',
        'hp',
        'huawei',
    ]

    configurations_types = {
        "RouterOspf": 0,
        "RouterRip": 1,
        "RouterConf": 2,
    }

    configurations_fields = {
        "RouterOspf": ["[rNetadd1]", "[rSubadd1]", "[avar]", "[rNetadd2]", "[rSubadd2]"],
        "RouterRip": ["[NUM]", "[network_address]", "[networ-address-2]"],
        "RouterConf": ["[HN]", "[GE]", "[netadd1]", "[subadd1]"],
    }

    @classmethod
    def request_types(cls):
        return cls.types

    @classmethod
    def companies(cls, exclude=None):
        companies = cls.all_companies.copy()
        if exclude and exclude in companies:
            companies.remove(exclude)
        return companies

    @classmethod
    def listing_data(cls, type, source_company):
        if type == "configurations":
            return list(cls.configurations_types.keys())
        df = pd.read_csv(cls.file_paths[type])
        df = df.dropna()
        hp_data = df[source_company].tolist()
        return hp_data

    @classmethod
    def fields_to_change(cls, type, command):
        if type == "commands_router":
            commands_router_fields = [
                "[network_address]",
                "[subnet_mask]",
            ]
            fields = []
            for field in commands_router_fields:
                if field in command:
                    fields.append(field)
            return fields
        elif type == "configurations":
            return cls.configurations_fields[command]
        else:
            return []

    @classmethod
    def get_desired_data(cls, type, source_company, command, extra_fields, destination_company):
        df = pd.read_csv(cls.file_paths[type])
        if type == "configurations":
            conf_row = cls.configurations_types[command]
            targeted_conf = df.loc[conf_row, destination_company]
            for field, value in extra_fields.items():
                targeted_conf = targeted_conf.replace(field, value)
            return {
                "result_conf": targeted_conf
            }
        else:
            network_address = extra_fields.get("[network_address]", "")
            subnet_mask = extra_fields.get("[subnet_mask]", "")
            matching_row = df[df[source_company] == command] 
            if not matching_row.empty:
                potential_command = matching_row[destination_company].iloc[0]
                command = potential_command if not isinstance(potential_command, float) else ''
                potential_description = matching_row["description"].iloc[0]
                description = potential_description if not isinstance(potential_description, float) else ''
                command = command.replace("[network_address]", network_address)
                command = command.replace("[subnet_mask]", subnet_mask)
                return {
                    "result_command": command,
                    "description": description
                }
            else:
                return {
                    "result_command": "",
                    "description": ""
                }
