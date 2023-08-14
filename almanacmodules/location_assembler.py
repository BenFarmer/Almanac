#!/bin/env python

""" location_assembler takes the biome data for the country that Almanac
    is processing and creates its version of a 'map' of where each biome
    within the country lies.
"""


# BUILT INS
import random
from operator import itemgetter

# THIRD PARTY
from pydantic import BaseModel

# PERSONAL
from almanacmodules.get_sheets import MasterConfig


# pydantic class schema
class IndvBiome(BaseModel):
    indv_id: int  # id of the individual biome
    biome_name: str  # name of biome contained ('forest', 'desert', 'plains', etc)
    cell_position_x: int  # x value of large cell
    cell_position_y: int  # y value of large cell
    region_id: int  # unique id of group within cell


# [[0, 'forest', 0, 1, 0],[1, 'forest', 0, 1, 0], [2, 'plains', 0, 1, 1]]


class LocationAssembler:
    def __init__(self, location_id):
        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.biome_config = master_config.biome_config_master

        self.location_id = location_id
        self.indv_biomes = []
        self.biomes = {
            "forest",
            "plains",
            "desert",
            "swamp",
            "jungle",
            "mountain",
            "lake",
            "river",
            "beach",
        }
        self.region_id = -1  # set because when regions are assigned it adds 1
        self.bucket_ranges = []

        self._biome_assigner()
        # takes the 100 initial scores and transforms them into 81 values in a list (indv_biomes)
        # that take the format of [id, biome], [id, biome], etc...
        self.cells = list(self._cell_mixer())
        # takes indv_biomes list, shuffles it randomly, then splits it into 9 even groups
        # and assigns it to a new list called 'cells'
        self._cell_coords()
        # appends self.cells with a 3rd value in each variable that is its cell location
        # and configures the cells into a 3x3 grid that can be referenced by coordinates
        # 3rd value is in format [x, y]
        # finished self.cells should look like: ([id, biome, [x, y]], [id, biome, [x, y]], etc
        self._cell_grouper()
        # sorts the like-biome indv_biomes within each cell
        # then assigns each unique indv_biome within the self.cells a group number
        # finished self.cells: ([id, biome, [x,y], 1], [id, biomes [x, y], 1], etc)

    #        print('cells', self.cells)

    def _biome_assigner(self):
        biome_score = self.world_config[self.location_id].dict(include=self.biomes)
        initial_buckets = biome_score.values()
        #        print('inital_buckets of 100', initial_buckets)
        buckets = []
        for value in initial_buckets:
            buckets.append(round(value * 0.81))
        #        print('buckets out of 81', buckets)

        bucket_count = 0
        for bucket in buckets:
            bucket_count += int(bucket)
        #            print(bucket_count)

        if bucket_count == 80:
            buckets[8] += 1
        elif bucket_count == 82:
            buckets[8] -= 1

        prior_bucket = 0
        for bucket_sub, bucket in enumerate(buckets):
            new_start = prior_bucket + 1
            new_stop = new_start + int(bucket) - 1
            try:
                self.bucket_ranges.append((new_start, new_stop))
            except IndexError:
                self.bucket_ranges.append(bucket, 81)
            finally:
                prior_bucket = new_stop

        #        print("buckets", buckets)
        #        print("bucket ranges", self.bucket_ranges)

        indv_bio_id = 0
        for bucket in buckets:
            for bio_id in range(bucket):
                r = self.bucket_ranges
                indv_bio_id += 1
                if indv_bio_id >= r[0][0] and bio_id <= r[0][1]:
                    biome_name = "forest"
                if indv_bio_id >= r[1][0] and bio_id <= r[1][1]:
                    biome_name = "plains"
                if indv_bio_id >= r[2][0] and bio_id <= r[2][1]:
                    biome_name = "desert"
                if indv_bio_id >= r[3][0] and bio_id <= r[3][1]:
                    biome_name = "swamp"
                if indv_bio_id >= r[4][0] and bio_id <= r[4][1]:
                    biome_name = "jungle"
                if indv_bio_id >= r[5][0] and bio_id <= r[5][1]:
                    biome_name = "mountain"
                if indv_bio_id >= r[6][0] and bio_id <= r[6][1]:
                    biome_name = "lake"
                if indv_bio_id >= r[7][0] and bio_id <= r[7][1]:
                    biome_name = "river"
                if indv_bio_id >= r[8][0] and bio_id <= r[8][1]:
                    biome_name = "beach"
                self.indv_biomes.append([indv_bio_id, biome_name])

    def _cell_mixer(self):
        n = 9
        random.shuffle(self.indv_biomes)
        for i in range(0, len(self.indv_biomes), n):
            yield self.indv_biomes[i : i + n]  # noqa: E203
            #            print('indv_bioms, (?)', self.indv_biomes)

    def _cell_coords(self):
        for id in enumerate(self.indv_biomes):
            index = 0
            if self.indv_biomes[id[0]] in self.cells[0]:
                index = self.cells[0].index(self.indv_biomes[id[0]])
                self.cells[0][index].append([0, 0])

            elif self.indv_biomes[id[0]] in self.cells[1]:
                index = self.cells[1].index(self.indv_biomes[id[0]])
                self.cells[1][index].append([1, 0])

            elif self.indv_biomes[id[0]] in self.cells[2]:
                index = self.cells[2].index(self.indv_biomes[id[0]])
                self.cells[2][index].append([2, 0])

            elif self.indv_biomes[id[0]] in self.cells[3]:
                index = self.cells[3].index(self.indv_biomes[id[0]])
                self.cells[3][index].append([0, 1])

            elif self.indv_biomes[id[0]] in self.cells[4]:
                index = self.cells[4].index(self.indv_biomes[id[0]])
                self.cells[4][index].append([1, 1])

            elif self.indv_biomes[id[0]] in self.cells[5]:
                index = self.cells[5].index(self.indv_biomes[id[0]])
                self.cells[5][index].append([2, 1])

            elif self.indv_biomes[id[0]] in self.cells[6]:
                index = self.cells[6].index(self.indv_biomes[id[0]])
                self.cells[6][index].append([0, 2])

            elif self.indv_biomes[id[0]] in self.cells[7]:
                index = self.cells[7].index(self.indv_biomes[id[0]])
                self.cells[7][index].append([1, 2])

            elif self.indv_biomes[id[0]] in self.cells[8]:
                index = self.cells[8].index(self.indv_biomes[id[0]])
                self.cells[8][index].append([2, 2])

    def _cell_grouper(self):
        for cell in self.cells:  # sorts each cell based on biome
            cell.sort(key=itemgetter(1))

        for cell in self.cells:
            for indv in enumerate(cell):
                current = cell[indv[0]]
                current.insert(3, "None")

        for cell in self.cells:
            #            print('---------------------------')
            for indv in enumerate(cell):
                current = cell[indv[0]]
                try:
                    nxt = cell[indv[0] + 1]
                except IndexError:
                    nxt = None
                finally:
                    prior = cell[indv[0] - 1]
                    self._id_giver(current, nxt, prior)

    #                print(current)

    def _id_giver(self, current, nxt, prior):
        if nxt is None:
            if current[1] == prior[1]:
                current[3] = self.region_id
                return
            else:
                self.region_id += 1
                current[3] = self.region_id
                return
        else:
            if current[1] == nxt[1] and current[1] != prior[1]:
                self.region_id += 1
                current[3] = self.region_id
                return

            elif current[1] != nxt[1] and current[1] == prior[1]:
                current[3] = self.region_id
                return

            elif current[1] == nxt[1] and current[1] == prior[1]:
                current[3] = self.region_id
                return

            elif current[1] != prior[1] and current[1] != nxt[1]:
                self.region_id += 1
                current[3] = self.region_id
                return

    def indv_model_maker(self):
        biomes_model = []
        for cell in self.cells:
            for current in cell:
                biomes_model.append(
                    IndvBiome(
                        indv_id=current[0],
                        biome_name=current[1],
                        cell_position_x=current[2][0],
                        cell_position_y=current[2][1],
                        region_id=current[3],
                    )
                )
        return biomes_model
