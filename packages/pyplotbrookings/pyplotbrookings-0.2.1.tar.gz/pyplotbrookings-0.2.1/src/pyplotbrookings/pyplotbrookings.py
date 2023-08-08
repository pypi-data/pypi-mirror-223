from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.colors 
from matplotlib import font_manager
import numpy as np
import os

_palettes = {
        # Categorical
        '1-color A': ['#003A70'],
        '1-color B': ['#0061A0'],
        '2-color A': ('#003A70', '#FF9E1B'),
        '2-color B': ('#003A70', '#8BB8E8'),
        '3-color A': ('#003A70', '#FF9E1B', '#8BB8E8'),
        '3-color B': ('#003A70', '#FF9E1B', '#B1B3B3'),
        '4-color A': ('#003A70', '#FF9E1B', '#8BB8E8', '#F2CD00'),
        '4-color B': ('#003A70', '#FF9E1B', '#8BB8E8', '#B1B3B3'),
        '5-color': ('#003A70', '#FF9E1B', '#8BB8E8', '#F2CD00', '#B1B3B3'),
        '6-color': ('#003A70', '#FF9E1B', '#8BB8E8', '#F2CD00', '#EF6A00', '#B1B3B3'),
                
        'sequential (single hue)': ('#00649f', '#0f78ba', '#1c8ad6',  '#2e97ea', '#56adf6', '#87c4fe', '#bcdefb'),
        'sequential (two hues)' : ('#00649f', '#2a7a8b', '#559077', '#80a662', '#aabd4e', '#d4d33a', '#ffe926'),
        'diverging': ('#ed3a35', '#ee7673', '#eeb3b1', '#efefef', '#adc9e2', '#6aa4d6', '#287ec9'),
        'vivid blue palette': ('#023147', '#0061A0', '#287EC9', '#66ACED', '#CAE1FA'),
        'orange palette': ('#EF6A00', '#FF851A', '#FF9E1B', '#FFB24D', '#FEC87F'),
        'paired': ('#003A70', '#326295', '#EF6A00', '#FF9E1B', '#418FDE', '#8BB8E8', '#E0BB00', '#FFDD00', '#949494', '#B1B3B3'),
        
        # Additional palettes
        'pos-neg A': ('#5CA632', '#CD1A1C'),
        'pos-neg B': ('#5CA632', '#F5CC00', '#CD1A1C'),
        
        '2-political A': ('#ed3a35', '#287ec9'),
        '2-political B': ('#ee7673', '#6aa4d6'),
        '3-political A': ('#ed3a35', '#287ec9', '#f2cd00'),
        '3-political B': ('#ee7673', '#6aa4d6', '#f1d850'),
        
        # Extended palettes
        'brand blue': ('#022A4E', '#003A70', '#1A4E80', '#326295', '#517EAD', '#7098C3', '#8DADD0', '#A8BDD5', '#DDE5ED'),
        'vivid blue': ('#023147', '#004B6E', '#0061A0', '#1372BA', '#287EC9', '#418FDE', '#66ACED', '#8BB8E8', '#CAE1FA'),
        'teal': ('#032B30', '#09484F', '#116470', '#1C8090', '#2A9AAD', '#3EB2C6', '#59C6DA', '#7CD9EA', '#A6E9F5'),
        'green': ('#1A3404', '#294D0A', '#33660F', '#45821B', '#5CA632', '#7DBF52', '#9CD674', '#BDED9D', '#DEF5CC'),
        'yellow': ('#594C09', '#877414', '#C7A70A', '#E0BB00', '#F2CD00', '#FFDD00', '#FFE926', '#FFF170', '#FFF9C2'),
        'orange': ('#663205', '#994B08', '#B85B0A', '#EF6A00', '#FF851A', '#FF9E1B', '#FFB24D', '#FEC87F', '#FBD9A5'),
        'red': ('#660507', '#A00D11', '#CD1A1C', '#E22827', '#ED3A35', '#F75C57', '#F98B83', '#FCB0AA', '#FDD7D4'),
        'magenta': ('#510831', '#8D1655', '#A82168', '#BF317B', '#D2468E', '#E160A2', '#EC81B7', '#F5A8CF', '#FAD4E7'),
        'purple': ('#3E2C72', '#533C91', '#6A50AD', '#7C60BF', '#8E72D0', '#9C82D9', '#B59DEA', '#D0BEF5', '#E9E0FC'),
        'gray': ('#191919', '#404040', '#666666', '#757575', '#949494', '#B1B3B3', '#CCCCCC', '#E6E6E6', '#F2F2F2'),
    }

