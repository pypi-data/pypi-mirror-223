class DirtyChunkSorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, c0, c1):
        i0 = c0.visible
        i1 = c1.visible
        if i0 and not i1:
            return -1
        if i1 and not i0:
            return 1
        return -1 if c0.distanceToSqr(self.__player) < c1.distanceToSqr(self.__player) else 1
