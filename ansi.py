
# *************************************** Module Constants

CSI = '\033['
DEFAULT_FOREGROUND_COLOR = 7
DEFAULT_BACKGROUND_COLOR = 0
DEFAULT_EFFECT = 0


# *************************************** CSI effect codes
BOLD = 1
DIM = 2
ITALIC = 3
UNDERLINE = 4
REVERSE = 7
STRIKEOUT = 9

SET_DEFAULT_FOREGROUND_COLOR = 49
SET_DEFAULT_BACKGROUND_COLOR = 49

SET_UNDERLINE_COLOR = 58            # requires a color code
DEFAULT_UNDERLINE_COLOR = 59

# *************************************** utilities


def esc(code: int = 0) -> str:
    '''
    Returns the ANSI escape sequence for
    the given 3/4 bit code.

    The default value is 0, which is reset.
    '''
    return f'{CSI}{code}m'


def encode(s: str = "0m") -> str:
    '''
    Returns the ANSI escape sequence for
    the given CSI sequence

    The default value is 0m, which is reset.
    '''
    return f'{CSI}{s}'


typical_ansi_colors = {
    "BLACK": 1,
}


class CLI:
    """ Class CLI provides ansi functionality for command line utilities.


        Common CSI escape codes

        - CSI n A	    CUU	    Cursor Up
            - Moves the cursor n (default 1) cells in the given direction. If the cursor is already at the edge of the screen, this has no effect.
        - CSI n B	    CUD	    Cursor Down
        - CSI n C	    CUF	    Cursor Forward
        - CSI n D	    CUB	    Cursor Back
        - CSI n E	    CNL	    Cursor Next Line
            - Moves cursor to beginning of the line n (default 1) lines down.
        - CSI n F	    CPL	    Cursor Previous Line
            - Moves cursor to beginning of the line n (default 1) lines up.
        - CSI n G	    CHA	    Cursor Horizontal Absolute
            - Moves the cursor to column n (default 1).
        - CSI n ; m H   CUP	    Cursor Position
            - Moves the cursor to row n, column m. The values are 1-based, and default to 1 (top left corner) if omitted. A sequence such as CSI ;5H is a synonym for CSI 1;5H as well as CSI 17;H is the same as CSI 17H and CSI 17;1H
        - CSI n J	    ED	    Erase in Display
            - Clears part of the screen. If n is 0 (or missing), clear from cursor to end of screen. If n is 1, clear from cursor to beginning of the screen. If n is 2, clear entire screen. If n is 3, clear entire screen and delete all lines saved in the scrollback buffer (this feature was added for xterm and is supported by other terminal applications).
        - CSI n K	    EL	    Erase in Line
            - Erases part of the line. If n is 0 (or missing), clear from cursor to the end of the line. If n is 1, clear from cursor to beginning of the line. If n is 2, clear entire line. Cursor position does not change.
        - CSI n S	    SU	    Scroll Up
            - Scroll whole page up by n (default 1) lines. New lines are added at the bottom.
        - CSI n T	    SD	    Scroll Down
            - Scroll whole page down by n (default 1) lines. New lines are added at the top.
        - CSI 6n	    DSR	    Device Status Report
            - Reports the cursor position (CPR) by transmitting ESC[n;mR, where n is the row and m is the column.)

        Reference: https://en.wikipedia.org/wiki/ANSI_escape_code

        """

    default_fg: int
    default_bg: int
    default_effect: int
    fg_col: int
    bg_col: int
    ef_codes: list[int]
    fg_str: str
    bg_str: str

    def __init__(self, fg: int = DEFAULT_FOREGROUND_COLOR, bg: int = DEFAULT_BACKGROUND_COLOR, ef: int = DEFAULT_EFFECT):
        self.default_fg = fg
        self.default_bg = bg
        self.default_effect = ef

    def ToggleEffect(self, ef: int = 0) -> str:
        """
        Toggle an effect code on or off.

        e.g. If the current text is bold(1) and italic(3), toggling bold
        will remove the bold effect and leave only the italic effect.
        """
        if ef in self.ef_codes:
            # remove effect from list of effects
            self.ef_codes.remove(ef)
        else:
            # add effect to list of effects
            self.ef_codes.append(ef)
        retval: str = CSI
        for effect in self.ef_codes:
            retval += f'{effect};'
        retval += 'm'
        return retval

    def Title(self, t: str = "") -> str:
        '{CSI}0;{t}{}'

    def Default(self) -> str:           # Reset foreground and background colors to default
        return f'{CSI}39;49;m'

    def Reset(self) -> str:             # Reset all colors and effects to default
        return f'{CSI}0m'

    def fg8(self, n=0) -> str:
        """
        Assign an 8-bit (256 color) ANSI foreground color.

        - ESC[38;5;⟨n⟩m Select foreground color
        - 0-  7:  standard colors (as in ESC [ 30–37 m)
        - 8- 15:  high intensity colors (as in ESC [ 90–97 m)
        - 16-231:  6 × 6 × 6 cube (216 colors): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
        - 232-255:  grayscale from black to white in 24 steps
        """
        return f'{CSI}38;5;{n}m'

    def bg8(self, n=0) -> str:
        """
        Assign an 8-bit (256 color) ANSI background color.

        - ESC[48;5;⟨n⟩m Select background color
        - 0-  7:  standard colors (as in ESC [ 40–47 m)
        - 8- 15:  high intensity colors (as in ESC [ 100–107 m)
        - 16-231:  6 × 6 × 6 cube (216 colors): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
        - 232-255:  grayscale from black to white in 24 steps
        """
        return f'{CSI}48;5;{n}m'

    def fg24(self, r=255, g=255, b=255) -> str:
        """
        Assign an 24-bit ("true" color) ANSI foreground color.

        ESC[ 38;2;⟨r⟩;⟨g⟩;⟨b⟩ m Select RGB foreground color
        """
        return f'{CSI}38;2;{r};{g};{b}m'

    def bg24(self, r=0, g=0, b=0) -> str:
        """
        Assign an 24-bit ("true" color) ANSI background color.

        ESC[ 48;2;⟨r⟩;⟨g⟩;⟨b⟩ m Select RGB background color
        """
        return f'{CSI}48;2;{r};{g};{b}m'

    def Up(self, n=1) -> str:           # Cursor Up
        """
        Move.

        """
        return f'{CSI}{n}A'

    def Down(self, n=1) -> str:         # Cursor Down
        return f'{CSI}{n}B'

    def Right(self, n=1) -> str:        # Cursor Forward
        return f'{CSI}{n}C'

    def Left(self, n=1) -> str:         # Cursor Back
        return f'{CSI}{n}D'

    def Next(self, n=1) -> str:         # Cursor Next Line
        return f'{CSI}{n}E'

    def Prev(self, n=1) -> str:         # Cursor Previous Line
        return f'{CSI}{n}F'

    def Horizontal(self, n=1) -> str:   # Cursor Horizontal Absolute
        return f'{CSI}{n}G'

    def Pos(self, n=1, m=1) -> str:     # Cursor Position
        return f'{CSI}{n};{m}H'

    def Erase(self, n=1) -> str:        # Erase in Display
        return f'{CSI}{n}J'

    def DelLine(self, n=1) -> str:      # Erase in Line
        return f'{CSI}{n}K'

    def ScrollUp(self, n=1) -> str:     # Scroll Up
        return f'{CSI}{n}S'

    def ScrollDown(self, n=1) -> str:   # Scroll Down
        return f'{CSI}{n}T'

    def DSR(self) -> str:               # Device Status Report
        return f'{CSI}6r'