def set_theme(font_size=12, line_width=1.4, font_family='Helvetica', 
              background_color='transparent'):
    '''
    Sets matplotlib default style parameters to be consistent with
    the Brookings style. 

    font_size (float): A number specifying the base font size of all 
        default plots

    line_width (float): A number specifying the default thickness of all
        lines in plots
        
    font_family (str): The font family for figures (either Helvetica or Roboto)

    background_color (str): The background color of the plot, specified as
        a named color string (e.g., 'white') or hexcode (e.g., '#FFFFFF').
        Defaults to a transparent plot background.
    '''
    # Reset matplotlib style parameters to the defaults
    mpl.rcdefaults()
    
    # Should the background plot be transparent
    transparent = (background_color == 'transparent')
    background_color = 'white' if transparent else background_color

    # Setting up Helvetica font
    cwd = os.path.join(os.path.dirname(__file__), 'fonts')
    font_files = font_manager.findSystemFonts(fontpaths=cwd, fontext="ttf")

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    # Dictionary of style features to set
    style_dict = {
        'axes.axisbelow': True,  # Place gride lines behind the plot
        'axes.facecolor': background_color,
        'figure.facecolor': background_color,

        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.labelsize': 0.833*font_size,
        'axes.labelweight': 'bold',
        'axes.linewidth': line_width,
        'axes.spines.left': False,
        'axes.spines.right': False,
        'axes.spines.top': False,
        
        # Setting label color to Gray 90
        'text.color': '#191919',
        'axes.labelcolor': '#191919',
        'xtick.color': '#191919',
        'ytick.color': '#191919',
        
        # Set default palettes
        'axes.prop_cycle': mpl.cycler(color=get_palette('6-color')),
        'image.cmap': get_cmap('sequential (two hues)'),

        'figure.figsize': (6, 4),
        'font.size': font_size,
        'font.family': font_family, 

        'grid.color': '#CCCCCC',
        'grid.linestyle': (0, (1, 4)),

        'legend.loc': 'upper center',
        'legend.frameon': False,  # Remove legend border
        'legend.handlelength': 0.75,  # Shorten size of legend key
        'legend.borderaxespad': -1,  # Place legend outside the figure
        'legend.fontsize': 0.833*font_size,

        'patch.linewidth': 0,

        'ytick.left': False,
        'ytick.labelsize': 0.833*font_size,
        'xtick.labelsize': 0.833*font_size,
        
        'savefig.transparent': transparent,
    }
    # Apply all styles
    for key, value in style_dict.items():
        mpl.rcParams[key] = value


def get_palette(name, list_supported=False):
    '''
    Given a palette name returns a tuple of hexcolor
    palette colors

    name (str): The palette name.

    list_supported (bool): If true list all supported palette 
        names (see below).

    Complete list of valid palette names:
        '1-color A', '1-color B', '2-color A', '2-color B', '3-color A', '3-color B', '4-color A',
        '4-color B', '5-color', '6-color', 'sequential (single hue)', 'sequential (two hues)', 'diverging', 
        'pos-neg A', 'pos-neg B', '2-political A', '2-political B', '3-political A', '3-political B', 
        'brand blue', 'vivid blue', 'teal', 'green', 'yellow', 'orange', 'red', 'magenta', 'purple', 'gray'
    '''    
    supported_palettes = list(_palettes.keys())

    # Return all palette names if 
    if list_supported:
        return supported_palettes
    
    if name not in supported_palettes:
        raise Exception(
            f'"{name}" is not a valid color palette. \
                Try one of the following: {supported_palettes}')
    
    return _palettes[name]


def get_color(name):
    '''
    Returns the hexcolor value of a named Brookings color
    
    name (str): The name of the Brookings color 
                (e.g., 'brookings blue' or 'yellow 50')
    '''
    # Cleaning string
    name = name.lower()
    
    # Checking for named colors
    if name == 'brookings blue':
        return '#003A70'
    
    if name == 'cool gray':
        return '#B1B3B3'
    
    # Accessing color from color palettes
    else:
        color = ' '.join(name.split(' ')[0:-1])
        # Converting string number to index
        value = int((int(name.split(' ')[-1]) / -10) + 9)
        
        return get_palette(color)[value]
    
    
