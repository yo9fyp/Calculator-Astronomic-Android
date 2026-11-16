from datetime import datetime
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from astronomie import calculeaza_eveniment_astronomic, formateaza_data_ro

BG = (0.035, 0.075, 0.14, 1)
PANEL = (0.075, 0.13, 0.22, 1)
GOLD = (0.97, 0.75, 0.34, 1)
WHITE = (0.95, 0.97, 1, 1)
MUTED = (0.70, 0.79, 0.88, 1)
EVENTS = [
    ('primavara', 'Echinocțiul de primăvară'),
    ('vara', 'Solstițiul de vară'),
    ('toamna', 'Echinocțiul de toamnă'),
    ('iarna', 'Solstițiul de iarnă'),
]

class CalculatorApp(App):
    def build(self):
        self.title = 'Calculator Astronomic'
        outer = BoxLayout(orientation='vertical', padding=dp(18), spacing=dp(12))
        from kivy.graphics import Color, Rectangle
        with outer.canvas.before:
            Color(*BG)
            self.bgrect = Rectangle(pos=outer.pos, size=outer.size)
        outer.bind(pos=lambda *_: setattr(self.bgrect, 'pos', outer.pos),
                   size=lambda *_: setattr(self.bgrect, 'size', outer.size))
        header = Label(text='ECHINOCȚII ȘI SOLSTIȚII', font_size='21sp', bold=True,
                       color=GOLD, size_hint_y=None, height=dp(48))
        outer.add_widget(header)
        subtitle = Label(text='Calculator astronomic • ora României (estimare)',
                         font_size='13sp', color=MUTED, size_hint_y=None, height=dp(30))
        outer.add_widget(subtitle)
        row = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        self.year = TextInput(text=str(datetime.now().year), multiline=False,
                              input_filter='int', font_size='22sp', halign='center',
                              foreground_color=WHITE, background_color=PANEL,
                              cursor_color=GOLD, size_hint_x=.38)
        self.year.bind(on_text_validate=lambda *_: self.calculate())
        row.add_widget(self.year)
        go = Button(text='CALCULEAZĂ', bold=True, font_size='15sp',
                    background_normal='', background_color=(.19,.42,.65,1))
        go.bind(on_release=lambda *_: self.calculate())
        row.add_widget(go)
        outer.add_widget(row)
        self.message = Label(text='', color=GOLD, font_size='13sp',
                             size_hint_y=None, height=dp(26))
        outer.add_widget(self.message)
        scroll = ScrollView(do_scroll_x=False)
        self.results = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter('height'))
        scroll.add_widget(self.results)
        outer.add_widget(scroll)
        copy = Button(text='COPIAZĂ REZULTATELE', size_hint_y=None, height=dp(50),
                      bold=True, background_normal='', background_color=(.23,.37,.48,1))
        copy.bind(on_release=lambda *_: self.copy_results())
        outer.add_widget(copy)
        foot = Label(text='Estimări matematice. Pentru anii istorici, fusul orar și ΔT sunt aproximative.',
                     font_size='11sp', color=MUTED, size_hint_y=None, height=dp(48),
                     text_size=(dp(315),None), halign='center', valign='middle')
        outer.add_widget(foot)
        self.calculate()
        return outer

    def calculate(self):
        value = self.year.text.strip()
        if not value.isdigit() or not 1000 <= int(value) <= 3000:
            self.message.text = 'Introduceți un an între 1000 și 3000.'
            return
        year = int(value)
        self.results.clear_widgets()
        self.lines = [f'Evenimente astronomice — {year} (estimări)']
        for kind, title in EVENTS:
            dt, tz = calculeaza_eveniment_astronomic(year, kind)
            formatted = formateaza_data_ro(dt)
            self.lines.append(f'{title}: {formatted} ({tz})')
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(106),
                             padding=[dp(12),dp(8)], spacing=dp(2))
            from kivy.graphics import Color, RoundedRectangle
            with card.canvas.before:
                Color(*PANEL)
                rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
            card.bind(pos=lambda w, *_args, r=rect: setattr(r,'pos',w.pos),
                      size=lambda w, *_args, r=rect: setattr(r,'size',w.size))
            card.add_widget(Label(text=title, bold=True, color=GOLD,
                                  font_size='16sp', halign='left',
                                  text_size=(dp(300),None)))
            card.add_widget(Label(text=formatted, color=WHITE, font_size='13sp',
                                  halign='left', text_size=(dp(300),None)))
            card.add_widget(Label(text=tz, color=MUTED, font_size='12sp',
                                  halign='left', text_size=(dp(300),None)))
            self.results.add_widget(card)
        self.message.text = f'Anul {year} • 4 evenimente'

    def copy_results(self):
        if getattr(self, 'lines', None):
            Clipboard.copy('\n'.join(self.lines) + '\nOre aproximative; fus orar convențional.')
            self.message.text = 'Rezultatele au fost copiate.'

if __name__ == '__main__':
    CalculatorApp().run()
