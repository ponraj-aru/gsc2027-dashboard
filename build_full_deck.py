import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Academic & Clean Palette
    NAVY_DARK = RGBColor(15, 23, 42)        # #0F172A
    NAVY_CARD = RGBColor(30, 41, 59)        # #1E293B
    WHITE = RGBColor(255, 255, 255)
    OFF_WHITE = RGBColor(248, 250, 252)     # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_GRAY = RGBColor(226, 232, 240)   # #E2E8F0
    TEXT_MAIN = RGBColor(15, 23, 42)        # #0F172A
    TEXT_MUTED = RGBColor(100, 116, 139)    # #64748B
    TEXT_LIGHT = RGBColor(148, 163, 184)   # #94A3B8
    BLUE_ACCENT = RGBColor(37, 99, 235)     # #2563EB
    TEAL_ACCENT = RGBColor(13, 148, 136)    # #0D9488
    PURPLE_ACCENT = RGBColor(124, 58, 237)  # #7C3AED
    GREEN_ACCENT = RGBColor(5, 150, 105)    # #059669
    AMBER_ACCENT = RGBColor(217, 119, 6)    # #D97706
    CYAN_ACCENT = RGBColor(2, 132, 199)     # #0284C7

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_GRAY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    def add_header(slide, title_text, category_text="GRONINGEN SUSTAINABILITY CONFERENCE 2027", is_dark=False):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(56, 189, 248) if is_dark else BLUE_ACCENT
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE if is_dark else TEXT_MAIN
        p_title.space_before = Pt(3)

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Academic Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, NAVY_DARK)

    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(0.12), Inches(4.8))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = RGBColor(56, 189, 248)
    accent_bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_badge = tf1.paragraphs[0]
    p_badge.text = "OFFICIAL SCIENTIFIC COMMITTEE ANALYTICAL REPORT"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(56, 189, 248)

    p_main = tf1.add_paragraph()
    p_main.text = "Groningen Sustainability Conference 2027"
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Comprehensive Abstract Submissions, Thematic Landscape & Global Country Mapping"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(186, 230, 253)
    p_sub.space_before = Pt(10)

    p_desc = tf1.add_paragraph()
    p_desc.text = "Rigorous empirical analysis of 301 conference submissions across 66 primary nations • Sequential Thematic Deep-Dives (Themes 1 to 5) • Discrete Global Mapping & Abstract Lexical Clusters"
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = TEXT_LIGHT
    p_desc.space_before = Pt(14)

    stat_items = [
        ("301", "Total Abstracts", RGBColor(56, 189, 248)),
        ("66", "Primary Nations", RGBColor(129, 140, 248)),
        ("5", "Core Themes", RGBColor(52, 211, 153)),
        ("246", "Oral Presentations", RGBColor(251, 191, 36))
    ]
    card_w = Inches(2.7)
    card_gap = Inches(0.25)
    start_x = Inches(1.2)
    start_y = Inches(4.7)

    for i, (val, lbl, color) in enumerate(stat_items):
        cx = start_x + i * (card_w + card_gap)
        c_shape = add_card(s1, cx, start_y, card_w, Inches(1.4), bg_color=NAVY_CARD, border_color=RGBColor(51, 65, 85))
        
        tb_card = s1.shapes.add_textbox(cx + Inches(0.2), start_y + Inches(0.2), card_w - Inches(0.4), Inches(1.0))
        tfc = tb_card.text_frame
        tfc.word_wrap = True
        tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0
        
        p1 = tfc.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = color
        
        p2 = tfc.add_paragraph()
        p2.text = lbl.upper()
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(2)

    tb_foot = s1.shapes.add_textbox(Inches(1.2), Inches(6.5), Inches(11.0), Inches(0.5))
    tb_foot.text_frame.word_wrap = True
    tb_foot.text_frame.margin_left = tb_foot.text_frame.margin_top = 0
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.text = "University of Groningen, Netherlands • Data Source: ConfTool Pro Export (adminPapersBrowse) • October 2026"
    p_foot.font.size = Pt(10)
    p_foot.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Executive Dashboard (Clean Light)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, OFF_WHITE)
    add_header(s2, "Executive Overview: Core Submission Metrics at a Glance", "EXECUTIVE DASHBOARD")

    kpi_cards = [
        ("301", "Total Submissions", "100% processed dataset", BLUE_ACCENT),
        ("66", "Primary Countries", "75 participating in total", TEAL_ACCENT),
        ("5", "Core Themes", "Sequential 1 to 5 tracks", AMBER_ACCENT),
        ("25", "Subtopics Covered", "Extensive interdisciplinary range", PURPLE_ACCENT),
        ("81.7%", "Oral Presentations", "246 individual talks requested", GREEN_ACCENT)
    ]
    k_width = Inches(2.2)
    k_gap = Inches(0.18)
    for i, (val, title, subtitle, color) in enumerate(kpi_cards):
        kx = Inches(0.8) + i * (k_width + k_gap)
        add_card(s2, kx, Inches(1.6), k_width, Inches(1.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        tb = s2.shapes.add_textbox(kx + Inches(0.15), Inches(1.72), k_width - Inches(0.3), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(2)
        
        p3 = tf.add_paragraph()
        p3.text = subtitle
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

    pillars = [
        ("Geographic Breadth & Inclusivity", [
            ("Unprecedented Global Reach: ", "Submissions received from 66 primary countries across all 6 inhabited continents."),
            ("Global South Leadership: ", "Over 58% of all abstracts originate from Asia and Africa, led by India, China, Indonesia, Nepal, Ghana, and South Africa."),
            ("Strong European Anchor: ", "The host country Netherlands (26), Germany (20), UK (14), and Belgium (7) represent major scholarly leadership.")
        ], TEAL_ACCENT),
        ("Sequential Thematic Balance", [
            ("Theme 1 (SDGs Beyond 2030): ", "60 abstracts (19.9%), focused heavily on SDG localization, multi-stakeholder governance, and post-2030 indicator systems."),
            ("Theme 2 (Resilience Across Systems): ", "76 abstracts (25.2%), the largest track in the conference, anchored by the Food-Water-Energy nexus and circular economy."),
            ("Theme 3 (Climate Nexus): ", "75 abstracts (24.9%), highlighting climate adaptation, governance, finance, and equitable net-zero transitions."),
            ("Theme 4 (Health) & Theme 5 (AI): ", "45 abstracts each (15.0% each), providing human health foundations and digital enablement tools.")
        ], BLUE_ACCENT),
        ("Session Architecture & Planning", [
            ("Massive Oral Demand: ", "246 abstracts (81.7%) request Oral Presentations, requiring robust multi-parallel track scheduling (4-5 concurrent tracks)."),
            ("Targeted Poster Track: ", "40 submissions (13.3%) designated for Poster Presentations across interactive exhibition areas."),
            ("High-Impact Panels: ", "15 curated sessions (8 Innovative Sessions and 7 Full Panel Sessions) proposed by premier research networks and consortia.")
        ], PURPLE_ACCENT)
    ]

    p_width = Inches(3.78)
    p_gap = Inches(0.18)
    for i, (p_title, bullets, acc_color) in enumerate(pillars):
        px = Inches(0.8) + i * (p_width + p_gap)
        add_card(s2, px, Inches(3.1), p_width, Inches(3.9), bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.2), Inches(3.3), Inches(0.08), Inches(0.35))
        strip.fill.solid()
        strip.fill.fore_color.rgb = acc_color
        strip.line.fill.background()
        
        tb = s2.shapes.add_textbox(px + Inches(0.35), Inches(3.28), p_width - Inches(0.5), Inches(0.45))
        tb.text_frame.word_wrap = True
        tb.text_frame.margin_left = tb.text_frame.margin_top = 0
        p = tb.text_frame.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        
        tb_b = s2.shapes.add_textbox(px + Inches(0.25), Inches(3.8), p_width - Inches(0.5), Inches(3.0))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = 0
        
        for j, (lead, body) in enumerate(bullets):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = "• "
            p.font.size = Pt(10)
            p.font.color.rgb = acc_color
            
            run_lead = p.add_run()
            run_lead.text = lead
            run_lead.font.bold = True
            run_lead.font.size = Pt(9.5)
            run_lead.font.color.rgb = TEXT_MAIN
            
            run_body = p.add_run()
            run_body.text = body
            run_body.font.size = Pt(9)
            run_body.font.color.rgb = TEXT_MUTED
            
            if j > 0:
                p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: Global Geographic Reach (Embedded World Map)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, OFF_WHITE)
    add_header(s3, "Global Geographic Footprint: 66 Primary Submitting Nations", "GEOGRAPHIC REACH")

    if os.path.exists('visuals/map_global.png'):
        s3.shapes.add_picture('visuals/map_global.png', Inches(0.8), Inches(1.5), Inches(8.3), Inches(4.7))

    add_card(s3, Inches(9.3), Inches(1.5), Inches(3.2), Inches(5.4), bg_color=CARD_BG, border_color=BORDER_GRAY)
    
    tb = s3.shapes.add_textbox(Inches(9.5), Inches(1.7), Inches(2.8), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Global Distribution Highlights"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    geo_points = [
        ("Host Nation Leading: ", "Netherlands leads with 26 submissions (43 including international co-authorships)."),
        ("Global South Strength: ", "India (26), China (23), Indonesia (16), Nepal (15), Ghana (13), and South Africa (12) demonstrate high research activity."),
        ("Broad African Engagement: ", "15 African countries submitted abstracts, reflecting intense interest in climate resilience and just transitions."),
        ("Multi-Country Consortia: ", "Over 75 countries participate when including international co-authors and panel speakers."),
        ("Discrete HTML Map: ", "Interactive browser map includes discrete binned legends and dynamic theme filters.")
    ]
    
    for lead, text in geo_points:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(10)
        p.font.color.rgb = BLUE_ACCENT
        p.space_before = Pt(8)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    tb_c = s3.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(8.3), Inches(0.6))
    tb_c.text_frame.word_wrap = True
    tb_c.text_frame.margin_left = tb_c.text_frame.margin_top = 0
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "Distribution of 301 abstracts across 66 primary submitting countries. Natural Earth projection."
    p_c.font.size = Pt(9.5)
    p_c.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Regional Analysis & Top Participating Nations
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, OFF_WHITE)
    add_header(s4, "Regional Breakdown & Top Contributing Nations Leaderboard", "GEOGRAPHIC ANALYSIS")

    if os.path.exists('visuals/chart_top_countries.png'):
        s4.shapes.add_picture('visuals/chart_top_countries.png', Inches(0.8), Inches(1.5), Inches(6.0), Inches(4.3))

    if os.path.exists('visuals/chart_regional.png'):
        s4.shapes.add_picture('visuals/chart_regional.png', Inches(7.0), Inches(1.5), Inches(5.5), Inches(4.3))

    reg_cards = [
        ("Asia: 107 Submissions (35.5%)", "India (26), China (23), Indonesia (16), Nepal (15), Bangladesh (7), Pakistan (7). Strong focus on agrarian adaptation, WEF nexus, and twin transition.", TEAL_ACCENT),
        ("Europe: 88 Submissions (29.2%)", "Netherlands (26), Germany (20), UK (14), Belgium (7), Italy (5), Spain (4). Centered on post-2030 governance, circular economy modeling, and planetary boundaries.", BLUE_ACCENT),
        ("Africa: 69 Submissions (22.9%)", "Ghana (13), South Africa (12), Nigeria (9), Morocco (6), Kenya (4). Critical focus on climate justice, Loss & Damage, health equity, and rural resilience.", AMBER_ACCENT)
    ]
    rc_w = Inches(3.78)
    rc_gap = Inches(0.18)
    for i, (rtitle, rdesc, rcol) in enumerate(reg_cards):
        rx = Inches(0.8) + i * (rc_w + rc_gap)
        add_card(s4, rx, Inches(5.9), rc_w, Inches(1.15), bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        tb = s4.shapes.add_textbox(rx + Inches(0.15), Inches(5.98), rc_w - Inches(0.3), Inches(0.98))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        
        p = tf.paragraphs[0]
        p.text = rtitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = rcol
        
        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: Overall Thematic Landscape (Strict 1 -> 5 Order)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, OFF_WHITE)
    add_header(s5, "Thematic Distribution: Across 5 Core Pillars (Theme 1 to 5)", "THEMATIC LANDSCAPE")

    if os.path.exists('visuals/chart_themes.png'):
        s5.shapes.add_picture('visuals/chart_themes.png', Inches(0.8), Inches(1.5), Inches(6.0), Inches(4.3))

    table_shape = s5.shapes.add_table(6, 4, Inches(7.0), Inches(1.5), Inches(5.5), Inches(4.3))
    table = table_shape.table
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(0.8)
    table.columns[3].width = Inches(1.0)

    t_headers = ["Theme", "Focus Description", "Papers", "Share (%)"]
    for col_idx, h_text in enumerate(t_headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.LEFT if col_idx < 2 else PP_ALIGN.RIGHT

    theme_rows_ordered = [
        ("Theme 1", "Lessons from SDGs Beyond 2030", "60", "19.9%"),
        ("Theme 2", "Building Resilience Across Systems", "76", "25.2%"),
        ("Theme 3", "Climate Change–Development Nexus", "75", "24.9%"),
        ("Theme 4", "Health, Well-being & Social Foundations", "45", "15.0%"),
        ("Theme 5", "AI, Big Data & Digitalization", "45", "15.0%")
    ]

    for row_idx, rdata in enumerate(theme_rows_ordered, start=1):
        for col_idx, val in enumerate(rdata):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = (col_idx == 0 or col_idx == 2)
            p.font.color.rgb = TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT if col_idx < 2 else PP_ALIGN.RIGHT

    add_card(s5, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s5.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "KEY THEMATIC TAKEAWAYS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Themes 1 through 5 provide an integrated systemic continuum from post-2030 governance (Theme 1), natural-human resilience (Theme 2), and climate justice (Theme 3) to health equity (Theme 4) and digital enablers (Theme 5).\n• Themes 2 and 3 represent 50.1% of all submissions, highlighting immense research interest in resource resilience and climate action."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: Presentation Formats Breakdown & Scheduling
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, OFF_WHITE)
    add_header(s6, "Presentation Formats & Session Architecture", "PROGRAM SCHEDULING")

    if os.path.exists('visuals/chart_formats.png'):
        s6.shapes.add_picture('visuals/chart_formats.png', Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.3))

    fmt_details = [
        ("Oral Presentations", "246 Submissions (81.7%)", "Requires approximately 40 to 45 standard oral sessions (5-6 papers per 90-minute session). Suggest scheduling across 4 parallel thematic tracks over 3 full conference days.", BLUE_ACCENT),
        ("Poster Presentations", "40 Submissions (13.3%)", "Ideal for two dedicated interactive poster reception slots. Posters cluster around empirical fieldwork in Themes 1, 2, and 3, plus pilot models in AI and health analytics.", GREEN_ACCENT),
        ("Innovative Sessions", "8 Submissions (2.7%)", "Interactive workshops, co-design labs, and policy dialogues (e.g. decarbonization co-design, nature relationship index, participatory stakeholder modeling). High engagement value.", AMBER_ACCENT),
        ("Full Panel Sessions", "7 Submissions (2.3%)", "Curated multi-institutional expert panels (e.g. EU-China modeling consortium, water-energy-food governance, open data for SDG 6, regenerative supply chains). Prime plenary candidates.", PURPLE_ACCENT)
    ]

    card_y = Inches(1.5)
    c_h = Inches(1.0)
    c_gap = Inches(0.12)
    for i, (title, sub, desc, col) in enumerate(fmt_details):
        cy = card_y + i * (c_h + c_gap)
        add_card(s6, Inches(6.8), cy, Inches(5.7), c_h, bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        st = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), cy + Inches(0.12), Inches(0.08), c_h - Inches(0.24))
        st.fill.solid()
        st.fill.fore_color.rgb = col
        st.line.fill.background()
        
        tb = s6.shapes.add_textbox(Inches(7.1), cy + Inches(0.08), Inches(5.3), c_h - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        
        p = tf.paragraphs[0]
        p.text = f"{title} • "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        
        r = p.add_run()
        r.text = sub
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = col
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(2)

    add_card(s6, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_rec = s6.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True
    tf_rec.margin_left = tf_rec.margin_top = 0
    p = tf_rec.paragraphs[0]
    p.text = "PROGRAM COMMITTEE RECOMMENDATION"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    p2 = tf_rec.add_paragraph()
    p2.text = "• Designate 4 continuous parallel oral presentation streams (Stream A: Climate Nexus; Stream B: Integrated Resilience; Stream C: SDGs Beyond 2030; Stream D: Digital & Health).\n• Schedule the 15 special panel and innovative sessions in non-overlapping 90-minute prime conference blocks to maximize cross-disciplinary attendance."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 7: Theme 1 Deep-Dive (Strict Order: 1 First!)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, OFF_WHITE)
    add_header(s7, "Theme 1 Deep-Dive: Lessons from SDGs for Sustainable Development Beyond 2030", "THEME 1 ANALYSIS")

    if os.path.exists('visuals/wordcloud_theme1.png'):
        s7.shapes.add_picture('visuals/wordcloud_theme1.png', Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.3))

    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Theme 1 Metrics & Subtopics Breakdown"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    
    t1_details = [
        ("Volume & Representation: ", "60 Submissions (19.9% of conference). 46 Oral, 11 Posters, 3 Innovative Sessions. Contributing countries led by Netherlands (9), India (5), UK (4), Nepal (3), Spain (3)."),
        ("1.1 National & Local SDG Implementation (25 papers, 41.7%): ", "The heaviest subtopic, analyzing institutional barriers, municipal Voluntary Local Reviews (VLRs), and grassroots community alignment."),
        ("1.5 Methods & Processes for Post-2030 (11 papers, 18.3%): ", "Proposals for next-generation indicator frameworks, dynamic targets, and participatory foresight methodologies beyond the 2030 horizon."),
        ("1.2 SDG Governance & Partnerships (9 papers, 15.0%): ", "Multi-stakeholder partnerships, public-private pacts, and accountability structures."),
        ("1.4 Missing Links & Post-2030 Reforms (9 papers, 15.0%): ", "Critiques of current SDG gaps: planetary boundaries, indigenous sovereignty, and degrowth."),
        ("1.3 Integrated SDG Progress Assessment (6 papers, 10.0%): ", "Cross-goal trade-offs, spillover indices, and quantitative evaluation tools.")
    ]
    
    for lead, text in t1_details:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9)
        p.font.color.rgb = AMBER_ACCENT
        p.space_before = Pt(3)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s7, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s7.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "THEME 1 ABSTRACT WORD CLUSTER & TOP KEYWORDS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Top Abstract Words: development (152), sustainable (124), sustainability (91), environmental (61), local (59), institutional (55), sdgs (53), policy (51), goals (50), governance (49), implementation (47).\n• Key Author Keywords: sustainable development goals (11), sdgs (5), post-2030 agenda (5), sdg localization (4), sdg implementation (3), msmes (2)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 8: Theme 2 Deep-Dive (Strict Order: 2 Second!)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, OFF_WHITE)
    add_header(s8, "Theme 2 Deep-Dive: Building Resilience across Natural & Human Systems", "THEME 2 ANALYSIS")

    if os.path.exists('visuals/wordcloud_theme2.png'):
        s8.shapes.add_picture('visuals/wordcloud_theme2.png', Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.3))

    add_card(s8, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Theme 2 Metrics & Subtopics Breakdown"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    
    t2_details = [
        ("Volume & Dominance: ", "76 Submissions (25.2% of entire conference) — the LARGEST single theme! 68 Oral, 3 Posters, 4 Panels, 1 Innovative Session. Top countries: China (12), Belgium (5), Nepal (5), India (5), Germany (5)."),
        ("2.1 Food-Water-Energy Nexus (31 papers, 40.8%): ", "The largest single subtopic across the conference! Focuses on agricultural food systems, watershed governance, clean energy access, and resource interdependencies."),
        ("2.5 Beyond GDP & Circularity (15 papers, 19.7%): ", "Circular economy models, regenerative supply chains, industrial symbiosis, and bioeconomy innovations."),
        ("2.3 Roles of Equity & Justice (14 papers, 18.4%): ", "Environmental justice, indigenous land stewardship, social vulnerability, and community resilience."),
        ("2.2 Landscapes & Seascapes (10 papers, 13.2%): ", "Ecosystem service valuations, coastal mangrove restoration, marine biodiversity conservation."),
        ("2.4 Urban Transformation & Mobility (6 papers, 7.9%): ", "Low-carbon urban transit, resilient urban planning, and infrastructure retrofitting.")
    ]
    
    for lead, text in t2_details:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9)
        p.font.color.rgb = GREEN_ACCENT
        p.space_before = Pt(3)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s8, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s8.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "THEME 2 ABSTRACT WORD CLUSTER & TOP KEYWORDS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Top Abstract Words: water (95), environmental (92), food (91), energy (89), sustainable (91), resilience (63), local (62), climate (61), circular (54), agricultural (52), ecosystem (49).\n• Key Author Keywords: community resilience (6), food system transformation (5), equity (4), social equity (4), sustainable resource management (4), business models (4), biodiversity (4)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 9: Theme 3 Spotlight & Overview (Strict Order: 3 Third!)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, OFF_WHITE)
    add_header(s9, "Theme 3 Deep-Dive: Navigating the Climate Change–Development Nexus", "THEME 3 SPOTLIGHT")

    if os.path.exists('visuals/chart_theme3_subtopics.png'):
        s9.shapes.add_picture('visuals/chart_theme3_subtopics.png', Inches(0.8), Inches(1.5), Inches(6.2), Inches(4.3))

    add_card(s9, Inches(7.2), Inches(1.5), Inches(5.3), Inches(4.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
    
    tb = s9.shapes.add_textbox(Inches(7.4), Inches(1.65), Inches(4.9), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Theme 3 Structure & Subtopics"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACCENT
    
    p_lead = tf.add_paragraph()
    p_lead.text = "Theme 3 captures the intersection of climate action and equitable human progress. 75 abstracts make it the 2nd largest track, covering 5 distinct subtopics:"
    p_lead.font.size = Pt(9.5)
    p_lead.font.color.rgb = TEXT_MUTED
    p_lead.space_before = Pt(3)
    
    t3_bullets = [
        ("3.2 Actions for Climate Adaptation (23 papers, 30.7%): ", "Focuses on building societal resilience, grassroots agricultural adaptations, and nature-based solutions."),
        ("3.5 Climate Governance & Finance (22 papers, 29.3%): ", "Examines international negotiations, carbon pricing, Article 6, Loss & Damage funds, and multi-level climate policies."),
        ("3.3 Mitigation & Net-Zero Pathways (16 papers, 21.3%): ", "Explores renewable transitions, industrial decarbonization, and socially just phase-out of fossil fuels."),
        ("3.4 Climate Actions for Human Security (9 papers, 12.0%): ", "Addresses climate migration, conflict vulnerabilities, displacement, and livelihood security."),
        ("3.1 Earth System Modeling & Impacts (5 papers, 6.7%): ", "Quantitative climate forecasting, tipping point analytics, and localized socio-ecological impact simulations.")
    ]
    
    for lead, text in t3_bullets:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9.5)
        p.font.color.rgb = PURPLE_ACCENT
        p.space_before = Pt(4)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    t3_kpis = [
        ("75", "Submissions (24.9%)"),
        ("28", "Contributing Nations"),
        ("57", "Oral Presentations"),
        ("13", "Poster Presentations"),
        ("5", "Special Sessions (3 Inn, 2 Pan)")
    ]
    tw = Inches(2.2)
    tg = Inches(0.18)
    for i, (v, l) in enumerate(t3_kpis):
        tx = Inches(0.8) + i * (tw + tg)
        add_card(s9, tx, Inches(6.0), tw, Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        tb = s9.shapes.add_textbox(tx + Inches(0.1), Inches(6.08), tw - Inches(0.2), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        
        p = tf.paragraphs[0]
        p.text = v
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = PURPLE_ACCENT
        
        p2 = tf.add_paragraph()
        p2.text = l
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Theme 3 Geographic Reach & Abstract Word Cluster
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, OFF_WHITE)
    add_header(s10, "Theme 3 Global Geography & Abstract Word Cluster", "THEME 3 ANALYSIS")

    if os.path.exists('visuals/map_theme3.png'):
        s10.shapes.add_picture('visuals/map_theme3.png', Inches(0.8), Inches(1.5), Inches(6.2), Inches(4.3))

    if os.path.exists('visuals/wordcloud_theme3.png'):
        s10.shapes.add_picture('visuals/wordcloud_theme3.png', Inches(7.2), Inches(1.5), Inches(5.3), Inches(4.3))

    add_card(s10, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s10.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "THEME 3 GEOGRAPHIC & LEXICAL SUMMARY"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = PURPLE_ACCENT
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Top Contributing Nations (28 total): India (9), Netherlands (7), Germany (7), Nepal (5), United Kingdom (5), Bangladesh (5), South Africa (5), Nigeria (3), Ghana (3), USA (3), China (3).\n• Top Abstract Words: climate (219), development (102), policy (65), sustainable (64), adaptation (57), governance (48), resilience (45), just transition (5), climate justice (4)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 11: Theme 4 Deep-Dive (Strict Order: 4 Fourth!)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11, OFF_WHITE)
    add_header(s11, "Theme 4 Deep-Dive: Health, Well-being, and Societal Foundations", "THEME 4 ANALYSIS")

    if os.path.exists('visuals/wordcloud_theme4.png'):
        s11.shapes.add_picture('visuals/wordcloud_theme4.png', Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.3))

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb = s11.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Theme 4 Metrics & Subtopics Breakdown"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(124, 58, 237)
    
    t4_details = [
        ("Volume & Geographic Diversity: ", "45 Submissions (15.0% of conference). 39 Oral, 6 Posters. High participation from Global South: India (6), Ghana (6), Indonesia (5), Nigeria (5), Germany (3)."),
        ("4.4 Health Equity & Societal Outcomes (21 papers, 46.7%): ", "The core anchor of Theme 4! Evaluates inner development, mental health, gender disparities, social determinants, and community well-being."),
        ("4.5 Health as Outcome & Driver of Sustainability (9 papers, 20.0%): ", "Economic productivity linkages, universal health coverage (UHC), and social foundation resilience."),
        ("4.3 Solutions & Innovations for Healthier Societies (8 papers, 17.8%): ", "Community-based healthcare interventions, digital health tools, and indigenous medical practices."),
        ("4.2 Environmental Health & Exposure Science (5 papers, 11.1%): ", "Air pollution exposure (e.g. Max Planck Mainz particulate analysis), microplastics, chemical toxins."),
        ("4.1 One Health Nexus & Ecological Ceilings (2 papers, 4.4%): ", "Zoonotic disease emergence, animal-human-ecosystem health integration.")
    ]
    
    for lead, text in t4_details:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(124, 58, 237)
        p.space_before = Pt(3)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s11, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s11.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "THEME 4 ABSTRACT WORD CLUSTER & TOP KEYWORDS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(124, 58, 237)
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Top Abstract Words: health (133), well-being (47), social (41), environmental (39), climate (36), urban (34), exposure (27), access (26), healthcare (25), community (24), mental (21).\n• Key Author Keywords: sustainable development (3), well-being (3), climate change (3), nigeria (3), air pollution (2), india (2), child health (2), sdg 3 (2)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 12: Theme 5 Deep-Dive (Strict Order: 5 Fifth!)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12, OFF_WHITE)
    add_header(s12, "Theme 5 Deep-Dive: AI, Big Data & Digitalization as Enablers", "THEME 5 ANALYSIS")

    if os.path.exists('visuals/wordcloud_theme5.png'):
        s12.shapes.add_picture('visuals/wordcloud_theme5.png', Inches(0.8), Inches(1.5), Inches(5.8), Inches(4.3))

    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb = s12.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p = tf.paragraphs[0]
    p.text = "Theme 5 Metrics & Subtopics Breakdown"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    t5_details = [
        ("Volume & Frontier Scope: ", "45 Submissions (15.0% of conference). 36 Oral, 7 Posters, 1 Panel, 1 Innovative Session. Top contributing nations: Netherlands (5), Germany (4), Kenya (4), Indonesia (3), China (3)."),
        ("5.5 AI & Digitalization by/beyond 2030 (21 papers, 46.7%): ", "The flagship subtopic exploring macro-level digital transformation, sustainable smart cities, and AI in SDG achievement."),
        ("5.2 Twin Transition (Green + Digital) (9 papers, 20.0%): ", "Investigating how digitalization and green transition intersect, rebound effects, and energy consumption of data infrastructure."),
        ("5.1 AI Methods & Analytics (6 papers, 13.3%): ", "Machine learning algorithms, remote sensing earth observation, and satellite data analytics for ecological monitoring."),
        ("5.4 Trustworthy AI & Governance (5 papers, 11.1%): ", "Algorithmic bias in sustainability policy, digital public goods, data sovereignty, and ethical AI safeguards."),
        ("5.3 AI Tools for Decision-Making (4 papers, 8.9%): ", "Decision-support systems for municipal resource allocation and disaster management.")
    ]
    
    for lead, text in t5_details:
        p = tf.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9)
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(3)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s12, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.05), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_bot = s12.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.3), Inches(0.9))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = 0
    p = tf_bot.paragraphs[0]
    p.text = "THEME 5 ABSTRACT WORD CLUSTER & TOP KEYWORDS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    p2 = tf_bot.add_paragraph()
    p2.text = "• Top Abstract Words: digital (94), development (74), sustainable (67), governance (47), systems (41), climate (40), intelligence (33), analytics (31), technologies (30), earth observation (24).\n• Key Author Keywords: artificial intelligence (9), sustainable development (6), digitalization (5), big data (4), responsible innovation (4), data governance (3)."
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 13: Cross-Thematic Synergy & Comparative Matrix
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13, OFF_WHITE)
    add_header(s13, "Cross-Thematic Synergies & Thematic Intersection Matrix", "CROSS-CUTTING ANALYSIS")

    t_shape = s13.shapes.add_table(6, 6, Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.6))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.3)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.1)
    tbl.columns[3].width = Inches(2.7)
    tbl.columns[4].width = Inches(2.8)
    tbl.columns[5].width = Inches(2.8)

    hdrs = ["Theme", "Papers", "Countries", "Top Subtopic", "Dominant Word Cluster", "Cross-Theme Synergy"]
    for c_i, h in enumerate(hdrs):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    matrix_rows = [
        ("Theme 1 (SDGs)", "60 (19.9%)", "20", "1.1 SDG Local Implementation (25)", "development, institutional, localization, governance", "Feeds governance frameworks into Themes 2 & 3"),
        ("Theme 2 (Resilience)", "76 (25.2%)", "22", "2.1 Food-Water-Energy Nexus (31)", "water, food, energy, circular, biodiversity", "Supplies ecological baselines for Health (T4) & Climate (T3)"),
        ("Theme 3 (Climate)", "75 (24.9%)", "28", "3.2 Climate Adaptation (23)", "climate, adaptation, policy, just transition", "Intersects with AI analytics (T5) & Human Security (T4)"),
        ("Theme 4 (Health)", "45 (15.0%)", "18", "4.4 Health Equity & Well-being (21)", "health, well-being, exposure, urban, equity", "Bridges pollution data with climate extreme impacts"),
        ("Theme 5 (AI/Digital)", "45 (15.0%)", "19", "5.5 AI by/beyond 2030 (21)", "digital, intelligence, systems, twin transition", "Enables data monitoring across ALL themes (1, 2, 3, 4)")
    ]

    for r_i, rvals in enumerate(matrix_rows, start=1):
        for c_i, val in enumerate(rvals):
            cell = tbl.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = (c_i <= 1)
            p.font.color.rgb = TEXT_MAIN

    add_card(s13, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.75), bg_color=CARD_BG, border_color=BORDER_GRAY)
    tb_syn = s13.shapes.add_textbox(Inches(1.0), Inches(5.42), Inches(11.3), Inches(1.5))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True
    tf_syn.margin_left = tf_syn.margin_top = 0
    p = tf_syn.paragraphs[0]
    p.text = "STRATEGIC CROSS-THEMATIC CONVERGENCES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    syn_bullets = [
        ("The 'Twin Transition' Interface: ", "Strong natural convergence between Theme 3 (Climate mitigation) and Theme 5 (AI & big data), specifically in digital carbon accounting, satellite earth observation, and smart grid optimization."),
        ("The Ecological Health Nexus: ", "Theme 2 (Water/Food) and Theme 4 (Health) share critical empirical ground regarding agricultural pesticides, clean water access, and urban microclimates."),
        ("Justice & Just Transition as the Universal Thread: ", "Social equity is prominently featured in Theme 1 (indigenous voices), Theme 2 (fair resource allocation), and Theme 3 (just transition in coal/fossil regions).")
    ]
    
    for lead, text in syn_bullets:
        p = tf_syn.add_paragraph()
        p.text = "• "
        p.font.size = Pt(9.5)
        p.font.color.rgb = BLUE_ACCENT
        p.space_before = Pt(3)
        
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = TEXT_MAIN
        
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 14: Strategic Conference Planning & Scheduling Guidance
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14, OFF_WHITE)
    add_header(s14, "Actionable Conference Planning & Track Allocation Guidance", "PROGRAM RECOMMENDATIONS")

    recs = [
        ("Track Allocation & Parallel Rooms", [
            ("Establish 4 Dedicated Parallel Streams: ", "Stream A (Climate Nexus), Stream B (Natural-Human Systems), Stream C (SDGs & Governance), Stream D (AI & Health)."),
            ("Room Sizing by Volume: ", "Allocate the largest auditorium facilities to Theme 2 (76 papers) and Theme 3 (75 papers) which will draw peak delegate interest."),
            ("Session Granularity: ", "Plan approximately 45 oral sessions with 5-6 papers each (15 min presentation + Q&A).")
        ], BLUE_ACCENT),
        ("Poster Sessions & Exhibition", [
            ("Thematic Clustering of 40 Posters: ", "Cluster posters into 4 thematic islands matching the main conference pillars."),
            ("Two Dedicated Unopposed Poster Slots: ", "Schedule two 60-minute reception slots (e.g., late afternoon Day 1 and Day 2) with refreshments to guarantee high delegate interaction."),
            ("Rapid Poster Pitch Competition: ", "Provide 60-second lightning pitches for early-career scholars prior to the poster session.")
        ], GREEN_ACCENT),
        ("Curated Panels & Interactive Labs", [
            ("Elevate 15 Special Sessions: ", "The 7 Full Panels and 8 Innovative Sessions involve multi-institutional consortia (e.g. EU-China, SDSN, Jagiellonian, CAS, Max Planck)."),
            ("Semi-Plenary Positioning: ", "Schedule panels in prominent mid-morning slots to anchor plenary debates and foster cross-theme dialogue."),
            ("Workshop Co-Design Rooms: ", "Equip innovative session rooms with flexible round-table seating rather than standard theater style.")
        ], PURPLE_ACCENT)
    ]

    rw = Inches(3.78)
    rg = Inches(0.18)
    for i, (rtitle, rbullets, rcol) in enumerate(recs):
        rx = Inches(0.8) + i * (rw + rg)
        add_card(s14, rx, Inches(1.5), rw, Inches(5.4), bg_color=CARD_BG, border_color=BORDER_GRAY)
        
        cbar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, rx + Inches(0.2), Inches(1.7), Inches(0.08), Inches(0.4))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = rcol
        cbar.line.fill.background()
        
        tb = s14.shapes.add_textbox(rx + Inches(0.35), Inches(1.68), rw - Inches(0.5), Inches(0.5))
        tb.text_frame.word_wrap = True
        tb.text_frame.margin_left = tb.text_frame.margin_top = 0
        p = tb.text_frame.paragraphs[0]
        p.text = rtitle
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        
        tb_b = s14.shapes.add_textbox(rx + Inches(0.2), Inches(2.3), rw - Inches(0.4), Inches(4.4))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = 0
        
        for j, (lead, body) in enumerate(rbullets):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = "• "
            p.font.size = Pt(10)
            p.font.color.rgb = rcol
            p.space_before = Pt(10) if j > 0 else Pt(0)
            
            r1 = p.add_run()
            r1.text = lead
            r1.font.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = TEXT_MAIN
            
            r2 = p.add_run()
            r2.text = body
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 15: Closing & Deliverables Index (Dark Academic Navy)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15, NAVY_DARK)
    add_header(s15, "Analytical Package & Deliverables Summary", "CONCLUSION & RESOURCES", is_dark=True)

    deliv_items = [
        ("PowerPoint Report (PPTX)", "GSC2027_Abstract_Submissions_Analysis_Report.pptx", "15 comprehensive widescreen slides featuring discrete maps, sequential thematic deep-dives (Themes 1 to 5), and scheduling recommendations.", RGBColor(56, 189, 248)),
        ("Interactive World Map Dashboard (HTML)", "gsc2027_interactive_world_map.html", "Clean white academic dashboard with discrete binned map tiers, dynamic theme selector (Strict 1 to 5), pie charts, word clusters, and sortable table.", RGBColor(129, 140, 248)),
        ("Master Submissions Database (Excel & CSV)", "GSC2027_Abstract_Submissions_Master.xlsx / .csv", "Complete cleaned dataset of all 301 abstracts with ID, title, author lists, organizations, verified country, subtopic codes, keywords, and text.", RGBColor(52, 211, 153)),
        ("High-Res Visual Assets Suite", "visuals/ directory (13 High-DPI Assets)", "Includes global and Theme 3 choropleth maps, theme distribution charts, subtopic bars, format breakdowns, and 6 specialized NLP word clouds.", RGBColor(251, 191, 36))
    ]

    card_y = Inches(1.5)
    c_h = Inches(1.1)
    c_gap = Inches(0.18)
    for i, (title, filename, desc, col) in enumerate(deliv_items):
        cy = card_y + i * (c_h + c_gap)
        add_card(s15, Inches(0.8), cy, Inches(11.7), c_h, bg_color=NAVY_CARD, border_color=RGBColor(51, 65, 85))
        
        cbar = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), cy + Inches(0.15), Inches(0.08), c_h - Inches(0.3))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.fill.background()
        
        tb = s15.shapes.add_textbox(Inches(1.2), cy + Inches(0.12), Inches(11.1), c_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        
        p = tf.paragraphs[0]
        p.text = title + " — "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        r = p.add_run()
        r.text = filename
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = col
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(3)

    tb_foot = s15.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5))
    tb_foot.text_frame.word_wrap = True
    tb_foot.text_frame.margin_left = tb_foot.text_frame.margin_top = 0
    p = tb_foot.text_frame.paragraphs[0]
    p.text = "Groningen Sustainability Conference 2027 (GSC 2027) • University of Groningen, Netherlands • Scientific Advisory & Analytics Desk"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(148, 163, 184)

    output_filename = "GSC2027_Abstract_Submissions_Analysis_Report.pptx"
    prs.save(output_filename)
    print(f"Successfully re-generated {output_filename} with strict Theme 1 -> Theme 5 sequence!")

if __name__ == '__main__':
    build_presentation()
