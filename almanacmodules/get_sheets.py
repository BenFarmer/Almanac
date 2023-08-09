#!/bin/env python

from almanacmodules import cred_check
from almanacmodules import config

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import (
    Credentials,
)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

EXTENDED_CFG_ID = "16Q2BKEWQW5A2nQ77AQbSINZ7tG4LJRVhGHfvfKHC0EM"
ranges = (
    "world!A2:R",
    "monsters!A2:O36",
    "biome!A2:B",
    "astral!A2:D",
    "natural!A2:P",
    "effects!A2:J7",
)


class MasterConfig:
    # these _confi_master contain the finalized data and are what need to be imported
    world_config_master = []
    monster_config_master = []
    biome_config_master = []
    astral_config_master = []
    natural_config_master = []
    effects_config_master = []

    def __init__(self):
        self.master_config = (
            MasterConfig.world_config_master,
            MasterConfig.monster_config_master,
            MasterConfig.biome_config_master,
            MasterConfig.astral_config_master,
            MasterConfig.natural_config_master,
            MasterConfig.effects_config_master,
        )

    def append_configs(
        self,
        world_config,
        monster_config,
        biome_config,
        astral_config,
        natural_config,
        effects_config,
    ):
        MasterConfig.world_config_master = world_config
        MasterConfig.monster_config_master = monster_config
        MasterConfig.biome_config_master = biome_config
        MasterConfig.astral_config_master = astral_config
        MasterConfig.natural_config_master = natural_config
        MasterConfig.effects_config_master = effects_config


class SheetConversion:
    def __init__(self):
        self.raw_data = self.sheet_api(
            cred_check.confirmation()
        )  # this reads the sheets info
        self.configs = (
            self.get_config()
        )  # this takes raw_data and turns it into finished_configs

    def get_config(self):
        (
            world_raw,
            monster_raw,
            biome_raw,
            astral_raw,
            natural_raw,
            effects_raw,
        ) = self.raw_data
        finished_configs = self.config_maker(
            world_raw, monster_raw, biome_raw, astral_raw, natural_raw, effects_raw
        )
        return finished_configs

    def config_maker(
        self, world_raw, monster_raw, biome_raw, astral_raw, natural_raw, effects_raw
    ):
        world_model = []
        for row in world_raw:
            world_model.append(
                config.world(
                    id=row[0],
                    name=row[1],
                    type=row[2],
                    forest=row[3],
                    plains=row[4],
                    desert=row[5],
                    swamp=row[6],
                    jungle=row[7],
                    mountain=row[8],
                    lake=row[9],
                    river=row[10],
                    beach=row[11],
                    ocean=row[12],
                    underdark=row[13],
                    urban=row[14],
                    temp_zone=row[15],
                    capital=row[16],
                    owner=row[17],
                )
            )

        monster_model = []
        for row in monster_raw:
            monster_model.append(
                config.monster(
                    id=row[0],
                    name=row[1],
                    type=row[2],
                    forest=row[3],
                    plains=row[4],
                    desert=row[5],
                    swamp=row[6],
                    jungle=row[7],
                    mountain=row[8],
                    lake=row[9],
                    river=row[10],
                    ocean=row[11],
                    beach=row[12],
                    underdark=row[13],
                    urban=row[14],
                )
            )

        biome_model = []
        for row in biome_raw:
            biome_model.append(config.biome(id=row[0], name=row[1]))

        astral_model = []
        for row in astral_raw:
            astral_model.append(
                config.astral(id=row[0], name=row[1], type=row[2], moon_of=row[3])
            )

        natural_model = []
        for row in natural_raw:
            natural_model.append(
                config.natural(
                    id=row[0],
                    name=row[1],
                    forest=row[2],
                    plains=row[3],
                    desert=row[4],
                    swamp=row[5],
                    jungle=row[6],
                    mountain=row[7],
                    lake=row[8],
                    river=row[9],
                    ocean=row[10],
                    beach=row[11],
                    underdark=row[12],
                    urban=row[13],
                    season=row[14],
                    temp_zone=[int(x) for x in row[15].split(",")],
                )
            )

        effects_model = []
        for row in effects_raw:
            effects_model.append(
                config.effects(
                    id=row[0],
                    type=row[1],
                    rarity=row[2],
                    base_duration=row[3],
                    tags=[str(x) for x in row[4].split(",")],
                    effect_text_rarity=[int(x) for x in row[5].split(",")],
                    initial_text=row[6],
                    modifier=[str(x) for x in row[7].split(",")],
                    effect_text=[str(x) for x in row[8].split(",")],
                    fallout=[str(x) for x in row[9].split(",")],
                )
            )

        return (
            world_model,
            monster_model,
            biome_model,
            astral_model,
            natural_model,
            effects_model,
        )

    def sheet_api(self, creds):
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        world_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[0]).execute()
        )

        monster_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[1]).execute()
        )

        biome_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[2]).execute()
        )

        astral_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[3]).execute()
        )

        natural_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[4]).execute()
        )

        effects_data = (
            sheet.values().get(spreadsheetId=EXTENDED_CFG_ID, range=ranges[5]).execute()
        )

        world_raw = world_data.get("values", [])
        monster_raw = monster_data.get("values", [])
        biome_raw = biome_data.get("values", [])
        astral_raw = astral_data.get("values", [])
        natural_raw = natural_data.get("values", [])
        effects_raw = effects_data.get("values", [])

        return (world_raw, monster_raw, biome_raw, astral_raw, natural_raw, effects_raw)
