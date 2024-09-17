from Json.json import BaseEntity

class Item(BaseEntity):
    def __init__(self, item_id, description, price, moral, energy, effect):
        self.item_id = item_id
        self.description = description
        self.price = price
        self.moral = moral
        self.energy = energy
        self.effect = effect

    # This method is used to create a list of instances of the class Item with the data from items
    @classmethod
    def load_items(cls, file_path):
        data = cls.load_entity(file_path)

        # Ensure the correct structure is accessed
        items_data = data.get('items', {})
        shop_items = items_data.get('shop_items', [])
        no_shop_items = items_data.get('no_shop', [])

        items = {}

        # Process shop_items
        for item_data in shop_items:
            item_id = item_data['id']  # 'id' field serves as the key for the item
            items[item_id] = cls(item_id, item_data['description'], item_data['price'], item_data['moral'], item_data['energy'], item_data.get('effect', 0), item_data['consommable'])

        # Process no_shop
        for item_data in no_shop_items:
            item_id = item_data['id']
            items[item_id] = cls(item_id, item_data['description'], item_data['price'], item_data['moral'], item_data['energy'], item_data.get('effect', 0), item_data['consommable'])

        return items
# the instances are the values of the dictionary, the keys are the object_id
    # example :
    # item = {
    #   'item_id': Item('item_id', 'description', 'price', 'moral', 'energy', 'effect', 'consomable'), key : object
    #   'item_id': Item('item_id', 'description', 'price', 'moral', 'energy', 'effect', 'consomable'), key : object

    # }
    # events['event_id']  returns -> Event('event_id', 'description', 'time_slots', 'phases')

    # Used to return the data of an item
    def get_item_data(self):
        return self.return_entity_data(self, ['item_id', 'description', 'price', 'phases'])

    # Used to return the list of shop items
    def get_shop_items(self):
        return [item for item in self.items if item['shop']]

    # Used to return the list of no shop items
    def get_no_shop_items(self):
        return [item for item in self.items if not item['shop']]


# Example usage
items = Item.load_items("items.json")
for item_id, item in items.items():
    print(f"Item ID: {item_id}")
    print(f"--------------------\n Item ram id : {item}\n--------------------")
    print(item.get_item_data())
    print(item.price)
    print(item.description)
    print(item.item_id)

print("--------------------\nFinished\n--------------------")