import sqlite3
import os

#Program Info:
#Used VSCode, python, Extensions: sqlite, kivy, kivymd

#Reference: 
#(Would have a doc of video link further on)
# Used poe: Assistant (ChatGPT?) assistance on some unknown errors (Since this is the first time learning kivy interface programming)

#Currently Done:
#Interface ~ Main Screen, Search Screen, Add_Contact Screen, Recent Screen (Not linked database)
#Screen Transitions, Order by type, Searching, Updating user list, Highlight sort button, Delete Contact
#Interface ~ User Info Interface, Editing Info
#App Remarks


#Working on:
#Recent database (Another database)
#Class Arrangement (Making Interfaces into different small classes)

#Possibly Will work on:
#Packing Apk, Connection between phonebook and recent Database

conn = sqlite3.connect("phonebook.db")
print(conn.total_changes)
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS phonebook(
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            tel_no TEXT PRIMARY KEY,
            email TEXT,
            address TEXT,
            groups TEXT,
            fav BOOL NOT NULL
            )
        """)

c.execute("DELETE FROM phonebook")
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)", ("Tom","Cruise","12343434","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Tom","Holland","45653344","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Harry","Potter","32863532","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Army","Strong","23573132","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Larry","Madison","24524627","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Outboard","Einstein","84235742","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Eddie","Benedict","23547876","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Parry","Hotter","76316842","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Tommy","Boy","31574521","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Jackie","Chang","45723433","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Fan","Bart","93275732","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Fan","Art","43462442","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Fand","Bart","62363421","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Fam","Cart","65483434","","","",False))
c.execute("INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)",("Fam","Mart","61236735","","","",False))

c.execute("""CREATE TABLE IF NOT EXISTS recent(
          tel_no TEXT PRIMARY KEY,
          time TEXT,
          day DATE)
        """)
conn.commit()

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from os.path import join, dirname
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField

put, col, order = "", "first_name", "ASC" #Variables related to search engine
st = 0

class Target(BoxLayout): #For selecting ordering criteria
    def __init__(self, **kwargs):
        global put, col, order 
        super(Target, self).__init__(orientation='horizontal', height=self.height, size_hint=(1, 0.15))
        self.refresh()

    def refresh(self, instance=None): #Building criteria bar
        self.label_height = '10dp'
        fsize = "12dp"
        type = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
        typex = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
        typey = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))

        self.default_color = (0.8, 0.8, 0.8, 1)
        self.selected_color = (0.7, 1, 0.7, 1)  # Color when selected

        # Create Introduction 
        self.sortlabel = MDLabel(text="Sort:", font_size="12dp", text_size=self.size,
                                  size_hint_x=.2, md_bg_color=(0.8, 0.8, 0.8, 1), color="black", bold=True) 

        # Create buttons for "ordering by selected criteria"
        self.buttons = [
            Button(text="First_name", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.first),
            Button(text="Last_name", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.last),
            Button(text="Tel_no", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.tel),
            Button(text="Email", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.email),
            Button(text="Address", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.address),
            Button(text="Groups", bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.groups)
        ]

        #Create Button for ascending or decending order
        self.orders = Button(text=order, bold=True, background_color=self.default_color, height=self.label_height, font_size=fsize, on_press=self.ord, size_hint_x=.15)

        #Insert Labels and items into layout
        self.add_widget(self.sortlabel)
        typex.add_widget(self.buttons[0])
        typex.add_widget(self.buttons[1])
        typex.add_widget(self.buttons[2])
        typey.add_widget(self.buttons[3])
        typey.add_widget(self.buttons[4])
        typey.add_widget(self.buttons[5])

        type.add_widget(typex)
        type.add_widget(typey)
        self.add_widget(type)
        self.add_widget(self.orders)

        # Ensure the selected button retains its color after refresh
        self.update_button_colors()

    def update_button_colors(self): # Update color of the buttons according to saved variables
        for index, button in enumerate(self.buttons):
            button.background_color = self.selected_color if index == st else self.default_color

    def first(self, instance): #Saving criterias
        global col, st
        col = "first_name"
        st = 0
        self.update_button_colors()

    def last(self, instance):
        global col, st
        col = "last_name"
        st = 1
        self.update_button_colors()

    def tel(self, instance):
        global col, st
        col = "tel_no"
        st = 2
        self.update_button_colors()

    def email(self, instance):
        global col, st
        col = "email"
        st = 3
        self.update_button_colors()

    def address(self, instance):
        global col, st
        col = "address"
        st = 4
        self.update_button_colors()

    def groups(self, instance):
        global col, st
        col = "groups"
        st = 5
        self.update_button_colors()

    def ord(self, instance):
        global order
        order = "DESC" if order == "ASC" else "ASC"
        self.orders.text = order


class UserInfoScreen(Screen): #Main user info layout screen for MainScreen and SearchScreen
    def init(self, **kwargs):
        super(UserInfoScreen, self).init(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.name_label = MDLabel()
        self.phone_label = MDLabel()
        self.extra_label = MDLabel()

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.phone_label)
        self.layout.add_widget(self.extra_label)

        self.add_widget(self.layout)

    def display_user_info(self, user): #Display Name, Tel. no and selected criteria (If name/tel.no/groups then groups) by each user
        self.name_label.text = f"Name: {user[0]} {user[1]}"
        self.phone_label.text = f"Phone: {user[2]}"
        self.extra_label.text = f"Extra Info: {user[3]}"

    def go_to_info(self,instance): #Button at right transit to full user profile
        self.manager.current = "info"
        self.manager.transition.direction = "left"


class UserList(GridLayout): #Creating layout for user infos
    def __init__(self, **kwargs):
        super(UserList, self).__init__(cols=3, padding=5, spacing=5, size_hint=(1, None), **kwargs)
        self.bind(minimum_height=self.setter('height'))

        self.label_height = '40dp'
        self.container = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.container.bind(minimum_height=self.container.setter('height'))

        
        self.add_top()
        self.populate_user_rows()

        self.add_widget(self.container)

    def add_top(self):
        top_layout = BoxLayout(orientation='horizontal', height=self.label_height, size_hint=(1, None))
        stats = [
            ("Name", self.headex()),
            ("Tel.", ""),
            (self.headex(), "")
        ]
        #
        for text, extra_text in stats:
            label = MDLabel(
                text=text,
                valign='middle',
                halign='left',
                color=(0, 0, 0, 1),
                font_size="13dp",
                md_bg_color=(0.5, 0.5, 0.5, 1),
                height=self.label_height,
                bold=True
            )
            top_layout.add_widget(label)

        top_layout.add_widget(MDLabel(size_hint=(0.2, 1)))
        self.container.add_widget(top_layout)

    def populate_user_rows(self): #Get all users info from database
        self.users = self.get_users()
        for user in self.users: #Input user contact info each by each
            self.add_user_row(user)

    def add_user_row(self, user): #Create format for showcase (design)
        user_layout = BoxLayout(orientation='horizontal', height=self.label_height, size_hint=(1, None))
        labels = [
            f"{user[0]} {user[1]}",user[2],user[self.extra()]]
    
        for text in labels:
            label = MDLabel(
                text=text,valign='middle',halign='left',
                color=(0, 0, 0, 1),font_size="13dp",
                md_bg_color=(0.7, 0.7, 0.7, 1),height=self.label_height
            )
            user_layout.add_widget(label)

        button = Button(text=":", size_hint=(0.2, 1), bold=True,
                        background_color=(0.8, 0.8, 0.8, 1), height=self.label_height)
        button.bind(on_press=lambda instance, user=user: self.save_user_data(user))
        user_layout.add_widget(button)

        self.container.add_widget(user_layout)

    def save_user_data(self, user): #Collect data from the row for info and edit page (directing to that user's info)
        app = MDApp.get_running_app() #Simulate ongoing app windows
        info_screen = app.root.get_screen('info') #Define running environment
        edit_screen = app.root.get_screen('edit')

        user_info = self.get_info(user[2])  #Get phone number of the row
        if user_info: 
            info_screen.populate_info(user_info) #Collect row info for other windows
            edit_screen.populate_info(user_info)
            app.root.current = "info" #Switch window to info page (Full contact info)
        else:
            print("User information not found.") #Prevent error after deleted contact

    def get_info(self, phone_number): #Search for phone number of the corresponding user of the button
        try:
            with sqlite3.connect("phonebook.db") as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM phonebook WHERE tel_no = ?", (phone_number,))
                return c.fetchone() or []
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def headex(self): #Select the 3rd showcase info (If name/tel no./groups then showcase groups)
        return ["Email", "Address", "Groups"][st - 3] if st >= 3 else "Groups"

    def extra(self): #Position variable test
        return st if st > 2 else 5

    def get_users(self): #Collect user data with criterias (keywords, input field and ordering)
        sql_query = "SELECT * FROM phonebook"
        where_clause = [] #criterias
        params = [] #user info

        if put.strip(): #Search by keyword
            where_clause.append("(first_name LIKE ? OR last_name LIKE ? OR tel_no LIKE ? OR email LIKE ? OR address LIKE ? OR groups LIKE ?)")
            params.extend([f'%{put}%'] * 6)

        if where_clause: #If has keyword in one of the field, order by selected input field by selected ordering method
            sql_query += " WHERE " + " AND ".join(where_clause)
        sql_query += f" ORDER BY {col} {order}" 

        try:
            with sqlite3.connect("phonebook.db") as conn:
                c = conn.cursor()
                c.execute(sql_query, params) #Select suitable user infos by previous ordering pattern
                return c.fetchall() #Showcase "Select" result
        except sqlite3.Error as e: #In case error
            print(f"An error occurred: {e}")
            return []
        
class Main(Screen): #Main screen
    def __init__(self, app, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.refresh_page() #load screen

    def refresh_page(self, instance=None):
        self.clear_widgets() #Clear all the widgets every time called (so to show updated widgets)
        layout = BoxLayout(orientation='vertical')

        top = self.create_top_bar() #Top bar
        self.user_list = UserList(size_hint_y=None, height=0) #Showcase user info
        self.scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True) #Add scrolling function to the showcase
        self.scroll_view.add_widget(self.user_list) #Insert showcase into scroll function

        layout.add_widget(top)
        layout.add_widget(Target()) #criteria bar
        layout.add_widget(self.scroll_view)#scroll function
        layout.add_widget(Bottom(go_to_main=self.go_to_main, go_to_recent=self.go_to_recent))#Bottom bar + call function

        self.add_widget(layout)

    def create_top_bar(self): 
        top = BoxLayout(orientation='horizontal', size_hint=(1, 0.07))

        self.main_title = MDLabel(text="Phonebook",color=(0, 0, 0, 1),md_bg_color=(0.8, 0.8, 0.8, 1),
                                    font_size="24dp",size_hint_x=0.4,bold=True)

        #Create Buttons
        buttons = [
            ('Refresh', self.refresh_page, 0.25), #Refresh user info layout by criteria
            ('Search', self.go_to_search, 0.2), #Search Screen
            ('+', self.go_to_add, 0.15)] #Add contact

        top.add_widget(self.main_title) 
        for text, handler, size_hint_x in buttons: #Add buttons to the layout
            button = Button(text=text, on_press=handler, size_hint_x=size_hint_x)
            top.add_widget(button)

        return top

    def go_to_add(self, instance): #Screen switch settings
        self.switch_screen('add', "left")

    def go_to_search(self, instance):
        self.switch_screen('search', "left")

    def go_to_info(self, instance):
        self.switch_screen('info', "left")

    def go_to_main(self, instance):
        self.switch_screen('main', "right")

    def go_to_recent(self, instance):
        self.switch_screen('recent', "left")
    

    def switch_screen(self, screen_name, transition_direction): #Switch screen to names by a direction
        self.manager.current = screen_name
        self.manager.transition.direction = transition_direction

class Search(Screen):

    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.refresh_page() #load screen

    def refresh_page(self, instance=None): #Refresh page when called
        self.clear_widgets() #Clear all widgets for incoming updated widgets
        layout = BoxLayout(orientation='vertical')

        top = self.create_top_bar() #Call top layout
        self.user_list = UserList(size_hint_y=None, height=0) #Call and Showcase user info
        self.scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True) #Add scroll function
        self.scroll_view.add_widget(self.user_list) #Put showcase into scroll function

        tar = Target() #Call criteria bar

        layout.add_widget(top) #Add top layout
        layout.add_widget(tar) #Add criteria bar
        layout.add_widget(self.scroll_view) #Add showcase in scroll function
        self.add_widget(layout) #Add layout to screen

    def create_top_bar(self): #Top bar
        top = BoxLayout(orientation='horizontal', size_hint=(1, 0.07))

        #Add items
        self.bar = TextInput(multiline=False, size_hint_x=0.45, font_size="11dp", hint_text="Input keyword:")
        self.refresh = Button(text='Refresh', on_press=self.refresh_page, size_hint_x=0.25)
        self.mainsearch = Button(text="Search", on_press=self.search, size_hint_x=0.2)
        self.back = Button(text="Return", on_press=self.go_to_main, size_hint_x=0.2)

        top.add_widget(self.bar)
        top.add_widget(self.refresh)
        top.add_widget(self.mainsearch)
        top.add_widget(self.back)

        return top

    def search(self, instance): #Add keyword criteria to user info showcase
        global put
        put = self.bar.text
        self.refresh_page()

    def go_to_main(self, instance): #Screen switching functions & reset search bar input
        global put
        put = ""
        self.manager.current = 'main'
        self.manager.transition.direction = 'right'

    def go_to_add(self, instance):
        self.manager.current = 'add'

    def go_to_info(self, instance):
        self.manager.current = 'info'

    def go_to_recent(self, instance):
        self.manager.current = 'recent'



class Info(Screen):
    def __init__(self, **kwargs):
        super(Info, self).__init__(**kwargs)
        self.info_layout = InfoContactLayout() #Call layout
        self.clear_widgets() #Clear widgets for rebuild
        self.add_widget(self.info_layout) 

    def populate_info(self, user_data):
        self.info_layout.main_layout.populate_fields(user_data) #Call row user info

    def go_to_edit(self): #Transition function to edit screen
        self.manager.current = "edit"
        self.manager.transition.direction = "left"
    pass

class InfoContactLayout(BoxLayout): #Layout for info
    def __init__(self, **kwargs):
        super(InfoContactLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        #Create layout by parts
        self.create_top_layout()
        self.create_main_layout()
        self.bottom_layout = self.create_bottom_layout() 

    #Call layout classes by parts
    def create_top_layout(self): 
        self.top_layout = InfoTopLayout(go_back=self.back)
        self.add_widget(self.top_layout)

    def create_main_layout(self):
        self.main_layout = InfoMainLayout()
        self.add_widget(self.main_layout)

    def create_bottom_layout(self):
        bottom_layout = InfoBottomLayout()
        self.add_widget(bottom_layout)
        return bottom_layout  

    def back(self, instance): #Transition function to main
        self.parent.parent.current = "main"
        
    

class InfoTopLayout(BoxLayout):  # Top Layout
    def __init__(self, go_back, **kwargs):
        super(InfoTopLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.create_widgets(go_back)

    def create_widgets(self, go_back):  # Add items to layout + design
        self.title = MDLabel(text="Profile:",valign='middle',halign='left',
            color=(0, 0, 0, 1),font_size="13dp",size_hint_x=0.7,md_bg_color=(0.6, 0.6, 0.6, 1))
        self.clear = Button(text="Return", on_press=go_back, size_hint_x=0.3)
        self.add_widget(self.title)
        self.add_widget(self.clear)

class InfoMainLayout(BoxLayout):  # Main Layout
    def __init__(self, **kwargs):
        super(InfoMainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 0.5

        #Assign input fields
        self.input_fields = [
            ('F_Name', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1))),
            ('L_Name', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1))),
            ('Tel', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1))),
            ('Email', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1))),
            ('Address', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1))),
            ('Groups', MDLabel(valign='middle', halign='left', color=(0, 0, 0, 1),
                    font_size="13dp", md_bg_color=(0.7, 0.7, 0.7, 1)))
        ]

        self.field_labels = {}
        self.create_input_fields()

    def create_input_fields(self):
        for label_text, display_label in self.input_fields:
            layout = BoxLayout(orientation="horizontal")
            label = MDLabel(text=f"{label_text}:",size_hint_x=0.5,valign='middle',halign='left',
                color=(0, 0, 0, 1),md_bg_color=(0.7, 0.7, 0.7, 1),font_size="13dp")
            
            display_label.text = " "  # Initialize with empty text
            layout.add_widget(label)
            layout.add_widget(display_label)
            self.field_labels[label_text] = display_label  
            self.add_widget(layout)

    def populate_fields(self, user_data):
        #Insert labels with user data
        self.field_labels['F_Name'].text = user_data[0]
        self.field_labels['L_Name'].text = user_data[1]
        self.field_labels['Tel'].text = user_data[2]
        self.field_labels['Email'].text = user_data[3]
        self.field_labels['Address'].text = user_data[4]
        self.field_labels['Groups'].text = user_data[5]

        # Access bottom_layout if needed
        bottom_layout = self.parent.bottom_layout  # Access bottom layout
        bottom_layout.phone_number = user_data[2]  # Set bottom layout phone number to contact's tel no.
        bottom_layout.update_favorite_button(user_data[6])  #Check fav status

class InfoBottomLayout(BoxLayout): #Bottom Layout
    def __init__(self, **kwargs):
        super(InfoBottomLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        
        self.phone_number = None  # Initialize phone_number

        #Add buttons
        self.fav = Button(text="Favourite",on_press=self.on_fav_button_press)
        self.edit_button = Button(text="Edit",on_press=self.go_to_edit)
        self.delete_button = Button(text="Delete",on_press=self.open_popup)
        self.add_widget(self.fav)
        self.add_widget(self.edit_button)
        self.add_widget(self.delete_button)

    def go_to_edit(self, instance): 
        # Get the parent Info instance and call go_to_edit
        info_screen = self.parent.parent  # Navigate to the Info screen
        info_screen.go_to_edit() 

    def on_fav_button_press(self, instance): #Check and switch fav status
        if self.phone_number:  # Check if phone_number is set
            new_fav = self.toggle_favorite(self.phone_number)
            if new_fav is not None:
                self.fav.text = "Unfavorite" if new_fav else "Favorite"
                
    def open_popup(self, instance): #Open popup for confirmation "Delete"
        popup = ConfirmDelete(add_instance=self, phone_number=self.phone_number)
        popup.open()

    def update_favorite_button(self, is_fav):
        self.fav.text = "Unfavorite" if is_fav else "Favorite"

    def toggle_favorite(self, phone_number):
        # Toggle favorite status
        try:
            with sqlite3.connect("phonebook.db") as conn:
                c = conn.cursor()
                c.execute("SELECT fav FROM phonebook WHERE tel_no = ?", (phone_number,)) #Select corresponding user
                current_fav = c.fetchone()

                if current_fav is not None:
                    new_fav = not current_fav[0]  # Toggle 
                    c.execute("UPDATE phonebook SET fav = ? WHERE tel_no = ?", (new_fav, phone_number)) #Update fav status
                    conn.commit()
                    return new_fav
                else:
                    print("User not found.") #In case deleted
                    return None
        except sqlite3.Error as e: #In case error
            print(f"An error occurred: {e}")
            return None
        
class ConfirmDelete(Popup): #gui for confirm "Delete Contact"
    def __init__(self, add_instance, phone_number, **kwargs):
        super().__init__(**kwargs)
        content = BoxLayout(orientation='vertical', size_hint_y=1)
        self.add_instance = add_instance
        self.phone_number = phone_number  # Store the phone number

        self.size_hint = (0.8, 0.5)
        self.title = "Confirm Delete"
        self.check = MDLabel(text='Are you sure you want to delete this contact?',
                            valign="center", halign="center")
        self.check.color = (1, 1, 1, 1)

        buttons = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        return_button = Button(text='Return', on_press=self.dismiss) #Close popup
        yes_button = Button(text='Delete', on_press=self.delete_contact) #Direct to delete
        buttons.add_widget(return_button)
        buttons.add_widget(yes_button)

        content.add_widget(self.check)
        content.add_widget(buttons)

        self.add_widget(content)

    def delete_contact(self, instance):
        if self.phone_number:  # Check if phone_number is set
            try:
                with sqlite3.connect("phonebook.db") as conn:
                    c = conn.cursor()
                    # Proceed with deletion
                    c.execute("DELETE FROM phonebook WHERE tel_no = ?", (self.phone_number,))
                    conn.commit()
                    print("Contact deleted successfully.")
                    self.dismiss()  # Close the popup after deletion
                    self.add_instance.parent.parent.manager.current = 'main' #Return to main bc deleted contact
            except sqlite3.Error as e:
                print(f"An error occurred while deleting contact: {e}")
        



class Recent(Screen): #Recent calls
    def __init__(self, **kwargs):
        super(Recent, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        top = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        self.title = MDLabel(text="Recent Calls",md_bg_color= (.4,.4,.4,1),bold=True)
        self.delete = Button(text="-", size_hint=(.1, 1))
        top.add_widget(self.title)
        top.add_widget(self.delete)
        

        self.mid = MDLabel(text="Coming Soon",size_hint_y= .8,md_bg_color= (.7,.7,.7,1),halign="center")

        self.bottom = Bottom(go_to_main=self.go_to_main, go_to_recent=self.go_to_recent)

        layout.add_widget(top)
        layout.add_widget(self.mid)
        layout.add_widget(self.bottom)
        self.add_widget(layout)

    def go_to_main(self, instance):
        self.switch_screen('main', "right")

    def go_to_recent(self, instance):
        self.switch_screen('recent', "left")
    

    def switch_screen(self, screen_name, transition_direction): #Switch screen to names by a direction
        self.manager.current = screen_name
        self.manager.transition.direction = transition_direction


class Edit(Screen):
    def __init__(self, **kwargs):
        super(Edit, self).__init__(**kwargs)
        self.info_layout = EditContactLayout() #Setup layout
        self.clear_widgets() #Clear widgets for updated widgets
        self.add_widget(self.info_layout) #Add layout to screen
        

    def populate_info(self, user_info): #Call user info
        self.info_layout.main_layout.populate_fields(user_info)

    def go_to_info(self, instance): #Function for transition to info page
        self.manager.current = 'info'
        self.manager.transition.direction = 'right'


class EditContactLayout(BoxLayout):
    def __init__(self, **kwargs):  
        super(EditContactLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        #Create by parts
        self.create_top_layout()
        self.create_main_layout()
        self.bottom_layout = self.create_bottom_layout()

    def create_top_layout(self): #Call layouts
        self.top_layout = EditTopLayout()
        self.add_widget(self.top_layout)

    def create_main_layout(self):
        self.main_layout = EditMainLayout()
        self.add_widget(self.main_layout)

    def create_bottom_layout(self):
        bottom_layout = EditBottomLayout(on_cancel=self.cancel, on_save=self.saving)
        self.add_widget(bottom_layout)
        return bottom_layout

    def cancel(self, instance): #Redirect cancel function to screen
        self.parent.go_to_info(instance=None)

    def saving(self, instance): #redirect save contact function
        self.main_layout.save_contact()


class EditTopLayout(BoxLayout): #Top layout
    def __init__(self, **kwargs):  # Fixed constructor name
        super(EditTopLayout, self).__init__(**kwargs)
        self.size_hint_y = 0.1
        self.label = MDLabel(text="Edit Contact", md_bg_color=(0.4, 0.4, 0.4, 1))
        self.add_widget(self.label)


class EditMainLayout(BoxLayout): #Main layout
    def __init__(self, **kwargs):
        super(EditMainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.phone_number = None    # Initialize phone_number

        #Setup design for layout of fields inputs
        self.main_layout = BoxLayout(orientation="vertical")
        self.add_widget(self.main_layout)

        self.output = MDLabel(text="<Output>", size_hint_y=None, height=30,
                                valign='middle', halign='left', color=(0, 0, 0, 1),
                                font_size="8pt", md_bg_color=(0.4, 0.4, 0.4, 1)) #Status showcase row

        self.field_inputs = {
            'F_Name': TextInput(hint_text="Input F_Name", multiline=False),
            'L_Name': TextInput(hint_text="Input L_Name", multiline=False),
            'Tel': TextInput(hint_text="Input Tel", multiline=False),
            'Email': TextInput(hint_text="Input Email", multiline=False),
            'Address': TextInput(hint_text="Input Address", multiline=False),
            'Groups': TextInput(hint_text="Input Groups", multiline=False)
        }

        for label_text, input_field in self.field_inputs.items():
            layout = BoxLayout(orientation="horizontal")
            label = MDLabel(text=f"{label_text}:", size_hint_x=0.3,
                            valign='middle', halign='left', color=(0, 0, 0, 1),
                            font_size="8pt", md_bg_color=(0.7, 0.7, 0.7, 1))
            layout.add_widget(label)
            layout.add_widget(input_field)
            self.main_layout.add_widget(layout)

        self.main_layout.add_widget(self.output)

    def populate_fields(self, user_data): #Insert user info into input fields when loaded
        if len(user_data) >= 6:
            self.field_inputs['F_Name'].text = user_data[0]
            self.field_inputs['L_Name'].text = user_data[1]
            self.field_inputs['Tel'].text = user_data[2]
            self.field_inputs['Email'].text = user_data[3]
            self.field_inputs['Address'].text = user_data[4]
            self.field_inputs['Groups'].text = user_data[5]
            self.phone_number = user_data[2]

    def save_contact(self): #Save Contacts + check if tel no. unique + Names and tel filled
        if (self.field_inputs['F_Name'].text and 
            self.field_inputs['L_Name'].text and 
            self.field_inputs['Tel'].text):
            
            c.execute("SELECT COUNT(*) FROM phonebook WHERE tel_no = ?", (self.field_inputs['Tel'].text,))
            count = c.fetchone()[0]
            
            if self.field_inputs['Tel'].text == self.phone_number: #If tel no not changed, proceed edit.
                count -= 1
            
            if count > 0: #If tel. no duplicated with others, reject edit.
                self.output.text = ">> The phone number already exists in the database."
                return
            else: #Update database by text inputs
                sql_query = "UPDATE phonebook SET first_name = ?, last_name = ?, tel_no = ?, email = ?, address = ?, groups = ? WHERE tel_no = ?"
                params = [
                    self.field_inputs['F_Name'].text, 
                    self.field_inputs['L_Name'].text, 
                    self.field_inputs['Tel'].text,
                    self.field_inputs['Email'].text, 
                    self.field_inputs['Address'].text, 
                    self.field_inputs['Groups'].text, 
                    self.phone_number  # Use the stored phone number
                ]
                
                try: #Use SQL command
                    c.execute(sql_query, params)
                    conn.commit()
                    self.output.text = ">> Contact saved successfully."
                except Exception as e:
                    self.output.text = f">> Error saving contact: {e}"
        else: #Name or tel no. not filled
            self.output.text = ">> Please fill in all the required fields."

class EditBottomLayout(BoxLayout): #Bottom Layout
    def __init__(self, on_cancel, on_save, **kwargs): #Create bottom buttons
        super(EditBottomLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.15
        self.create_widgets(on_cancel, on_save)

    def create_widgets(self, on_cancel, on_save): #Design bottom buttons + function redirect
        self.back = Button(text="Cancel", on_press=on_cancel)
        self.save = Button(text="Save", on_press=on_save)
        self.add_widget(self.back)
        self.add_widget(self.save)



class AddScreen(Screen): #Main Screen
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.add_contact_layout = AddContactLayout() #Call layout
        self.add_contact_layout.bind(on_cancel=self.go_to_main)
        self.add_widget(self.add_contact_layout)

    def go_to_main(self): #Function for transition to main screen
        self.manager.current = 'main'
        self.manager.transition.direction = "right"

class AddContactLayout(BoxLayout): #For adding contact
    def __init__(self,**kwargs):
        super(AddContactLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        #Create by parts
        self.create_top_layout()
        self.create_main_layout()
        self.bottom_layout = self.create_bottom_layout() 

    def create_top_layout(self): #Call parts with function names
        self.top_layout = AddTopLayout(on_clear=self.open_popup)
        self.add_widget(self.top_layout)
        pass

    def create_main_layout(self):
        self.main_layout = AddMainLayout()
        self.add_widget(self.main_layout)

    def create_bottom_layout(self):
        bottom_layout = AddBottomLayout(on_cancel=self.cancel, on_save=self.saving)
        self.add_widget(bottom_layout)
        return bottom_layout  

    def open_popup(self, instance): #For confirmation of clear input fields
        popup = Addclear(add_instance=self)
        popup.open()

    def cancel(self, instance): #Redirect go to main function
        self.parent.go_to_main()

    def saving(self, instance): #Redirect save contact function
        self.main_layout.save_contact()

    def clearing(self, instance): #Clear all input fields
        for _, input_field in self.main_layout.input_fields:
            input_field.text = ""

class AddTopLayout(BoxLayout): #Top layout
    def __init__(self, on_clear, **kwargs): #Design layout
        super(AddTopLayout, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.15
        self.create_widgets(on_clear)

    def create_widgets(self, on_clear): #Create widgets
        self.title = MDLabel(text="Add Contact:",md_bg_color=(.4,.4,.4,1))
        self.clear = Button(text="Clear", on_press=on_clear)
        self.add_widget(self.title)
        self.add_widget(self.clear)

class AddMainLayout(BoxLayout): #Main layout
    def __init__(self, **kwargs):
        super(AddMainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 0.8
        
        self.main_layout = BoxLayout(orientation="vertical")
        self.add_widget(self.main_layout)

        self.create_input_fields() # Call input fields

    def create_input_fields(self): # Design input fields
        self.infn = TextInput(hint_text=f"Input F_Name", multiline=False)
        self.inln = TextInput(hint_text=f"Input L_Name", multiline=False)
        self.intel = TextInput(hint_text=f"Input Tel", multiline=False)
        self.inem = TextInput(hint_text=f"Input Email", multiline=False)
        self.inadd = TextInput(hint_text=f"Input Address", multiline=False)
        self.ingp = TextInput(hint_text=f"Input Groups", multiline=False)

        self.output = MDLabel(text="<Output>",text_size=self.size,
                                valign='middle', halign='left', color=(0, 0, 0, 1),
                                font_size="8pt", md_bg_color=(0.7, 0.7, 0.7, 1))
        self.input_fields = [
            ('F_Name', self.infn),
            ('L_Name', self.inln),
            ('Tel', self.intel),
            ('Email', self.inem),
            ('Address', self.inadd),
            ('Groups', self.ingp)]
        
        for label_text, input_field in self.input_fields:
            layout = BoxLayout(orientation="horizontal")
            label = MDLabel(text=f"{label_text}:", text_size=layout.size,
                            valign='middle', halign='left', color=(0, 0, 0, 1),
                            font_size="8pt", md_bg_color=(0.7, 0.7, 0.7, 1),
                            size_hint_x=0.3)
            layout.add_widget(label)
            layout.add_widget(input_field)
            self.main_layout.add_widget(layout)  
        self.main_layout.add_widget(self.output)

    def save_contact(self): #Save Contacts + check if tel no. unique + Names and tel filled
        if self.infn.text != "" and self.inln.text != "" and self.intel.text != "":
            c.execute("SELECT COUNT(*) FROM phonebook WHERE tel_no = ?", (self.intel.text,))
            count = c.fetchone()[0]
            if count > 0:
                # Phone number already exists
                self.output.text = (">>The phone number already exists in the database.")
                return
            else:
                # Insert the new contact into database
                sql_query = "INSERT INTO phonebook VALUES (?,?,?,?,?,?,?)"
                params = [self.infn.text, self.inln.text, self.intel.text,
                        self.inem.text, self.inadd.text, self.ingp.text,False] 
                #Run SQL
                try:
                    c.execute(sql_query, params)
                    conn.commit()
                    self.output.text = (">>Contact saved successfully.")
                except Exception as e:
                    self.output.text = (f">>Error saving contact: {e}")
        else: #Name or tel no. not filled
            self.output.text = (">>Please fill in all the required fields.")
            pass

class AddBottomLayout(BoxLayout): #Bottom layout
    def __init__(self, on_cancel, on_save, **kwargs):
        super(AddBottomLayout, self).__init__(**kwargs) #Design layout
        self.orientation = 'horizontal'
        self.size_hint_y = 0.15
        self.create_widgets(on_cancel, on_save)

    def create_widgets(self, on_cancel, on_save): #Add widgets + functions redirect
        self.back = Button(text="Cancel", on_press=on_cancel)
        self.save = Button(text="Save", on_press=on_save) 
        self.add_widget(self.back)
        self.add_widget(self.save)

class Addclear(Popup): #For confirmation of clear input fields
    def __init__(self, add_instance, **kwargs):
        super().__init__(**kwargs)
        self.add_instance = add_instance 

        self.size_hint = (0.8, 0.5)
        self.title = "Confirm Clear" #Title

        #Design layout
        content = BoxLayout(orientation='vertical', size_hint_y=1) 
        self.check = MDLabel(text='Are you sure you want to clear all inputs in boxes?',
                            valign="center", halign="center",
                            text_size=content.size)
        self.check.color = (1, 1, 1, 1)
        content.add_widget(self.check)

        buttons = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        Return = Button(text='Return', on_press=self.dismiss) #Remove popup when pressed
        Yes = Button(text='Clear Input', on_press=self.clear_inputs) #Redirect to clear inputs function
        buttons.add_widget(Return)
        buttons.add_widget(Yes)
        content.add_widget(buttons)

        self.content = content

    def clear_inputs(self, instance): #Redirect to clearing function
        self.add_instance.clearing(instance)
        self.dismiss()

class Bottom(BoxLayout):  # Common bottom switch screen for main and recent screen
    def __init__(self, go_to_main, go_to_recent, **kwargs):
        super(Bottom, self).__init__(**kwargs)  # Design layout
        self.orientation = 'horizontal'
        self.size_hint = (1, 0.1)

        self.contacts = Button(text='Contacts', on_press=go_to_main)  # Add buttons + Function redirect
        self.recent = Button(text='Recent', on_press=go_to_recent)
        self.add_widget(self.contacts)
        self.add_widget(self.recent)



class PhonebookzApp(MDApp): #App build
    def build(self):
        root = ScreenManager() #Manage and link screens
        root.add_widget(Main(self,name='main'))
        root.add_widget(AddScreen(name='add'))
        root.add_widget(Info(name='info'))
        root.add_widget(Recent(name='recent'))
        root.add_widget(Search(name='search'))
        root.add_widget(Edit(name='edit'))
        return root


PhonebookzApp().run() #Build app



