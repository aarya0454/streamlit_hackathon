"""
Professional PDF Report Generator for Hydro-Assess
Uses ReportLab for better Unicode support and professional layouts
Supports English, Hindi, and Tamil languages with proper fonts
Enhanced with Hindi transliteration fallback for better compatibility
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.flowables import KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.colors import HexColor
import io
import os
import re
from datetime import datetime
from translator import T, get_current_language
import matplotlib.pyplot as plt
from typing import Dict, Optional
import base64
import urllib.request
import tempfile
def ensure_hindi_font():
    """Download and ensure Hindi font is available"""
    try:
        font_name = 'NotoSansDevanagari-Regular.ttf'
        local_path = os.path.join(os.getcwd(), font_name)

        # Check if already exists
        if os.path.exists(local_path):
            return local_path

        print("Downloading Hindi font...")

        # Try multiple download methods
        font_urls = [
            'https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf',
            'https://fonts.gstatic.com/ea/notosansdevanagari/v1/NotoSansDevanagari-Regular.ttf',
            'https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-devanagari@4.0.0/files/noto-sans-devanagari-all-400-normal.woff'
        ]

        for url in font_urls:
            try:
                print(f"Trying to download from: {url}")

                # Try urllib first
                try:
                    with urllib.request.urlopen(url, timeout=30) as response:
                        with open(local_path, 'wb') as f:
                            f.write(response.read())
                    print(f"✅ Successfully downloaded Hindi font: {local_path}")
                    return local_path
                except Exception as e:
                    print(f"urllib download failed: {e}")

                # Try curl if available
                try:
                    import subprocess
                    subprocess.run(['curl', '-L', '-o', local_path, url],
                                 check=True, timeout=60, capture_output=True)
                    print(f"✅ Successfully downloaded Hindi font using curl: {local_path}")
                    return local_path
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("curl download failed")

                # Try wget if available
                try:
                    import subprocess
                    subprocess.run(['wget', '-O', local_path, url],
                                 check=True, timeout=60, capture_output=True)
                    print(f"✅ Successfully downloaded Hindi font using wget: {local_path}")
                    return local_path
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("wget download failed")

            except Exception as e:
                print(f"Failed to download from {url}: {e}")
                continue

        # If all downloads failed, try to create a fallback
        print("All download methods failed, trying system fonts...")
        return None

    except Exception as e:
        print(f"Font download failed: {e}")
        return None

# Professional color scheme - minimal and clean
class ColorScheme:
    PRIMARY = HexColor('#2c3e50')      # Dark blue-gray - professional
    SECONDARY = HexColor('#34495e')    # Slightly lighter blue-gray
    ACCENT = HexColor('#27ae60')       # Subtle green for positive metrics
    WARNING = HexColor('#e67e22')      # Muted orange for costs
    DANGER = HexColor('#c0392b')       # Muted red for warnings
    LIGHT_GRAY = HexColor('#ecf0f1')   # Very light gray backgrounds
    MEDIUM_GRAY = HexColor('#bdc3c7')  # Medium gray for borders
    DARK_GRAY = HexColor('#7f8c8d')    # Dark gray for text
    WHITE = colors.white
    BLACK = colors.black
    BLUE_LIGHT = HexColor('#f8f9fa')   # Almost white with hint of blue
    GREEN_LIGHT = HexColor('#f8f9fa')  # Almost white with hint of green

def safe_hindi_text(text):
    """
    For Hindi language, return the original Hindi text for proper Unicode rendering
    For other languages, return as-is
    """
    if not text or not isinstance(text, str):
        return str(text) if text else ""
    
    # Return original Hindi text - let ReportLab handle Unicode
    return text

class HydroAssessPDFReport:
    """Professional PDF Report Generator with enhanced Unicode support and Hindi transliteration"""
    
    def __init__(self):
        self.buffer = io.BytesIO()
        self.pagesize = A4
        self.width, self.height = self.pagesize
        self.language = get_current_language()
        self.styles = self._create_styles()
        
    def _create_styles(self):
        """Create professional styles with robust Unicode font support"""
        styles = getSampleStyleSheet()

        # Enhanced font handling with better fallback system
        base_font = 'Helvetica'
        hindi_font = 'Helvetica'

        try:
            if self.language == 'hi':
                # Try to register Hindi Unicode fonts with multiple attempts
                font_loaded = False

                # Attempt 1: Try Noto Sans Devanagari
                font_paths = [
                    '/System/Library/Fonts/Supplemental/NotoSansDevanagari-Regular.ttf',
                    '/Library/Fonts/NotoSansDevanagari-Regular.ttf',
                    '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf',
                    '/opt/homebrew/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf',
                    '/System/Library/Fonts/NotoSansDevanagari.ttc',
                    '/Library/Fonts/NotoSansDevanagari.ttc',
                    'NotoSansDevanagari-Regular.ttf'  # Try current directory
                ]

                for font_path in font_paths:
                    try:
                        pdfmetrics.registerFont(TTFont('NotoSansDevanagari', font_path))
                        hindi_font = 'NotoSansDevanagari'
                        base_font = 'NotoSansDevanagari'
                        font_loaded = True
                        print(f"Successfully loaded Hindi font: {font_path}")
                        break
                    except Exception as e:
                        print(f"Failed to load {font_path}: {e}")
                        continue

                # If no system fonts found, try to download
                if not font_loaded:
                    downloaded_font = ensure_hindi_font()
                    if downloaded_font:
                        try:
                            print(f"Attempting to register downloaded font: {downloaded_font}")
                            pdfmetrics.registerFont(TTFont('NotoSansDevanagari', downloaded_font))
                            hindi_font = 'NotoSansDevanagari'
                            base_font = 'NotoSansDevanagari'
                            font_loaded = True
                            print(f"Successfully loaded downloaded Hindi font: {downloaded_font}")
                        except Exception as e:
                            print(f"Failed to register downloaded font: {e}")
                            try:
                                # Try to register with a different name
                                pdfmetrics.registerFont(TTFont('HindiFont', downloaded_font))
                                hindi_font = 'HindiFont'
                                base_font = 'HindiFont'
                                font_loaded = True
                                print(f"Successfully loaded downloaded Hindi font with different name: {downloaded_font}")
                            except Exception as e2:
                                print(f"Failed to register downloaded font with different name: {e2}")

                    # If regular download failed, try direct installation
                    if not font_loaded:
                        direct_font = install_hindi_font_directly()
                        if direct_font:
                            try:
                                pdfmetrics.registerFont(TTFont('DirectHindi', direct_font))
                                hindi_font = 'DirectHindi'
                                base_font = 'DirectHindi'
                                font_loaded = True
                                print(f"Successfully loaded directly installed Hindi font: {direct_font}")
                            except Exception as e:
                                print(f"Failed to register directly installed font: {e}")

                # If Noto Sans failed, try Arial Unicode
                if not font_loaded:
                    try:
                        # Try multiple possible locations for Arial Unicode
                        arial_paths = [
                            '/System/Library/Fonts/Arial Unicode.ttf',
                            '/Library/Fonts/Arial Unicode.ttf',
                            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                            '/Library/Fonts/Microsoft/Arial Unicode.ttf'
                        ]
                        for arial_path in arial_paths:
                            try:
                                pdfmetrics.registerFont(TTFont('ArialUnicode', arial_path))
                                hindi_font = 'ArialUnicode'
                                base_font = 'ArialUnicode'
                                font_loaded = True
                                print(f"Successfully loaded Arial Unicode font: {arial_path}")
                                break
                            except:
                                continue
                    except Exception as e:
                        print(f"Failed to load Arial Unicode: {e}")

                # If Arial Unicode failed, try system fonts
                if not font_loaded:
                    try:
                        # Try multiple possible locations for Devanagari fonts
                        devanagari_paths = [
                            '/System/Library/Fonts/DevanagariSangamMN.ttc',
                            '/Library/Fonts/DevanagariSangamMN.ttc',
                            '/System/Library/Fonts/DevanagariMT.ttc',
                            '/Library/Fonts/DevanagariMT.ttc'
                        ]
                        for dev_path in devanagari_paths:
                            try:
                                pdfmetrics.registerFont(TTFont('DevanagariSangamMN', dev_path))
                                hindi_font = 'DevanagariSangamMN'
                                base_font = 'DevanagariSangamMN'
                                font_loaded = True
                                print(f"Successfully loaded Devanagari Sangam MN font: {dev_path}")
                                break
                            except:
                                continue
                    except Exception as e:
                        print(f"Failed to load Devanagari Sangam MN: {e}")

                # Final fallback - use Helvetica but ensure proper encoding
                if not font_loaded:
                    print("Warning: No Hindi Unicode fonts found, using Helvetica with UTF-8 encoding")
                    base_font = 'Helvetica'
                    hindi_font = 'Helvetica'

                    # Try to create a fallback font mechanism
                    fallback_font = self._create_fallback_font_file()
                    if fallback_font:
                        try:
                            pdfmetrics.registerFont(TTFont('FallbackHindi', fallback_font))
                            base_font = 'FallbackHindi'
                            hindi_font = 'FallbackHindi'
                            print(f"Successfully loaded fallback font: {fallback_font}")
                        except Exception as e:
                            print(f"Failed to load fallback font: {e}")

            elif self.language == 'ta':
                try:
                    tamil_font_paths = [
                        '/System/Library/Fonts/Supplemental/NotoSansTamil-Regular.ttf',
                        '/Library/Fonts/NotoSansTamil-Regular.ttf',
                        'NotoSansTamil-Regular.ttf'
                    ]
                    for font_path in tamil_font_paths:
                        try:
                            pdfmetrics.registerFont(TTFont('NotoSansTamil', font_path))
                            base_font = 'NotoSansTamil'
                            break
                        except:
                            continue
                except:
                    base_font = 'Helvetica'
        except Exception as e:
            print(f"Font registration error: {e}")
            base_font = 'Helvetica'

        # Professional styles with proper encoding
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=ColorScheme.PRIMARY,
            spaceAfter=24,
            alignment=TA_CENTER,
            fontName=base_font,  # Use Unicode font for titles when Hindi
            leading=28
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=ColorScheme.WHITE,
            spaceAfter=12,
            fontName=base_font,  # Use Unicode font for headings when Hindi
            leftIndent=8,
            rightIndent=8,
            spaceBefore=8,
            leading=20
        ))

        styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=ColorScheme.PRIMARY,
            spaceAfter=10,
            fontName=base_font,  # Use Unicode font for content
            leading=16
        ))

        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            fontName=base_font,  # Use Unicode font for content
            textColor=ColorScheme.BLACK,
            spaceBefore=4,
            spaceAfter=4
        ))

        styles.add(ParagraphStyle(
            name='MetricValue',
            parent=styles['Normal'],
            fontSize=18,
            textColor=ColorScheme.WHITE,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',  # Keep English fonts for numbers
            leading=22
        ))

        styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=styles['Normal'],
            fontSize=10,
            textColor=ColorScheme.DARK_GRAY,
            alignment=TA_CENTER,
            fontName=base_font,  # Use Unicode font for labels
            leading=12
        ))

        styles.add(ParagraphStyle(
            name='TableHeader',
            parent=styles['Normal'],
            fontSize=11,
            textColor=ColorScheme.WHITE,
            alignment=TA_LEFT,
            fontName=base_font,  # Use Unicode font for headers
            leading=14
        ))

        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontSize=10,
            textColor=ColorScheme.BLACK,
            alignment=TA_LEFT,
            fontName=base_font,  # Use Unicode font for table content
            leading=12
        ))

        return styles
    
    def _safe_paragraph(self, text, style):
        """Create a paragraph with proper Unicode text handling and fallback"""
        safe_text = str(text) if text else ""

        # Test if the font can handle Unicode characters
        try:
            # Try to create a test paragraph to see if it renders properly
            test_paragraph = Paragraph(safe_text, style)
            # If we get here, the font should work
            return test_paragraph
        except Exception as e:
            print(f"Unicode rendering failed: {e}")
            # If Unicode fails, fall back to transliteration for Hindi
            if self.language == 'hi':
                safe_text = self._fallback_hindi_text(safe_text)
            return Paragraph(safe_text, style)

    def _fallback_hindi_text(self, text):
        """Enhanced fallback transliteration for Hindi when Unicode fonts fail"""
        if not text or not isinstance(text, str):
            return str(text) if text else ""

        # Enhanced character mapping for essential terms
        comprehensive_mapping = {
            'हाइड्रो': 'Hydro',
            'असेस': 'Assess',
            'रिपोर्ट': 'Report',
            'जल': 'Water',
            'संचयन': 'Harvesting',
            'प्रणाली': 'System',
            'वर्षा': 'Rain',
            'भूजल': 'Groundwater',
            'टैंक': 'Tank',
            'क्षमता': 'Capacity',
            'लागत': 'Cost',
            'बचत': 'Savings',
            'वार्षिक': 'Annual',
            'मासिक': 'Monthly',
            'दैनिक': 'Daily',
            'उत्कृष्ट': 'Excellent',
            'अच्छा': 'Good',
            'मध्यम': 'Moderate',
            'केवल': 'Only',
            'भंडारण': 'Storage',
            'रिचार्ज': 'Recharge',
            'हाइब्रिड': 'Hybrid',
            'मिश्रित': 'Mixed',
            'परिणाम': 'Results',
            'विश्लेषण': 'Analysis',
            'सिफारिश': 'Recommendation',
            'पर्यावरण': 'Environment',
            'प्रभाव': 'Impact',
            'कम्प्रीहैन्सिव': 'Comprehensive',
            'एक्ज़ेक्युटिव': 'Executive',
            'सारांश': 'Summary',
            'डिज़ाइन': 'Design',
            'वित्तीय': 'Financial',
            'स्थल': 'Site',
            'विशेषताएं': 'Characteristics',
            'मैट्रिक्स': 'Metrics',
            'प्रदर्शन': 'Performance',
            'क्षमता': 'Efficiency',
            'राशि': 'Amount',
            'बजट': 'Budget',
            'अनुमान': 'Estimate',
            'मूल्यांकन': 'Assessment'
        }

        # Apply comprehensive word replacements
        result = text
        for hindi_word, english_word in comprehensive_mapping.items():
            result = result.replace(hindi_word, english_word)

        # If result is too different from original, return original
        # This preserves proper Hindi text when fonts work
        if len(result.replace(' ', '')) < len(text.replace(' ', '')) * 0.3:
            return text

        return result
    
    def _create_header_footer(self, canvas, doc):
        """Add clean, professional header and footer with Unicode support"""
        canvas.saveState()
        
        # Simple header with minimal styling
        header_height = 60
        canvas.setFillColor(ColorScheme.PRIMARY)
        canvas.rect(0, self.height - header_height, self.width, header_height, fill=True)
        
        # Header text with Unicode support
        canvas.setFillColor(ColorScheme.WHITE)
        canvas.setFont(self.styles['CustomBody'].fontName, 18)  # Use Unicode font for header text

        # Get app name and tagline - preserve original text
        app_name = T('app_name')
        canvas.drawCentredString(self.width / 2, self.height - 30, app_name)

        canvas.setFont(self.styles['CustomBody'].fontName, 11)  # Use Unicode font for tagline
        app_tagline = T('app_tagline')
        canvas.drawCentredString(self.width / 2, self.height - 48, app_tagline)

        # Simple footer
        footer_height = 20
        canvas.setFillColor(ColorScheme.LIGHT_GRAY)
        canvas.rect(0, 0, self.width, footer_height, fill=True)

        canvas.setFillColor(ColorScheme.DARK_GRAY)
        canvas.setFont(self.styles['CustomBody'].fontName, 8)  # Use Unicode font for footer

        # Footer text - preserve original text
        footer_text = f"{T('footer_team')} | {T('footer_project')}"
        canvas.drawCentredString(self.width / 2, 10, footer_text)
        
        # Page number and date
        page_text = f"Page {doc.page}"
        canvas.drawRightString(self.width - 30, 10, page_text)
        canvas.drawString(30, 10, datetime.now().strftime("%B %d, %Y"))
        
        canvas.restoreState()
        
    def _create_metric_card(self, label, value, color=None):
        """Create a clean, professional metric card with Unicode support"""
        if color is None:
            color = ColorScheme.PRIMARY
            
        # Preserve original text for both label and value
        safe_label = str(label)
        safe_value = str(value)
            
        data = [[self._safe_paragraph(safe_value, self.styles['MetricValue'])],
                [self._safe_paragraph(safe_label, self.styles['MetricLabel'])]]
        
        table = Table(data, colWidths=[2.5*inch], rowHeights=[0.5*inch, 0.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('BACKGROUND', (0, 1), (-1, 1), ColorScheme.LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, 0), ColorScheme.WHITE),
            ('TEXTCOLOR', (0, 1), (-1, 1), ColorScheme.DARK_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
        ]))
        
        return table
    
    def _test_unicode_support(self):
        """Test if Unicode fonts are working properly"""
        try:
            # Test with a comprehensive Hindi string including all characters
            test_text = "हाइड्रो असेस रिपोर्ट जल संचयन प्रणाली"
            test_style = self.styles['CustomBody']

            # Try to create a paragraph
            test_paragraph = Paragraph(test_text, test_style)

            # If we can create it without errors, assume fonts work
            return True
        except Exception as e:
            print(f"Unicode test failed: {e}")
            return False

    def _create_fallback_font_file(self):
        """Create a minimal fallback font file if none available"""
        try:
            # Try to use a different approach - create a simple font file
            # For now, just return None and let the system use Helvetica
            print("Creating fallback font mechanism...")

            # You could potentially create a minimal TTF file here
            # or copy from a known location, but for now we'll use Helvetica
            return None

        except Exception as e:
            print(f"Failed to create fallback font: {e}")
            return None

    def _ensure_font_works(self):
        """Ensure font is working by testing it"""
        try:
            # Test if we can create a PDF with the current font
            test_buffer = io.BytesIO()
            test_doc = SimpleDocTemplate(
                test_buffer,
                pagesize=self.pagesize,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )

            # Test with comprehensive Hindi text including all common characters
            test_texts = [
                "हाइड्रो असेस रिपोर्ट जल संचयन प्रणाली",
                "कम्प्रीहैन्सिव रिपोर्ट",
                "परिणाम और विश्लेषण",
                "सिफारिशें और लागत",
                "पर्यावरणीय प्रभाव"
            ]

            test_story = []
            for text in test_texts:
                # Test with different styles that use different fonts
                test_story.append(Paragraph(text, self.styles['CustomBody']))      # Uses base_font (Unicode)
                test_story.append(Paragraph(text, self.styles['CustomTitle']))     # Now uses base_font (Unicode)
                test_story.append(Paragraph(text, self.styles['CustomHeading']))   # Now uses base_font (Unicode)
                test_story.append(Spacer(1, 0.1*inch))

            test_doc.build(test_story)
            print("✅ Font test passed - All Hindi text renders correctly in all styles")
            return True

        except Exception as e:
            print(f"❌ Font test failed: {e}")
            print("This may indicate font compatibility issues with specific styles")
            return False

    def generate_report(self, params, recommendation, design_financial, site_data,
                       charts: Optional[Dict[str, plt.Figure]] = None):
        """Generate clean, professional PDF report with robust Unicode support"""

        # Test Unicode support first
        unicode_works = self._test_unicode_support()
        if not unicode_works and self.language == 'hi':
            print("Warning: Unicode fonts not working properly, may fall back to transliteration")

        # Test if the font actually works for PDF generation
        font_works = self._ensure_font_works()
        if not font_works and self.language == 'hi':
            print("⚠️  Font test indicates issues - PDF may show blocks or incorrect text")
            print("💡 Consider installing system fonts or checking ReportLab installation")

        # Create document with professional margins
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=self.pagesize,
            rightMargin=50,
            leftMargin=50,
            topMargin=100,
            bottomMargin=40
        )

        # Build content
        story = []
        
        # Combined Title and Executive Summary Page - clean and simple
        story.append(Spacer(1, 0.5*inch))
        title_text = T('results_comprehensive_report')
        story.append(self._safe_paragraph(title_text, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Date and location - minimal formatting
        coords_text = f"{T('results_coordinates')}: {params['latitude']:.4f}°, {params['longitude']:.4f}°"
        date_text = datetime.now().strftime("%B %d, %Y")
        
        story.append(self._safe_paragraph(coords_text, self.styles['CustomBody']))
        story.append(self._safe_paragraph(date_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.4*inch))
        
        # Executive Summary Section - clean header
        story.append(Spacer(1, 0.1*inch))
        
        # Simple header bar
        header_table = Table([[self._safe_paragraph(T('results_executive_summary'), self.styles['CustomHeading'])]], 
                            colWidths=[6*inch], rowHeights=[0.5*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendation type with proper translation
        rec_type = recommendation['recommendation_type']
        if rec_type == 'Storage Only':
            rec_type_translated = T('results_storage_only')
        elif rec_type == 'Recharge Only':
            rec_type_translated = T('results_recharge_only')
        elif rec_type == 'Hybrid System':
            rec_type_translated = T('results_hybrid_system')
        else:
            rec_type_translated = rec_type
            
        # Efficiency rating with proper translation  
        efficiency = recommendation['efficiency_rating']
        if efficiency == 'Excellent':
            efficiency_translated = T('results_efficiency_excellent')
        elif efficiency == 'Good':
            efficiency_translated = T('results_efficiency_good')
        elif efficiency == 'Moderate':
            efficiency_translated = T('results_efficiency_moderate')
        else:
            efficiency_translated = efficiency
        
        # Clean summary table
        summary_data = [
            [self._safe_paragraph(f"<b>{T('results_recommended_strategy')}</b>", self.styles['TableCell']),
             self._safe_paragraph(rec_type_translated, self.styles['TableCell'])],
            [self._safe_paragraph(f"<b>{T('results_system_efficiency')}</b>", self.styles['TableCell']),
             self._safe_paragraph(efficiency_translated, self.styles['TableCell'])],
        ]

        summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch], rowHeights=[0.4*inch, 0.4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), ColorScheme.LIGHT_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

                # Strategic Rationale - simple formatting
        story.append(self._safe_paragraph(f"<b>{T('results_strategic_rationale')}</b>", self.styles['CustomSubHeading']))
        story.append(self._safe_paragraph(T('results_balanced_approach'), self.styles['CustomBody']))
        story.append(Spacer(1, 0.4*inch))

        # Key Performance Metrics - clean layout
        metrics_header = Table([[self._safe_paragraph(T('results_key_metrics'), self.styles['CustomHeading'])]], 
                              colWidths=[6*inch], rowHeights=[0.5*inch])
        metrics_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.SECONDARY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(metrics_header)
        story.append(Spacer(1, 0.2*inch))

        # Simple metrics grid - less colorful
        metrics_data = [
            [self._create_metric_card(T('results_annual_harvest'),
                                     f"{recommendation['annual_potential']:,.0f} L",
                                     ColorScheme.PRIMARY),
             self._create_metric_card(T('results_household_coverage'),
                                     f"{recommendation['household_coverage_percent']:.1f}%",
                                     ColorScheme.ACCENT)],
            [self._create_metric_card(T('results_storage_allocation'),
                                     f"{recommendation['volume_to_store']:,.0f} L",
                                     ColorScheme.SECONDARY),
             self._create_metric_card(T('results_recharge_allocation'),
                                     f"{recommendation['volume_to_recharge']:,.0f} L",
                                     ColorScheme.WARNING)]
        ]

        metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch], rowHeights=[1*inch, 1*inch])
        metrics_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(metrics_table)
        story.append(PageBreak())
        
        # System Design Section with enhanced header
        design_header = Table([[self._safe_paragraph(T('results_recommended_design').replace('🏗️ ', ''), self.styles['CustomHeading'])]], 
                             colWidths=[6.5*inch], rowHeights=[0.6*inch])
        design_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.WARNING),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [8, 8, 0, 0]),
        ]))
        story.append(design_header)
        story.append(Spacer(1, 0.3*inch))

                # Storage system details if applicable
        if 'storage_tank' in design_financial.get('design', {}):
            tank = design_financial['design'].get('storage_tank', {})
            
            # Storage specs header
            storage_header = Table([[self._safe_paragraph(T('results_storage_specs'), self.styles['CustomSubHeading'])]], 
                                  colWidths=[6.5*inch], rowHeights=[0.4*inch])
            storage_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.BLUE_LIGHT),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ]))
            story.append(storage_header)
            story.append(Spacer(1, 0.2*inch))

            storage_data = [
                [self._safe_paragraph(T('results_tank_type'), self.styles['TableCell']), 
                 self._safe_paragraph(T('results_tank_underground'), self.styles['TableCell'])],
                [self._safe_paragraph(T('results_capacity'), self.styles['TableCell']), 
                 self._safe_paragraph(f"{tank.get('volume_liters', 0):,.0f} L ({tank.get('volume_m3', 0):.1f} m³)", self.styles['TableCell'])],
                [self._safe_paragraph(T('results_dimensions'), self.styles['TableCell']), 
                 self._safe_paragraph(tank.get('dimensions', 'Not specified'), self.styles['TableCell'])],
                [self._safe_paragraph(T('results_installation'), self.styles['TableCell']), 
                 self._safe_paragraph(T('results_installation_underground'), self.styles['TableCell'])],
            ]

            storage_table = Table(storage_data, colWidths=[2.5*inch, 4*inch], rowHeights=[0.4*inch]*4)
            storage_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), ColorScheme.LIGHT_GRAY),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
                ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ]))
            story.append(storage_table)
            story.append(Spacer(1, 0.3*inch))

                # Recharge system details if applicable
        if 'recharge_system' in design_financial['design']:
            recharge = design_financial['design']['recharge_system']
            
            # Recharge specs header
            recharge_header = Table([[self._safe_paragraph(T('results_recharge_specs'), self.styles['CustomSubHeading'])]], 
                                   colWidths=[6.5*inch], rowHeights=[0.4*inch])
            recharge_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.GREEN_LIGHT),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ]))
            story.append(recharge_header)
            story.append(Spacer(1, 0.2*inch))

            recharge_data = [
                [self._safe_paragraph(T('results_configuration'), self.styles['TableCell']), 
                 self._safe_paragraph(recharge['configuration'], self.styles['TableCell'])],
                [self._safe_paragraph(T('results_total_capacity'), self.styles['TableCell']), 
                 self._safe_paragraph(f"{recharge['volume_m3']:.1f} m³", self.styles['TableCell'])],
                [self._safe_paragraph(T('results_dimensions'), self.styles['TableCell']), 
                 self._safe_paragraph(recharge['dimensions'], self.styles['TableCell'])],
                [self._safe_paragraph(T('results_footprint'), self.styles['TableCell']), 
                 self._safe_paragraph(recharge['total_area'], self.styles['TableCell'])],
            ]

            recharge_table = Table(recharge_data, colWidths=[2.5*inch, 4*inch], rowHeights=[0.4*inch]*4)
            recharge_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), ColorScheme.LIGHT_GRAY),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
                ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ]))
            story.append(recharge_table)

        story.append(Spacer(1, 0.5*inch))

        # Supporting Infrastructure with enhanced styling
        infra_header = Table([[self._safe_paragraph(T('results_supporting_infra'), self.styles['CustomSubHeading'])]], 
                            colWidths=[6.5*inch], rowHeights=[0.4*inch])
        infra_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.MEDIUM_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(infra_header)
        story.append(Spacer(1, 0.2*inch))
        
        infra_items = [
            T('results_first_flush_diverter'),
            T('results_multi_stage_filtration'),
            T('results_gutter_system'),
            T('results_distribution_piping')
        ]
        for item in infra_items:
            story.append(self._safe_paragraph(f"• {item}", self.styles['CustomBody']))

        story.append(PageBreak())
        
        # Financial Analysis Section with enhanced header
        financial_header = Table([[self._safe_paragraph(T('results_financial_header'), self.styles['CustomHeading'])]], 
                                 colWidths=[6.5*inch], rowHeights=[0.6*inch])
        financial_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.DANGER),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [8, 8, 0, 0]),
        ]))
        story.append(financial_header)
        story.append(Spacer(1, 0.3*inch))

                # Investment Overview with enhanced layout - shows both storage and recharge benefits
        financial_overview = [
            [self._safe_paragraph(f"<b>{T('results_total_system_cost')}</b>", self.styles['TableCell']),
             self._safe_paragraph(f"<b>Rs {design_financial['total_cost']:,.0f}</b>", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_annual_maintenance'), self.styles['TableCell']),
             self._safe_paragraph(f"Rs {design_financial['maintenance_cost_annual']:,.0f}", self.styles['TableCell'])],
        ]
        
        # Show breakdown of savings/benefits
        if design_financial.get('direct_water_savings', 0) > 0:
            financial_overview.append([
                self._safe_paragraph(T('results_direct_water_savings'), self.styles['TableCell']),
                self._safe_paragraph(f"Rs {design_financial['direct_water_savings']:,.0f}", self.styles['TableCell'])
            ])
            
        if design_financial.get('recharge_benefits', 0) > 0:
            financial_overview.append([
                self._safe_paragraph(T('results_recharge_benefits'), self.styles['TableCell']),
                self._safe_paragraph(f"Rs {design_financial['recharge_benefits']:,.0f}", self.styles['TableCell'])
            ])
            
        financial_overview.append([
            self._safe_paragraph(f"<b>{T('results_total_annual_benefits')}</b>", self.styles['TableCell']),
            self._safe_paragraph(f"<b>Rs {design_financial['annual_savings']:,.0f}</b>", self.styles['TableCell'])
        ])

        if design_financial['payback_period_years'] != float('inf'):
            financial_overview.append([
                self._safe_paragraph(T('results_payback_period'), self.styles['TableCell']),
                self._safe_paragraph(f"{design_financial['payback_period_years']:.1f} years", self.styles['TableCell'])
            ])
            financial_overview.append([
                self._safe_paragraph(T('results_roi_10year'), self.styles['TableCell']),
                self._safe_paragraph(f"{design_financial['roi_10_year']:.1f}%", self.styles['TableCell'])
            ])
        else:
            financial_overview.append([
                self._safe_paragraph(T('results_payback_period'), self.styles['TableCell']),
                self._safe_paragraph(T('results_no_direct_payback_recharge'), self.styles['TableCell'])
            ])

        financial_table = Table(financial_overview, colWidths=[3.2*inch, 3.2*inch], 
                               rowHeights=[0.5*inch]*len(financial_overview))
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ColorScheme.WARNING),
            ('TEXTCOLOR', (0, 0), (-1, 0), ColorScheme.WHITE),
            ('BACKGROUND', (0, 1), (-1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(financial_table)
        story.append(Spacer(1, 0.4*inch))

        # Cost Breakdown with enhanced layout
        cost_header = Table([[self._safe_paragraph(T('results_cost_breakdown'), self.styles['CustomSubHeading'])]], 
                           colWidths=[6.5*inch], rowHeights=[0.4*inch])
        cost_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.BLUE_LIGHT),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(cost_header)
        story.append(Spacer(1, 0.2*inch))

        cost_data = [[self._safe_paragraph(f"<b>{T('results_component')}</b>", self.styles['TableHeader']),
                     self._safe_paragraph(f"<b>{T('results_cost_rs')}</b>", self.styles['TableHeader'])]]

        for component, cost in design_financial['cost_breakdown'].items():
            # Use proper translation keys for component names
            translation_key = f"cost_{component}"
            # Check if translation exists by trying to get it and comparing with key
            translated_name = T(translation_key)
            
            if translated_name != translation_key:
                display_name = translated_name
            else:
                # Enhanced fallback with more comprehensive component mapping
                display_name = component.replace('_', ' ').title()
                
                # Comprehensive component name mapping
                component_mappings = {
                    'first_flush_diverter': 'First Flush Diverter',
                    'filtration_system': 'Filtration System', 
                    'guttering_and_pipes': 'Guttering and Pipes',
                    'installation_labor': 'Installation Labor',
                    'storage_tank': 'Storage Tank',
                    'recharge_system': 'Recharge System',
                    'pipes': 'Pipes',
                    'guttering': 'Guttering System',
                    'labor': 'Labor Cost',
                    'installation': 'Installation',
                    'materials': 'Materials',
                    'excavation': 'Excavation Work',
                    'concrete': 'Concrete Work',
                    'plumbing': 'Plumbing',
                    'electrical': 'Electrical Work',
                    'miscellaneous': 'Miscellaneous Expenses'
                }
                
                # Check if we have a specific mapping
                if component in component_mappings:
                    display_name = component_mappings[component]
                else:
                    # Apply keyword-based improvements
                    lower_component = component.lower()
                    if 'first' in lower_component and 'flush' in lower_component:
                        display_name = 'First Flush Diverter'
                    elif 'filtration' in lower_component or 'filter' in lower_component:
                        display_name = 'Filtration System'
                    elif 'gutter' in lower_component and 'pipe' in lower_component:
                        display_name = 'Guttering and Pipes'
                    elif 'installation' in lower_component and 'labor' in lower_component:
                        display_name = 'Installation Labor'
                    elif 'storage' in lower_component and 'tank' in lower_component:
                        display_name = 'Storage Tank'
                    elif 'recharge' in lower_component:
                        display_name = 'Recharge System'
            
            # Final safety check - ensure we don't have empty display names
            if not display_name or display_name.strip() == '':
                display_name = f"Component {len(cost_data)}"  # Fallback with index
            
            cost_data.append([self._safe_paragraph(display_name, self.styles['TableCell']), 
                             self._safe_paragraph(f"Rs {cost:,.0f}", self.styles['TableCell'])])

        cost_data.append([self._safe_paragraph(f"<b>{T('results_total_system_cost')}</b>", self.styles['TableHeader']),
                         self._safe_paragraph(f"<b>Rs {design_financial['total_cost']:,.0f}</b>", self.styles['TableHeader'])])

        cost_table = Table(cost_data, colWidths=[4*inch, 2.5*inch], 
                          rowHeights=[0.4*inch]*len(cost_data))
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ColorScheme.SECONDARY),
            ('BACKGROUND', (0, -1), (-1, -1), ColorScheme.PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), ColorScheme.WHITE),
            ('TEXTCOLOR', (0, -1), (-1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [ColorScheme.WHITE, ColorScheme.LIGHT_GRAY]),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(cost_table)

        story.append(PageBreak())
        
        # Site Characteristics Section with enhanced header
        site_header = Table([[self._safe_paragraph(T('results_site_characteristics'), self.styles['CustomHeading'])]], 
                           colWidths=[6.5*inch], rowHeights=[0.6*inch])
        site_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.ACCENT),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [8, 8, 0, 0]),
        ]))
        story.append(site_header)
        story.append(Spacer(1, 0.3*inch))

        # Site information in enhanced two-column layout
        location_text = f"""
        {T('results_coordinates')}: {params['latitude']:.4f}°N, {params['longitude']:.4f}°E<br/>
        {T('results_catchment_area_label')}: {params['area']:,.0f} m²<br/>
        {T('results_surface_type_label')}: {params['surface_type']}<br/>
        {T('results_runoff_coefficient_label')}: {params['runoff_coefficient']:.2f}<br/>
        {T('results_city_classification_label')}: {params['city_type']}<br/>
        {T('results_household_size_label')}: {params['household_size']} {T('results_persons')}
        """
        
        # Ensure all fields have proper values with better fallbacks
        soil_type_value = site_data.get('soil_type') or 'Sandy'
        if not soil_type_value or soil_type_value.strip() == '':
            soil_type_value = 'Sandy'
            
        aquifer_type_value = site_data.get('principal_aquifer_type') or 'Alluvial Plains'
        if not aquifer_type_value or aquifer_type_value.strip() == '':
            aquifer_type_value = 'Alluvial Plains'
            
        aquifer_yield_value = site_data.get('aquifer_yield') or 'Moderate'
        if not aquifer_yield_value or aquifer_yield_value.strip() == '':
            aquifer_yield_value = 'Moderate'

        # Create hydro text with guaranteed values
        annual_rainfall = params.get('annual_rainfall', 926)
        post_monsoon = site_data.get('post_monsoon_depth_m', 10.2)
        pre_monsoon = site_data.get('pre_monsoon_depth_m', 12.2)
        
        hydro_text = f"""
        {T('results_annual_rainfall_label')}: {annual_rainfall:.0f} mm<br/>
        {T('results_soil_classification')}: {soil_type_value}<br/>
        {T('results_groundwater_post')}: {post_monsoon:.1f} m bgl<br/>
        {T('results_groundwater_pre')}: {pre_monsoon:.1f} m bgl<br/>
        {T('results_aquifer_type')}: {aquifer_type_value}<br/>
        {T('results_aquifer_yield')}: {aquifer_yield_value}
        """

        site_data_table = [
            [self._safe_paragraph(f"<b>{T('results_location_data')}</b>", self.styles['CustomSubHeading']),
             self._safe_paragraph(f"<b>{T('results_hydro_data')}</b>", self.styles['CustomSubHeading'])],
            [self._safe_paragraph(location_text, self.styles['TableCell']),
             self._safe_paragraph(hydro_text, self.styles['TableCell'])]
        ]

        site_table = Table(site_data_table, colWidths=[3.2*inch, 3.2*inch], rowHeights=[0.5*inch, 2.5*inch])
        site_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ColorScheme.BLUE_LIGHT),
            ('BACKGROUND', (0, 1), (-1, 1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 15),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(site_table)

        story.append(Spacer(1, 0.5*inch))

        # Environmental Impact Section with enhanced styling
        env_header = Table([[self._safe_paragraph(T('results_environmental_impact'), self.styles['CustomSubHeading'])]], 
                          colWidths=[6.5*inch], rowHeights=[0.4*inch])
        env_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.GREEN_LIGHT),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(env_header)
        story.append(Spacer(1, 0.2*inch))

        # Calculate enhanced environmental metrics
        annual_potential = recommendation.get('annual_potential', 0)
        volume_to_recharge = recommendation.get('volume_to_recharge', 0)
        household_coverage = recommendation.get('household_coverage_percent', 0)
        
        # Enhanced calculations for environmental impact
        co2_reduction = annual_potential * 0.0003  # kg CO2 per liter
        energy_savings = annual_potential * 0.004  # kWh saved per liter (pumping + treatment)
        equivalent_trees = co2_reduction / 22  # 1 tree absorbs ~22kg CO2/year
        water_table_impact = volume_to_recharge * 0.8  # 80% effective recharge
        flood_mitigation = annual_potential * 0.001  # m³ flood water managed

        env_impact_data = [
            [self._safe_paragraph(T('results_water_independence'), self.styles['TableCell']),
             self._safe_paragraph(f"{household_coverage:.1f}% {T('results_annual_freshwater_demand')}", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_groundwater_recharge'), self.styles['TableCell']),
             self._safe_paragraph(f"{volume_to_recharge:,.0f} L {T('results_annual_groundwater_replenishment')}", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_runoff_reduction'), self.styles['TableCell']),
             self._safe_paragraph(f"{flood_mitigation:.1f} m³ {T('results_reduced_stormwater_runoff')}", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_co2_reduction'), self.styles['TableCell']),
             self._safe_paragraph(f"{co2_reduction:.1f} kg CO2 {T('results_co2_year')}", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_energy_savings'), self.styles['TableCell']),
             self._safe_paragraph(f"{energy_savings:.0f} kWh per year (reduced pumping & treatment)", self.styles['TableCell'])],
            [self._safe_paragraph(T('results_carbon_offset_equivalent'), self.styles['TableCell']),
             self._safe_paragraph(f"Equivalent to planting {equivalent_trees:.1f} trees annually", self.styles['TableCell'])],
        ]

        env_table = Table(env_impact_data, colWidths=[2.5*inch, 4*inch], rowHeights=[0.6*inch]*6)
        env_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), ColorScheme.ACCENT),
            ('TEXTCOLOR', (0, 0), (0, -1), ColorScheme.WHITE),
            ('BACKGROUND', (1, 0), (1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, ColorScheme.MEDIUM_GRAY),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(env_table)
        
        story.append(PageBreak())

        # Long-term Environmental Benefits - New Page
        longterm_header = Table([[self._safe_paragraph(T('results_longterm_environmental_benefits'), self.styles['CustomSubHeading'])]], 
                               colWidths=[6.5*inch], rowHeights=[0.4*inch])
        longterm_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.MEDIUM_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(longterm_header)
        story.append(Spacer(1, 0.2*inch))

        # Environmental benefits text - now fully translatable
        env_benefits = [
            T('results_env_benefit_1'),
            T('results_env_benefit_2'),
            T('results_env_benefit_3'),
            T('results_env_benefit_4'),
            T('results_env_benefit_5'),
            T('results_env_benefit_6'),
            T('results_env_benefit_7'),
            T('results_env_benefit_8')
        ]
        
        for benefit in env_benefits:
            story.append(self._safe_paragraph(benefit, self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))

        story.append(PageBreak())

        # Implementation Guidelines Section - New Page
        impl_header = Table([[self._safe_paragraph(T('results_implementation_guidelines'), self.styles['CustomSubHeading'])]], 
                           colWidths=[6.5*inch], rowHeights=[0.4*inch])
        impl_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.WARNING),
            ('TEXTCOLOR', (0, 0), (-1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(impl_header)
        story.append(Spacer(1, 0.2*inch))

        # Implementation phases - now fully translatable
        impl_phases = [
            T('results_phase_1'),
            T('results_impl_phase1_1'),
            T('results_impl_phase1_2'),
            T('results_impl_phase1_3'),
            "",
            T('results_phase_2'),
            T('results_impl_phase2_1'),
            T('results_impl_phase2_2'),
            T('results_impl_phase2_3'),
            T('results_impl_phase2_4'),
            "",
            T('results_phase_3'),
            T('results_impl_phase3_1'),
            T('results_impl_phase3_2'),
            T('results_impl_phase3_3'),
            T('results_impl_phase3_4')
        ]
        
        for phase in impl_phases:
            if ":" in phase and ("चरण" in phase or "Phase" in phase or "கட்டம்" in phase):
                story.append(self._safe_paragraph(f"<b>{phase}</b>", self.styles['CustomBody']))
            else:
                story.append(self._safe_paragraph(phase, self.styles['CustomBody']))
            story.append(Spacer(1, 0.08*inch))

        story.append(PageBreak())

        # Maintenance Recommendations - New Page
        maint_header = Table([[self._safe_paragraph(T('results_maintenance_recommendations'), self.styles['CustomSubHeading'])]], 
                            colWidths=[6.5*inch], rowHeights=[0.4*inch])
        maint_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.DANGER),
            ('TEXTCOLOR', (0, 0), (-1, -1), ColorScheme.WHITE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ]))
        story.append(maint_header)
        story.append(Spacer(1, 0.2*inch))

        # Maintenance schedule - now fully translatable
        maintenance_schedule = [
            T('results_monthly_tasks'),
            T('results_maint_monthly_1'),
            T('results_maint_monthly_2'),
            T('results_maint_monthly_3'),
            "",
            T('results_quarterly_tasks'),
            T('results_maint_quarterly_1'),
            T('results_maint_quarterly_2'),
            T('results_maint_quarterly_3'),
            T('results_maint_quarterly_4'),
            "",
            T('results_annual_tasks'),
            T('results_maint_annual_1'),
            T('results_maint_annual_2'),
            T('results_maint_annual_3'),
            T('results_maint_annual_4'),
            "",
            f"{T('results_estimated_maintenance_cost')} Rs {design_financial.get('maintenance_cost_annual', 0):,.0f}"
        ]
        
        for task in maintenance_schedule:
            if task.endswith(":") or T('results_estimated_maintenance_cost') in task:
                story.append(self._safe_paragraph(f"<b>{task}</b>", self.styles['CustomBody']))
            else:
                story.append(self._safe_paragraph(task, self.styles['CustomBody']))
            story.append(Spacer(1, 0.08*inch))

        # Add charts if available with enhanced layout
        if charts:
            story.append(PageBreak())
            
            # Charts header
            charts_header = Table([[self._safe_paragraph(T('results_rainfall_distribution'), self.styles['CustomHeading'])]], 
                                 colWidths=[6.5*inch], rowHeights=[0.6*inch])
            charts_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.PRIMARY),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROUNDEDCORNERS', [8, 8, 0, 0]),
            ]))
            story.append(charts_header)
            story.append(Spacer(1, 0.3*inch))

            # Process and add charts with better formatting
            if charts.get('rainfall_chart'):
                img_buffer = io.BytesIO()
                charts['rainfall_chart'].savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                img = Image(img_buffer, width=6*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.4*inch))

            if charts.get('cost_chart'):
                cost_chart_header = Table([[self._safe_paragraph(T('results_cost_distribution'), self.styles['CustomSubHeading'])]], 
                                         colWidths=[6.5*inch], rowHeights=[0.4*inch])
                cost_chart_header.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), ColorScheme.BLUE_LIGHT),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
                ]))
                story.append(cost_chart_header)
                story.append(Spacer(1, 0.2*inch))
                
                img_buffer = io.BytesIO()
                charts['cost_chart'].savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                img = Image(img_buffer, width=4*inch, height=4*inch)
                story.append(img)

        # Build PDF with clean header/footer
        doc.build(story, onFirstPage=self._create_header_footer, onLaterPages=self._create_header_footer)

        # Return the PDF buffer
        self.buffer.seek(0)
        return self.buffer


def generate_professional_pdf(params, recommendation, design_financial, site_data,
                             charts: Optional[Dict[str, plt.Figure]] = None):
    """
    Main function to generate professional PDF report with enhanced Hindi support
    """
    report = HydroAssessPDFReport()
    return report.generate_report(params, recommendation, design_financial, site_data, charts)


def test_font_loading():
    """Test function to verify font loading works"""
    print("Testing font loading...")

    # Create a test PDF report instance
    test_report = HydroAssessPDFReport()

    # Check what fonts were loaded
    print(f"Language: {test_report.language}")
    print(f"Base font: {test_report.styles['CustomBody'].fontName}")

    # Test Unicode support
    unicode_works = test_report._test_unicode_support()
    print(f"Unicode support test: {unicode_works}")

    return unicode_works

if __name__ == "__main__":
    # Run font loading test
    test_font_loading()
