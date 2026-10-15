import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, num_pages):
        page_num = self._pageNumber
        if page_num == 1:
            # Cover Page - draw polygon accents
            self.saveState()
            # Top right subtle polygon
            p = self.beginPath()
            p.moveTo(480, 842)
            p.lineTo(595, 842)
            p.lineTo(595, 740)
            p.lineTo(520, 740)
            p.close()
            self.setFillColor(colors.HexColor("#E2E8F0"))
            self.drawPath(p, fill=1, stroke=0)

            p2 = self.beginPath()
            p2.moveTo(540, 842)
            p2.lineTo(595, 842)
            p2.lineTo(595, 785)
            p2.close()
            self.setFillColor(colors.HexColor("#CBD5E1"))
            self.drawPath(p2, fill=1, stroke=0)

            # Bottom right vibrant magenta/burgundy polygon accent (matching Future IT Touch style)
            p3 = self.beginPath()
            p3.moveTo(400, 0)
            p3.lineTo(595, 0)
            p3.lineTo(595, 120)
            p3.lineTo(530, 120)
            p3.lineTo(470, 70)
            p3.close()
            self.setFillColor(colors.HexColor("#C2185B"))
            self.drawPath(p3, fill=1, stroke=0)

            p4 = self.beginPath()
            p4.moveTo(460, 0)
            p4.lineTo(595, 0)
            p4.lineTo(595, 70)
            p4.lineTo(510, 70)
            p4.close()
            self.setFillColor(colors.HexColor("#AD1457"))
            self.drawPath(p4, fill=1, stroke=0)

            p5 = self.beginPath()
            p5.moveTo(520, 0)
            p5.lineTo(595, 0)
            p5.lineTo(595, 45)
            p5.close()
            self.setFillColor(colors.HexColor("#880E4F"))
            self.drawPath(p5, fill=1, stroke=0)

            self.restoreState()
            return

        # Subsequent pages
        self.saveState()
        # Header
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#C2185B"))
        self.drawString(54, 800, "Future IT Touch Private Limited")
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(541, 800, "DineStay SRS - Phase 1 MVP")
        
        # Header rule
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 792, 541, 792)

        # Bottom polygon accent
        p = self.beginPath()
        p.moveTo(450, 0)
        p.lineTo(595, 0)
        p.lineTo(595, 45)
        p.lineTo(500, 45)
        p.close()
        self.setFillColor(colors.HexColor("#C2185B"))
        self.drawPath(p, fill=1, stroke=0)

        p_dark = self.beginPath()
        p_dark.moveTo(520, 0)
        p_dark.lineTo(595, 0)
        p_dark.lineTo(595, 25)
        p_dark.close()
        self.setFillColor(colors.HexColor("#880E4F"))
        self.drawPath(p_dark, fill=1, stroke=0)

        # Footer
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, f"Page {page_num} of {num_pages}")
        self.drawRightString(430, 30, "Confidential - Future IT Touch Pvt. Ltd.")
        self.restoreState()