def make_palette(colors, n, name):
    '''
    Given a list of colors and number of segments, creates a multi-hue 
    sequential palette of n colors.
    
    colors (array): A list like object of colors to be used for the color palette
    
    n (int): Number of colors in the final palette (n > len(colors))
    
    name (str): Name of the palette (for access later on)
    '''
    # Interpolating between listed colors
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", colors, N=n)
    palette = tuple([mpl.colors.to_hex(cmap(i)) for i in range(n)])
    
    # Adding the named palette
    _palettes[name] = palette
    

def add_title(title=None, subtitle=None, tag=None, v_pad=0, h_pad=0, text_pad=0):
    '''
    Adds titles to the current figure.

    title (str): The title of the plot. Title should be short

    subtitle (str): The subtitle of the plot. Subtitle can be longer and
         add description to the figure 

    tag (str): The figure name/number plotted above the titles

    v_pad (float): Vertical padding, a number specifying additional amount of 
        spacing to add between the top of the figure and the first title.

    h_pad (float): Horizontal padding, the amount of additional space to offset 
        the title text in the x direction.

    text_pad (float): Number specifying additional amount of spacing to add
        between lines of text.
    '''
    # Get the font size
    font_size = mpl.rcParams['font.size']
    # Set starting y coords
    x = get_coords('left') + h_pad/100
    y = get_coords('top') + v_pad/100
    # Font size to pad
    text_pad = (0.47 + text_pad/100) * font_size
    
    # Add some blank space padding
    plt.figtext(x, y, ' ', size=text_pad+4*text_pad)   

    if subtitle:
        y = get_coords('top')
        plt.figtext(x, y, subtitle, size=0.833*font_size, wrap=True)
        # Increment next titles vertical offset if text was added
        y = get_coords('top')
        plt.figtext(x, y, ' ', size=1.5*text_pad)
        
    if title:    
        y = get_coords('top')
        plt.figtext(x, y, title,
                    size=font_size, weight='bold', wrap=True)
        y = get_coords('top')
        plt.figtext(x, y, ' ', size=2*font_size)

    if tag:
        y = get_coords('top')
        right = get_coords('right') - x
        # Adding the tag in a seprate subplot 
        # Figure annotations can be finicky so a new subplot is easiest way to add them   
        ax = plt.gcf().add_axes([x, y, right, 0.01], zorder=1)
        
        
        ax.set_ylim(0.9, 1.5)
        # Adding the tag and line at the top of the figure
        ax.annotate(tag + '   ', xytext=(0, 1.25), xy=(1, 1.5), 
                    fontsize=0.75*font_size, weight="light", color='#666666',
                    arrowprops=dict(arrowstyle="-", linewidth=0.5, color='#666666'))
        
        # Turning off axis so only text is displayed
        ax.axis('off')


def add_notes(*args, v_pad=-5, h_pad=0, text_pad=0):
    '''
    Adds footnotes to the current figure.

    *args (str): String arguments containing text to place at the bottom of 
        the figure. Any text before the first colon will be bolded.

    v_pad (float): Vertical padding, a number specifying additional amount of
        spacing to add between the bottom of the figure and the first note.

    h_pad (float): Horizontal padding, the amount of additional space to offset 
        the notes text in the x direction.

    text_pad (float): Number specifying additional amount of spacing to add
        between lines of text.
    '''
    # Get the font size
    font_size = mpl.rcParams['font.size']  

    # Set starting y coords
    x = get_coords('left') + h_pad/100
    y = get_coords('bottom') + v_pad/100
    # Pad font size
    text_pad = (2 + text_pad/100) * font_size

    for text in args:
        # Add some blank space padding
        plt.figtext(x, y, ' ', size=text_pad)
        
        # Decrease y value
        y = get_coords('bottom')
        
        # If there is a colon, bold the text prior to the colon
        if ":" in text:
            bold_text = text.split(":")[0] + ":"
            text = ":".join(text.split(":")[1:])
        else:
            bold_text = ''

        # Add any bold text to the beginning of the footnote text
        txt = plt.figtext(x, y,
                    bold_text, size=0.75*font_size, color="#666666", weight='bold', va='top')
        
        # If there are line feeds, add this extra text below the first line
        if '\n' in text:
            # Extra paragraphs of text
            extra_text = '\n'+'\n'.join(text.splitlines()[1:])
            # Main text is now just the first line
            text = text.splitlines()[0]
            plt.figtext(x, y,
                    extra_text, size=0.75*font_size, color="#666666", va='top')
        
        # off set in x direction from bold text on first line
        x_off = get_coords('right', obj=txt)
        # Add the non bold text to the bottom of the figure
        plt.figtext(x_off, y,
                    text, size=0.75*font_size, color="#666666", va='top')

        # Increment the offset for the next set of text
        y = get_coords('bottom')


