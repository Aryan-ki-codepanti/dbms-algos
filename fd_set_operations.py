import json


class FunctionalDependencySet:

    fd_file = "fds.json"

    def __init__(self, qname, fd_set_name):
        file = json.load(open(FunctionalDependencySet.fd_file))
        self.qname = qname
        self.fds = file[qname][fd_set_name]
        print(self.fds)

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
        # returns wether 'self' covers 'obj' (both FunctionDependencySet)

        if not isinstance(obj, FunctionalDependencySet):
            return False

        F = self.fds
        G = obj.fds

        for lhs, rhs in G:
            closure_wrt_F = self.compute_closure(set(lhs))
            if not set(rhs).issubset(closure_wrt_F):
                print(
                    f"rhs :  {rhs} , lhs : {lhs} , closure : {closure_wrt_F}")
                return False
        return True

    def __eq__(self, obj):
        # returns wether self and obj are equivalent or not
        return self.does_covers(obj) and obj.does_covers(self)


f1 = FunctionalDependencySet("Q1", "F")
g1 = FunctionalDependencySet("Q1", "G")
# print(f1 == g1)
print(f1.does_covers(g1))
print(f1 == g1)
