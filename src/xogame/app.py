"""
X-O O'yini
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from random import randrange


class XOGame(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.size = (400, 500)

        # Main container
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

        # Score display
        score_box = toga.Box(style=Pack(direction=ROW, padding=10))
        self.yzv1 = toga.Label(
            "Siz: 0", style=Pack(font_size=12, flex=1, text_align="left")
        )
        self.ntj = toga.Label("", style=Pack(font_size=12, flex=1, text_align="center"))
        self.yzv2 = toga.Label(
            "Kompyuter: 0", style=Pack(font_size=12, flex=1, text_align="right")
        )
        score_box.add(self.yzv1)
        score_box.add(self.ntj)
        score_box.add(self.yzv2)

        # Grid layout for buttons
        self.grid_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.x_o = []
        self.tkshr = [True] * 9

        for i in range(3):
            row_box = toga.Box(style=Pack(direction=ROW))
            for j in range(3):
                btn = toga.Button(
                    "",
                    on_press=self.uyinchi,
                    style=Pack(
                        width=75, height=75, background_color="lightblue", font_size=18
                    ),
                )
                row_box.add(btn)
                self.x_o.append(btn)
            self.grid_box.add(row_box)

        # Reset button
        self.rst = toga.Button(
            "Reset",
            on_press=self.tozala,
            style=Pack(width=75, height=55, background_color="orange", font_size=12),
        )

        main_box.add(score_box)
        main_box.add(self.grid_box)
        main_box.add(self.rst)

        self.main_window.content = main_box
        self.main_window.show()

        self.uynlar = 0
        self.odam = 0
        self.komp = 0
        self.ind_olsh = self.indexniOlish()

    def tbOlish(self, lst: list) -> list[list]:
        blgs1 = [list(bls) for bls in zip(lst[0], lst[1], lst[2])]
        blgs2 = [[lst[i][i] for i in range(3)], [lst[i][-(i + 1)] for i in range(3)]]
        return [*blgs1, *blgs2]

    def tugrlabOlish(self) -> list[list]:
        blgs1 = [
            [btn.text for btn in self.x_o[:3]],
            [btn.text for btn in self.x_o[3:6]],
            [btn.text for btn in self.x_o[6:]],
        ]
        return [*blgs1, *self.tbOlish(blgs1)]

    def indexniOlish(self) -> list[list]:
        blgs1 = [list(range(3)), list(range(3, 6)), list(range(6, 9))]
        return [*blgs1, *self.tbOlish(blgs1)]

    def yutgan(self, blg: str) -> bool:
        for bls in self.tugrlabOlish():
            if bls.count(blg) == 3:
                return True
        return False

    def durrang(self) -> bool:
        return "" not in [btn.text for btn in self.x_o]

    def blokla(self, text: str, rang: str) -> None:
        self.ntj.text = text
        self.ntj.style.update(color=rang)
        self.yzv1.text = f"Siz: {self.odam}"
        self.yzv2.text = f"Kompyuter: {self.komp}"
        for i in range(9):
            self.tkshr[i] = False
        self.uynlar += 1
        if self.uynlar == 100:
            self.uynlar = 0

    def xavfYokiYutuq(self, blg: str) -> tuple[bool, int]:
        for bls, ins in zip(self.tugrlabOlish(), self.ind_olsh):
            if "" in bls and bls.count(blg) == 2:
                return True, ins[bls.index("")]
        return False, 0

    def kompyuter(self) -> None:
        if True in self.tkshr:
            tksh, t_ind = self.xavfYokiYutuq("o")
            if tksh:
                ind = t_ind
            else:
                tksh, t_ind = self.xavfYokiYutuq("x")
                if tksh:
                    ind = t_ind
                else:
                    while True:
                        ind = randrange(0, 9)
                        if self.tkshr[ind]:
                            break
            self.x_o[ind].text = "o"
            self.tkshr[ind] = False
            if self.yutgan("o"):
                self.komp += 1
                self.blokla("Siz yutqazdingiz", "red")
            elif self.durrang():
                self.blokla("Durrang", "orange")

    def uyinchi(self, widget) -> None:
        ind = self.x_o.index(widget)
        if self.tkshr[ind]:
            self.x_o[ind].text = "x"
            self.tkshr[ind] = False
            if self.yutgan("x"):
                self.odam += 1
                self.blokla("Siz yutdingiz", "lightgreen")
            elif self.durrang():
                self.blokla("Durrang", "orange")
            else:
                self.kompyuter()

    def tozala(self, widget) -> None:
        for i in range(9):
            self.x_o[i].text = ""
            self.tkshr[i] = True
        self.ntj.text = ""
        if self.uynlar % 2 != 0:
            self.kompyuter()


def main():
    return XOGame()