def add_logo(logo_path, offsets=(0, 0), scale=0.25, list_supported=False):
    '''
    Adds a logo to the bottom right of a figure

    logo_path (str): Path to a local file path or an abbreviation for one
         of the package supported logos (see documentation below for more 
         details on supported logos)

    offsets (tuple): Tuple with the X, Y offsets for a figure (in fraction 
        of the figure size)

    scale (float): Scale factor to set the logo size

    list_supported (bool): If true return a list of all valid logo 
        abbreviations (see below)

    Complete list of supported logos abbreviations:
        bc: Brown Center
        bi: Bass Initiative on Innovation and Placemaking
        brookings: Brookings Institution
        cc: China Center
        ccf: Center on Children and Families
        ceaps: Center for East Asia Policy Studies
        cepm: Center for Effective Policy Management 
        chp: Center for Health Policy
        cmep: Center for Middle Eastern Policy
        crm: Center on Regulation and Markets
        csd: Center for Sustainable Development
        cti: Center for Technology Innovation
        cue: Center for Universal Education
        cuse: Center on United States and Europe
        es: Economic Studies 
        fp: Foreign Policy
        global: Global Studies 
        gs: Governance Studies
        hc: Hutchins Center
        metro: Metropolitan Policy Studies
        thp: The Hamilton Project
    '''
    # List of supported logos
    supported_logos = ["bc", "bi", "brookings", "cc", "ccf", "ceaps", "cepm", "chp", "cmep", "crm", "csd",
                       "cti", "cue", "cuse", "es", "fp", "global", "gs", "hc", "metro", "thp"]
    
    if list_supported:
        return supported_logos

    # Set up the subplot coordinates
    dx, dy = offsets
    font_size = mpl.rcParams['font.size']
    # Map of logo position names to coordinates
    logo_loc = [0.65+dx, -0.12+dy-font_size*0.006, scale, 0.2]

    # Updating string to directory path if using a supported logo
    if logo_path in supported_logos:
        path = os.path.join(os.path.dirname(__file__), 'logos')
        logo_path = os.path.join(path, logo_path + '.png')

    try:
        # Read the image
        logo = mpimg.imread(logo_path)

    except FileNotFoundError:
        # Throw error listing valid logo names
        raise Exception(f'No such file or directory: " {logo_path}. Check your \
                        path or try one of the following: {supported_logos}')

    # Get current figure
    fig = plt.gcf()
    # Add an axis for the logo plot
    ax = fig.add_axes(logo_loc, zorder=1)

    # Add logo to new axis and turn off axis labeling
    ax.imshow(logo, cmap='viridis')
    ax.axis('off')


def get_cmap(name, reverse=False, **kargs):
    '''
    Given a palette name returns a Brookings theme colormap. 
    Note not all palettes (e.g., brand 1) should be used as colormaps.

    name (str): Name of the color map from either the color palette or 
        extended color palette.

    reverse (bool): If the color map should be reversed
    '''
    colors = get_palette(name)

    # Reverse colors if needed
    if reverse:
        colors = colors[::-1]

    # Return a color map over the list of colors
    return mpl.colors.LinearSegmentedColormap.from_list("", colors, **kargs)


def set_palette(name, ax=None, reverse=False):
    '''
    Sets the a color palette cycler for the current axis

    name (str): Name of the Brookings color palette

    ax: Optional matplotlib axis object to specify which axis to apply 
        the color palette to

    reverse (bool): If the color palette should be reversed
    '''
    palette = get_palette(name)
    # Reverse the palette if specified
    if reverse:
            palette = palette[::-1]

    # Get current axis if not specified
    if not ax:
        ax = plt.gca()

    # Create a cycler for the selected color palette
    palette_cycler = cycler(color=palette)
    # Set the cycler as base for the current/given axis
    ax.set_prop_cycle(palette_cycler)


