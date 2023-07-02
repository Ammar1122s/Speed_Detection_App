from flet import *

def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = MainAxisAlignment.CENTER

    txt_number = TextField(value="0", text_align=TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click),
            ],
            alignment=MainAxisAlignment.CENTER,
        )
    )

app(target=main)


