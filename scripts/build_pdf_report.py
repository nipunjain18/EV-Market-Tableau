"""Script to generate the professional EV Market Analysis Project Report PDF.
Author: Nipun Jain
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4b6356"))
        
        # Header (pages 1 to N)
        self.drawString(54, 11 * 72 - 36, "Global EV Market Analysis | SmartBridge Skill Wallet | Data Analytics with Tableau")
        page_str = f"Page {self._pageNumber}"
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, page_str)
        self.setStrokeColor(colors.HexColor("#d8e5de"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer (pages 2 to N)
        if self._pageNumber > 1:
            self.line(54, 45, 8.5 * 72 - 54, 45)
            self.drawString(54, 32, "EV Market Analysis — Tableau & SQL Engineering Project Report | Author: Nipun Jain")
            self.drawRightString(8.5 * 72 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def create_report(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom palette
    DARK_GREEN = colors.HexColor("#0d2e21")
    TEAL_ACCENT = colors.HexColor("#178a63")
    LIGHT_BG = colors.HexColor("#f8faf9")
    BORDER_COLOR = colors.HexColor("#d8e5de")
    TEXT_DARK = colors.HexColor("#13241c")
    TEXT_MUTED = colors.HexColor("#4b6356")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=DARK_GREEN,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=TEAL_ACCENT,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=DARK_GREEN,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=TEAL_ACCENT,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f3d2e"),
        backColor=colors.HexColor("#f0f5f2"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=TEXT_DARK
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=TEXT_MUTED,
        alignment=1, # Center
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charts_dir = os.path.join(base_dir, "docs", "charts")
    sc_dir = os.path.join(base_dir, "docs", "screenshots")

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Global Electric Vehicle Market Analysis", title_style))
    story.append(Paragraph("Performance, Pricing, Battery Technology and Sales", subtitle_style))
    story.append(Paragraph("<b>SmartBridge Skill Wallet Project:</b> Data Analytics with Tableau", body_style))
    story.append(Paragraph("<b>Stack:</b> Python, SQL (SQLite / MySQL), Tableau Public, Flask, Git", body_style))
    story.append(Spacer(1, 14))

    # Student metadata table
    meta_data = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("<b>Nipun Jain</b>", body_style)],
        [Paragraph("<b>Project Domain</b>", body_style), Paragraph("Data Analytics and Business Intelligence", body_style)],
        [Paragraph("<b>GitHub Repository</b>", body_style), Paragraph("<font color='#178a63'><u>https://github.com/nipunjain18/ev-market-tableau</u></font>", body_style)],
        [Paragraph("<b>Tableau Public Story</b>", body_style), Paragraph("<font color='#178a63'><u>https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1</u></font>", body_style)],
        [Paragraph("<b>Tableau Dashboard</b>", body_style), Paragraph("<font color='#178a63'><u>https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview</u></font>", body_style)],
        [Paragraph("<b>Dataset Verified</b>", body_style), Paragraph("<code>ev_market_test.csv</code> (Exactly 100,000 Records, 37 Features)", body_style)],
        [Paragraph("<b>Demo Video Walkthrough</b>", body_style), Paragraph("<font color='#178a63'><u>https://drive.google.com/file/d/1Oik0Z53AKzTwvmX7_oB2swu_yIT3qbFW/view?usp=drivesdk</u></font>", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[140, 364])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Table of Contents</b>", h2_style))
    toc_data = [
        [Paragraph("1. Problem Understanding & Objectives", body_style), Paragraph("7. Dashboards & Responsive Architecture", body_style)],
        [Paragraph("2. Verified Dataset Description (100k Records)", body_style), Paragraph("8. Tableau Story Narrative (6 Scenes)", body_style)],
        [Paragraph("3. Relational Database Architecture (SQLite/MySQL)", body_style), Paragraph("9. Web Integration with Flask Application", body_style)],
        [Paragraph("4. SQL Operations & Query Benchmarks", body_style), Paragraph("10. Performance Testing & Optimization", body_style)],
        [Paragraph("5. Tableau Connection & Data Preparation", body_style), Paragraph("11. Key Insights & Data Analytics Findings", body_style)],
        [Paragraph("6. Worksheets & Calculated Fields", body_style), Paragraph("12. Conclusion, Scope & References", body_style)]
    ]
    t_toc = Table(toc_data, colWidths=[252, 252])
    t_toc.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROBLEM UNDERSTANDING & DATASET DESCRIPTION
    # =========================================================================
    story.append(Paragraph("1. Problem Understanding", h1_style))
    story.append(Paragraph(
        "Electric vehicles (EVs) have transitioned from niche technology to the mainstream foundation of global transportation decarbonization. "
        "However, automotive manufacturers, fleet operators, infrastructure planners, and buyers encounter significant market complexity. "
        "Vehicle models exhibit stark divergence in retail price, battery chemistry, usable range, charging velocity, and consumer adoption. "
        "Without unified business intelligence, stakeholders struggle to determine which vehicle categories drive mass-market volume, "
        "how driving range and battery pack size govern capital costs, and which battery chemistries deliver optimal multi-year durability.",
        body_style
    ))
    story.append(Paragraph("<b>Core Project Objectives:</b>", h2_style))
    story.append(Paragraph("&bull; <b>Market Sizing & Segmentation:</b> Quantify market scale across 15 vehicle categories, 200 manufacturers, and 7 global regions.", bullet_style))
    story.append(Paragraph("&bull; <b>Pricing & Range Drivers:</b> Evaluate the quantitative relationship between retail price, driving range, and battery capacity.", bullet_style))
    story.append(Paragraph("&bull; <b>Battery Chemistry Benchmarking:</b> Compare 5 distinct battery technologies on cycle life, 5-year degradation, and fast-charging.", bullet_style))
    story.append(Paragraph("&bull; <b>Environmental Impact Assessment:</b> Quantify carbon displacement (CO₂ tons saved per year) by category and geography.", bullet_style))
    story.append(Paragraph("&bull; <b>Interactive Web Deployment:</b> Deliver an executive BI solution via an interactive Tableau Public workbook embedded in Flask.", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Verified Dataset Description", h1_style))
    story.append(Paragraph(
        "The project is built upon the primary reference dataset <code>ev_market_test.csv</code> provided by SmartBridge Skill Wallet. "
        "The dataset contains exactly <b>100,000 records</b> and <b>37 columns</b>. Each individual record represents a distinct EV model or trim variant "
        "with a unique <code>vehicle_id</code> and zero duplicate records. Model years span 2018 through 2026.",
        body_style
    ))

    groups_data = [
        [Paragraph("<b>Attribute Group</b>", table_header_style), Paragraph("<b>Included Feature Fields (37 Total Columns)</b>", table_header_style)],
        [Paragraph("<b>Vehicle Identity</b>", table_cell_style), Paragraph("vehicle_id (unique key), model_name, manufacturer (200 brands), model_year (2018–2026), manufacturing_country (10 nations), market_region (7 regions), category (15 classes)", table_cell_style)],
        [Paragraph("<b>Battery Architecture</b>", table_cell_style), Paragraph("battery_capacity_kwh, battery_type (NMC, LFP, NCA, Sodium-Ion, Solid-State), battery_cycle_life, battery_degradation_pct_5yr", table_cell_style)],
        [Paragraph("<b>Performance Metrics</b>", table_cell_style), Paragraph("range_km, efficiency_wh_per_km, motor_power_kw, torque_nm, num_motors, drivetrain (FWD, RWD, AWD), top_speed_kmph, acceleration_0_100_sec", table_cell_style)],
        [Paragraph("<b>Charging Specs</b>", table_cell_style), Paragraph("max_dc_charging_kw, charging_dc_fast_time_min, charging_ac_time_hr, num_charging_ports", table_cell_style)],
        [Paragraph("<b>Physical & Features</b>", table_cell_style), Paragraph("num_seats, weight_kg, cargo_capacity_liters, infotainment_screen_inch, autonomous_level, safety_rating_stars", table_cell_style)],
        [Paragraph("<b>Commercial Economics</b>", table_cell_style), Paragraph("price_usd, insurance_cost_usd_yearly, warranty_years, resale_value_pct_3yr, annual_sales_units, customer_rating", table_cell_style)],
        [Paragraph("<b>Impact & Usability</b>", table_cell_style), Paragraph("co2_saved_tons_per_year, recommended_use_case (7 distinct operational profiles)", table_cell_style)]
    ]
    t_groups = Table(groups_data, colWidths=[130, 374])
    t_groups.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_groups)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DATA QUALITY AUDIT & DATABASE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("Data Quality & Integrity Audit", h2_style))
    story.append(Paragraph(
        "A rigorous missing-value and integrity scan was executed across all 100,000 rows. Missing values are present in only 5 numeric columns, "
        "all representing less than 3.1% missingness. Nulls are intentionally preserved as unpopulated values so that Tableau and SQL aggregations "
        "compute unbiased true averages without artificial imputation distortion.",
        body_style
    ))

    null_data = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Missing Rows</b>", table_header_style), Paragraph("<b>Missing Pct</b>", table_header_style), Paragraph("<b>Handling Rationale in Analytics</b>", table_header_style)],
        [Paragraph("<code>resale_value_pct_3yr</code>", table_cell_style), Paragraph("3,057", table_cell_style), Paragraph("3.06%", table_cell_style), Paragraph("Preserved blank; excluded from 3-yr depreciation means", table_cell_style)],
        [Paragraph("<code>battery_cycle_life</code>", table_cell_style), Paragraph("2,028", table_cell_style), Paragraph("2.03%", table_cell_style), Paragraph("Preserved blank; excluded from cycle-life technology benchmarks", table_cell_style)],
        [Paragraph("<code>customer_rating</code>", table_cell_style), Paragraph("1,931", table_cell_style), Paragraph("1.93%", table_cell_style), Paragraph("Preserved blank; excluded from customer satisfaction distributions", table_cell_style)],
        [Paragraph("<code>infotainment_screen_inch</code>", table_cell_style), Paragraph("1,506", table_cell_style), Paragraph("1.51%", table_cell_style), Paragraph("Preserved blank; basic models without central display", table_cell_style)],
        [Paragraph("<code>annual_sales_units</code>", table_cell_style), Paragraph("989", table_cell_style), Paragraph("0.99%", table_cell_style), Paragraph("Preserved blank; boutique / unreleased concept models", table_cell_style)]
    ]
    t_null = Table(null_data, colWidths=[140, 80, 80, 204])
    t_null.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_null)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Relational Database Architecture (SQLite & MySQL)", h1_style))
    story.append(Paragraph(
        "To establish reproducible SQL data engineering, the raw CSV dataset is ingested into a relational schema. "
        "The project provides complete automated loading via <code>scripts/load_to_db.py</code>, targeting SQLite (<code>data/ev_market.db</code>) "
        "for instant zero-dependency execution and MySQL (<code>ev_db</code>) for enterprise deployments.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Ingestion Pipeline (<code>scripts/load_to_db.py</code>):</b>", body_style
    ))
    code_ingest = (
        'df = pd.read_csv("data/raw/ev_market_test.csv")\n'
        'df.to_sql("ev_market", conn, if_exists="replace", index=False)\n'
        '# Verified: 100,000 records successfully populated into table ev_market'
    )
    story.append(Paragraph(code_ingest, code_style))

    story.append(Paragraph(
        "<b>Performance Indexing:</b> Dedicated B-tree indexes were constructed on high-cardinality and filtering dimensions: "
        "<code>idx_category</code>, <code>idx_year</code>, <code>idx_region</code>, and <code>idx_manufacturer</code>.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SQL OPERATIONS & SCREENSHOTS 1 & 2
    # =========================================================================
    story.append(Paragraph("4. SQL Operations & Query Execution Benchmarks", h1_style))
    story.append(Paragraph(
        "Ten multi-dimensional SQL queries were authored and verified against the 100,000-record database. "
        "The queries evaluate volume ranking, pricing segmentation, battery chemistry lifespans, and regional performance.",
        body_style
    ))

    # Figure 1: DB Sanity
    f1_path = os.path.join(sc_dir, "01_db_sanity_100k_rows.png")
    if os.path.exists(f1_path):
        story.append(Image(f1_path, width=480, height=140))
        story.append(Paragraph("<b>Figure 1:</b> Database verification query showing 100,000 rows stored in table <code>ev_market</code>, 200 manufacturers, and 15 categories.", caption_style))

    # Figure 2: Top 10 Manufacturers
    f2_path = os.path.join(sc_dir, "02_sql_top10_manufacturers.png")
    if os.path.exists(f2_path):
        story.append(Image(f2_path, width=480, height=140))
        story.append(Paragraph("<b>Figure 2:</b> Query 2 execution output: Top 10 EV manufacturers by total annual sales volume.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SQL SCREENSHOTS 3 & 4
    # =========================================================================
    story.append(Paragraph("Category Sizing & Battery Technology SQL Benchmarks", h2_style))

    # Figure 3: Category summary
    f3_path = os.path.join(sc_dir, "03_sql_category_sales_price.png")
    if os.path.exists(f3_path):
        story.append(Image(f3_path, width=480, height=155))
        story.append(Paragraph("<b>Figure 3:</b> Query 3 execution output: Sales volume, model count, and average price broken down across 15 vehicle categories.", caption_style))

    # Figure 4: Battery tech
    f4_path = os.path.join(sc_dir, "04_sql_battery_tech.png")
    if os.path.exists(f4_path):
        story.append(Image(f4_path, width=480, height=145))
        story.append(Paragraph("<b>Figure 4:</b> Query 4 execution output: Comparative battery chemistry benchmarking (range, fast-charge time, cycle life, 5-yr degradation).", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SQL SCREENSHOTS 5 & 6
    # =========================================================================
    story.append(Paragraph("Regional Dynamics & Multi-Year Evolution SQL Benchmarks", h2_style))

    # Figure 5: Region performance
    f5_path = os.path.join(sc_dir, "05_sql_regional_performance.png")
    if os.path.exists(f5_path):
        story.append(Image(f5_path, width=480, height=155))
        story.append(Paragraph("<b>Figure 5:</b> Query 5 execution output: Region-wise model distribution, average vehicle price, customer rating, and CO₂ offset.", caption_style))

    # Figure 6: Yearly trends
    f6_path = os.path.join(sc_dir, "06_sql_yearly_trends.png")
    if os.path.exists(f6_path):
        story.append(Image(f6_path, width=480, height=145))
        story.append(Paragraph("<b>Figure 6:</b> Query 6 execution output: Model year progression from 2018 to 2026 showing volume, average range, and price stability.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: TABLEAU CONNECTION & DATA PREPARATION
    # =========================================================================
    story.append(Paragraph("5. Tableau Connection and Data Preparation", h1_style))
    story.append(Paragraph(
        "The verified 100,000-record dataset was connected to Tableau Public as a packaged Hyper extract (<code>EV Market Analysis.twbx</code>). "
        "Tableau Public requires file-based packaged extracts for hosted interactive publishing.",
        body_style
    ))
    story.append(Paragraph("<b>Data Preparation & Transformation Rules:</b>", h2_style))
    story.append(Paragraph("&bull; <b>Null Handling:</b> Unpopulated values in resale percentage and ratings are preserved as nulls, allowing Tableau to calculate uncorrupted measures.", bullet_style))
    story.append(Paragraph("&bull; <b>Data Types & Roles:</b> <code>model_year</code> is classified as a discrete integer dimension; <code>manufacturing_country</code> is assigned the standard Geographic Role (Country/Region) for spatial rendering.", bullet_style))
    story.append(Paragraph("&bull; <b>High Cardinality Handling:</b> The 200 distinct manufacturers are dynamically filtered via an interactive <code>Top N Manufacturers</code> integer parameter and calculated rank field.", bullet_style))
    story.append(Paragraph("&bull; <b>Domain Filtering:</b> Non-positive price and range records were audited (0 records found with negative or zero values).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Tableau Calculated Fields:</b>", h2_style))
    calc_data = [
        [Paragraph("<b>Calculated Field</b>", table_header_style), Paragraph("<b>Exact Formula Implementation</b>", table_header_style), Paragraph("<b>Business Intelligence Purpose</b>", table_header_style)],
        [Paragraph("<b>Range per $1000</b>", table_cell_style), Paragraph("<code>[range_km] / [price_usd] * 1000</code>", table_cell_style), Paragraph("Value metric: driving range obtained per $1,000 retail spend", table_cell_style)],
        [Paragraph("<b>Price Segment</b>", table_cell_style), Paragraph("<code>IF [price_usd] < 20000 THEN 'Budget'<br/>ELSEIF [price_usd] < 60000 THEN 'Mid-range'<br/>ELSEIF [price_usd] < 120000 THEN 'Premium'<br/>ELSE 'Luxury' END</code>", table_cell_style), Paragraph("Four-tier economic price categorization", table_cell_style)],
        [Paragraph("<b>Range Class</b>", table_cell_style), Paragraph("<code>IF [range_km] >= 450 THEN 'Long'<br/>ELSEIF [range_km] >= 250 THEN 'Medium'<br/>ELSE 'Short' END</code>", table_cell_style), Paragraph("Tri-tier usable range classification", table_cell_style)],
        [Paragraph("<b>Fast Charge Rating</b>", table_cell_style), Paragraph("<code>IF [charging_dc_fast_time_min] <= 15 THEN 'Ultra-fast'<br/>ELSEIF [charging_dc_fast_time_min] <= 25 THEN 'Fast'<br/>ELSE 'Standard' END</code>", table_cell_style), Paragraph("DC fast-charging velocity benchmark", table_cell_style)],
        [Paragraph("<b>Revenue (Est.)</b>", table_cell_style), Paragraph("<code>[price_usd] * [annual_sales_units]</code>", table_cell_style), Paragraph("Gross model revenue estimation proxy", table_cell_style)],
        [Paragraph("<b>Sales Share %</b>", table_cell_style), Paragraph("<code>SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))</code>", table_cell_style), Paragraph("Relative contribution to fleet sales volume", table_cell_style)],
        [Paragraph("<b>Is Top N</b>", table_cell_style), Paragraph("<code>RANK(SUM([annual_sales_units])) <= [Top N Manufacturers]</code>", table_cell_style), Paragraph("Dynamic ranking filter driven by user parameter", table_cell_style)]
    ]
    t_calc = Table(calc_data, colWidths=[110, 230, 164])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_calc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: WORKSHEETS & VISUALIZATIONS OVERVIEW
    # =========================================================================
    story.append(Paragraph("6. Worksheets & Visualizations Overview", h1_style))
    story.append(Paragraph(
        "The Tableau workbook preserves 12 dedicated worksheets designed to answer targeted market, engineering, and environmental questions.",
        body_style
    ))

    ws_data = [
        [Paragraph("<b>#</b>", table_header_style), Paragraph("<b>Worksheet Name</b>", table_header_style), Paragraph("<b>Chart Type</b>", table_header_style), Paragraph("<b>Key Business Question Addressed</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("<b>Sales by Category</b>", table_cell_style), Paragraph("Horizontal Bar", table_cell_style), Paragraph("Which vehicle categories command the greatest volume? (Scooters: 85.0M)", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("<b>Sales by Year</b>", table_cell_style), Paragraph("Trend Line", table_cell_style), Paragraph("How has annual sales volume progressed over model years (2018–2026)?", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("<b>Top Manufacturers</b>", table_cell_style), Paragraph("Ranked Bar", table_cell_style), Paragraph("Who are the top volume leaders among 200 competing brands?", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("<b>Country Map</b>", table_cell_style), Paragraph("Filled Map", table_cell_style), Paragraph("Where are global EV manufacturing centers concentrated spatially?", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("<b>Region Price</b>", table_cell_style), Paragraph("Categorical Bar", table_cell_style), Paragraph("How does vehicle acquisition cost vary across the 7 geographic regions?", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("<b>Battery Share</b>", table_cell_style), Paragraph("Donut / Pie", table_cell_style), Paragraph("What is the market penetration of the 5 core battery chemistries?", table_cell_style)],
        [Paragraph("7", table_cell_style), Paragraph("<b>Battery Durability</b>", table_cell_style), Paragraph("Dual-Axis Bar", table_cell_style), Paragraph("Which chemistries yield superior cycle life and lowest 5-year degradation?", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("<b>Price vs Range</b>", table_cell_style), Paragraph("Scatter Plot", table_cell_style), Paragraph("Does higher capital investment guarantee proportional driving range?", table_cell_style)],
        [Paragraph("9", table_cell_style), Paragraph("<b>Drivetrain Heatmap</b>", table_cell_style), Paragraph("Matrix Heatmap", table_cell_style), Paragraph("How do FWD, RWD, and AWD drivetrains distribute across classes?", table_cell_style)],
        [Paragraph("10", table_cell_style), Paragraph("<b>Use Case</b>", table_cell_style), Paragraph("Treemap", table_cell_style), Paragraph("What proportions of EV models serve urban, commercial, or family profiles?", table_cell_style)],
        [Paragraph("11", table_cell_style), Paragraph("<b>CO2 Saved</b>", table_cell_style), Paragraph("Stacked Bar", table_cell_style), Paragraph("Which vehicle categories generate the largest emissions displacement?", table_cell_style)],
        [Paragraph("12", table_cell_style), Paragraph("<b>Rating Histogram</b>", table_cell_style), Paragraph("Histogram", table_cell_style), Paragraph("What is the fleet-wide customer satisfaction distribution (1.0–5.0 stars)?", table_cell_style)]
    ]
    t_ws = Table(ws_data, colWidths=[20, 114, 85, 285])
    t_ws.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_ws)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Global Dashboard Interactive Filters (6):</b>", h2_style))
    story.append(Paragraph("1. <code>model_year</code> (Range Slider) | 2. <code>market_region</code> (Multi-select) | 3. <code>category</code> (Multi-select) | 4. <code>battery_type</code> (Single-select dropdown) | 5. <code>Price Segment</code> (Categorical check-list) | 6. <code>Top N Manufacturers</code> (Integer Parameter 5–30).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SAMPLE VISUAL CHARTS (FIGURES 7 & 8)
    # =========================================================================
    story.append(Paragraph("Sample Visual Analytics Outputs", h1_style))
    story.append(Paragraph("Visual outputs computed directly from the 100,000-record dataset reflecting Tableau worksheet visual encodings:", body_style))

    c1_path = os.path.join(charts_dir, "01_sales_by_category.png")
    c2_path = os.path.join(charts_dir, "02_top_manufacturers.png")
    if os.path.exists(c1_path):
        story.append(Image(c1_path, width=440, height=140))
        story.append(Paragraph("<b>Chart 1:</b> Sales by Category — Volume leadership dominated by Two-Wheeler Scooters, Sedans, and Compact SUVs.", caption_style))
    if os.path.exists(c2_path):
        story.append(Image(c2_path, width=440, height=140))
        story.append(Paragraph("<b>Chart 2:</b> Top 10 Manufacturers — SurgeWorks (4.88M) and CurrentMobility (4.78M) leading a balanced competitive field.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SAMPLE VISUAL CHARTS CONTINUED (FIGURES 9 & 10)
    # =========================================================================
    story.append(Paragraph("Battery Durability & Economic Regression Outputs", h1_style))

    c3_path = os.path.join(charts_dir, "03_battery_comparison.png")
    c4_path = os.path.join(charts_dir, "04_price_vs_range.png")
    if os.path.exists(c3_path):
        story.append(Image(c3_path, width=440, height=140))
        story.append(Paragraph("<b>Chart 3:</b> Battery Durability Comparison — Solid-State (2,999 cycles) and LFP (2,498 cycles) exhibit benchmark degradation resistance.", caption_style))
    if os.path.exists(c4_path):
        story.append(Image(c4_path, width=440, height=140))
        story.append(Paragraph("<b>Chart 4:</b> Price vs Driving Range — Scatter plot demonstrating divergence in capital cost across light-duty and commercial EV segments.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: DASHBOARDS & STORY NARRATIVE
    # =========================================================================
    story.append(Paragraph("7. Coordinated Dashboards", h1_style))
    story.append(Paragraph(
        "The 12 worksheets are organized into three responsive, synchronized dashboards utilizing coordinated filter actions: "
        "<br/>&bull; <b>Market Overview:</b> KPI Cards (Total Models, Sales, Avg Price, Avg Range), Sales by Category, Sales by Year, Top N Manufacturers, Region Price."
        "<br/>&bull; <b>Technology:</b> Battery Type Share, Battery Durability, Price vs Range Scatter, Category x Drivetrain Heatmap."
        "<br/>&bull; <b>Geography and Impact:</b> Manufacturing Country Filled Map, Recommended Use Case Treemap, CO₂ Saved Stacked Bar, Rating Histogram."
        "<br/><b>Live Dashboard URL:</b> <font color='#178a63'><u>https://public.tableau.com/views/EVMarketAnalysis_17932840807840/MarketOverview</u></font>",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. Tableau Story Architecture (6 Narrative Scenes)", h1_style))
    story.append(Paragraph(
        "The narrative story guides executive stakeholders from macro market sizing to operational takeaways: "
        "<br/><b>Published Story URL:</b> <font color='#178a63'><u>https://public.tableau.com/views/EVMarketAnalysis_17932840807840/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link</u></font>",
        body_style
    ))

    story_data = [
        [Paragraph("<b>Scene</b>", table_header_style), Paragraph("<b>Story Scene Caption</b>", table_header_style), Paragraph("<b>Analytical Narrative & Core Finding</b>", table_header_style)],
        [Paragraph("<b>1</b>", table_cell_style), Paragraph("<b>Market Snapshot</b>", table_cell_style), Paragraph("Overview of 100,000 models, average retail price of $65,010, average range of 324.3 km.", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_style), Paragraph("<b>Who Sells the Most</b>", table_cell_style), Paragraph("Two-wheeler scooters (85.0M), sedans (78.3M), and compact SUVs (76.1M) command 31% of total volume.", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_style), Paragraph("<b>Price vs Range</b>", table_cell_style), Paragraph("Battery pack capacity correlates 0.84 with price, whereas range correlates only 0.28.", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_style), Paragraph("<b>Battery Technology</b>", table_cell_style), Paragraph("Solid-State (2,999 cycles, 7.36% degradation) and LFP (2,498 cycles, 10.11%) lead durability.", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_style), Paragraph("<b>Regions & Countries</b>", table_cell_style), Paragraph("Regional sales and manufacturing footprint are distributed without single-country monopoly.", table_cell_style)],
        [Paragraph("<b>6</b>", table_cell_style), Paragraph("<b>Strategic Recommendations</b>", table_cell_style), Paragraph("Automakers must prioritize high-durability chemistries for urban fleet applications.", table_cell_style)]
    ]
    t_story = Table(story_data, colWidths=[36, 114, 354])
    t_story.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_story)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: FLASK WEB INTEGRATION & SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("9. Web Integration with Flask Application", h1_style))
    story.append(Paragraph(
        "To deliver a turnkey BI experience, the interactive Tableau views are embedded inside a production-ready Flask application. "
        "The application integrates the <b>Tableau Embedding API v3</b>, featuring responsive layout containers, dark/light theme switching, and zero-code URL configuration.",
        body_style
    ))

    # Figure 7: Flask Home
    f7_path = os.path.join(sc_dir, "07_web_home_page.png")
    if os.path.exists(f7_path):
        story.append(Image(f7_path, width=440, height=130))
        story.append(Paragraph("<b>Figure 7:</b> Web portal landing page running at <code>http://127.0.0.1:5000</code> displaying core project architecture.", caption_style))

    # Figure 8: Flask Dashboard Embed
    f8_path = os.path.join(sc_dir, "08_web_dashboard_embed.png")
    if os.path.exists(f8_path):
        story.append(Image(f8_path, width=440, height=130))
        story.append(Paragraph("<b>Figure 8:</b> Dashboard page embedding the Tableau Public Market Overview dashboard with live filters.", caption_style))

    # Figure 9: Flask Story Embed
    f9_path = os.path.join(sc_dir, "09_web_story_embed.png")
    if os.path.exists(f9_path):
        story.append(Image(f9_path, width=440, height=130))
        story.append(Paragraph("<b>Figure 9:</b> Story page embedding the 6-scene interactive Tableau Story narrative.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: PERFORMANCE TESTING, KEY INSIGHTS, CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("10. Performance Testing & Optimization", h1_style))
    perf_data = [
        [Paragraph("<b>Parameter</b>", table_header_style), Paragraph("<b>Specification / Benchmark Result</b>", table_header_style)],
        [Paragraph("Underlying Records Rendered", table_cell_style), Paragraph("100,000 rows (from verified <code>ev_market_test.csv</code>)", table_cell_style)],
        [Paragraph("Total Columns & Derived Measures", table_cell_style), Paragraph("37 base dimensions + 5 calculated fields", table_cell_style)],
        [Paragraph("Data Filters & Global Parameters", table_cell_style), Paragraph("6 synchronized filters + dynamic Top N parameter", table_cell_style)],
        [Paragraph("Visualizations & Dashboards", table_cell_style), Paragraph("12 worksheets, 3 dashboards, 6 story points", table_cell_style)],
        [Paragraph("Packaged Hyper Extract Load Time", table_cell_style), Paragraph("< 0.8 seconds response during interactive cross-filtering", table_cell_style)]
    ]
    t_perf = Table(perf_data, colWidths=[180, 324])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 4))

    story.append(Paragraph("11. Key Insights & Empirical Findings", h1_style))
    story.append(Paragraph("&bull; <b>Volume Disparity:</b> Two-Wheeler Scooters lead global sales (85.0M units, avg price $2,530), followed by Sedans (78.3M, $42,557) and Compact SUVs (76.1M, $36,528). Commercial Buses (5.1M) and Heavy Trucks (5.1M) represent low volume but high unit revenue.", bullet_style))
    story.append(Paragraph("&bull; <b>Battery Cost Dominance:</b> Retail price correlates strongly with battery capacity (r = 0.84) rather than driving range (r = 0.28). Electric Buses (avg $274k) and Heavy Trucks ($169k) command premium prices due to massive pack capacities.", bullet_style))
    story.append(Paragraph("&bull; <b>Battery Longevity:</b> Solid-State averages 2,999 cycles and 7.36% 5-year degradation; LFP follows with 2,498 cycles and 10.11%. In contrast, NMC (1,799 cycles, 14.01%), Sodium-Ion (1,797 cycles, 13.98%), and NCA (1,598 cycles, 14.02%) show faster capacity loss.", bullet_style))
    story.append(Paragraph("&bull; <b>Charging Parity:</b> Fast-charging times average ~21.1 minutes and range averages ~324 km across all chemistries, proving chemistry choice influences lifecycle durability rather than charge speed.", bullet_style))
    story.append(Paragraph("&bull; <b>Competitive Landscape:</b> Top 5 automakers (SurgeWorks 4.88M, CurrentMobility 4.78M, ElektraMobility 4.75M, VelocityMobility 4.68M, WattDynamics 4.65M) demonstrate a balanced, highly competitive marketplace without monopoly concentration.", bullet_style))
    story.append(Paragraph("&bull; <b>Dataset Synthetic Character:</b> Temporal distribution is uniform across 2018–2026 (~11,100 models/year) with flat price and range averages, indicating synthetic generation without historical technological curves.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12. Conclusion, Future Scope & Academic Attribution", h1_style))
    story.append(Paragraph(
        "<b>Conclusion:</b> This project completes an end-to-end data analytics lifecycle — transforming raw CSV records into an indexed database, "
        "executing SQL queries, engineering Tableau calculations, building synchronized dashboards, and deploying an interactive web application. "
        "<br/><b>Future Scope:</b> Ingest real-world telemetry and charging infrastructure datasets; integrate automated ML sales forecasting models; and deploy the containerized web app to cloud platforms. "
        "<br/><b>Academic Attribution:</b> Project customized and verified by <b>Nipun Jain</b> for the Data Analytics and Business Intelligence domain. "
        "Architectural patterns adapted from an established project baseline with strict validation against the 100,000-record reference dataset.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {output_pdf_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "EV_Market_Tableau_Project_Report.pdf")
    create_report(target_path)
