from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import mysql.connector

class PhonebookApp(App):
    def build(self):
        self.layout = BoxLayout(padding=10, spacing=10)
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # تغيير لون الخلفية إلى رمادي
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)

        # اتصال بقاعدة البيانات
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook_db"
        )
        self.cursor = self.conn.cursor()

        # تقسيم الواجهة إلى نصفين
        left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        right_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))
        self.layout.add_widget(left_layout)
        self.layout.add_widget(right_layout)

        # زيادة حجم خانات الإدخال في الجهة اليسرى
        self.name_input = TextInput(hint_text='Enter name', size_hint=(1, 0.2), height=40)
        left_layout.add_widget(self.name_input)

        self.phone_input = TextInput(hint_text='Enter phone number', size_hint=(1, 0.2), height=40)
        left_layout.add_widget(self.phone_input)

        # زيادة حجم الأزرار في الجهة اليسرى
        self.add_button = Button(text='Add', size_hint=(1, 0.2), height=40, background_color=(0, 1, 0, 1))
        self.add_button.bind(on_press=self.add_record)
        left_layout.add_widget(self.add_button)

        self.query_button = Button(text='Query', size_hint=(1, 0.2), height=40, background_color=(0, 1, 0, 1))
        self.query_button.bind(on_press=self.query_record)
        left_layout.add_widget(self.query_button)

        self.show_all_button = Button(text='Show All', size_hint=(1, 0.2), height=40, background_color=(0, 1, 0, 1))
        self.show_all_button.bind(on_press=self.show_all_records)
        left_layout.add_widget(self.show_all_button)

        # إضافة مساحة لعرض الأسماء والأرقام في النصف الأيمن
        self.names_label = Label(text='', size_hint=(1, 1), color=(0, 0, 0, 1), font_size=20, halign='left', valign='middle')
        right_layout.add_widget(self.names_label)

        return self.layout

    def add_record(self, instance):
        # إضافة سجل إلى قاعدة البيانات
        name = self.name_input.text
        phone = self.phone_input.text
        query = f"INSERT INTO phonebook (name, phone) VALUES ('{name}', '{phone}')"
        self.cursor.execute(query)
        self.conn.commit()  # حفظ التغييرات في قاعدة البيانات

    def query_record(self, instance):
        # البحث عن السجل بواسطة الاسم
        name = self.name_input.text
        query = f"SELECT * FROM phonebook WHERE name = '{name}'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        # عرض النتائج
        if results:
            # تفريغ المساحة قبل عرض النتائج
            self.names_label.text = ""
            # عرض النتائج في الجهة اليمنى
            for result in results:
                self.names_label.text += f"Name: {result[1]}, Phone: {result[2]}\n\n"
        else:
            # تفريغ المساحة وعرض رسالة عندما لا يتم العثور على سجل
            self.names_label.text = "Record not found"

    def show_all_records(self, instance):
        # جلب كل السجلات
        query = "SELECT name, phone FROM phonebook"
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # تنظيف المساحة قبل عرض النتائج
        self.names_label.text = ""

        # عرض النتائج
        for record in records:
            self.names_label.text += f"Name: {record[0]}, Phone: {record[1]}\n\n"

        # حفظ التغييرات في قاعدة البيانات
        self.conn.commit()

    def on_stop(self):
        # إغلاق الاتصال بقاعدة البيانات عند إيقاف التطبيق
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    PhonebookApp().run()