class CLI4bit(CLI):

    def fg(self, color=9, effect=0) -> str:
        """ Assign a 3/4-bit (16 color) ANSI foreground color.

            Color Codes:
            ---
            - 0	    Black
            - 1	    Red
            - 2	    Green
            - 3	    Yellow
            - 4	    Blue
            - 5	    Magenta
            - 6	    Cyan
            - 7	    White

            - 9     Default color

            Examples of the use of effects (color,effect):
            ---
            - 1,1   Bright (BOLD) Red
            - 2,2   Dim Green
            - 3,3   Italic Yellow
            - 4,4   Underlined Blue
            - 5,7   Reverse Magenta
            - 6,9   Strikeout Cyan
            - 7,1   Bright White
            """
        if color < 0 or color > 9:
            return ""
        if fg_col == fg:
            return fg_str
        if not effect:          # prevent reset when no effect is specified
            self.fg_str = encode(f'3{color}m')
        else:
            self.fg_str = encode(f'{effect};3{color}m')
        return self.fg_str

    def bg(self, c=49, effect=0) -> str:
        """ Assign a 3/4-bit (16 color) ANSI background color.

            Color Codes:
            ---
            - 0	    Black
            - 1	    Red
            - 2	    Green
            - 3	    Yellow
            - 4	    Blue
            - 5	    Magenta
            - 6	    Cyan
            - 7	    White

            - 9     Default color

            Examples of the use of effects (color,effect):
            ---
            - 1,1   Bright (BOLD) Red
            - 2,2   Dim Green
            - 3,3   Italic Yellow
            - 4,4   Underlined Blue
            - 5,7   Reverse Magenta
            - 6,9   Strikeout Cyan
            - 7,1   Bright White
            """
        if c < 40 or c > 49:
            return ""
        if not effect:          # prevent reset when no effect is specified
            return f'{CSI}{c}m'
        return f'{CSI}{effect}{c}m'


