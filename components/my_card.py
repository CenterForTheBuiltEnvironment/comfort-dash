from __future__ import annotations

import dash_mantine_components as dmc


def my_card(children, span: int | dict = 6, title: str = None, id=None):
    content = []
    if title:
        content.append(dmc.Text(title, m="xs", fw=700))
    content.append(children)
    if id is not None:
        return dmc.GridCol(dmc.Paper(children=content), span=span, id=id)
    else:
        return dmc.GridCol(dmc.Paper(children=content), span=span)
