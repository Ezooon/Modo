from .apirequest import api_request


class Item:
    ALLITEMS = {}

    def __init__(self, data: dict):
        self.data = data

        # setting attributes
        self.id = data.pop("id") or -1
        self.name = data.get("name") or "name"
        self.description = data.get("description") or "description"
        self.image = data.get("image")
        self.add_by = data.get("add_by") or 1
        self.stock = data.get("stock") or 1

        # add to ALLITEMS
        Item.ALLITEMS[self.id] = self

    @classmethod
    def get_items(cls, on_success=print):
        def item_wrapper(thread, response):
            items_data = response["results"]
            items = []
            for data in items_data:
                items.append(Item(data))
            on_success(items)

        api_request("items", item_wrapper)

    def __repr__(self):
        return f"<id: {self.id}, {self.name}>"
