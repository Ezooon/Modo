from .apirequest import api_request


class Item:
    ALLITEMS = {}

    def __init__(self, data: dict):
        self.data = data

        # setting attributes
        self.id = data.get("id") or -1
        self.name = data.get("name") or "name"
        self.price = data.get("price") or 1
        self.description = data.get("description") or "description"
        self.image = data.get("image") or ""
        self.add_by = data.get("add_by") or 1
        self.stock = data.get("stock") or 1

        # add to ALLITEMS
        Item.ALLITEMS[self.id] = self

    @classmethod
    def get_items(cls, on_success=lambda x: None, **kwargs):
        def item_wrapper(thread, response):
            items_data = response.get("results")
            items = []
            for data in items_data:
                items.append(Item(data))
            on_success(items)

        api_request("items/all-items/", item_wrapper, **kwargs)

    def favorite(self, on_success=lambda x: None, **kwargs):
        def success(_, data):
            on_success(data)

        api_request("account/favorite/" + str(self.id) + "/", on_success=success, method="POST")

    def __repr__(self):
        return f"<id: {self.id}, {self.name}>"
