from typing import List, Dict


class CausalPath:
    def __init__(self, nodes: List[str]) -> None: self.nodes = nodes

    def extend(self, node: str):
        return CausalPath([node] + self.nodes)

    def __str__(self) -> str:
        return f'({self.s}, {self.t})'

    def __hash__(self) -> int:
        return hash(tuple(self.nodes))

    def __eq__(self, other):
        return isinstance(other, CausalPath) and self.nodes == other.nodes


class TimeStampedLink:
    def __init__(self, source: str, target: str, timestamp: int) -> None:
        self.source, self.target, self.timestamp = source, target, timestamp

    def as_causal_path(self):
        return CausalPath([self.source, self.target])

    def __str__(self) -> str:
        return f'{self.source} -> {self.target} ({self.timestamp})'


class TimeStampedLinkWithCount(TimeStampedLink):
    def __init__(self, source: str, target: str, timestamp: int, c: Dict[CausalPath, int]) -> None:
        super().__init__(source, target, timestamp)
        self.c = c

    def __str__(self) -> str:
        return f'{self.source} -> {self.target} ({self.timestamp})'


class TimeStampedLinkList:
    def __init__(self, links: List[TimeStampedLink]) -> None:
        self.links = sorted(links, key=lambda x: x.timestamp)

    def __iter__(self):
        return iter(self.links)

    def __str__(self) -> str:
        return '\n'.join([link.__str__() for link in self.links])

    @staticmethod
    def from_edgelist(edge_list: List):
        timestamped_links = [TimeStampedLink(
            e[0], e[1], e[2]) for e in edge_list]
        return TimeStampedLinkList(timestamped_links)


def paco(data: TimeStampedLinkList, max_time: int, max_steps: int):
    """
    Function counts all instances of causal paths of lengths k <= K for a given maximum path length K and a maximum time difference (delta) between subsequent links on causal paths.

    :param data: Timestamp links (D)
    :param max_steps: Represents maximum path length (K)
    :param max_time: Represents maximum time difference (𝛿)
    """

    # Define C
    C = {}

    # Define W
    window: List[TimeStampedLinkWithCount] = []

    for link in data:
        c_i: Dict[CausalPath, int] = {}
        c_i[link.as_causal_path()] = 1

        for link1 in window:
            if link1.timestamp < link.timestamp - max_time:
                window.remove(link1)
            else:
                if link1.target == link.source and link.timestamp > link1.timestamp:
                    for p in link1.c.keys():
                        if len(p.nodes) <= max_steps:
                            p_d = p.extend(link.target)
                            if p_d not in c_i.keys():
                                c_i[p_d] = link1.c[p]
                            else:
                                c_i[p_d] += link1.c[p]

        for p in c_i.keys():
            if p not in C.keys():
                C[p] = c_i[p]
            else:
                C[p] += c_i[p]
        window.append(TimeStampedLinkWithCount(
            link.source, link.target, link.timestamp, c_i))
    return C
