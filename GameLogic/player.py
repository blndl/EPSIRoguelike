class Player:
    def __init__(self, name, energy=5, moral=5, max_energy=5, max_moral=5):
        self.max_energy = max_energy
        self.max_moral = max_moral
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

    def update_player(self, event):
        print(f"event : {event}")
        print(f"event money : {event.get('money', 'Not found')}")
        print(f"event energy : {event.get('energy', 'Not found')}")
        print(f"event moral : {event.get('moral', 'Not found')}")

        self.money += event.get('money', 0)
        self.energy += event.get('energy', 0)
        self.moral += event.get('moral', 0)
        if self.money < 0:
            self.negative_stats("money")
        if self.energy < 0:
            self.negative_stats("energy")
        if self.moral < 0:
            self.negative_stats("moral")
        self.energy = min(self.energy, self.max_energy)
        self.moral = min(self.moral, self.max_moral)
        print(f"\nmoney : {self.money}, \nenergy : {self.energy},\nmoral : {self.moral}")
        return self

    def negative_stats(self, stat):
        print("You have negative ", stat)