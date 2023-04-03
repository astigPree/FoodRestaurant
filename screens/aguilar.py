
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty , ObjectProperty
from kivy.clock import Clock

aguilar_class_kv = """
<ItemsCalculation> :
    canvas.before :
        Color :
            rgb : chex('9fa8da')
        Rectangle :
            pos : self.pos
            size : self.size
            #radius : ( 10 , 10 , 10 , 10 )

    orientation : 'vertical'
    spacing : dp(2)

    calculations : calculations.__self__

    BoxLayout :
        size_hint : 1 , 0.1
        spacing : dp(2)

        TitleBarCalculationInfo:
            size_hint : 0.3 , 1
            text : 'NAME'

        TitleBarCalculationInfo:
            size_hint : 0.35 , 1
            text : 'PRICE'

        TitleBarCalculationInfo:
            size_hint : 0.25 , 1
            text : 'QUANTITY'

    ScrollView :
        size_hint : 1 , 0.8
        always_overscroll : False

        MDGridLayout :
            id : calculations
            size_hint : 1 , None
            adaptive_height : True
            cols : 3
            spacing : dp(2)

            CalculationData :
                size_hint : 0.3 , None
                text : 'M.J.H'

            CalculationData :
                size_hint : 0.35 , None
                text : '$10,000.00'

            CalculationData :
                size_hint : 0.25 , None
                text : '10'


    BoxLayout :
        size_hint : 1 , 0.1
        spacing : dp(2)

        TitleBarCalculationInfoTotal:
            size_hint : 0.3 , 1
            text : 'TOTAL    : '

        TitleBarCalculationInfoTotal:
            size_hint : 0.35 , 1
            text : f'Php {root.calc_total[0]:.2f}'

        TitleBarCalculationInfoTotal:
            size_hint : 0.25 , 1
            text : f'{root.calc_total[1]}'

<CalculationData>:
    size_hint : 1 , None
    height : 25
    font_size : sp(16)
    font_name : 'font'
    color : 'black'

    canvas.before :
        Color :
            rgb : chex('eceff1')
        RoundedRectangle :
            pos : self.pos
            size : self.size
            radius : ( 2 , 2, 2, 2)


<TitleBarCalculationInfoTotal@MDLabel>:
    background_color : 0 , 0 , 0 , 0
    font_name : 'fontlight'
    halign : 'center'
    color : 'white'

    canvas.before :
        Color :
            rgb : chex('303f9f')
        RoundedRectangle :
            pos : self.pos
            size : self.size
            radius : ( 5 , 5 , 0 , 0 )
    font_name : 'fontlight'
    font_size : sp(16)


<TitleBarCalculationInfo@Label>:
    background_color : 0 , 0 , 0 , 0
    font_name : 'fontlight'

    canvas.before :
        Color :
            rgb : chex('303f9f')
        RoundedRectangle :
            pos : self.pos
            size : self.size
            radius : ( 0 , 0 , 5 , 5 )

    font_name : 'font'
    font_size : sp(16)

"""

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

