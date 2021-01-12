class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return False if self.isEmpty() else self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def toString(self):
        char = ""
        for x in self.items:
            char += str(x) + " "

        return "vazia" if self.isEmpty() else char
