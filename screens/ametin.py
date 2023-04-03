from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty , StringProperty

ametin_class_kv = """
<FoodPicture>:
    size_hint : 1 , None
    height : 200

    MDSmartTile:
        radius: 24
        box_radius: [0, 0, 24, 24]
        box_color: 1, 1, 1, .2
        source: root.picture
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: 1 , 1

        on_release :
            root.selected = False if root.selected else True
            root.removeItInSelectedItems()

        MDIconButton:
            icon: "cart-outline" if not root.selected else 'cart'
            theme_icon_color: "Custom"
            icon_color: chex('1b5e20') if root.selected else (  0 , 0 , 0 , 1 )
            pos_hint: {"center_y": .5}

            on_release :
                root.selected = False if root.selected else True
                root.removeItInSelectedItems()

        MDLabel:
            text: root.name
            font_name : 'font'
            color: chex('1b5e20') if root.selected else (  0 , 0 , 0 , 1 )


"""

class FoodPicture(BoxLayout):
    selected = BooleanProperty(False)
    picture = StringProperty('')
    name = StringProperty('')
    food_id = ''
    data = None

    def update_data(self, key : str ,data : list):
        # [ filename , name , price , quantity  ]
        self.food_id = key
        self.data = data
        self.picture = data[0]
        self.name = data[1]

    def removeItInSelectedItems(self):
        if self.selected :
            return None
        for child in self.parent.parent.parent.parent.parent.selected_items.children:  # if not selected remove it in selected items
            if child.food_id == self.food_id:
                self.parent.parent.parent.parent.parent.selected_items.selected.remove(self.food_id)
                self.parent.parent.parent.parent.parent.selected_items.deleteSelected(self.food_id)