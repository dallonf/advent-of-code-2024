class PriorityQueue[T]:
    "Returns items with the lowest priority value first."

    def __init__(self, initial_item: T | None = None):
        self.items = list[tuple[T, int]]()
        if initial_item is not None:
            self.items.append((initial_item, 0))

    def add(self, new_item: T, item_priority: int):
        new_items = list[tuple[T, int]]()
        added = False
        for item, priority in self.items:
            if not added and priority < item_priority:
                new_items.append((new_item, item_priority))
                added = True
            new_items.append((item, priority))
        if not added:
            new_items.append((new_item, item_priority))
        self.items = new_items

    def pop(self) -> T | None:
        if len(self.items) == 0:
            return None
        return self.items.pop()[0]
