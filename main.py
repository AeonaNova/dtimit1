from PIL import Image, ImageDraw, ImageFont
import datetime
import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
from kivy.utils import get_color_from_hex

Config.set('graphics', 'resizable', False)
Window.clearcolor = get_color_from_hex('#282828')
Window.size = (300, 400)


class ImmitateTimeApp(App):
    def build(self):
        self.title = 'Имитировать время'
        layout = BoxLayout(orientation='vertical')

        self.open_button = Button(
            text='Выбрать картинку',
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.open_button.bind(on_press=self.select_image)

        layout.add_widget(self.open_button)

        return layout

    def select_image(self, *args):
        from kivy.uix.filechooser import FileChooserListView
        file_chooser = FileChooserListView()
        file_chooser.filters = ['*.jpg']

        popup = Popup(
            title="Выберите картинку",
            content=file_chooser,
            size_hint=(0.8, 0.8),
        )

        file_chooser.bind(on_submit=lambda instance, x: self.on_file_selected(instance.selection))

        popup.open()

    def on_file_selected(self, selection):
        for image_path in selection:
            image = Image.open(image_path)
            f = image.size[0] / 13

            # Создаем объекты для рисования и шрифта
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('arial.ttf', int(f))

            # Получаем текущую дату и время
            current_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

            # Вычисляем размер текста
            text_size = draw.textsize(current_time, font=font)

            # Определяем координаты текста
            x = image.size[0] - text_size[0] - image.size[0] / 4.4
            y = image.size[1] - text_size[1] - image.size[1] / 9

            # Рисуем текст на изображении
            draw.text((x, y), current_time, fill=(255, 255, 0), font=font)

            # Сохраняем изображение с новой надписью
            output_path = os.path.splitext(image_path)[0] + '_output.jpg'
            image.save(output_path)

            save_popup = Popup(
                title="Сохранить изображение",
                content=Label(text='Введите имя файла:'),
                size_hint=(0.5, 0.5),
            )

            def save_file(name):
                image.save(os.path.join('.', name))
                save_popup.dismiss()

            save_button = Button(text='Сохранить', size_hint=(0.5, 0.2))
            cancel_button = Button(text='Отмена', size_hint=(0.5, 0.2))

            buttons_layout = BoxLayout(orientation='horizontal')
            buttons_layout.add_widget(save_button)
            buttons_layout.add_widget(cancel_button)

            text_input = ctk.CTkTextInput(hint_text='Введите имя файла', multiline=False)

            save_popup.content.add_widget(text_input)
            save_popup.content.add_widget(buttons_layout)

            cancel_button.bind(on_press=save_popup.dismiss)
            save_button.bind(on_press=lambda x: save_file(text_input.text))

            save_popup.open()


if __name__ == '__main__':
    ImmitateTimeApp().run() 
