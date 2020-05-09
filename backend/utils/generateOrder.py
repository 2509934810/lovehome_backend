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
    def __init__(self, filename, filepath):
        self.filename = filename
        self.file_path = filepath
        self.title_style = ParagraphStyle(
            name="TitleStyle", fontSize=48, alignment=TA_CENTER
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

    def genTaskPDF(self, order):
        story = []
        # 首页内容
        story.append(Spacer(1, 20 * mm))
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("Order", self.title_style))
        story.append(Spacer(1, 20 * mm))
        story.append(Paragraph("Designed by lovehome", self.sub_title_style))
        story.append(Spacer(1, 45 * mm))
        story.append(Paragraph("OrderId : " + order.id, self.content_style))
        story.append(
            Paragraph("OrderPath : " + order.info.live_addr, self.content_style)
        )
        story.append(
            Paragraph(
                "CustomName : " + order.baseuser.user.username, self.content_style
            )
        )
        story.append(
            Paragraph(
                "CustomTelephone : " + order.baseuser.user.telephone, self.content_style
            )
        )
        story.append(
            Paragraph(
                "CustomAddress : " + order.baseuser.user.username, self.content_style
            )
        )
        story.append(
            Paragraph("OrderType : " + str(order.info.serviceType), self.content_style)
        )

        story.append(Spacer(1, 40 * mm))
        story.append(Paragraph("Copyright by lovehome", self.foot_style))
        story.append(PageBreak())
        doc = SimpleDocTemplate(
            self.file_path + self.filename + ".pdf",
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )
        doc.build(story)


# class Order(object)
#     def __init__(self, orderId, OrderPath, CustomName, CustomTelephone, CustomAddress, OrderType):
#         self.orderId=orderId
#         self.OrderPath = OrderPath
#         self.CustomName = CustomName
#         self.CustomTelephone = CustomTelephone
#         self.CustomAddress = CustomAddress
#         self.OrderType = OrderType

# order = Order(orderId="123", OrderPath= "./", CustomName="123", CustomTelephone="123", CustomAddress="123", OrderType="123")
# pdf = PDFGenerator("text", filepath=os.path.abspath(os.path.curdir)+ "/")
# pdf.genTaskPDF(order)
