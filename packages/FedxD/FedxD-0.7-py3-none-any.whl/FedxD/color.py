def rgbcolor(color):
    color_dict = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42),
        'gray': (128, 128, 128),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'lightblue': (173, 216, 230),
        'lime': (0, 255, 0),
        'maroon': (128, 0, 0),
        'navy': (0, 0, 128),
        'olive': (128, 128, 0),
        'teal': (0, 128, 128),
        'violet': (238, 130, 238),
        'silver': (192, 192, 192),
        'gold': (255, 215, 0),
        'skyblue': (135, 206, 235),
        'coral': (255, 127, 80),
        'indigo': (75, 0, 130),
        'lavender': (230, 230, 250),
        'orchid': (218, 112, 214),
        'salmon': (250, 128, 114),
        'tan': (210, 180, 140),
        'aquamarine': (127, 255, 212)
    }
    if color.lower() in color_dict:
        return color_dict[color]
    else:
        raise ValueError('Invalid color')


def hexcolor(color):
    color_to_hex = {
        'black': '#000000',
        'white': '#FFFFFF',
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        'yellow': '#FFFF00',
        'orange': '#FFA500',
        'purple': '#800080',
        'pink': '#FFC0CB',
        'brown': '#A52A2A',
        'gray': '#808080',
        'cyan': '#00FFFF',
        'magenta': '#FF00FF',
        'lightblue': '#ADD8E6',
        'lime': '#00FF00',
        'maroon': '#800000',
        'navy': '#000080',
        'olive': '#808000',
        'teal': '#008080',
        'violet': '#EE82EE',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
        'skyblue': '#87CEEB',
        'coral': '#FF7F50',
        'indigo': '#4B0082',
        'lavender': '#E6E6FA',
        'orchid': '#DA70D6',
        'salmon': '#FA8072',
        'tan': '#D2B48C',
        'aquamarine': '#7FFFD4'
    }
    if color.lower() in color_to_hex:
        return color_to_hex[color]
    else:
        raise ValueError('Invalid color')
