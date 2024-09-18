class Player:
    def __init__(self, name, energy=10, moral=10, max_energy=10, max_moral=10, project=0, max_project=10):
        self.max_energy = max_energy
        self.max_moral = max_moral
        self.energy = energy
        self.moral = moral
        self.project = project
        self.max_project = max_project
        self.name = name
        self.money = 0

        "Inventory slot"
        self.inventory_slot_1 = None
        self.inventory_slot_2 = None
        self.inventory_slot_3 = None
        self.inventory_slot_4 = None

        "bag"
        self.bag = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "C1", "C2"] # max size of 32 items

        self.effects = []

    def update_player(self, event):

        # get the variables from the event/ item
        money = event.get('money', 0)
        energy = event.get('energy', 0)
        moral = event.get('moral', 0)
        project = event.get('project', 0)

        self.statChange(money, moral, energy, project)
        self.negative_stats(money, "money")
        self.negative_stats(moral, "moral")
        self.negative_stats(energy, "energy")
        if self.project >= self.max_project:
            print("You have completed the project! \nCongratulations!")

        self.energy = min(self.energy, self.max_energy)
        self.moral = min(self.moral, self.max_moral)
        print(f"\nmoney: {self.money}, \nenergy: {self.energy},\nmoral: {self.moral}")
        return self

    def statChange(self, money, moral, energy, project):
        self.money += money
        self.moral += moral
        self.energy += energy
        self.project += project
        print(self.moral,self.energy)
        
    def negative_stats(self, stat, name):
        if stat < 0:
            stat = 0
            print("You have negative", name)