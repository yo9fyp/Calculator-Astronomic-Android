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
from kivy.graphics import Color, Rectangle, RoundedRectangle
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


def responsive_label(text, font_size, color, bold=False, halign='left'):
    label = Label(text=text, font_size=font_size, color=color, bold=bold,
                  halign=halign, valign='middle')
    label.bind(size=lambda w, *_: setattr(w, 'text_size', (w.width, w.height)))
    return label


class CalculatorApp(App):
    def build(self):
        self.title = 'Calculator Astronomic'
        outer = BoxLayout(orientation='vertical', padding=[dp(14), dp(12), dp(14), dp(18)],
                          spacing=dp(7))
        with outer.canvas.before:
            Color(*BG)
            self.bgrect = Rectangle(pos=outer.pos, size=outer.size)
        outer.bind(pos=lambda *_: setattr(self.bgrect, 'pos', outer.pos),
                   size=lambda *_: setattr(self.bgrect, 'size', outer.size))

        header = responsive_label('ECHINOCȚII ȘI SOLSTIȚII', '17sp', GOLD,
                                  bold=True, halign='center')
        header.size_hint_y = None
        header.height = dp(38)
        outer.add_widget(header)

        subtitle = responsive_label('Calculator astronomic • ora României (estimare)',
                                    '11sp', MUTED, halign='center')
        subtitle.size_hint_y = None
        subtitle.height = dp(27)
        outer.add_widget(subtitle)

        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.year = TextInput(text=str(datetime.now().year), multiline=False,
                              input_filter='int', font_size='19sp', halign='center',
                              foreground_color=WHITE, background_color=PANEL,
                              cursor_color=GOLD, size_hint_x=.34)
        self.year.bind(on_text_validate=lambda *_: self.calculate())
        row.add_widget(self.year)
        go = Button(text='CALCULEAZĂ', bold=True, font_size='13sp',
                    background_normal='', background_color=(.19, .42, .65, 1))
        go.bind(on_release=lambda *_: self.calculate())
        row.add_widget(go)
        outer.add_widget(row)

        self.message = responsive_label('', '12sp', GOLD, halign='center')
        self.message.size_hint_y = None
        self.message.height = dp(25)
        outer.add_widget(self.message)

        scroll = ScrollView(do_scroll_x=False)
        self.results = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter('height'))
        scroll.add_widget(self.results)
        outer.add_widget(scroll)

        copy = Button(text='COPIAZĂ REZULTATELE', size_hint_y=None, height=dp(45),
                      font_size='13sp', bold=True, background_normal='',
                      background_color=(.23, .37, .48, 1))
        copy.bind(on_release=lambda *_: self.copy_results())
        outer.add_widget(copy)

        foot = responsive_label(
            'Estimări matematice. Pentru anii istorici, fusul orar și ΔT sunt aproximative.',
            '9sp', MUTED, halign='center')
        foot.size_hint_y = None
        foot.height = dp(39)
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
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(96),
                             padding=[dp(11), dp(7)], spacing=dp(2))
            with card.canvas.before:
                Color(*PANEL)
                rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
            card.bind(pos=lambda w, *_args, r=rect: setattr(r, 'pos', w.pos),
                      size=lambda w, *_args, r=rect: setattr(r, 'size', w.size))
            card.add_widget(responsive_label(title, '13sp', GOLD, bold=True))
            card.add_widget(responsive_label(formatted, '11sp', WHITE))
            card.add_widget(responsive_label(tz, '10sp', MUTED))
            self.results.add_widget(card)
        self.message.text = f'Anul {year} • 4 evenimente'

    def copy_results(self):
        if getattr(self, 'lines', None):
            Clipboard.copy('\n'.join(self.lines) + '\nOre aproximative; fus orar convențional.')
            self.message.text = 'Rezultatele au fost copiate.'


if __name__ == '__main__':
    CalculatorApp().run()

