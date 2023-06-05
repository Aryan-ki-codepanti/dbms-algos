import json
from copy import deepcopy


class FunctionalDependencySet:

    fd_file = "fds.json"

    def __init__(self, qname=None, fd_set_name=None):
        try:
            file = json.load(open(FunctionalDependencySet.fd_file))
            self.qname = qname
            self.fds = file[qname][fd_set_name]
        except:
            self.qname = "no_question"
            self.fds = []

    @classmethod
    def from_fds(cls, fds):
        fd = FunctionalDependencySet()
        fd.fds = fds
        return fd

    def compute_closure(self, x: set[str], fds=None):

        if isinstance(x, str) or isinstance(x, list):
            x = set(x)

        if fds is None:
            fds = self.fds

        closure = set(x)
        prev = set(x)

        while True:

            for lhs, rhs in fds:
                if set(lhs).issubset(closure):
                    closure.update(rhs)

            if prev == closure:
                break
            prev = set(closure)
        return closure

    def does_covers(self, obj):
        """ returns wether 'self' covers 'obj' (both FunctionDependencySet) """

        if not isinstance(obj, FunctionalDependencySet):
            return False

        F = self.fds
        G = obj.fds

        for lhs, rhs in G:
            closure_wrt_F = self.compute_closure(set(lhs))
            if not set(rhs).issubset(closure_wrt_F):
                return False
        return True

    def compute_minimal_cover(self):
        min_cover = []

        # 1. canonical form
        for lhs, rhs in self.fds:
            if len(rhs) > 1:
                for attr in rhs:
                    min_cover.append([lhs, attr])
                continue
            min_cover.append([lhs, rhs])

        # 2. redundant lhs attributes
        for i, (lhs, rhs) in enumerate(min_cover):
            if len(lhs) > 1:
                # remove attribute from lhs and get new fds
                for attr in lhs:
                    rem_attr = self._remove_attr(min_cover, i, attr)
                    rem_attr_fds = FunctionalDependencySet.from_fds(rem_attr)

                    # check equivalence
                    if self == rem_attr_fds:
                        # remove attribute and update cover
                        min_cover = rem_attr

        # 3. redundant fds
        for fd in min_cover:
            # drop the fd
            rem_fd = self._remove_fd(min_cover, fd)
            rem_fd_set = FunctionalDependencySet.from_fds(rem_fd)

            # check equivalence
            if self == rem_fd_set:
                min_cover = rem_fd
        return min_cover

    def _remove_attr(self, fds: list, fd: int, attr: str):
        """Removes attribute 'attr' from lhs of fd at index 'fd' and returns new fds list """
        lhs, rhs = fds[fd]

        # deeepp copy of fd list
        tmp = deepcopy(fds)
        rem_attr = [[x, y] for x, y in tmp if x != lhs]
        new_lhs = list(lhs)
        new_lhs.remove(attr)
        rem_attr.append([new_lhs, rhs])
        return rem_attr

    def _remove_fd(self, fds: list, fd):
        """Removes  fd at index 'fd' and returns new fds list """
        # deeeeeppp copy of fd list
        rem_fd = deepcopy(fds)
        rem_fd.remove(fd)
        return rem_fd

    def __eq__(self, obj):
        """returns wether self and obj are equivalent or not"""
        return self.does_covers(obj) and obj.does_covers(self)

    def __str__(self):
        fds = ""
        for (lhs, rhs) in self.fds:
            fds += f'{lhs} -> {rhs}\n'
        return fds


f1 = FunctionalDependencySet("Q1", "F")
g1 = FunctionalDependencySet("Q1", "G")

f2 = FunctionalDependencySet("Q2", "F")
f3 = FunctionalDependencySet("Q3", "F")
print(f2.compute_minimal_cover())
print(f1.compute_minimal_cover())
print(g1.compute_minimal_cover())
print(f3.compute_minimal_cover())
