from kivymd.uix.gridlayout import MDGridLayout
from backend import DataManagement

heart_class_kv = """
<CalculationsButtons> :
    adaptive_width : True
    rows : 3
    spacing : dp(5)
    padding : dp(10)

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'Create Reciept'

            on_release:
                root.createReciept()

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'Clear Selected'

            on_release :
                root.removeAllSelected()

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'View Past Reciept'

            on_release :
                root.viewPastReciept()

<CalculationsButtons> :
    adaptive_width : True
    rows : 3
    spacing : dp(5)
    padding : dp(10)

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'Create Reciept'

            on_release:
                root.createReciept()

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'Clear Selected'

            on_release :
                root.removeAllSelected()

    BoxLayout:
        size_hint : None , 1
        width : 150
        CalculationsButtonsActivity:
            size_hint : 1 , 1
            text : 'View Past Reciept'

            on_release :
                root.viewPastReciept()

<CalculationsButtonsActivity@MDRectangleFlatButton>:
    size_hint : 1 , 1
    font_size : sp(16)
    font_name : 'font'
    theme_text_color: "Custom"
    text_color: "white"
    line_color: chex('303f9f')
    md_bg_color : chex('303f9f')
"""

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