def build_pdf(filename="DineStay_Software_Requirements_Specification_SRS.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_company = ParagraphStyle(
        'CompanyTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#1E40AF") # Royal Blue matching screenshot
    )
    
    meta_info = ParagraphStyle(
        'MetaInfo',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    doc_srs_badge = ParagraphStyle(
        'DocSRSBadge',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=30,
        spaceAfter=15
    )

    big_title = ParagraphStyle(
        'BigTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    sub_title = ParagraphStyle(
        'SubTitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#475569"),
        spaceAfter=30
    )

    sec_heading = ParagraphStyle(
        'SecHeading',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    subsec_heading = ParagraphStyle(
        'SubSecHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_text = ParagraphStyle(
        'BodyTextCustom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    bullet_text = ParagraphStyle(
        'BulletCustom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.white
    )

    story = []

    # ================= PAGE 1: COVER =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Future IT Touch Private Limited", title_company))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Address:</b> Sco No. 113-114, 2nd Floor, Near Mukat Hospital<br/>Sector 34 A, Chandigarh, 160022<br/><b>Phone No:</b> +91-7056937000 / +91-7056997000<br/><b>Email:</b> info@futuretouch.in", meta_info))
    
    story.append(Spacer(1, 40))
    story.append(Paragraph("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", doc_srs_badge))
    story.append(Paragraph("DineStay: Restaurant, Hotel & Banquet Reservation Platform", big_title))
    story.append(Paragraph("Phase 1 – Minimum Viable Product (MVP)", sub_title))
    
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=10, spaceAfter=25))
    
    story.append(Paragraph("<b>Document Information</b>", subsec_heading))
    
    doc_info_data = [
        [Paragraph("<b>Document Title</b>", table_cell), Paragraph("DineStay Platform – Software Requirements Specification", table_cell)],
        [Paragraph("<b>Branding / Project Name</b>", table_cell), Paragraph("DineStay (Restaurants • Hotels • Experiences)", table_cell)],
        [Paragraph("<b>Version</b>", table_cell), Paragraph("1.0 (Phase 1 MVP Production Specification)", table_cell)],
        [Paragraph("<b>Prepared By</b>", table_cell), Paragraph("Future IT Touch Pvt. Ltd.", table_cell)],
        [Paragraph("<b>Prepared For</b>", table_cell), Paragraph("Client Executive Team / Stakeholders", table_cell)],
        [Paragraph("<b>Document Type</b>", table_cell), Paragraph("Software Requirements Specification (SRS)", table_cell)],
        [Paragraph("<b>UI Verification</b>", table_cell), Paragraph("42 High-Fidelity Mobile Application Wireframes & Web Portals", table_cell)],
        [Paragraph("<b>Status</b>", table_cell), Paragraph("Approved / Governing Implementation Document", table_cell)],
    ]
    t_info = Table(doc_info_data, colWidths=[160, 327])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_info)
    story.append(PageBreak())

    # ================= PAGE 2: EXECUTIVE SUMMARY & OBJECTIVES =================
    story.append(Paragraph("1. Executive Summary", sec_heading))
    story.append(Paragraph(
        "The <b>DineStay Platform</b> is an advanced digital hospitality and reservation ecosystem engineered "
        "to streamline table dining, hotel room reservations, and banquet/party hall event bookings into a single, cohesive experience. "
        "Built for both discerning consumers and hospitality business operators, DineStay bridges modern mobile convenience with centralized enterprise management.",
        body_text
    ))
    story.append(Paragraph(
        "The proposed Phase-1 MVP delivers end-to-end business capabilities: consumer onboarding, cross-vertical search and discovery "
        "(restaurants, hotels, and party halls in Chandigarh and surrounding regions), real-time table and room availability allocation, "
        "multi-channel digital payments (UPI, Cards, NetBanking, Wallets), dynamic discount coupons, and a comprehensive unified administration and partner portal suite.",
        body_text
    ))
    story.append(Paragraph(
        "The solution is architected as an interconnected ecosystem communicating via secure, rate-limited RESTful APIs built on Laravel, "
        "with an ultra-fast Flutter mobile application (Android and iOS) and responsive ReactJS portals.",
        body_text
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Project Objectives", sec_heading))
    story.append(Paragraph("The primary strategic and technical objectives of Phase-1 include:", body_text))
    story.append(Paragraph("• <b>Digitize Restaurant Table Reservations:</b> Enable instant visual slot selection, party size specification, and guest special requests with instant SMS/Email confirmation.", bullet_text))
    story.append(Paragraph("• <b>Simplify Hotel Room Booking:</b> Real-time inventory check, room category comparison (King, Twin, Suite), multi-night stay rates, and check-in/out scheduling.", bullet_text))
    story.append(Paragraph("• <b>Banquet & Party Hall Inquiries:</b> Connect event organizers with premier party halls (50 to 500+ guest capacities) with venue specifications, catering, and valet details.", bullet_text))
    story.append(Paragraph("• <b>Instant Customer Discovery:</b> Geolocation-aware search across Chandigarh, filter chips for cuisines, star ratings, price tiers, and active promotional deals.", bullet_text))
    story.append(Paragraph("• <b>Automated Offers Engine:</b> Configurable coupon codes (e.g., DINE20, STAY15) with percentage/flat discounts and minimum spend thresholds.", bullet_text))
    story.append(Paragraph("• <b>Centralized Platform Administration:</b> Unified control over partner onboarding, verification of GST and licenses, commission accounting, and dispute handling.", bullet_text))
    story.append(Paragraph("• <b>Scalable Cloud Architecture:</b> Future-proof foundation supporting payments, loyalty rewards, multi-language support, and multi-city geographic rollout.", bullet_text))

    story.append(PageBreak())

    # ================= PAGE 3: DELIVERABLES & ARCHITECTURE =================
    story.append(Paragraph("3. Project Deliverables", sec_heading))
    story.append(Paragraph("The DineStay Phase-1 MVP comprises six specialized software components:", body_text))

    deliv_data = [
        [Paragraph("Module", table_header), Paragraph("Target Platform", table_header), Paragraph("Core Technology", table_header), Paragraph("Scope Summary", table_header)],
        [Paragraph("<b>Customer Mobile App</b>", table_cell), Paragraph("Android & iOS", table_cell), Paragraph("Flutter 3.x / Dart", table_cell), Paragraph("42 Verified UI Screens, Discovery, Bookings, Payments, Profile", table_cell)],
        [Paragraph("<b>Restaurant Business Portal</b>", table_cell), Paragraph("Web (Responsive)", table_cell), Paragraph("ReactJS / Tailwind", table_cell), Paragraph("Menu builder, slot allocation, live reservations table, analytics", table_cell)],
        [Paragraph("<b>Hotel Business Portal</b>", table_cell), Paragraph("Web (Responsive)", table_cell), Paragraph("ReactJS / Tailwind", table_cell), Paragraph("Room category management, daily tariff control, guest check-ins", table_cell)],
        [Paragraph("<b>Party Hall Business Portal</b>", table_cell), Paragraph("Web (Responsive)", table_cell), Paragraph("ReactJS / Tailwind", table_cell), Paragraph("Hall calendar, booking leads, package pricing, catering packages", table_cell)],
        [Paragraph("<b>Administration Portal</b>", table_cell), Paragraph("Web (Desktop)", table_cell), Paragraph("ReactJS / AdminKit", table_cell), Paragraph("Partner KYC approval, global coupons, revenue audits, user bans", table_cell)],
        [Paragraph("<b>Backend API Services</b>", table_cell), Paragraph("Cloud Server", table_cell), Paragraph("Laravel 11 REST API", table_cell), Paragraph("JWT authentication, booking state engine, notifications, cron jobs", table_cell)],
        [Paragraph("<b>Database Tier</b>", table_cell), Paragraph("Managed Server", table_cell), Paragraph("MySQL 8.0 / Redis", table_cell), Paragraph("Relational schema, transaction safety, Redis session & rate limiting", table_cell)],
    ]
    t_deliv = Table(deliv_data, colWidths=[120, 95, 105, 167])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_deliv)

    story.append(Spacer(1, 15))
    story.append(Paragraph("4. System Architecture & Topology", sec_heading))
    story.append(Paragraph(
        "DineStay adopts a scalable client-server architecture. All frontend client applications communicate exclusively with the Laravel REST API layer over secure TLS 1.3 encrypted HTTPS channels.",
        body_text
    ))

    arch_data = [
        [Paragraph("<b>Client Layer:</b>", table_cell), Paragraph("Flutter Mobile App (iOS / Android) • ReactJS Web Portals (Restaurant, Hotel, Party Hall, Admin)", table_cell)],
        [Paragraph("<b>Security & Gateway:</b>", table_cell), Paragraph("Cloudflare WAF • SSL/TLS 1.3 • Rate Limiting • CORS Protection • JWT Bearer Tokens", table_cell)],
        [Paragraph("<b>Application Layer:</b>", table_cell), Paragraph("Laravel 11 RESTful API Service • Controllers, Middleware, Form Requests, Observers", table_cell)],
        [Paragraph("<b>Integrations Layer:</b>", table_cell), Paragraph("Payment Gateway (UPI/Cards/NetBanking) • SMS Gateway (OTP) • AWS S3 / Cloudinary (Media)", table_cell)],
        [Paragraph("<b>Persistence Layer:</b>", table_cell), Paragraph("MySQL 8.0 (ACID Relational Storage) • Redis 7.x (Caching, Slot Locking, Queues)", table_cell)],
    ]
    t_arch = Table(arch_data, colWidths=[130, 357])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # ================= PAGE 4: USER ROLES & PERMISSIONS =================
    story.append(Paragraph("5. User Roles & Access Control", sec_heading))
    story.append(Paragraph("DineStay implements rigorous Role-Based Access Control (RBAC) across five user categories:", body_text))

    story.append(Paragraph("5.1 Platform Administrator", subsec_heading))
    story.append(Paragraph("The superuser with global oversight and configuration privileges across the entire DineStay ecosystem:", body_text))
    story.append(Paragraph("• <b>Business KYC & Onboarding:</b> Review submitted business licenses, GST certificates, and physical address proof for restaurants, hotels, and halls before public listing.", bullet_text))
    story.append(Paragraph("• <b>Account Moderation:</b> Instant suspension or restoration of offending partner accounts or abusive customer accounts.", bullet_text))
    story.append(Paragraph("• <b>Financial & Commission Auditing:</b> Set commission percentages per category, monitor gross transactional revenue, and generate payout sheets.", bullet_text))
    story.append(Paragraph("• <b>Global Campaign Engine:</b> Create platform-wide promotional codes (e.g., WELCOME50, FESTIVE) and manage hero app banners.", bullet_text))

    story.append(Paragraph("5.2 Restaurant Partner", subsec_heading))
    story.append(Paragraph("• Manage restaurant profile, culinary cuisines, operating hours, and photo gallery.", bullet_text))
    story.append(Paragraph("• Configure visual digital menu with categorization, pricing, and Veg/Non-Veg badges.", bullet_text))
    story.append(Paragraph("• Set table capacity, available time slots (12:00 PM – 10:00 PM), and accept/reject reservations.", bullet_text))
    story.append(Paragraph("• Launch venue-specific coupons and track daily guest covers and revenue.", bullet_text))

    story.append(Paragraph("5.3 Hotel Partner", subsec_heading))
    story.append(Paragraph("• Manage property description, star rating, address, amenities (Pool, Wi-Fi, Spa, Gym, Restaurant).", bullet_text))
    story.append(Paragraph("• Configure room inventories: King Room, Twin Room, Suite Room with occupancy rules and pricing.", bullet_text))
    story.append(Paragraph("• Process check-in and check-out logs, view booking vouchers, and handle cancellation requests.", bullet_text))

    story.append(Paragraph("5.4 Party & Banquet Hall Partner", subsec_heading))
    story.append(Paragraph("• Manage hall capacity limits (e.g., 50–500 guests), event types (Weddings, Corporate, Birthday).", bullet_text))
    story.append(Paragraph("• Manage package pricing, parking arrangements, and in-house catering menu options.", bullet_text))

    story.append(Paragraph("5.5 Customer / End User", subsec_heading))
    story.append(Paragraph("• Search, filter, compare, reserve dining tables, book hotel stays, and request banquet quotations.", bullet_text))
    story.append(Paragraph("• View booking history, cancel reservations with automated policy enforcement, save addresses, and earn coupon discounts.", bullet_text))

    story.append(PageBreak())

    # ================= PAGE 5: COMPLETE 42-SCREEN MOBILE UI SPECIFICATION =================
    story.append(Paragraph("6. Customer Mobile Application – UI Screen Inventory", sec_heading))
    story.append(Paragraph(
        "The customer mobile application consists of <b>42 purpose-built screens</b> matching the verified UI wireframe specification. "
        "Each screen has been designed according to DineStay's forest green & warm terracotta visual identity:",
        body_text
    ))

    screens_data = [
        [Paragraph("#", table_header), Paragraph("Screen Name", table_header), Paragraph("Category / Row", table_header), Paragraph("Key Functional Components & Interactivity", table_header)],
        [Paragraph("1", table_cell), Paragraph("<b>Splash Screen</b>", table_cell), Paragraph("Row 1: Onboarding", table_cell), Paragraph("Full-bleed dining backdrop, DineStay pin badge, tagline 'Restaurants • Hotels • Experiences', carousel dashes.", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Onboarding 1</b>", table_cell), Paragraph("Row 1: Onboarding", table_cell), Paragraph("Restaurants focus, circular hero illustration, pagination indicator, Skip & Next CTA.", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Onboarding 2</b>", table_cell), Paragraph("Row 1: Onboarding", table_cell), Paragraph("Hotel stays focus, cozy luxury bed illustration, pagination indicator, Skip & Next CTA.", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Onboarding 3</b>", table_cell), Paragraph("Row 1: Onboarding", table_cell), Paragraph("Best offers focus, digital discount vouchers illustration, 'Get Started' action.", table_cell)],
        [Paragraph("5", table_cell), Paragraph("<b>Login Screen</b>", table_cell), Paragraph("Row 1: Auth", table_cell), Paragraph("Email/Mobile input, Password, Forgot Password link, Google & Apple social OAuth buttons.", table_cell)],
        [Paragraph("6", table_cell), Paragraph("<b>Forgot Password</b>", table_cell), Paragraph("Row 1: Auth", table_cell), Paragraph("Security key badge, SMS/Email delivery toggle, mobile input with +91 flag, Send Recovery Code CTA.", table_cell)],
        [Paragraph("7", table_cell), Paragraph("<b>Create Account</b>", table_cell), Paragraph("Row 1: Auth", table_cell), Paragraph("Customer / Business pill toggle, Full Name, Mobile (+91), Email, Password, Terms agreement checkbox.", table_cell)],
        [Paragraph("8", table_cell), Paragraph("<b>OTP Verification</b>", table_cell), Paragraph("Row 1: Auth", table_cell), Paragraph("6-digit discrete PIN inputs, resend countdown timer (00:25), Secure verification CTA.", table_cell)],
        [Paragraph("9", table_cell), Paragraph("<b>City & Location Selector</b>", table_cell), Paragraph("Row 1: Discovery", table_cell), Paragraph("Search input, GPS auto-detect button, popular city cards (Chandigarh, Mohali, Panchkula, Delhi, Mumbai).", table_cell)],
        [Paragraph("10", table_cell), Paragraph("<b>Home / Explore</b>", table_cell), Paragraph("Row 1: Discovery", table_cell), Paragraph("Location picker, notification bell, category icons (4), Flat 20% promo carousel, popular venues.", table_cell)],
        [Paragraph("11", table_cell), Paragraph("<b>Search & Filters</b>", table_cell), Paragraph("Row 2: Discovery", table_cell), Paragraph("Search input, dynamic filter chips (Cuisine, Rating 4.0+, Offers, Sort), search result count.", table_cell)],
        [Paragraph("12", table_cell), Paragraph("<b>Restaurant Details</b>", table_cell), Paragraph("Row 2: Dining", table_cell), Paragraph("Hero gallery, star badge, distance, Call / Directions / Share / Save, Overview / Menu / Photos tabs.", table_cell)],
        [Paragraph("13", table_cell), Paragraph("<b>Restaurant Photo Gallery</b>", table_cell), Paragraph("Row 2: Dining", table_cell), Paragraph("Full-screen photo grid (48 photos), category tabs (Ambiance, Food & Drinks, Rooftop), Reserve Table CTA.", table_cell)],
        [Paragraph("14", table_cell), Paragraph("<b>Restaurant Menu</b>", table_cell), Paragraph("Row 2: Dining", table_cell), Paragraph("Category chips (Recommended, Starters, Mains), Veg/Non-Veg indicators, pricing, Add to order button.", table_cell)],
        [Paragraph("15", table_cell), Paragraph("<b>Table Reservation</b>", table_cell), Paragraph("Row 2: Dining", table_cell), Paragraph("Horizontal date picker, lunch/dinner time slots, guest counter [- 2 +], special request notes.", table_cell)],
        [Paragraph("16", table_cell), Paragraph("<b>Review Reservation</b>", table_cell), Paragraph("Row 2: Dining", table_cell), Paragraph("Booking summary card, chosen venue, date, time, party size, cancellation policy, Confirm Reservation CTA.", table_cell)],
        [Paragraph("17", table_cell), Paragraph("<b>Party Halls List</b>", table_cell), Paragraph("Row 2: Banquets", table_cell), Paragraph("Found halls count, venue photo cards (The Grand Hall, Royal Banquet), pricing from ₹25,000.", table_cell)],
        [Paragraph("18", table_cell), Paragraph("<b>Party Hall Details</b>", table_cell), Paragraph("Row 2: Banquets", table_cell), Paragraph("Grand ballroom hero, tags (Weddings, Corporate), capacity (50-300), parking, in-house catering.", table_cell)],
        [Paragraph("19", table_cell), Paragraph("<b>Hotels Search</b>", table_cell), Paragraph("Row 2: Hotels", table_cell), Paragraph("Dates & occupancy bar, Price/Rating chips, Hotel cards (Hyatt Regency, Taj) with amenities.", table_cell)],
        [Paragraph("20", table_cell), Paragraph("<b>Hotel Details</b>", table_cell), Paragraph("Row 2: Hotels", table_cell), Paragraph("Luxury room hero, amenities grid (Pool, Wi-Fi, Spa, Dining), about property, View Rooms CTA.", table_cell)],
        [Paragraph("21", table_cell), Paragraph("<b>Hotel Photo Gallery</b>", table_cell), Paragraph("Row 2: Hotels", table_cell), Paragraph("36 verified photos, category tabs (Executive King, Infinity Pool, Lobby, Spa), Choose Rooms CTA.", table_cell)],
        [Paragraph("22", table_cell), Paragraph("<b>Select Room</b>", table_cell), Paragraph("Row 3: Stays", table_cell), Paragraph("Room cards: King Room (₹9,800), Twin Room (₹11,500), Suite Room (₹15,200), Select button.", table_cell)],
        [Paragraph("23", table_cell), Paragraph("<b>Hotel Booking Review</b>", table_cell), Paragraph("Row 3: Stays", table_cell), Paragraph("Check-in/out dates, price computation (Room ₹9,800 + Taxes ₹1,200 = ₹10,200), Proceed to Payment.", table_cell)],
        [Paragraph("24", table_cell), Paragraph("<b>Payment Method</b>", table_cell), Paragraph("Row 3: Checkout", table_cell), Paragraph("Payment options: UPI (GPay/PhonePe), Credit/Debit Card, Net Banking, Wallet, Save card option.", table_cell)],
        [Paragraph("25", table_cell), Paragraph("<b>Booking Confirmed</b>", table_cell), Paragraph("Row 3: Checkout", table_cell), Paragraph("Celebratory checkmark, Booking ID #BR25678, View Digital Pass & Share actions.", table_cell)],
        [Paragraph("26", table_cell), Paragraph("<b>Digital Booking Pass (QR)</b>", table_cell), Paragraph("Row 3: Checkout", table_cell), Paragraph("Digital perforated ticket card, scannable QR Code for host check-in, reference #DS-78219-CH, directions.", table_cell)],
        [Paragraph("27", table_cell), Paragraph("<b>My Bookings</b>", table_cell), Paragraph("Row 3: Account", table_cell), Paragraph("Tabs: Upcoming (2), Past (5), Cancelled (1); booking cards with View Pass & Cancel actions.", table_cell)],
        [Paragraph("28", table_cell), Paragraph("<b>Cancel Reservation</b>", table_cell), Paragraph("Row 3: Account", table_cell), Paragraph("Warning prompt, reservation summary, dropdown cancellation reasons, Confirm Cancel & Keep CTA.", table_cell)],
        [Paragraph("29", table_cell), Paragraph("<b>Rate & Review Experience</b>", table_cell), Paragraph("Row 3: Account", table_cell), Paragraph("5-star interactive rating, feedback praise tags, detailed comment area, +50 DinePoints reward bonus.", table_cell)],
        [Paragraph("30", table_cell), Paragraph("<b>Notifications Inbox</b>", table_cell), Paragraph("Row 3: Account", table_cell), Paragraph("Filter tabs (All, Bookings, Offers, Updates), timestamped interactive notification cards.", table_cell)],
        [Paragraph("31", table_cell), Paragraph("<b>User Profile</b>", table_cell), Paragraph("Row 3: Account", table_cell), Paragraph("Avatar, name (Sneha Patel), contact details, links to Bookings, Addresses, Settings, Logout.", table_cell)],
        [Paragraph("32", table_cell), Paragraph("<b>Account Settings</b>", table_cell), Paragraph("Row 4: Account", table_cell), Paragraph("Profile info, change password, push notification toggles, language, privacy policy, app version.", table_cell)],
        [Paragraph("33", table_cell), Paragraph("<b>Change Password & Security</b>", table_cell), Paragraph("Row 4: Security", table_cell), Paragraph("Current password, new password with strength meter, confirm password, 2-Factor Authentication toggle.", table_cell)],
        [Paragraph("34", table_cell), Paragraph("<b>Offers & Coupons</b>", table_cell), Paragraph("Row 4: Promotions", table_cell), Paragraph("Coupon cards: FLAT 20% OFF (DINE20), FLAT 15% OFF (STAY15), category tabs, one-tap Apply.", table_cell)],
        [Paragraph("35", table_cell), Paragraph("<b>Favorites Wishlist</b>", table_cell), Paragraph("Row 4: Discovery", table_cell), Paragraph("Saved restaurants, hotels, and party halls with instant booking shortcuts.", table_cell)],
        [Paragraph("36", table_cell), Paragraph("<b>Saved Addresses</b>", table_cell), Paragraph("Row 4: Account", table_cell), Paragraph("Home & Work address cards (Sector 26 / Sector 22 Chandigarh), '+ Add New Address' action.", table_cell)],
        [Paragraph("37", table_cell), Paragraph("<b>Help & Support</b>", table_cell), Paragraph("Row 4: Support", table_cell), Paragraph("Interactive FAQ accordion, Contact Form, Report Issue, Feedback, and Direct Call shortcut.", table_cell)],
        [Paragraph("38", table_cell), Paragraph("<b>No Results Found</b>", table_cell), Paragraph("Row 4: States", table_cell), Paragraph("Clean empty search illustration, helpful corrective tips, 'Clear Filters' recovery button.", table_cell)],
        [Paragraph("39", table_cell), Paragraph("<b>Loading State (List)</b>", table_cell), Paragraph("Row 4: States", table_cell), Paragraph("CSS shimmer skeleton cards matching restaurant and hotel search result layouts.", table_cell)],
        [Paragraph("40", table_cell), Paragraph("<b>Loading State (Grid)</b>", table_cell), Paragraph("Row 4: States", table_cell), Paragraph("Skeleton placeholders for image thumbnails and detail cards during network fetch.", table_cell)],
        [Paragraph("41", table_cell), Paragraph("<b>Error State</b>", table_cell), Paragraph("Row 4: States", table_cell), Paragraph("'Something Went Wrong' illustration, descriptive error message, 'Try Again' reload CTA.", table_cell)],
        [Paragraph("42", table_cell), Paragraph("<b>Empty Bookings</b>", table_cell), Paragraph("Row 4: States", table_cell), Paragraph("Folder/calendar icon, 'No Bookings Yet' notice, 'Explore Now' navigation shortcut.", table_cell)],
    ]

    t_screens = Table(screens_data, colWidths=[20, 115, 95, 257])
    t_screens.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_screens)

    story.append(PageBreak())

    # ================= PAGE 6: FUNCTIONAL SPECIFICATIONS =================
    story.append(Paragraph("7. Detailed Functional Specifications", sec_heading))
    
    story.append(Paragraph("7.1 Authentication & Security Module", subsec_heading))
    story.append(Paragraph("• <b>Dual User Registration:</b> Segregated signup workflows for Consumers and Business Partners with field validations.", bullet_text))
    story.append(Paragraph("• <b>OTP Phone Verification:</b> 6-digit cryptographic OTP generation with 5-minute expiry and 60-second resend cooldown.", bullet_text))
    story.append(Paragraph("• <b>Token Lifecycle:</b> JWT stateless tokens with 30-day refresh lifetime and instant revocation on logout/password change.", bullet_text))

    story.append(Paragraph("7.2 Search & Geolocation Discovery", subsec_heading))
    story.append(Paragraph("• <b>Multi-Criteria Query Engine:</b> Full-text fuzzy search across business names, menu items, cuisines, and landmark sectors.", bullet_text))
    story.append(Paragraph("• <b>Filter Combination:</b> Intersecting filters: Cuisine (North Indian, Italian, Continental), Rating (4.0+), Price Tiers (₹ to ₹₹₹₹), and Active Offers.", bullet_text))

    story.append(Paragraph("7.3 Dining Table Reservation Workflow", subsec_heading))
    story.append(Paragraph("• <b>Dynamic Slot Allocation:</b> Real-time checking against restaurant table limits for requested time (12:00 PM – 10:00 PM).", bullet_text))
    story.append(Paragraph("• <b>Reservation State Machine:</b> Pending → Confirmed → Seated → Completed / Cancelled.", bullet_text))
    story.append(Paragraph("• <b>Special Accommodations:</b> User request capture (e.g., 'Window seat, Anniversary decor').", bullet_text))

    story.append(Paragraph("7.4 Hotel Stay & Room Selection Engine", subsec_heading))
    story.append(Paragraph("• <b>Nightly Tariff Calculation:</b> Base room rate × Number of nights + 18% GST and municipal hospitality cess.", bullet_text))
    story.append(Paragraph("• <b>Room Inventory Locking:</b> 10-minute temporary checkout hold preventing double-booking during payment.", bullet_text))

    story.append(Paragraph("7.5 Payment Gateway Integration", subsec_heading))
    story.append(Paragraph("• <b>Supported Modes:</b> Unified Payments Interface (UPI via GPay, PhonePe, Paytm), Credit/Debit Cards (3D Secure 2.0), Net Banking (40+ Indian banks), and Wallets.", bullet_text))
    story.append(Paragraph("• <b>Webhook Reconciliation:</b> Automated server-to-server callback processing ensuring 100% booking confirmation accuracy.", bullet_text))

    story.append(Paragraph("7.6 Promotional Discount Engine", subsec_heading))
    story.append(Paragraph("• <b>Coupon Logic:</b> Validation of active date range, minimum cart amount, single-use per customer rules, and maximum discount caps.", bullet_text))

    story.append(PageBreak())

    # ================= PAGE 7: BUSINESS PORTALS & ADMIN =================
    story.append(Paragraph("8. Business Portals & Administration Console", sec_heading))
    story.append(Paragraph("In addition to the mobile app, the platform delivers three dedicated web management consoles:", body_text))

    story.append(Paragraph("8.1 Restaurant & Hotel Business Portal", subsec_heading))
    story.append(Paragraph("• <b>Operational Dashboard:</b> Real-time KPI cards for Today's Bookings, Expected Covers, Active Room Occupancy, and Daily Revenue.", bullet_text))
    story.append(Paragraph("• <b>Booking Management:</b> Color-coded calendar timeline view. Ability to accept walk-ins, mark no-shows, and cancel with remarks.", bullet_text))
    story.append(Paragraph("• <b>Profile & Catalog Builder:</b> Upload high-res photography, update business hours, and toggle menu item out-of-stock.", bullet_text))

    story.append(Paragraph("8.2 Central Administration Portal", subsec_heading))
    story.append(Paragraph("• <b>Partner Approval Pipeline:</b> Document viewer for FSSAI licenses, GSTIN validation, and bank passbooks before going live.", bullet_text))
    story.append(Paragraph("• <b>Commission & Payout Engine:</b> Configurable commission rates (e.g., 8% for dining, 12% for hotel bookings) with automated settlement logs.", bullet_text))
    story.append(Paragraph("• <b>Platform Audit & Security:</b> Immutable activity audit trail capturing every administrative modification.", bullet_text))

    story.append(Spacer(1, 10))
    story.append(Paragraph("9. Revenue Model", sec_heading))
    rev_data = [
        [Paragraph("Revenue Stream", table_header), Paragraph("Mechanism", table_header), Paragraph("Target Economics", table_header)],
        [Paragraph("<b>Transaction Commission</b>", table_cell), Paragraph("Percentage levied on confirmed hotel stays and dining vouchers.", table_cell), Paragraph("8% – 15% per confirmed booking", table_cell)],
        [Paragraph("<b>Featured Placement</b>", table_cell), Paragraph("Priority ranking on explore screen and top category badges.", table_cell), Paragraph("Monthly subscription (₹3,000 – ₹10,000 / mo)", table_cell)],
        [Paragraph("<b>Banquet Lead Generation</b>", table_cell), Paragraph("Fixed fee per qualified customer lead for high-ticket party halls.", table_cell), Paragraph("₹500 – ₹1,500 per verified event lead", table_cell)],
    ]
    t_rev = Table(rev_data, colWidths=[130, 207, 150])
    t_rev.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_rev)

    story.append(PageBreak())

    # ================= PAGE 8: NON-FUNCTIONAL REQUIREMENTS & TIMELINE =================
    story.append(Paragraph("10. Non-Functional Quality Requirements", sec_heading))
    
    nfr_data = [
        [Paragraph("Dimension", table_header), Paragraph("Requirement Specification", table_header), Paragraph("Verification Metric", table_header)],
        [Paragraph("<b>API Performance</b>", table_cell), Paragraph("Average response time under standard server load.", table_cell), Paragraph("&lt; 200ms latency (95th percentile)", table_cell)],
        [Paragraph("<b>Mobile Fluidity</b>", table_cell), Paragraph("Native 60 FPS transitions, skeleton shimmer during data load.", table_cell), Paragraph("Startup time &lt; 2.5s on mid-tier Android", table_cell)],
        [Paragraph("<b>Availability & Uptime</b>", table_cell), Paragraph("Redundant server deployment with automated failover.", table_cell), Paragraph("99.5% Service Level Agreement (SLA)", table_cell)],
        [Paragraph("<b>Data Security</b>", table_cell), Paragraph("OWASP top-10 mitigation, SQL injection guard, Argon2id passwords.", table_cell), Paragraph("Zero critical vulnerabilities on pen-test", table_cell)],
    ]
    t_nfr = Table(nfr_data, colWidths=[120, 217, 150])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_nfr)

    story.append(Spacer(1, 15))
    story.append(Paragraph("11. Project Implementation Timeline", sec_heading))
    story.append(Paragraph("The Phase-1 development schedule spans <b>45 to 60 working days</b> structured into six milestones:", body_text))

    time_data = [
        [Paragraph("Phase", table_header), Paragraph("Duration", table_header), Paragraph("Core Deliverables", table_header)],
        [Paragraph("<b>1. UI/UX & Wireframing</b>", table_cell), Paragraph("10 Working Days", table_cell), Paragraph("Complete 35 screens design system, brand assets, interactive click-through.", table_cell)],
        [Paragraph("<b>2. Database & API Engine</b>", table_cell), Paragraph("20 Working Days", table_cell), Paragraph("Laravel schema, JWT auth, business endpoints, booking state machine.", table_cell)],
        [Paragraph("<b>3. Mobile App Development</b>", table_cell), Paragraph("20 Working Days", table_cell), Paragraph("Flutter frontend for 35 screens, state management, payment gateway integration.", table_cell)],
        [Paragraph("<b>4. Web Admin & Partner Portals</b>", table_cell), Paragraph("15 Working Days", table_cell), Paragraph("ReactJS portals for business verification, reservations, and analytics.", table_cell)],
        [Paragraph("<b>5. QA & Security Audits</b>", table_cell), Paragraph("10 Working Days", table_cell), Paragraph("End-to-end integration testing, boundary edge tests, performance optimization.", table_cell)],
        [Paragraph("<b>6. Staging & Production Launch</b>", table_cell), Paragraph("5 Working Days", table_cell), Paragraph("Cloud server provisioning, CI/CD pipelines, Google Play & App Store submissions.", table_cell)],
    ]
    t_time = Table(time_data, colWidths=[140, 100, 247])
    t_time.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_time)

    story.append(PageBreak())

    # ================= PAGE 9: COMMERCIAL PROPOSAL & SIGN-OFF =================
    story.append(Paragraph("12. Commercial Proposal & Payment Milestones", sec_heading))
    
    comm_data = [
        [Paragraph("Particulars", table_header), Paragraph("Scope Covered", table_header), Paragraph("Amount (INR)", table_header)],
        [Paragraph("<b>Phase 1 MVP Development</b>", table_cell), Paragraph("Full Flutter Mobile App (35 Screens) + 3 Web Portals + Laravel Backend + Database + 3 Months Support", table_cell), Paragraph("<b>₹75,000</b>", table_cell)],
        [Paragraph("<b>Applicable GST</b>", table_cell), Paragraph("Standard Indian Goods & Services Tax (18% Extra)", table_cell), Paragraph("₹13,500", table_cell)],
        [Paragraph("<b>Total Investment</b>", table_cell), Paragraph("Comprehensive Phase 1 Turnkey Package", table_cell), Paragraph("<b>₹88,500</b>", table_cell)],
    ]
    t_comm = Table(comm_data, colWidths=[140, 227, 120])
    t_comm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t_comm)

    story.append(Spacer(1, 15))
    story.append(Paragraph("Payment Schedule", subsec_heading))

    pay_data = [
        [Paragraph("Milestone", table_header), Paragraph("Trigger / Deliverable Stage", table_header), Paragraph("Percentage", table_header), Paragraph("Amount", table_header)],
        [Paragraph("<b>Milestone 1</b>", table_cell), Paragraph("Project Initiation & Architecture Sign-Off", table_cell), Paragraph("20%", table_cell), Paragraph("₹15,000", table_cell)],
        [Paragraph("<b>Milestone 2</b>", table_cell), Paragraph("UI/UX Wireframes & 35 Screens Prototype Approval", table_cell), Paragraph("30%", table_cell), Paragraph("₹22,500", table_cell)],
        [Paragraph("<b>Milestone 3</b>", table_cell), Paragraph("Backend REST APIs & Portal Integration Completion", table_cell), Paragraph("20%", table_cell), Paragraph("₹15,000", table_cell)],
        [Paragraph("<b>Milestone 4</b>", table_cell), Paragraph("UAT Sign-off, App Store Build Delivery & Launch", table_cell), Paragraph("30%", table_cell), Paragraph("₹22,500", table_cell)],
    ]
    t_pay = Table(pay_data, colWidths=[90, 237, 75, 85])
    t_pay.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F4735")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pay)

    story.append(Spacer(1, 15))
    story.append(Paragraph("13. Warranty & Post-Launch Support", sec_heading))
    story.append(Paragraph(
        "Future IT Touch Pvt. Ltd. provides <b>3 Months of Complimentary Technical Support</b> commencing from the date of final delivery. "
        "Support covers defect resolution, bug fixes, and server performance optimization. Feature expansions and UI redesigns outside the 35 verified screens will be scoped separately.",
        body_text
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("14. Acceptance & Sign-Off", sec_heading))
    story.append(Paragraph(
        "This Software Requirements Specification serves as the binding contractual baseline for Phase-1 development of the DineStay Platform.",
        body_text
    ))

    sign_data = [
        [Paragraph("<b>Prepared By:</b>", table_cell), Paragraph("<b>Approved By:</b>", table_cell)],
        [Paragraph("<b>Future IT Touch Private Limited</b><br/>Sector 34 A, Chandigarh<br/><br/>Authorized Signatory: ___________________<br/><br/>Date: ___________________", table_cell),
         Paragraph("<b>Client Stakeholders / DineStay Platform</b><br/>Enterprise Client<br/><br/>Authorized Signatory: ___________________<br/><br/>Date: ___________________", table_cell)]
    ]
    t_sign = Table(sign_data, colWidths=[243, 244])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {filename} successfully!")

if __name__ == "__main__":
    build_pdf()
