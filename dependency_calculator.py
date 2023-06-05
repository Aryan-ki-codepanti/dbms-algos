import json


class Relation:

    fd_file = "fds.json"

    def __init__(self, relation_name: str):
        a = json.load(open("fds.json"))
        self.relation_name = relation_name
        self.attributes = set(a[relation_name]['Attributes'])
        self.fds = a[relation_name]['FDs']

    def attribute_closure(self, x: set, fds=None):

        if fds is None:
            fds = self.fds

        if isinstance(x, str) or isinstance(x, list):
            x = set(x)

        if not x.issubset(self.attributes):
            return set()

        closure = x
        temp = set(closure)

        while True:

            for lhs, rhs in fds:
                if set(lhs).issubset(closure):
                    closure.update(rhs)

            if temp == closure:
                break
            temp = set(closure)

        return closure

    def candidate_keys(self):
        all_possible_keys = Relation.all_subsets(self.attributes)
        keys = []
        for temp_key in all_possible_keys:
            # pass by val so passing a deep copy ded lmao big bug found
            copy = set(temp_key)
            closure = self.attribute_closure(copy)
            if closure == self.attributes and not self.is_redundant(temp_key):
                keys.append(temp_key)
        keys.sort(key=len)
        return keys

    def is_redundant(self, key: set):
        for attribute in key:
            # remove it and check if still a key
            rem_key = key.difference([attribute])
            copy = set(rem_key)
            if self.attribute_closure(copy) == self.attributes:
                return True
        return False

    @staticmethod
    def all_subsets(s: set):
        # non empty subsets only
        subsets = []
        n = len(s)
        s = list(s)
        for i in range(1, 2**n):
            subset = set()
            for j in range(n):
                if (1 << j) & i != 0:
                    subset.add(s[j])
            subsets.append(subset)
        return subsets

    def __str__(self):
        fds = ""

        for (lhs, rhs) in self.fds:
            fds += f'{lhs} -> {rhs}\n'

        s = f"Attributes : {self.attributes}\n\nFDS\n{fds}"
        return s


class FunctionalDependencySet:

    def __init__(self):
        pass


r = Relation("R1")

r2 = Relation("R2")
print(r2.candidate_keys())

r3 = Relation("BOOK")
print(r3.candidate_keys())

r4 = Relation("R4")
print(r4.candidate_keys())

r5 = Relation("R5")
print(r5.candidate_keys())

r6 = Relation("UNIVERSITY")
print(r6.candidate_keys())
