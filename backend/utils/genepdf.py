from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# from reportlab.lib.fon
# pdfmetrics.registerFont(TTFont('pingbold', 'PingBold.ttf'))
# pdfmetrics.registerFont(TTFont('ping', 'ping.ttf'))
# pdfmetrics.registerFont(TTFont('hv', 'Helvetica.ttf'))
import os

# 生成PDF文件
class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.file_path = os.path.abspath(os.path.curdir)
        self.title_style = ParagraphStyle(
            name="TitleStyle", fontSize=48, alignment=TA_LEFT
        )
        self.sub_title_style = ParagraphStyle(
            name="SubTitleStyle",
            fontSize=32,
            textColor=colors.HexColor(0x666666),
            alignment=TA_LEFT,
        )
        self.content_style = ParagraphStyle(
            name="ContentStyle",
            fontSize=18,
            leading=25,
            spaceAfter=20,
            underlineWidth=1,
            alignment=TA_LEFT,
        )
        self.foot_style = ParagraphStyle(
            name="FootStyle",
            fontSize=14,
            textColor=colors.HexColor(0xB4B4B4),
            leading=25,
            spaceAfter=20,
            alignment=TA_CENTER,
        )
        self.table_title_style = ParagraphStyle(
            name="TableTitleStyle",
            fontSize=20,
            leading=25,
            spaceAfter=10,
            alignment=TA_LEFT,
        )
        self.sub_table_style = ParagraphStyle(
            name="SubTableTitleStyle",
            fontSize=16,
            leading=25,
            spaceAfter=10,
            alignment=TA_LEFT,
        )

    def genTaskPDF(self, home_data):
        story = []
        # 首页内容
        story.append(Spacer(1, 20 * mm))
        # img = Image('/xxx/xxx.png')
        # img.drawHeight = 20 * mm
        # img.drawWidth = 40 * mm
        # img.hAlign = TA_LEFT
        # story.append(img)
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("Order", self.title_style))
        story.append(Spacer(1, 20 * mm))
        story.append(Paragraph("Designed by lovehome", self.sub_title_style))
        story.append(Spacer(1, 45 * mm))
        story.append(
            Paragraph("OrderId : " + home_data["report_code"], self.content_style)
        )
        story.append(
            Paragraph("OrderPath : " + home_data["task_name"], self.content_style)
        )
        story.append(
            Paragraph("CustomId : " + home_data["report_date"], self.content_style)
        )
        story.append(
            Paragraph(
                "CustomTelephone : " + home_data["report_creator"], self.content_style
            )
        )
        story.append(
            Paragraph(
                "CustomAddress : " + home_data["report_creator"], self.content_style
            )
        )
        story.append(
            Paragraph("OrderType : " + home_data["report_creator"], self.content_style)
        )

        story.append(Spacer(1, 40 * mm))
        story.append(Paragraph("Copyright by lovehome", self.foot_style))
        story.append(PageBreak())
        doc = SimpleDocTemplate(
            self.file_path + "/" + self.filename + ".pdf",
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )
        doc.build(story)


pdf = PDFGenerator("text")
home_data = {
    "report_code": "report_code",
    "task_name": "task_name",
    "report_date": "report_date",
    "report_creator": "report_creator",
}
pdf.genTaskPDF(home_data)
