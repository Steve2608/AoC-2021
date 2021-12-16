from dataclasses import dataclass
from functools import partial
from math import prod


from_base_2 = partial(int, base=2)
from_base_16 = partial(int, base=16)


@dataclass(slots=True)
class Package:
    version: int
    type_id: int

    @staticmethod
    def parse_version_type_id(bit_string: str):
        return from_base_2(bit_string[:3]), from_base_2(bit_string[3:6]), bit_string[6:]


@dataclass(slots=True)
class Literal(Package):
    groups: list[str]

    @property
    def value(self) -> int:
        return from_base_2(''.join(self.groups))

    @classmethod
    def from_string(cls, bit_string: str):
        v, t, bit_string = Package.parse_version_type_id(bit_string)

        groups = []
        while True:
            group = bit_string[:5]
            groups.append(group[1:])

            bit_string = bit_string[5:]
            if group[0] == '0':
                break

        return cls(v, t, groups), bit_string


@dataclass(slots=True)
class Operator(Package):
    length_type_id: int
    length: int
    packages: list[Package]

    @property
    def value(self) -> int:
        if self.type_id == 0:
            return sum(p.value for p in self.packages)
        if self.type_id == 1:
            return prod(p.value for p in self.packages)
        if self.type_id == 2:
            return min(p.value for p in self.packages)
        if self.type_id == 3:
            return max(p.value for p in self.packages)
        if self.type_id == 5:
            return int(self.packages[0].value > self.packages[1].value)
        if self.type_id == 6:
            return int(self.packages[0].value < self.packages[1].value)
        if self.type_id == 7:
            return int(self.packages[0].value == self.packages[1].value)

    @classmethod
    def from_string(cls, bit_string: str):
        v, t, bit_string = Package.parse_version_type_id(bit_string)

        length_type_id = from_base_2(bit_string[0])
        bit_string = bit_string[1:]

        if length_type_id == 0:
            length = from_base_2(bit_string[:15])
            bit_string = bit_string[15:]
        else:
            length = from_base_2(bit_string[:11])
            bit_string = bit_string[11:]

        sub_packages = []
        consumed_bits = 0
        while True:
            # lookahead
            t_ = from_base_2(bit_string[3:6])

            if t_ == 4:
                l, bit_string_ = Literal.from_string(bit_string)
                sub_packages.append(l)
            else:
                o, bit_string_ = Operator.from_string(bit_string)
                sub_packages.append(o)

            consumed_bits += len(bit_string) - len(bit_string := bit_string_)

            if length_type_id == 0 and consumed_bits >= length:
                break
            if length_type_id == 1 and len(sub_packages) >= length:
                break

        return cls(v, t, length_type_id, length, sub_packages), bit_string


def part1(hex_num: str) -> int:
    def version_sum(package: Package):
        if isinstance(package, Literal):
            return package.version
        return package.version + sum(map(version_sum, package.packages))

    bit_string = f'{from_base_16(hex_num):b}'.zfill(len(hex_num) * 4)
    o, _ = Operator.from_string(bit_string)
    return version_sum(o)


def part2(hex_num: str) -> int:
    bit_string = f'{from_base_16(hex_num):b}'.zfill(len(hex_num) * 4)
    o, _ = Operator.from_string(bit_string)
    return o.value


if __name__ == '__main__':
    if __debug__:
        assert part1(hex_num := '8A004A801A8002F478') == 16, f'{part1(hex_num)=} != 16'
        assert part2(hex_num := 'C200B40A82') == 3, f'{part2(hex_num)=} != 3'
        assert part2(hex_num := '9C0141080250320F1802104A08') == 1, f'{part2(hex_num)=} != 1'

    with open('input.txt') as in_file:
        hex_num = in_file.read().strip()
    print(part1(hex_num))
    print(part2(hex_num))