SGR_parameter_codes: dict[str, str] = {

}
"""
SGR Parameter Codes - Select Graphic Rendition (SGR) sets display attributes.
Several attributes can be set in the same sequence, separated by semicolons.
Each display attribute remains in effect until a following occurrence of SGR
resets it. If no codes are given, CSI m is treated as CSI 0 m (reset / normal).

0	Reset or normal	All attributes off
1	Bold or increased intensity	As with faint, the color change is a PC (SCO / CGA) invention.
2	Faint, decreased intensity, or dim	May be implemented as a light font weight like bold.
3	Italic	Not widely supported. Sometimes treated as inverse or blink.
4	Underline	Style extensions exist for Kitty, VTE, mintty and iTerm2.
5	Slow blink	Sets blinking to less than 150 times per minute
6	Rapid blink	MS-DOS ANSI.SYS, 150+ per minute; not widely supported
7	Reverse video or invert	Swap foreground and background colors; inconsistent emulation
8	Conceal or hide	Not widely supported.
9	Crossed-out, or strike	Characters legible but marked as if for deletion.
10	Primary (default) font
11–19	Alternative font	Select alternative font n − 10
20	Fraktur (Gothic)	Rarely supported
21	Doubly underlined; or: not bold	Double-underline per ECMA-48,: 8.3.117  but instead disables bold intensity on several terminals, including in the Linux kernel's console before version 4.17.[33]
22	Normal intensity	Neither bold nor faint; color changes where intensity is implemented as such.
23	Neither italic, nor blackletter
24	Not underlined	Neither singly nor doubly underlined
25	Not blinking	Turn blinking off
26	Proportional spacing	ITU T.61 and T.416, not known to be used on terminals
27	Not reversed
28	Reveal	Not concealed
29	Not crossed out
30–37	Set foreground color
38	Set foreground color	Next arguments are 5;n or 2;r;g;b
39	Default foreground color	Implementation defined (according to standard)
40–47	Set background color
48	Set background color	Next arguments are 5;n or 2;r;g;b
49	Default background color	Implementation defined (according to standard)
50	Disable proportional spacing	T.61 and T.416
51	Framed	Implemented as "emoji variation selector" in mintty.[34]
52	Encircled
53	Overlined
54	Neither framed nor encircled
55	Not overlined
58	Set underline color	Not in standard; implemented in Kitty, VTE, mintty, and iTerm2.[30][31] Next arguments are 5;n or 2;r;g;b.
59	Default underline color	Not in standard; implemented in Kitty, VTE, mintty, and iTerm2.[30][31]
"""

popular_control_codes = {
    "BEL":     7,
    "BS":      8,
    "HT":      9,
    "LF":      0x0A,
    "FF":      0x0C,
    "CR":      0x0D,
}
"""
Popular Control Codes:

- 7	        BEL     ^G	    Bell	            Makes an audible noise.
- 8	        BS      ^H	    Backspace	        Moves the cursor left (but may "backwards wrap" if cursor is at start of line).
- 9	        HT      ^I	    Tab	                Moves the cursor right to next multiple of 8.
- 0x0A	    LF      ^J	    Line Feed	        Moves to next line, scrolls the display up if at bottom of the screen.
- 0x0C	    FF      ^L	    Form Feed	        Move a printer to top of next page.
- 0x0D	    CR      ^M	    Carriage            Return	Moves the cursor to column zero.
- 0x1B	    ESC     ^[	    Escape	            Starts all the escape sequences

Reference: https://en.wikipedia.org/wiki/ANSI_escape_code
"""
