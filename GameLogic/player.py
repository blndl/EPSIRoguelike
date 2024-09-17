class Player:
    def __init__(self, name, energy=100, moral=100):
        self.energy = energy
        self.moral = moral
        self.name = name
        self.money = 0

        "Inventory slot"
        self.inventory_slot_1 = None
        self.inventory_slot_2 = None
        self.inventory_slot_3 = None
        self.inventory_slot_4 = None

        "bag"
        self.bag = []

        self.effects = []
