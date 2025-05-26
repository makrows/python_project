from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList, TwoLineAvatarIconListItem, ImageLeftWidget
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
import json
from kivy.clock import Clock

Window.size = (350, 600)

class ContentNavigationDrawer(MDBoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    
    def on_release(self):
        self.parent.set_color_item(self)
        app = MDApp.get_running_app()
        if self.text == "Wszyscy studenci":
            app.switch_screen("students_screen")
        elif self.text == "Zdający":
            app.switch_screen("passing_students_screen")
        elif self.text == "Niezdający":  # Fixed spelling from "Niezliczający"
            app.switch_screen("failing_students_screen")
        elif self.text == "Statystyki":
            app.switch_screen("statistics_screen")
        elif self.text == "Dodaj studenta":
            app.show_add_student_dialog()

class StudentListItem(TwoLineAvatarIconListItem):
    def __init__(self, student_data, **kwargs):
        super().__init__(**kwargs)
        self.student_data = student_data
        self.text = student_data["name"]
        self.secondary_text = f"Średnia: {student_data['average']:.1f} | Status: {'ZDAJE' if student_data['average'] >= 3.0 else 'NIE ZDAJE'}"
        
        # Set text color based on passing status
        if student_data["average"] >= 3.0:
            self.theme_text_color = "Custom"
            self.text_color = (0, 0.7, 0, 1)  # Green for passing
        else:
            self.theme_text_color = "Custom"
            self.text_color = (0.8, 0, 0, 1)  # Red for failing
        
        # Add avatar
        avatar = ImageLeftWidget()
        avatar.source = student_data.get("photo", "../landscape.jpg")
        self.add_widget(avatar)
    
    def on_release(self):
        app = MDApp.get_running_app()
        app.show_student_details(self.student_data)

class DrawerList(MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Called when you tap on the menu item.
        for item in self.children:
            if instance_item.text == item.text:
                item.text_color = (0.2, 0.4, 0.8, 1)  # Blue color for selected item
            else:
                item.text_color = (0, 0, 0, 1)  # Default black color

class MainScreen(MDScreen):
    pass

class StudentsScreen(MDScreen):
    pass

class PassingStudentsScreen(MDScreen):
    pass

class FailingStudentsScreen(MDScreen):
    pass

class StatisticsScreen(MDScreen):
    pass

class ERektor(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.students_data = []
        self.student_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("task3_app.kv")

    def on_start(self):
        """Called when the app starts."""
        self.load_student_data()
        self.setup_navigation_drawer()
        
    def load_student_data(self):
        """Load student data from JSON file."""
        try:
            with open("app_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.students_data = data.get("students", [])
                print(f"Loaded {len(self.students_data)} students")
        except FileNotFoundError:
            print("app_data.json not found")
            self.students_data = []
        except json.JSONDecodeError:
            print("Error reading app_data.json")
            self.students_data = []

    def setup_navigation_drawer(self):
        """Setup navigation drawer items."""
        icons_item = {
            "👥 Wszyscy studenci": "account-group",
            "✅ Zdający": "check-circle", 
            "❌ Niezdający": "close-circle",
            "📊 Statystyki": "chart-bar",
            "➕ Dodaj studenta": "plus",
        }
        
        # Use Clock.schedule_once to ensure widgets are ready
        def setup_items(dt):
            try:
                # Find the md_list widget in the entire widget tree
                md_list = self.find_widget_by_id(self.root, "md_list")
                if md_list:
                    # Clear any existing items
                    md_list.clear_widgets()
                    
                    for icon_name, icon in icons_item.items():
                        item = ItemDrawer(
                            icon=icon,
                            text=icon_name.split(" ", 1)[1],  # Remove emoji
                            text_color=(0, 0, 0, 1),
                        )
                        md_list.add_widget(item)
                    print(f"Navigation drawer items added successfully: {len(icons_item)} items")
                else:
                    print("md_list widget not found in the entire widget tree!")
            except Exception as e:
                print(f"Error setting up navigation drawer: {e}")
        
        Clock.schedule_once(setup_items, 1.0)  # Increased delay to ensure widgets are ready

    def navigate_to_next_screen(self):
        """Navigate to next screen in sequence for testing."""
        current_screen = self.root.ids.screen_manager.current
        screens = ["main_screen", "students_screen", "passing_students_screen", "failing_students_screen", "statistics_screen"]
        
        try:
            current_index = screens.index(current_screen)
            next_index = (current_index + 1) % len(screens)
            next_screen = screens[next_index]
            print(f"Navigating from {current_screen} to {next_screen}")
            self.switch_screen(next_screen)
        except ValueError:
            # If current screen not in list, go to students screen
            self.switch_screen("students_screen")

    def switch_screen(self, screen_name):
        """Switch to specified screen and populate with student data."""
        print(f"Switching to screen: {screen_name}")
        
        # Close navigation drawer if it exists
        try:
            nav_drawer = self.find_widget_by_id(self.root, "nav_drawer")
            if nav_drawer:
                nav_drawer.set_state("close")
        except Exception as e:
            print(f"Could not close navigation drawer: {e}")
        
        # Switch screen
        self.root.ids.screen_manager.current = screen_name
        
        # Populate screen with data
        Clock.schedule_once(lambda dt: self.populate_screen(screen_name), 0.1)

    def populate_screen(self, screen_name):
        """Populate screen with appropriate student data."""
        print(f"Populating screen: {screen_name}")
        
        if screen_name == "students_screen":
            self.populate_student_list("students_screen", self.students_data)
        elif screen_name == "passing_students_screen":
            passing_students = [s for s in self.students_data if s["average"] >= 3.0]
            self.populate_student_list("passing_students_screen", passing_students)
        elif screen_name == "failing_students_screen":
            failing_students = [s for s in self.students_data if s["average"] < 3.0]
            self.populate_student_list("failing_students_screen", failing_students)
        elif screen_name == "statistics_screen":
            self.populate_statistics()

    def find_widget_by_id(self, widget, widget_id):
        """Recursively find a widget by its ID."""
        if hasattr(widget, 'id') and widget.id == widget_id:
            return widget
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                found = self.find_widget_by_id(child, widget_id)
                if found:
                    return found
        
        # Also check if widget has ids attribute (for screens)
        if hasattr(widget, 'ids') and widget_id in widget.ids:
            return widget.ids[widget_id]
            
        return None

    def find_widget_by_type(self, widget, widget_type):
        """Recursively find a widget by its type."""
        if isinstance(widget, widget_type):
            return widget
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                found = self.find_widget_by_type(child, widget_type)
                if found:
                    return found
        
        return None
    
    def populate_student_list(self, screen_name, students):
        """Populate student list for specified screen."""
        print(f"Populating {screen_name} with {len(students)} students")
        
        # Get the screen
        screen = None
        for screen_widget in self.root.ids.screen_manager.screens:
            if screen_widget.name == screen_name:
                screen = screen_widget
                break
        
        if not screen:
            print(f"Screen {screen_name} not found!")
            return
        
        print(f"Found screen: {screen}")
        
        # Try multiple methods to find the student_list widget
        student_list = None
        
        # Method 1: Direct access via screen.ids
        if hasattr(screen, 'ids') and 'student_list' in screen.ids:
            student_list = screen.ids.student_list
            print("Found student_list via screen.ids")
        
        # Method 2: Recursive search
        if not student_list:
            student_list = self.find_widget_by_id(screen, "student_list")
            if student_list:
                print("Found student_list via recursive search")
        
        # Method 3: Search for MDList widget type
        if not student_list:
            def find_mdlist(widget):
                if hasattr(widget, '__class__') and 'MDList' in str(widget.__class__):
                    return widget
                if hasattr(widget, 'children'):
                    for child in widget.children:
                        found = find_mdlist(child)
                        if found:
                            return found
                return None
            
            student_list = find_mdlist(screen)
            if student_list:
                print("Found MDList widget via type search")
        
        if not student_list:
            print(f"student_list widget not found in {screen_name}!")
            print(f"Available IDs in screen: {getattr(screen, 'ids', {}).keys() if hasattr(screen, 'ids') else 'No ids'}")
            return
        
        print(f"Using student_list widget: {student_list}")
        
        # Clear existing items
        student_list.clear_widgets()
        
        # Add student items
        for student in students:
            item = StudentListItem(student)
            student_list.add_widget(item)
        
        print(f"Added {len(students)} students to {screen_name}")

    def populate_statistics(self):
        """Populate statistics screen with data."""
        print("Populating statistics")
        
        if not self.students_data:
            return
        
        # Calculate statistics
        total_students = len(self.students_data)
        passing_students = len([s for s in self.students_data if s["average"] >= 3.0])
        failing_students = total_students - passing_students
        pass_rate = (passing_students / total_students) * 100 if total_students > 0 else 0
        
        # Calculate grade distribution
        all_grades = []
        for student in self.students_data:
            all_grades.extend(student.get("grades", []))
        
        avg_grade = sum(all_grades) / len(all_grades) if all_grades else 0
        
        # Grade distribution by ranges
        grade_ranges = {
            "2.0-2.5": 0,
            "2.6-3.0": 0,
            "3.1-3.5": 0,
            "3.6-4.0": 0,
            "4.1-4.5": 0,
            "4.6-5.0": 0
        }
        
        for grade in all_grades:
            if 2.0 <= grade <= 2.5:
                grade_ranges["2.0-2.5"] += 1
            elif 2.6 <= grade <= 3.0:
                grade_ranges["2.6-3.0"] += 1
            elif 3.1 <= grade <= 3.5:
                grade_ranges["3.1-3.5"] += 1
            elif 3.6 <= grade <= 4.0:
                grade_ranges["3.6-4.0"] += 1
            elif 4.1 <= grade <= 4.5:
                grade_ranges["4.1-4.5"] += 1
            elif 4.6 <= grade <= 5.0:
                grade_ranges["4.6-5.0"] += 1
        
        # Create statistics text
        stats_text = f"""[size=20][b]📊 Statystyki studentów[/b][/size]

[size=16][b]Ogólne statystyki:[/b][/size]
• Łączna liczba studentów: [b]{total_students}[/b]
• Studenci zdający (≥3.0): [color=00AA00][b]{passing_students}[/b][/color]
• Studenci niezdający (<3.0): [color=CC0000][b]{failing_students}[/b][/color]
• Wskaźnik zdawalności: [b]{pass_rate:.1f}%[/b]

[size=16][b]Rozkład ocen:[/b][/size]
• Średnia ogólna: [b]{avg_grade:.2f}[/b]
• Łączna liczba ocen: [b]{len(all_grades)}[/b]

[size=14][b]Przedziały ocen:[/b][/size]"""

        for range_name, count in grade_ranges.items():
            percentage = (count / len(all_grades)) * 100 if all_grades else 0
            stats_text += f"\n• {range_name}: {count} ({percentage:.1f}%)"

        stats_text += f"""

[size=16][b]Lista studentów zdających:[/b][/size]"""
        
        passing_list = [s for s in self.students_data if s["average"] >= 3.0]
        for student in passing_list:
            stats_text += f"\n• [color=00AA00]{student['name']} - {student['average']:.1f}[/color]"

        stats_text += f"""

[size=16][b]Lista studentów niezdających:[/b][/size]"""
        
        failing_list = [s for s in self.students_data if s["average"] < 3.0]
        for student in failing_list:
            stats_text += f"\n• [color=CC0000]{student['name']} - {student['average']:.1f}[/color]"
        
        # Find statistics screen and update label
        stats_screen = None
        for screen in self.root.ids.screen_manager.screens:
            if screen.name == "statistics_screen":
                stats_screen = screen
                break
        
        if stats_screen:
            # Try multiple methods to find the stats_label
            stats_label = self.find_widget_by_id(stats_screen, "stats_label")
            
            # If direct ID search fails, try type-based search
            if not stats_label:
                stats_label = self.find_widget_by_type(stats_screen, MDLabel)
                if stats_label and hasattr(stats_label, 'id') and stats_label.id == "stats_label":
                    pass  # Found the right label
                else:
                    # Create the label if it doesn't exist
                    from kivymd.uix.card import MDCard
                    card = self.find_widget_by_type(stats_screen, MDCard)
                    if card:
                        stats_label = MDLabel(
                            id="stats_label",
                            text=stats_text,
                            halign="left",
                            valign="top",
                            font_style="Body1",
                            markup=True,
                            text_size=(None, None)
                        )
                        card.clear_widgets()
                        card.add_widget(stats_label)
                        print("Created new stats_label")
            
            if stats_label:
                stats_label.text = stats_text
                # Set text_size for proper text wrapping
                def set_text_size(dt):
                    if hasattr(stats_label, 'width') and stats_label.width > 0:
                        stats_label.text_size = (stats_label.width - 40, None)
                Clock.schedule_once(set_text_size, 0.1)
                print("Statistics updated successfully")
            else:
                print("Could not find or create stats_label!")
        else:
            print("Statistics screen not found!")

    def show_student_details(self, student_data):
        """Show detailed student information in a dialog."""
        if self.student_dialog:
            self.student_dialog.dismiss()
        
        # Format grades as a string
        grades_text = ", ".join([str(g) for g in student_data.get("grades", [])])
        
        content = f"""
[b]Imię i nazwisko:[/b] {student_data['name']}
[b]Email:[/b] {student_data['email']}
[b]Telefon:[/b] {student_data['phone']}
[b]Adres:[/b] {student_data['address']}

[b]Oceny:[/b] {grades_text}
[b]Średnia:[/b] {student_data['average']:.1f}
[b]Status:[/b] {'[color=00AA00]ZDAJE[/color]' if student_data['average'] >= 3.0 else '[color=CC0000]NIE ZDAJE[/color]'}
        """
        
        dialog_label = MDLabel(
            text=content.strip(),
            markup=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height="300dp",
            text_size=(None, None)
        )
        
        self.student_dialog = MDDialog(
            title=f"📋 Profil studenta",
            type="custom",
            content_cls=dialog_label,
            buttons=[
                MDFlatButton(
                    text="ZAMKNIJ",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.student_dialog.dismiss()
                ),
            ],
        )
        
        # Adjust dialog label text size after dialog is opened
        def adjust_text_size(dt):
            dialog_label.text_size = (dialog_label.width - 40, None)
        
        Clock.schedule_once(adjust_text_size, 0.1)
        self.student_dialog.open()

    def show_add_student_dialog(self):
        """Show dialog for adding a new student."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.gridlayout import MDGridLayout
        
        if self.student_dialog:
            self.student_dialog.dismiss()
        
        # Create input fields
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="400dp"
        )
        
        self.name_field = MDTextField(
            hint_text="Imię i nazwisko",
            required=True,
            helper_text="Wprowadź pełne imię i nazwisko",
            helper_text_mode="on_error"
        )
        
        self.email_field = MDTextField(
            hint_text="Email",
            required=True,
            helper_text="Wprowadź adres email",
            helper_text_mode="on_error"
        )
        
        self.phone_field = MDTextField(
            hint_text="Telefon",
            helper_text="Wprowadź numer telefonu"
        )
        
        self.address_field = MDTextField(
            hint_text="Adres",
            helper_text="Wprowadź adres zamieszkania"
        )
        
        self.grades_field = MDTextField(
            hint_text="Oceny (oddzielone przecinkami)",
            helper_text="Np: 3.5, 4.0, 3.0, 4.5",
            helper_text_mode="on_error"
        )
        
        content.add_widget(MDLabel(text="[b]Dodaj nowego studenta[/b]", markup=True, size_hint_y=None, height="30dp"))
        content.add_widget(self.name_field)
        content.add_widget(self.email_field)
        content.add_widget(self.phone_field)
        content.add_widget(self.address_field)
        content.add_widget(self.grades_field)
        
        self.student_dialog = MDDialog(
            title="➕ Dodaj studenta",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ANULUJ",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.student_dialog.dismiss()
                ),
                MDFlatButton(
                    text="DODAJ",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.add_new_student
                ),
            ],
        )
        self.student_dialog.open()
    
    def add_new_student(self, instance):
        """Add a new student to the database."""
        # Validate required fields
        if not self.name_field.text.strip():
            self.name_field.error = True
            return
        
        if not self.email_field.text.strip():
            self.email_field.error = True
            return
        
        # Parse grades
        grades = []
        if self.grades_field.text.strip():
            try:
                grade_strings = [g.strip() for g in self.grades_field.text.split(',')]
                grades = [float(g) for g in grade_strings if g]
                # Validate grade range
                for grade in grades:
                    if not (2.0 <= grade <= 5.0):
                        self.grades_field.error = True
                        self.grades_field.helper_text = "Oceny muszą być w zakresie 2.0-5.0"
                        return
            except ValueError:
                self.grades_field.error = True
                self.grades_field.helper_text = "Niepoprawny format ocen"
                return
        
        # Calculate average
        average = sum(grades) / len(grades) if grades else 0.0
        
        # Create new student record
        new_student = {
            "name": self.name_field.text.strip(),
            "email": self.email_field.text.strip(),
            "phone": self.phone_field.text.strip() or "Brak",
            "address": self.address_field.text.strip() or "Brak",
            "photo": "photos/default_student.jpg",  # Default photo
            "grades": grades,
            "average": round(average, 2)
        }
        
        # Add to students data
        self.students_data.append(new_student)
        
        # Save to file
        self.save_student_data()
        
        # Close dialog
        self.student_dialog.dismiss()
        
        # Refresh current screen
        current_screen = self.root.ids.screen_manager.current
        self.switch_screen(current_screen)
        
        # Show success message
        from kivymd.toast import toast
        toast(f"Student {new_student['name']} został dodany pomyślnie!")
    
    def save_student_data(self):
        """Save student data to JSON file."""
        try:
            data = {"students": self.students_data}
            with open("app_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print(f"Saved {len(self.students_data)} students to app_data.json")
        except Exception as e:
            print(f"Error saving student data: {e}")

if __name__ == "__main__":
    ERektor().run()