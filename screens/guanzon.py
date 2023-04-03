
from kivy.properties import StringProperty , NumericProperty , ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock

guanzon_class_kv = """
<SelectedItem>:
    size_hint : 1 , None
    height : 120
    padding : dp(5)

    canvas.before :
        Color :
            rgb : chex('3f51b5')
        RoundedRectangle :
            pos : self.pos
            size : self.size
            radius : ( 5 , 5 , 5 , 5 )

    FitImage :
        radius : ( 10 , 5, 10 , 5)
        size_hint : 0.15 , 1
        source : root.picture

    BoxLayout :
        size_hint : 0.85 , 1
        orientation : 'vertical'
        padding : dp(3)

        Label :
            size_hint : 1 , 0.6
            text : root.name
            color : 'black'
            font_size : sp(15)
            font_name : 'font'

            canvas.before :
                Color :
                    rgb : chex('9fa8da')
                RoundedRectangle:
                    pos : self.pos
                    size : self.size
                    radius : ( 10 , 0 , 10 , 0 )

        BoxLayout:
            size_hint : 1 , 0.4
            spacing : dp(5)

            Label :
                text : f'price : Php {root.price:.2f}'
                font_name : 'fontlight'

            Label :
                text : f'quantity : {root.quantity}'
                font_name : 'fontlight'

            MDFillRoundFlatButton:
                text : 'add'
                font_name : 'fontbold'
                text_color : chex('01579b')
                font_size : sp(16)

                on_release :
                    root.add_quantity()


            MDFillRoundFlatButton:
                text : 'minus'
                font_name : 'fontbold'
                text_color : chex('01579b')
                font_size : sp(16)

                on_release :
                    root.minus_quantity()


"""

class SelectedItem(BoxLayout):
    picture = StringProperty('')
    name = StringProperty('')
    price = NumericProperty(0)
    quantity = NumericProperty(0)

    food_id = None
    datas = ['' , '' , 0 , 0 ]
    updateIt = False

    def update_data(self, key : str , data : list):
        # [ filename , name , price , quantity  ]
        self.food_id = key
        self.datas = data
        self.data = data
        self.picture = data[0]
        self.name = data[1]
        self.price = float(data[2])
        self.quantity = 1
        self.updateIt = True

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.update_my_datas , 1 / 60 )

    def update_my_datas(self, interval ):
        if not self.updateIt :
            return
        self.datas[3] = self.quantity
        if self.parent :
            self.parent.parent.parent.parent.parent.datas.update_foods_list(self.food_id , self.datas)


    def minus_quantity(self):
        self.quantity -= 1
        if self.quantity == 0 :
            self.parent.selected.remove(self.food_id)
            for child in self.parent.parent.parent.parent.parent.food_list.children : # return false the selected value in FoodList
                if child.food_id == self.food_id :
                    child.selected = False
            self.parent.remove_widget(self)

    def add_quantity(self):
        self.quantity += 1

    def remove(self):
        self.updateIt = False
        self.datas[3] = 0
        if self.parent :
            self.parent.parent.parent.parent.parent.datas.update_foods_list(self.food_id , self.datas)

class SelectedItems(MDGridLayout):
    selected = ListProperty([])

    def deleteSelected(self , food_id : str):
        for child in self.children :
            if child.food_id == food_id :
                child.quantity = 0
                self.remove_widget(child)
                self.parent.scroll_y = 1
                break

    def deleteAllSelected(self):
        for child in self.children:
            child.remove()
        self.clear_widgets()