def view_palette(name):
    '''
    Given a color palette (base or extended) creates a preview of the palette
    '''

    def text_color(hexcolor):
        '''
        Returns recommended color of text (either black or white) 
        to use with the given hexcolor as a background color. Color
        selection is adherent to W3C guidelines. 
        
        hexcolor (str): String of a hexidecimal color
        
        @Source: Mark Ransom (https://stackoverflow.com/questions/3942878/
        how-to-decide-font-color-in-white-or-black-depending-on-background-color)
        '''
        # Convert hexcolor code to RGB
        rgb_color = list(int(hexcolor[i:i+2], 16) for i in (1, 3, 5))
        
        # Adjusting RGB values
        rgb_new = []
        for c in rgb_color:
            c = c / 255.0
            if c <= 0.04045:
                c = c/12.92 
            else:
                c = ((c+0.055)/1.055) ** 2.4
            rgb_new.append(c)
        # Getting color luminosity
        L = 0.2126 * rgb_new[0] + 0.7152 * rgb_new[1] + 0.0722 * rgb_new[2]
        
        # Return black or white depending on color luminosity
        return '#000000' if L > 0.179 else '#FFFFFF'

    # All valid color maps
    palette = get_palette(name)
    
    # Cast color to an array
    palette = np.array(palette)
    
    # Number of columns in the final figure 
    cols = int(np.ceil(len(palette)/2))
    
    # Reshape the data into a 2D image
    data = np.arange(2*cols).reshape(2, cols)
    
    # Append white "squares" to the end of the color map 
    palette_extended = np.append(palette, np.repeat('#FFFFFF', len(palette) % 2))
    
    # Create a color map
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", palette_extended)
    # Plot the image
    plt.imshow(data, cmap=cmap)
    
    # Counter for the order of the colors
    k = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            
            # If the palette is white breakout of labeling the colors
            if k >= len(palette):
                break

            # Get the correct text color
            color = text_color(palette[k])

            # Plot text on top of the palette color with the correct color
            # showing the hexcode and palette order number
            plt.text(j, i, str(k + 1) + '\n' + palette[k].upper(),
                           ha="center", va="center", color=color)
            # Increase the counter
            k += 1
    
    plt.axis('off')
    plt.show()


def figure(size, **kwargs):
    '''
    Create a figure using one of the standard Brookings sizes (small, medium, or large).
    Keyword arguments can be passed to pyplots plt.figure() function.
    '''
    if type(size) is str:
        sizes = {'small': (3.25, 2), 'medium':(6.5, 4), 'large':(9, 6.5)}

        # If name is invalid throw an error
        if size not in sizes.keys():
            raise Exception("Size must be one of 'small', 'medium', or 'large'")

        size = sizes[size]

    return plt.figure(figsize=sizes, **kwargs)


def save(filename, dpi=None, **kwargs):
    '''
    Save a plot using standard Brookings DPI values (retina, print, screen)
    Keyword arguments can be passed to pyplots plt.savefig() function.
    '''
    if not dpi:
        dpi = 'figure'

    elif type(dpi) is str:
        dpi_dict = {"retina": 320, "print": 300, "screen": 72}

        # If name is invalid throw an error
        if dpi not in dpi_dict.keys():
            raise Exception("DPI must be one of 'retina', 'print', or 'screen'")

        dpi = dpi_dict[dpi]
    
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', **kwargs)


def get_coords(loc, obj=None):
    '''
    Helper function for getting plot coordinates
    '''
    fig = plt.gcf()
    # If passed an object get its coords
    if obj is None:
        bbox = fig.get_tightbbox(fig.canvas.get_renderer())
        coords = fig.transFigure.inverted().transform(bbox)*100
    # Otherwise get the figure coords
    else:
        bbox = obj.get_tightbbox(fig.canvas.get_renderer())
        coords = fig.transFigure.inverted().transform(bbox)
    
    return {'left': coords[0, 0], 'right': coords[1, 0], 'bottom': coords[0, 1], 'top': coords[1, 1]}[loc]
