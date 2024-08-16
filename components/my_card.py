import dash_mantine_components as dmc


def my_card(children, span: int | dict = 6, title: str = None):
    content = []
    if title:
        content.append(dmc.Text(title, mb="xs", fw=700))
    content.append(children)
    return dmc.GridCol(
        dmc.Paper(children=content, shadow="xs", p="xs"),
        span=span,
    )
