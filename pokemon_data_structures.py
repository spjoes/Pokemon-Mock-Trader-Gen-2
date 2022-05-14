import struct
from pprint import pprint

# Offset from 'A' (0x41). This conversion isn't perfect, but letters match
# See https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_I)
POKE_TEXT_OFS = 0x3F
POKE_TEXT_TERMINATOR = 0x50
POKE_TEXT_MAX_LEN = 10
POKE_LIST_TERMINATOR = 0xFF

MAX_PARTY_POKEMON = 6
PREAMBLE_VALUE = 0xFD


def text_to_pokestr(s):
    if len(s) > POKE_TEXT_MAX_LEN:
        raise Exception(f'Pokestrs have a maximum length of {POKE_TEXT_MAX_LEN}')

    ps = [0] * (POKE_TEXT_MAX_LEN + 1)
    for i, c in enumerate(s):
        ps[i] = ord(c) + POKE_TEXT_OFS
    ps[len(s)] = POKE_TEXT_TERMINATOR

    return bytes(ps)


class Pokemon:

    def __init__(self, id, name):
        self.id = id  # Correct?
        self.held_item = 1
        self.move1 = 2
        self.move2 = 3
        self.move3 = 4
        self.move4 = 5
        self.trainer_id = 6
        self.xp = 7  # ↓
        self.hp_ev = 8
        self.atk_ev = 9
        self.def_ev = 10
        self.spd_ev = 11
        self.spc_ev = 12
        self.iv = 13
        self.move1_pp = 14
        self.move2_pp = 15
        self.move3_pp = 16
        self.move4_pp = 17
        self.friendship = 18
        self.pokerus = 19
        self.caught_data = 20
        self.level = 21
        self.status = 22
        self.unused = 23
        self.hp = 24
        self.max_hp = 25
        self.atk = 26
        self.defence = 27
        self.spd = 28
        self.spc_atk = 29
        self.spc_def = 30
        self.name = name

    def serialize(self):
        # See https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_in_Generation_II
        data = struct.pack(
            # ">BH9BH3B6H5B5H",
            ">2H4BHxxB6H6BH3B7H",
            # ">BBBBBBH3bHHHHHHBBBBBBHBBBHHHHHHH",
            self.id,
            self.held_item,
            self.move1,
            self.move2,
            self.move3,
            self.move4,
            self.trainer_id,
            self.xp,
            self.hp_ev,
            self.atk_ev,
            self.def_ev,
            self.spd_ev,
            self.spc_ev,
            self.iv,
            self.move1_pp,
            self.move2_pp,
            self.move3_pp,
            self.move4_pp,
            self.friendship,
            self.pokerus,
            self.caught_data,
            self.level,
            self.status,
            self.unused,
            self.hp,
            self.max_hp,
            self.atk,
            self.defence,
            self.spd,
            self.spc_atk,
            self.spc_def
        )
        print(data)
        return data


class Trainer:
    def __init__(self, name):
        self.party_pokemon = []
        self.name = name

    def add_party_pokemon(self, pokemon):
        if len(self.party_pokemon) > MAX_PARTY_POKEMON:
            raise Exception('Too many party pokemon')
        self.party_pokemon.append(pokemon)

    def serialize(self):
        serialized = bytes()
        serialized += text_to_pokestr(self.name)
        serialized += bytes([len(self.party_pokemon)])
        serialized += bytes(
            [mon.id for mon in self.party_pokemon] + \
            [POKE_LIST_TERMINATOR] * (MAX_PARTY_POKEMON - len(self.party_pokemon) + 1)
        )

        print("POKEMON COUNT: "+str(len(self.party_pokemon)))

        SERIALIZED_LEN = 49  # 45 = 4pkmn  null | 46 = 3pkmn  \0 | 47 = 2pkmn  \0\0 | 48 = 1pkmn  \0\0\0
        bytesNeeded = b'\0\0\0\0'

        for i in range(len(self.party_pokemon)):
            SERIALIZED_LEN -= 1
            bytesNeeded = bytesNeeded[:-1]

        print("SERIALIZED_LEN: " + str(SERIALIZED_LEN))
        print("bytesNeeded: " + str(bytesNeeded))

        serialized += bytesNeeded.join(mon.serialize() for mon in self.party_pokemon) + \
                      (b'\0' * SERIALIZED_LEN) * (MAX_PARTY_POKEMON - len(self.party_pokemon))
        serialized += b''.join(text_to_pokestr(self.name) for _ in self.party_pokemon) + \
                      (text_to_pokestr('') * (MAX_PARTY_POKEMON - len(self.party_pokemon)))
        serialized += b''.join(text_to_pokestr(mon.name) for mon in self.party_pokemon) + \
                      (text_to_pokestr('') * (MAX_PARTY_POKEMON - len(self.party_pokemon)))
        pprint(serialized)
        return serialized
