import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

palette = [
    ('text_background', 'black', 'light gray'),
    ('rowbar', 'black', 'dark red'),
    ('background', 'black', 'dark blue'),]

# Specify the line of text
txt = urwid.Text(('text_background', u" E L E C T R O N A U T  C O M P A N Y "), align='center')
txt2 = urwid.Text(('text_background', u" MAY THIS WILL WORK "), align='center')


# Map the 'rowbar' color attributes to the line of text
map1 = urwid.AttrMap(txt, 'rowbar')
map1b = urwid.AttrMap(txt2, 'rowbar')


# Apply map1 to the filler
fill = urwid.Filler(map1)
fillb = urwid.Filler(map1b)


# Map the 'background' color attributes to the fill
map2 = urwid.AttrMap(fill, 'background')
map2b = urwid.AttrMap(fillb, 'background')


loop = urwid.MainLoop(map2b, palette, unhandled_input=exit_on_q)
loop.run()