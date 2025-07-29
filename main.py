from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.icon_definitions import md_icons
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import json
import os


# 注册中文字体
LabelBase.register(name="Roboto",
                   fn_regular="C:/Windows/Fonts/msyh.ttc")  # 微软雅黑字体


class TaskItem(OneLineAvatarIconListItem):
    def __init__(self, task_text, task_id, main_app, **kwargs):
        super().__init__(**kwargs)
        self.text = task_text
        self.task_id = task_id
        self.main_app = main_app

        # 添加删除按钮
        delete_btn = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color="red",
            on_release=self.delete_task
        )
        self.add_widget(delete_btn)

    def delete_task(self, *args):
        self.main_app.delete_task(self.task_id)


class TodoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.task_counter = 0
        self.data_file = "tasks.json"
        self.load_tasks()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.font_styles.update({
            "H1": ["Roboto", 96, False, -1.5],
            "H2": ["Roboto", 60, False, -0.5],
            "H3": ["Roboto", 48, False, 0],
            "H4": ["Roboto", 34, False, 0.25],
            "H5": ["Roboto", 24, False, 0],
            "H6": ["Roboto", 20, False, 0.15],
            "Subtitle1": ["Roboto", 16, False, 0.15],
            "Subtitle2": ["Roboto", 14, False, 0.1],
            "Body1": ["Roboto", 16, False, 0.5],
            "Body2": ["Roboto", 14, False, 0.25],
            "Button": ["Roboto", 14, True, 1.25],
            "Caption": ["Roboto", 12, False, 0.4],
            "Overline": ["Roboto", 10, True, 1.5],
        })

        # 创建主屏幕
        screen = MDScreen()

        # 创建主布局
        main_layout = MDBoxLayout(orientation="vertical", spacing="10dp", padding="10dp")

        # 顶部工具栏
        toolbar = MDTopAppBar(
            title="My Todo List",  # 使用英文避免字体问题
            elevation=10,
        )
        main_layout.add_widget(toolbar)

        # 输入区域
        input_card = MDCard(
            MDBoxLayout(
                orientation="horizontal",
                spacing="10dp",
                padding="15dp",
                size_hint_y=None,
                height="80dp"
            ),
            elevation=5,
            size_hint_y=None,
            height="80dp"
        )

        self.task_input = MDTextField(
            hint_text="Enter new task...",  # 使用英文
            size_hint_x=0.8,
            multiline=False
        )

        add_button = MDRaisedButton(
            text="ADD",  # 使用英文
            size_hint_x=0.2,
            on_release=self.add_task
        )

        input_card.children[0].add_widget(self.task_input)
        input_card.children[0].add_widget(add_button)
        main_layout.add_widget(input_card)

        # 任务列表区域
        self.task_list = MDList()
        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        main_layout.add_widget(scroll)

        # 底部统计信息
        self.stats_label = MDLabel(
            text=f"Total: {len(self.tasks)} tasks",  # 使用英文
            size_hint_y=None,
            height="40dp",
            theme_text_color="Secondary"
        )
        main_layout.add_widget(self.stats_label)

        screen.add_widget(main_layout)

        # 加载现有任务
        self.refresh_task_list()

        return screen

    def add_task(self, *args):
        task_text = self.task_input.text.strip()
        if task_text:
            self.task_counter += 1
            task = {
                "id": self.task_counter,
                "text": task_text,
                "completed": False
            }
            self.tasks.append(task)
            self.task_input.text = ""
            self.save_tasks()
            self.refresh_task_list()

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list.clear_widgets()
        for task in self.tasks:
            task_item = TaskItem(
                task_text=task["text"],
                task_id=task["id"],
                main_app=self
            )
            self.task_list.add_widget(task_item)

        self.stats_label.text = f"Total: {len(self.tasks)} tasks"

    def save_tasks(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "tasks": self.tasks,
                    "counter": self.task_counter
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save failed: {e}")

    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.task_counter = data.get("counter", 0)
        except Exception as e:
            print(f"Load failed: {e}")
            self.tasks = []
            self.task_counter = 0


if __name__ == "__main__":
    TodoApp().run()
