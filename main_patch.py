
from kivy.core.window import Window
Window.size = (1000 , 600)

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

from kivy.core.text import LabelBase as CoreLabel
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty , StringProperty , BooleanProperty , NumericProperty , ListProperty , DictProperty
from kivy.utils import get_color_from_hex as chex
from kivy.clock import Clock
from kivy.metrics import dp

from backend import DataManagement
from screens.ametin import *
from screens.guanzon import *
from screens.aguilar import *
from screens.heart import *


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
        Builder.load_string(heart_class_kv)
        Builder.load_string(aguilar_class_kv)
        Builder.load_string(guanzon_class_kv)
        Builder.load_string(ametin_class_kv)
        return Builder.load_file('patch_design.kv')

if __name__ == '__main__':
    CoreLabel.register(name="font" , fn_regular="prog_files/UniformRegular.otf" )
    CoreLabel.register(name="fontlight", fn_regular="prog_files/UniformLight.otf")
    CoreLabel.register(name="fontbold", fn_regular="prog_files/UniformBold.otf")
    MyApp().run()


