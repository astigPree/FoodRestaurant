
from kivy.core.window import Window
Window.size = (1000 , 600)

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

from kivy.core.text import LabelBase as CoreLabel
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty , StringProperty , BooleanProperty , NumericProperty , ListProperty
from kivy.clock import Clock

from backend import DataManagement

# ===== Past Reciept Viewer
class PastReciept(ModalView):
    pass

# ===== Calculations Screens / Activity Screens
class CalculationsButtons(MDGridLayout):
    parent_datas : DataManagement = None

    def update_parent_datas(self , datas : DataManagement):
        self.parent_datas = datas

    def removeAllSelected(self):
        self.parent.parent.parent.parent.parent.removeAllSelected()

    def createReciept(self):
        self.parent.parent.parent.parent.parent.createReciept()

    def viewPastReciept(self):
        self.parent.parent.parent.parent.parent.viewPastReciept()


# ====== Calculations Screens / Calculations Info [ Jeremiah Aguilar ]
class CalculationData(Label):
    pass

class ItemsCalculation(BoxLayout):
    calculations : MDGridLayout = ObjectProperty(None)
    calc_info = ListProperty([])
    calc_total = ListProperty([0 , 0])

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.updateCalculationDisplay , 1 / 60)

    def updateCalculationDisplay(self , interval):
        if not self.parent.parent.parent.datas.get_total_of_selected():
            self.calculations.clear_widgets()
            self.calc_total[0] = 0
            self.calc_total[1] = 0
            return

        self.calc_info = self.parent.parent.parent.datas.get_selected_info()
        self.calc_total = self.parent.parent.parent.datas.get_total_of_selected()

        self.calculations.clear_widgets()
        for info in self.calc_info :
            name = CalculationData()
            price = CalculationData()
            quantity = CalculationData()
            name.size_hint = ( 0.3 , None)
            name.text = f'{info[0]:.10}..' if len(info[0]) > 10 else info[0]
            price.size_hint = (0.35, None)
            price.text = f'{info[1]:.2f}'
            quantity.size_hint = (0.25, None)
            quantity.text = f'{info[2]}'
            self.calculations.add_widget(name)
            self.calculations.add_widget(price)
            self.calculations.add_widget(quantity)

    def resetDataDisplay(self):
        self.calculations.clear_widgets()


# ========= Calculations Screens / Items Selected Screens [ Ericson Mark A. Guanzon ]
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


# ======= Foods Screeens [ Joshua Ametin ]
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


# ===== Main Holder Screens
class MainWidget(BoxLayout):

    datas = DataManagement('pictures' , 'database' , 'reciepts folder' )

    search_bar : MDTextField = ObjectProperty(None)
    food_list_scrollview : ScrollView = ObjectProperty(None)
    food_list : MDGridLayout = ObjectProperty(None)
    selected_items: SelectedItems = ObjectProperty(None)
    calculations: ItemsCalculation = ObjectProperty(None)
    calculation_buttons: CalculationsButtons = ObjectProperty(None)

    past_search = StringProperty('') # used to identify if already search in bar

    def check_debugging(self, interval):
        print(f"Food List : {self.datas.foods_list}")

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.check_debugging , 1)
        Clock.schedule_once(self.displayAllFoods)
        Clock.schedule_interval(self.displaySelectedFood , 1 / 60)
        Clock.schedule_interval(self.displayTheSearchFoods , 1 / 60 )
        Clock.schedule_interval(self.checkIfInSelectedFoods , 1 / 60)

    def displayTheSearchFoods(self , interval):
        if self.search_bar.text == '':
            if not self.food_list.children :
                self.displayAllFoods(1)
                self.food_list_scrollview.scroll_y = 1
            if self.past_search != '':
                self.past_search = ''
                self.food_list.clear_widgets()
                self.displayAllFoods(1)
                self.food_list_scrollview.scroll_y = 1
            return
        if self.search_bar.text == self.past_search :
            return

        self.past_search = self.search_bar.text
        self.food_list.clear_widgets()
        found = self.datas.search_food(self.search_bar.text)
        for key in found :
            widget = FoodPicture()
            widget.update_data(key, self.datas.foods_list[key])
            self.food_list.add_widget(widget)
            self.food_list_scrollview.scroll_y = 1

    def checkIfInSelectedFoods(self , interval):
        for food in self.food_list.children :
            if not food.selected and food.food_id in self.selected_items.selected :
                food.selected = True

    def displayAllFoods(self , interval ):
        for food_id , food in self.datas.foods_list.items() :
            widget = FoodPicture()
            widget.update_data(food_id , food)
            self.food_list.add_widget(widget)

    def displaySelectedFood(self , interval):
        for food in self.food_list.children :
            if food.selected and food.food_id not in self.selected_items.selected :
                widget = SelectedItem()
                widget.update_data(food.food_id , food.data)
                self.selected_items.add_widget(widget)
                self.selected_items.selected.append(food.food_id)

    def removeAllSelected(self):
        if not self.selected_items.children :
            return
        for food in self.food_list.children:
            food.selected = False
        self.selected_items.deleteAllSelected()
        self.selected_items.selected.clear()
        self.datas.reset_foods_list()
        self.calculations.resetDataDisplay()

    def createReciept(self):
        pass

    def viewPastReciept(self):
        pass


# ===== App Handler
class MyApp(MDApp):
    title = "Food Restaurant Serving"
    icon = "pictures/pizza,800.jpg"

    def build(self):
        return Builder.load_file('design.kv')

if __name__ == '__main__':
    CoreLabel.register(name="font" , fn_regular="prog_files/UniformRegular.otf" )
    CoreLabel.register(name="fontlight", fn_regular="prog_files/UniformLight.otf")
    CoreLabel.register(name="fontbold", fn_regular="prog_files/UniformBold.otf")
    MyApp().run()


