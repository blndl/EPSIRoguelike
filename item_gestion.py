from jsonLoader import BaseEntity

class Item(BaseEntity):
    def __init__(self, item_id, description, price, moral, energy, itemshop, consommable, img, name):
        self.item_id = item_id
        self.description = description
        self.price = price
        self.moral = moral
        self.energy = energy
        self.itemshop = itemshop
        self.consommable = consommable
        self.sprite_path = img
        self.name = name

    # This method is used to create a list of instances of the class Item with the data from items
    @classmethod
    def load_items(cls, file_path):
        data = cls.load_entity(file_path)
        return {item_id: cls(
            item_id, item_data['description'], item_data['price'], item_data['moral'], item_data['energy'], item_data['itemshop'], item_data['consommable'], item_data.get('image', 'Items/Sprites/luckyblock.png'), item_data['name'])
                for item_id, item_data in data['items'].items()}

# the instances are the values of the dictionary, the keys are the object_id
    # example :
    # item = {
    #   'item_id': Item('item_id', 'description', 'price', 'moral', 'energy', 'effect', 'consomable'), key : object
    #   'item_id': Item('item_id', 'description', 'price', 'moral', 'energy', 'effect', 'consomable'), key : object

    # }
    # events['event_id']  returns -> Event('event_id', 'description', 'time_slots', 'phases')

    # Used to return the list of shop items
    def get_shop_items(self):
        return [item for item in self.items if item['shop']]
