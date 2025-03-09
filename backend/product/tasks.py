# tasks.py

from celery import shared_task

import os
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


@shared_task
def my_task(arg1, arg2):
    # Task logic here
    result = arg1 + arg2
    return result


@shared_task
def make_pdf():   
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

    # we know some glyphs are missing, suppress warnings
    import reportlab.rl_config
    reportlab.rl_config.warnOnMissingFontGlyphs = 0

    # Create a canvas to draw on
    output_file = "./report_files/output.pdf"
    c = canvas.Canvas(output_file)

    c.setFont('Vera', 2)
    c.drawString(10, 150, "Some text encoded in UTF-8")
    c.drawString(10, 100, "In the Vera TT Font!")

    # Save the canvas
    c.save()