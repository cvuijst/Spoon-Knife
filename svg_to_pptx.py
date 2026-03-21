#!/usr/bin/env python3
"""
Convert SVG org-chart to PowerPoint (single slide).

SVG viewBox : 0 0 680 460
Slide size  : 10 × 6.77 inch  (maintains aspect ratio)
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# ── coordinate mapping ───────────────────────────────────────────────────────
_W_SVG, _H_SVG = 680, 460
_W_EMU = 9_144_000          # 10 inches
_SCALE = _W_EMU / _W_SVG    # ≈ 13 447 EMU per SVG-px


def e(v):
    """SVG px → EMU"""
    return Emu(int(v * _SCALE))


def c(h):
    """Hex string → RGBColor"""
    h = h.lstrip('#')
    return RGBColor(int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16))


# ── presentation ─────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Emu(int(_W_SVG * _SCALE))
prs.slide_height = Emu(int(_H_SVG * _SCALE))

sl = prs.slides.add_slide(prs.slide_layouts[6])   # blank


# ── helpers ──────────────────────────────────────────────────────────────────

def add_rect(x, y, w, h, fill, stroke, dashed=False, no_fill=False):
    """Rounded rectangle (MSO autoshape 5)."""
    sh = sl.shapes.add_shape(5, e(x), e(y), e(w), e(h))
    if no_fill:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = c(fill)
    sh.line.color.rgb = c(stroke)
    sh.line.width     = Pt(0.5)
    if dashed:
        spPr = sh.element.spPr
        ln   = spPr.find(qn('a:ln'))
        if ln is None:
            ln = etree.SubElement(spPr, qn('a:ln'))
        pd = etree.SubElement(ln, qn('a:prstDash'))
        pd.set('val', 'lgDash')
    if sh.has_text_frame:
        sh.text_frame.text = ''
    return sh


def add_label(cx, base_y, text, pt, color,
              bold=False, anchor='middle', box_w=200):
    """
    Floating text box.
    cx     – centre x (anchor='middle') or left x (anchor='start')
    base_y – SVG baseline; shifted up by ~1.15 × font-size to get cap-top
    """
    bh  = pt * 1.6
    lft = cx - box_w / 2 if anchor == 'middle' else cx
    top = base_y - pt * 1.15
    tb  = sl.shapes.add_textbox(e(lft), e(top), e(box_w), e(bh))
    tb.text_frame.word_wrap = False
    p = tb.text_frame.paragraphs[0]
    p.alignment    = PP_ALIGN.CENTER if anchor == 'middle' else PP_ALIGN.LEFT
    p.space_before = Pt(0)
    p.space_after  = Pt(0)
    r = p.add_run()
    r.text           = text
    r.font.size      = Pt(pt)
    r.font.bold      = bold
    r.font.color.rgb = c(color)
    return tb


_AONS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'


def add_line(x1, y1, x2, y2,
             color='888888', dashed=False,
             arrow_end=True, arrow_start=False):
    """Straight connector with optional arrowheads."""
    conn  = sl.shapes.add_connector(1, e(x1), e(y1), e(x2), e(y2))
    w_emu = 12_700   # 1 pt in EMU
    xml   = f'<a:ln {_AONS} w="{w_emu}">'
    xml  += f'<a:solidFill><a:srgbClr val="{color.lstrip("#")}"/></a:solidFill>'
    if dashed:
        xml += '<a:prstDash val="sysDash"/>'
    if arrow_start:
        xml += '<a:headEnd type="arrow" w="med" len="med"/>'
    if arrow_end:
        xml += '<a:tailEnd type="arrow" w="med" len="med"/>'
    xml += '</a:ln>'
    spPr = conn.element.spPr
    for old in spPr.findall(qn('a:ln')):
        spPr.remove(old)
    spPr.append(etree.fromstring(xml))
    return conn


# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 1 – background container
# ══════════════════════════════════════════════════════════════════════════════

add_rect(120, 102, 440, 70, None, 'aaaaaa', dashed=True, no_fill=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 2 – connecting lines
# ══════════════════════════════════════════════════════════════════════════════

# hierarchical (solid grey, arrow at end)
add_line(270,  76,  60, 112)                # Bestuurder → Bestuurssecretaris
add_line(410,  76, 620, 112)                # Bestuurder → Kwaliteitsmedewerker
add_line(340,  76, 340, 102)                # Bestuurder → Stafoverleg

add_line(350, 164, 145, 214)               # BV&ICT → ICT
add_line(350, 164, 295, 214)               # BV&ICT → Facilitair
add_line(350, 164, 445, 214)               # BV&ICT → Roosterbeheer
add_line(350, 164, 560, 214)               # BV&ICT → Fin. admin.

add_line(485, 164, 190, 314)               # M&O → P&O
add_line(485, 164, 395, 314)               # M&O → PR & communicatie
add_line(485, 164, 570, 314)               # M&O → Leerlingadmin.

# functional (dashed blue, arrow at end)
add_line(205, 130, 280,  76, color='3B8BD4', dashed=True)          # Controller → Bestuurder
add_line(205, 164, 205, 236, color='3B8BD4', dashed=True, arrow_end=False)  # ┐ L-path
add_line(205, 236, 513, 236, color='3B8BD4', dashed=True)                   # ┘ → Fin. admin.

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 3 – boxes (filled rectangles)
# ══════════════════════════════════════════════════════════════════════════════

add_rect(260,  34, 160,  42, 'EEEDFE', '534AB7')   # Bestuurder
add_rect( 10, 112, 100,  48, 'F1EFE8', '5F5E5A')   # Bestuurssecretaris
add_rect(570, 112, 100,  48, 'F1EFE8', '5F5E5A')   # Kwaliteitsmedewerker
add_rect(135, 130, 140,  34, 'E1F5EE', '0F6E56')   # Senior controller
add_rect(290, 130, 120,  34, 'FAECE7', '993C1D')   # Stafhoofd BV & ICT
add_rect(425, 130, 120,  34, 'E6F1FB', '185FA5')   # Stafhoofd M & O

add_rect( 85, 214, 110,  42, 'FAECE7', '993C1D')   # ICT
add_rect(225, 214, 110,  42, 'FAECE7', '993C1D')   # Facilitair
add_rect(375, 214, 130,  42, 'FAECE7', '993C1D')   # Roosterbeheer
add_rect(515, 214, 100,  42, 'FAECE7', '993C1D')   # Fin. admin.

add_rect(120, 314, 110,  42, 'E6F1FB', '185FA5')   # P&O
add_rect(310, 314, 150,  42, 'E6F1FB', '185FA5')   # PR & communicatie
add_rect(490, 314, 160,  42, 'E6F1FB', '185FA5')   # Leerlingadmin.

# ══════════════════════════════════════════════════════════════════════════════
#  LAYER 4 – text labels
# ══════════════════════════════════════════════════════════════════════════════

# Title
add_label(340,  18, 'Nieuwe structuur ondersteunende dienst (definitief)',
          12, '1a1a1a', bold=True, box_w=520)

# Bestuurder
add_label(340,  59, 'Bestuurder', 12, '3C3489', bold=True)

# Bestuurssecretaris
add_label( 60, 133, 'Bestuurs-',  11, '444441')
add_label( 60, 148, 'secretaris', 11, '444441')

# Kwaliteitsmedewerker
add_label(620, 133, 'Kwaliteits-', 11, '444441')
add_label(620, 148, 'medewerker',  11, '444441')

# Stafoverleg container label
add_label(340, 117, 'Stafoverleg', 11, '999999')

# Senior controller
add_label(205, 143, 'Senior controller',  11, '085041')
add_label(205, 156, '(nieuw te werven)',  11, '0F6E56')

# Stafhoofd BV & ICT
add_label(350, 143, 'Stafhoofd', 11, '712B13')
add_label(350, 156, 'BV & ICT',  11, '993C1D')

# Stafhoofd M & O
add_label(485, 143, 'Stafhoofd',    11, '0C447C')
add_label(485, 156, 'M & O  \u2605', 11, '185FA5')

# BV & ICT teams
add_label(140, 232, 'ICT',           12, '712B13', bold=True)
add_label(140, 246, '2 mw',          11, '993C1D')
add_label(280, 232, 'Facilitair',    12, '712B13', bold=True)
add_label(280, 246, '1 mw',          11, '993C1D')
add_label(440, 232, 'Roosterbeheer', 12, '712B13', bold=True)
add_label(440, 246, '3 mw',          11, '993C1D')
add_label(565, 232, 'Fin. admin.',   12, '712B13', bold=True)
add_label(565, 246, '1 mw',          11, '993C1D')

# M & O teams
add_label(175, 332, 'P&O',               12, '0C447C', bold=True)
add_label(175, 346, '5 mw',              11, '185FA5')
add_label(385, 338, 'PR & communicatie', 12, '0C447C', bold=True)
add_label(570, 332, 'Leerlingadmin.',    12, '0C447C', bold=True)
add_label(570, 346, '1 mw',              11, '185FA5')

# ══════════════════════════════════════════════════════════════════════════════
#  LEGEND  (bottom of slide)
# ══════════════════════════════════════════════════════════════════════════════

add_line( 40, 404,  80, 404)
add_label( 88, 408, 'Hi\u00ebrarchisch', 11, '666666',
           anchor='start', box_w=160)

add_line(200, 404, 240, 404, color='3B8BD4', dashed=True)
add_label(248, 408, 'Functioneel (inhoudelijke aansturing)', 11, '666666',
          anchor='start', box_w=320)

add_label( 48, 432, '\u2605', 11, 'BA7517', anchor='start', box_w=18)
add_label( 62, 432, 'Co\u00f6rdinator OD (primus inter pares)', 11, '666666',
           anchor='start', box_w=300)

# ══════════════════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════════════════

out = 'org_chart.pptx'
prs.save(out)
print(f'Saved: {out}')
