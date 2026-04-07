#!/usr/bin/env python3
"""
Gerador do PDF "7 Armadilhas Escondidas em Imóveis Perfeitos"
Lead magnet para Joice Leite — Advogada Imobiliária
Design: Dark theme premium (navy + rose gold)
"""

import os
import urllib.request
import zipfile
import io
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, KeepTogether, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, String
from reportlab.pdfgen import canvas

# ============================================================
# CONFIGURAÇÃO
# ============================================================

SCRIPT_DIR = Path(__file__).parent
FONTS_DIR = SCRIPT_DIR / "fonts"
ASSETS_DIR = SCRIPT_DIR / "assets"
OUTPUT_PDF = ASSETS_DIR / "guia-7-armadilhas.pdf"

# Cores
NAVY = HexColor("#0B1120")
NAVY_LIGHT = HexColor("#111B30")
NAVY_LIGHTER = HexColor("#162040")
ROSE_GOLD = HexColor("#C4956A")
ROSE_GOLD_DIM = HexColor("#8B6A4A")
WHITE = HexColor("#F1F0EE")
TEXT_SECONDARY = HexColor("#A0A0B0")
RED_FLAG_BG = HexColor("#1A0F0A")
RED_FLAG_BORDER = HexColor("#C4956A")

# Dimensões
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

# ============================================================
# DOWNLOAD DE FONTES
# ============================================================

def download_font(url, filename):
    """Baixa uma fonte TTF do Google Fonts."""
    filepath = FONTS_DIR / filename
    if filepath.exists():
        return filepath

    print(f"  Baixando {filename}...")
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, filepath)
    return filepath


def setup_fonts():
    """Baixa e registra as fontes Cinzel e Inter."""
    print("Configurando fontes...")

    # Cinzel - títulos
    cinzel_regular = download_font(
        "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
        "Cinzel-Variable.ttf"
    )
    cinzel_bold = download_font(
        "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
        "Cinzel-Bold.ttf"
    )

    # Inter - corpo
    inter_regular = download_font(
        "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
        "Inter-Variable.ttf"
    )
    inter_bold = download_font(
        "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
        "Inter-Bold.ttf"
    )

    # Registrar fontes
    try:
        pdfmetrics.registerFont(TTFont("Cinzel", str(cinzel_regular)))
        pdfmetrics.registerFont(TTFont("Cinzel-Bold", str(cinzel_bold)))
        pdfmetrics.registerFont(TTFont("Inter", str(inter_regular)))
        pdfmetrics.registerFont(TTFont("Inter-Bold", str(inter_bold)))
        print("  Fontes registradas com sucesso!")
        return True
    except Exception as e:
        print(f"  Aviso: Erro ao registrar fontes ({e}). Usando fontes padrão.")
        return False


# ============================================================
# ESTILOS
# ============================================================

def create_styles(has_custom_fonts):
    """Cria todos os estilos de parágrafo."""
    title_font = "Cinzel" if has_custom_fonts else "Helvetica"
    title_bold = "Cinzel-Bold" if has_custom_fonts else "Helvetica-Bold"
    body_font = "Inter" if has_custom_fonts else "Helvetica"
    body_bold = "Inter-Bold" if has_custom_fonts else "Helvetica-Bold"

    styles = {}

    # Capa
    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName=title_font,
        fontSize=28,
        leading=36,
        textColor=ROSE_GOLD,
        alignment=TA_CENTER,
        spaceAfter=8 * mm,
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle",
        fontName=body_font,
        fontSize=16,
        leading=22,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=12 * mm,
    )
    styles["cover_author"] = ParagraphStyle(
        "cover_author",
        fontName=body_font,
        fontSize=12,
        leading=16,
        textColor=TEXT_SECONDARY,
        alignment=TA_CENTER,
        spaceAfter=6 * mm,
    )
    styles["cover_tagline"] = ParagraphStyle(
        "cover_tagline",
        fontName=body_font,
        fontSize=11,
        leading=15,
        textColor=ROSE_GOLD_DIM,
        alignment=TA_CENTER,
    )

    # Títulos
    styles["h1"] = ParagraphStyle(
        "h1",
        fontName=title_font,
        fontSize=22,
        leading=28,
        textColor=ROSE_GOLD,
        alignment=TA_LEFT,
        spaceAfter=6 * mm,
        spaceBefore=2 * mm,
    )
    styles["h2"] = ParagraphStyle(
        "h2",
        fontName=title_font,
        fontSize=16,
        leading=22,
        textColor=ROSE_GOLD,
        alignment=TA_LEFT,
        spaceAfter=4 * mm,
        spaceBefore=6 * mm,
    )
    styles["h3"] = ParagraphStyle(
        "h3",
        fontName=title_bold,
        fontSize=12,
        leading=16,
        textColor=ROSE_GOLD,
        alignment=TA_LEFT,
        spaceAfter=3 * mm,
        spaceBefore=5 * mm,
    )

    # Corpo
    styles["body"] = ParagraphStyle(
        "body",
        fontName=body_font,
        fontSize=10,
        leading=16,
        textColor=WHITE,
        alignment=TA_JUSTIFY,
        spaceAfter=3 * mm,
    )
    styles["body_secondary"] = ParagraphStyle(
        "body_secondary",
        fontName=body_font,
        fontSize=9,
        leading=14,
        textColor=TEXT_SECONDARY,
        alignment=TA_JUSTIFY,
        spaceAfter=2 * mm,
    )

    # Destaque / quote
    styles["quote"] = ParagraphStyle(
        "quote",
        fontName=body_bold,
        fontSize=12,
        leading=18,
        textColor=ROSE_GOLD,
        alignment=TA_CENTER,
        spaceAfter=5 * mm,
        spaceBefore=5 * mm,
        leftIndent=15 * mm,
        rightIndent=15 * mm,
    )

    # Lista numerada
    styles["list_item"] = ParagraphStyle(
        "list_item",
        fontName=body_font,
        fontSize=9.5,
        leading=14,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=2 * mm,
        leftIndent=6 * mm,
    )

    # Red flag
    styles["red_flag"] = ParagraphStyle(
        "red_flag",
        fontName=body_bold,
        fontSize=9.5,
        leading=15,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=0,
    )

    # CTA
    styles["cta"] = ParagraphStyle(
        "cta",
        fontName=body_bold,
        fontSize=14,
        leading=20,
        textColor=ROSE_GOLD,
        alignment=TA_CENTER,
        spaceAfter=4 * mm,
        spaceBefore=4 * mm,
    )

    # Disclaimer
    styles["disclaimer"] = ParagraphStyle(
        "disclaimer",
        fontName=body_font,
        fontSize=7.5,
        leading=11,
        textColor=TEXT_SECONDARY,
        alignment=TA_JUSTIFY,
        spaceAfter=2 * mm,
    )

    # Armadilha número grande decorativo
    styles["trap_number"] = ParagraphStyle(
        "trap_number",
        fontName=title_font,
        fontSize=72,
        leading=72,
        textColor=HexColor("#1A2540"),
        alignment=TA_LEFT,
    )

    return styles


# ============================================================
# ELEMENTOS VISUAIS
# ============================================================

def draw_background(canvas, doc):
    """Desenha o fundo navy e elementos decorativos em todas as páginas."""
    canvas.saveState()

    # Fundo navy
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Linha decorativa superior rose gold
    canvas.setStrokeColor(ROSE_GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 12 * mm, PAGE_W - MARGIN, PAGE_H - 12 * mm)

    # Linha decorativa inferior
    canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)

    # Header "JL" em todas as páginas exceto a capa (página 1)
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.setFillColor(ROSE_GOLD_DIM)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(MARGIN, PAGE_H - 10 * mm, "JL")

        # Número da página
        canvas.setFillColor(TEXT_SECONDARY)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_W - MARGIN, 8 * mm, f"{page_num}")

    canvas.restoreState()


def draw_cover_background(canvas, doc):
    """Fundo especial para a capa."""
    canvas.saveState()

    # Fundo navy
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Linhas decorativas diagonais sutis
    canvas.setStrokeColor(HexColor("#131D35"))
    canvas.setLineWidth(0.3)
    for i in range(0, int(PAGE_W + PAGE_H), 40):
        canvas.line(i, PAGE_H, i - PAGE_H, 0)

    # Moldura rose gold
    canvas.setStrokeColor(ROSE_GOLD)
    canvas.setLineWidth(1)
    m = 15 * mm
    canvas.rect(m, m, PAGE_W - 2 * m, PAGE_H - 2 * m, fill=0, stroke=1)

    # Segunda moldura interna mais sutil
    canvas.setStrokeColor(ROSE_GOLD_DIM)
    canvas.setLineWidth(0.3)
    m2 = 18 * mm
    canvas.rect(m2, m2, PAGE_W - 2 * m2, PAGE_H - 2 * m2, fill=0, stroke=1)

    # Escudo decorativo no topo
    cx = PAGE_W / 2
    cy = PAGE_H - 60 * mm
    canvas.setFillColor(ROSE_GOLD)
    canvas.setStrokeColor(ROSE_GOLD)
    canvas.setLineWidth(1.5)

    # Desenhar escudo simples
    shield = canvas.beginPath()
    shield.moveTo(cx, cy + 22)
    shield.lineTo(cx + 18, cy + 14)
    shield.lineTo(cx + 18, cy - 2)
    shield.curveTo(cx + 18, cy - 14, cx, cy - 22, cx, cy - 22)
    shield.curveTo(cx, cy - 22, cx - 18, cy - 14, cx - 18, cy - 2)
    shield.lineTo(cx - 18, cy + 14)
    shield.close()
    canvas.drawPath(shield, fill=0, stroke=1)

    # Check mark dentro do escudo
    canvas.setLineWidth(2)
    canvas.line(cx - 7, cy - 2, cx - 2, cy - 8)
    canvas.line(cx - 2, cy - 8, cx + 8, cy + 6)

    canvas.restoreState()


def create_rose_line():
    """Cria uma linha decorativa rose gold como separador."""
    d = Drawing(CONTENT_W, 4)
    d.add(Line(0, 2, CONTENT_W, 2, strokeColor=ROSE_GOLD, strokeWidth=0.5))
    return d


def create_red_flag_box(text, styles):
    """Cria o box de Red Flag com fundo escuro e borda rose gold."""
    # Texto com ícone
    flag_text = f"SINAL DE ALERTA: {text}"
    p = Paragraph(flag_text, styles["red_flag"])

    t = Table(
        [[p]],
        colWidths=[CONTENT_W - 12 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), RED_FLAG_BG),
        ("BOX", (0, 0), (-1, -1), 1, RED_FLAG_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("ROUNDEDCORNERS", [3 * mm, 3 * mm, 3 * mm, 3 * mm]),
    ]))
    return t


# ============================================================
# CONTEÚDO
# ============================================================

def build_cover(styles):
    """Constrói a página de capa."""
    story = []
    story.append(Spacer(1, 80 * mm))

    story.append(Paragraph(
        '7 Armadilhas Escondidas<br/>em Imóveis "Perfeitos"',
        styles["cover_title"]
    ))

    story.append(Paragraph(
        "E Como Descobrir Antes de Assinar",
        styles["cover_subtitle"]
    ))

    story.append(create_rose_line())
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph(
        "Por Joice Leite — Advogada Imobiliária, OAB/SP",
        styles["cover_author"]
    ))

    story.append(Spacer(1, 40 * mm))

    story.append(Paragraph(
        '<i>"O guia que eu gostaria que tivessem me dado antes da minha primeira compra."</i>',
        styles["cover_tagline"]
    ))

    story.append(PageBreak())
    return story


def build_intro(styles):
    """Constrói a página de introdução."""
    story = []

    story.append(Paragraph("Por que eu escrevi este guia", styles["h1"]))
    story.append(create_rose_line())
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(
        "Você encontrou o imóvel dos sonhos.",
        styles["body"]
    ))
    story.append(Paragraph(
        'A localização é perfeita. O acabamento é lindo. O preço cabe no orçamento. '
        'O corretor já está te pressionando: "tem mais gente interessada". E dentro de '
        'você, uma voz diz: <i>"Esse é o momento. Se eu não fechar agora, vou perder."</i>',
        styles["body"]
    ))
    story.append(Paragraph(
        "Eu entendo esse sentimento. Já vi ele centenas de vezes nos olhos dos meus clientes. "
        "E é exatamente nesse momento — quando tudo parece perfeito demais — que os maiores "
        "erros acontecem.",
        styles["body"]
    ))
    story.append(Paragraph(
        "Eu sou a Joice Leite. Advogada, consultora imobiliária, e alguém que já viu de perto "
        "o estrago que um negócio mal feito causa na vida de uma família. Em mais de 200 "
        "transações imobiliárias aqui em São José dos Campos e em todo o Vale do Paraíba, "
        "eu aprendi uma coisa que mudou a minha forma de trabalhar:",
        styles["body"]
    ))

    story.append(Paragraph(
        '"O problema nunca está onde você está olhando."',
        styles["quote"]
    ))

    story.append(Paragraph(
        "Ninguém perde dinheiro por causa do piso ou da torneira com defeito. As pessoas "
        "perdem as economias de uma vida inteira por causa do que está escondido nos "
        "documentos — ou pior, do que <i>não</i> está em documento nenhum.",
        styles["body"]
    ))
    story.append(Paragraph(
        "Este guia reúne as 7 armadilhas que eu mais encontro na minha prática. São as "
        "mesmas verificações que faço para cada cliente que me procura antes de assinar um "
        "contrato. Decidi compartilhar com você porque acredito que <b>conhecimento protege</b>. "
        "E porque a maior compra da sua vida merece o mesmo cuidado que você daria se soubesse "
        "que um único erro poderia tirar tudo de você.",
        styles["body"]
    ))
    story.append(Paragraph("Porque pode.", styles["body"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Leia cada armadilha com atenção. Use os passos práticos. E se, ao final, você sentir "
        "que precisa de alguém ao seu lado nesse processo — eu estou aqui.",
        styles["body"]
    ))
    story.append(Paragraph("Vamos lá.", styles["body"]))

    story.append(PageBreak())
    return story


def build_trap(num, title, caso, verificar_items, red_flag_text, styles):
    """Constrói uma página de armadilha."""
    story = []

    # Número grande decorativo
    story.append(Paragraph(f"0{num}", styles["trap_number"]))
    story.append(Spacer(1, -18 * mm))

    # Título
    story.append(Paragraph(title, styles["h1"]))
    story.append(create_rose_line())
    story.append(Spacer(1, 3 * mm))

    # O Caso
    story.append(Paragraph("O CASO", styles["h3"]))
    for p in caso:
        story.append(Paragraph(p, styles["body"]))

    # O Que Verificar
    story.append(Paragraph("O QUE VERIFICAR", styles["h3"]))
    for i, item in enumerate(verificar_items, 1):
        story.append(Paragraph(
            f'<font color="#C4956A"><b>{i}.</b></font> {item}',
            styles["list_item"]
        ))

    # Red Flag
    story.append(Spacer(1, 3 * mm))
    story.append(create_red_flag_box(red_flag_text, styles))

    story.append(PageBreak())
    return story


def build_final_page(styles):
    """Constrói a página final com CTA."""
    story = []

    story.append(Paragraph(
        "Você chegou até aqui.<br/>Isso já te coloca à frente de 90% dos compradores.",
        styles["h1"]
    ))
    story.append(create_rose_line())
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(
        "A maioria das pessoas que compra um imóvel confia na palavra do vendedor, confia no "
        "corretor, confia na \"aparência\" da documentação. E muitas dessas pessoas só descobrem "
        "o problema quando é tarde demais — quando já assinaram, já pagaram e já perderam o "
        "poder de negociar.",
        styles["body"]
    ))
    story.append(Paragraph(
        "Você agora sabe o que procurar. Sabe quais certidões pedir. Sabe onde estão as "
        "cláusulas perigosas. Sabe reconhecer os sinais de alerta.",
        styles["body"]
    ))
    story.append(Paragraph(
        "Mas eu preciso ser honesta com você: <b>este guia é o começo, não o fim.</b>",
        styles["body"]
    ))
    story.append(Paragraph(
        "Cada imóvel é único. Cada situação tem nuances que um guia genérico não consegue cobrir. "
        "Uma matrícula com linguagem estranha, uma cláusula contratual ambígua, um detalhe na "
        "certidão que parece irrelevante — são nesses detalhes que mora o risco.",
        styles["body"]
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Quer que eu analise o seu caso?", styles["h2"]))
    story.append(Paragraph(
        "Se você está pensando em comprar, vender ou já tem um contrato na mão e não tem "
        "certeza se está tudo certo, me chama no WhatsApp. Eu posso te ajudar a verificar a "
        "documentação, revisar o contrato e garantir que você não caia em nenhuma dessas armadilhas.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>A conversa inicial é sem compromisso.</b> Me conta a sua situação e eu te digo, "
        "com sinceridade, se você precisa de ajuda profissional ou se pode seguir sozinho(a) "
        "com segurança.",
        styles["body"]
    ))

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        'Fale comigo pelo WhatsApp: <a href="https://wa.me/5512997681554" color="#C4956A">(12) 99768-1554</a>',
        styles["cta"]
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(create_rose_line())
    story.append(Spacer(1, 3 * mm))

    # Disclaimer na página do CTA
    story.append(Paragraph(
        "Este guia tem caráter exclusivamente informativo e educacional. Ele não substitui a "
        "consulta a um advogado para análise do seu caso específico. Cada transação imobiliária "
        "possui particularidades que exigem avaliação individualizada. As situações descritas "
        "neste material são fictícias, inspiradas em casos reais, e servem para ilustrar riscos "
        "comuns em negociações imobiliárias.",
        styles["disclaimer"]
    ))

    # ---- PÁGINA 11: Sobre a autora (com foto) ----
    story.append(PageBreak())

    story.append(Paragraph("Sobre a autora", styles["h1"]))
    story.append(create_rose_line())
    story.append(Spacer(1, 6 * mm))

    # Foto da Joice
    photo_path = ASSETS_DIR / "joice-foto.jpg"
    if photo_path.exists():
        img = Image(str(photo_path), width=55 * mm, height=73 * mm)
        # Foto à esquerda com bio à direita usando tabela
        bio_text = Paragraph(
            "<b>Joice Leite</b> é advogada e consultora imobiliária em São José dos Campos, "
            "atuante em todo o Vale do Paraíba.<br/><br/>"
            "Já acompanhou mais de <b>200 transações imobiliárias</b>, entre compras, vendas, "
            "locações e regularizações.<br/><br/>"
            "Sua missão é garantir que a maior compra da sua vida seja também a mais segura.<br/><br/>"
            "<b>OAB/SP [número]</b>",
            styles["body"]
        )
        photo_table = Table(
            [[img, bio_text]],
            colWidths=[60 * mm, CONTENT_W - 65 * mm],
        )
        photo_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("LEFTPADDING", (1, 0), (1, 0), 5 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(photo_table)
    else:
        # Fallback sem foto
        story.append(Paragraph(
            "<b>Joice Leite</b> é advogada e consultora imobiliária em São José dos Campos, "
            "atuante em todo o Vale do Paraíba. Já acompanhou mais de 200 transações imobiliárias, "
            "entre compras, vendas, locações e regularizações. Sua missão é garantir que a maior "
            "compra da sua vida seja também a mais segura.",
            styles["body"]
        ))
        story.append(Paragraph("<b>OAB/SP [número]</b>", styles["body_secondary"]))

    story.append(Spacer(1, 8 * mm))

    # Quote assinatura
    story.append(Paragraph(
        '"A maior compra da sua vida merece o mesmo cuidado que você daria '
        'se soubesse que um único erro poderia tirar tudo de você. Porque pode."',
        styles["quote"]
    ))

    story.append(Spacer(1, 8 * mm))
    story.append(create_rose_line())
    story.append(Spacer(1, 6 * mm))

    # CTA repetido
    story.append(Paragraph(
        'Fale comigo pelo WhatsApp: <a href="https://wa.me/5512997681554" color="#C4956A">(12) 99768-1554</a>',
        styles["cta"]
    ))

    story.append(Spacer(1, 15 * mm))
    story.append(create_rose_line())
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(
        "© 2026 Joice Leite — Todos os direitos reservados.",
        styles["disclaimer"]
    ))
    story.append(Paragraph(
        '<i>"Conhecimento que protege. Cuidado que acolhe."</i>',
        styles["cover_tagline"]
    ))

    return story


# ============================================================
# DADOS DAS 7 ARMADILHAS
# ============================================================

TRAPS = [
    {
        "num": 1,
        "title": "A Certidão que 9 em 10 Compradores Esquecem de Pedir",
        "caso": [
            "O Marcos e a Priscila encontraram um apartamento lindo em Urbanova, São José dos "
            "Campos. Três quartos, vista para a Serra da Mantiqueira, condomínio com lazer "
            "completo. O preço era justo, o vendedor simpático, e o corretor garantiu: "
            '"está tudo certo, pode fechar."',
            "Eles fecharam. Pagaram o sinal. Iniciaram a transferência.",
            "Trinta dias depois, receberam uma notificação judicial. O vendedor tinha uma ação "
            "trabalhista em andamento — e o juiz decretou a <b>penhora do imóvel</b> para "
            "garantir o pagamento da dívida. Aquele apartamento dos sonhos agora pertencia a "
            "um processo judicial.",
            "O que o Marcos e a Priscila não sabiam é que existe uma certidão que revela "
            "isso <i>antes</i> da compra. E eles nunca pediram.",
        ],
        "verificar": [
            "<b>Peça o CPF ou CNPJ completo do vendedor</b> (todos os proprietários que constam na matrícula)",
            "<b>Solicite a Certidão de Distribuição Cível</b> no site do Tribunal de Justiça do Estado de São Paulo (TJSP)",
            "<b>Solicite a Certidão de Distribuição Trabalhista</b> no site do Tribunal Regional do Trabalho (TRT-15 para o Vale do Paraíba)",
            "<b>Solicite a Certidão da Justiça Federal</b> no site do TRF-3 (para ações federais e execuções fiscais)",
            "<b>Verifique também protestos</b> no cartório de protestos da cidade do vendedor",
        ],
        "red_flag": (
            "Se o vendedor se recusar a fornecer o CPF completo ou pedir para "
            '"agilizar sem tanta burocracia", pare imediatamente. Vendedor transparente '
            "não tem medo de certidão. Quem tem algo a esconder, tem pressa para fechar."
        ),
    },
    {
        "num": 2,
        "title": "O Truque da Cláusula 14 nos Contratos de Incorporadora",
        "caso": [
            "A Camila, professora em Jacareí, juntou dinheiro por 8 anos para comprar seu "
            "primeiro apartamento na planta. Escolheu um empreendimento novo, de uma "
            'incorporadora conhecida. Assinou o contrato de 47 páginas no estande de vendas, '
            'confiando que "contrato de empresa grande é padrão".',
            "Quando o prédio ficou pronto — 14 meses atrasado —, a Camila descobriu que: "
            "o atraso não gerava nenhuma multa para a incorporadora (cláusula de \"tolerância\" "
            "de 180 dias, mais extensão por \"caso fortuito\"); ela é que teria que pagar multa "
            "de 2% se atrasasse qualquer parcela em 5 dias; e a cláusula 14 transferia "
            "<b>todo</b> o risco de variação do INCC (Índice Nacional de Custo da Construção) "
            "para ela, sem teto máximo.",
            "O apartamento que custava R$ 280 mil saiu por R$ 347 mil. E a incorporadora "
            "estava protegida por um contrato que a Camila assinou sem questionar.",
        ],
        "verificar": [
            '<b>Procure a cláusula de prazo de entrega</b> — Verifique se existe "prazo de tolerância" (geralmente 180 dias). Isso é legal, mas você precisa saber',
            "<b>Leia a cláusula de reajuste</b> — Identifique qual índice é usado (INCC é o mais comum) e se existe um teto máximo de reajuste",
            "<b>Compare as multas</b> — A multa por atraso do comprador é a mesma que a multa por atraso da incorporadora? Se não, o contrato é desequilibrado",
            '<b>Procure a palavra "caso fortuito" ou "força maior"</b> — Incorporadoras usam isso para estender o prazo indefinidamente',
            "<b>Verifique a cláusula de distrato</b> — Se você desistir, quanto perde? A lei do distrato (Lei 13.786/2018) permite retenção de até 50% em patrimônio de afetação",
        ],
        "red_flag": (
            'Se o contrato tem mais de 30 páginas e o vendedor diz "é padrão, todo mundo '
            'assina igual", desconfie. Quanto mais páginas, mais cláusulas escondidas. '
            "Leve o contrato para casa. Leia com calma. Melhor ainda: leve para um advogado "
            "ler antes de você assinar."
        ),
    },
    {
        "num": 3,
        "title": 'A Dívida Oculta que o Vendedor "Esqueceu" de Mencionar',
        "caso": [
            "O Roberto comprou uma casa no Jardim das Indústrias, em São José dos Campos. "
            "Casa ampla, rua tranquila, vizinhança boa. Fez a escritura, registrou no cartório, "
            "mudou a família.",
            "Dois meses depois, chegou uma cobrança da prefeitura: R$ 23 mil em IPTU atrasado "
            "dos últimos 4 anos. O vendedor não pagava desde 2022.",
            '"Mas eu não sou responsável pelas dívidas anteriores!", pensou o Roberto.',
            "Pensou errado. <b>Dívidas de IPTU acompanham o imóvel, não o dono.</b> Isso "
            "significa que, ao comprar a casa, o Roberto comprou junto a dívida. E a prefeitura "
            "pode executar o imóvel para cobrar.",
            "E o IPTU não é a única dívida que \"gruda\" no imóvel. Condomínio atrasado também.",
        ],
        "verificar": [
            "<b>Certidão Negativa de Débitos Municipais</b> — Solicite na prefeitura (ou pelo site) usando o número de inscrição imobiliária do imóvel. Mostra IPTU, taxas de lixo, contribuição de melhoria",
            "<b>Certidão de Nada Consta do Condomínio</b> — Peça ao síndico ou à administradora uma declaração assinada de que não existem débitos condominiais. Exija por escrito, com data",
            "<b>Certidão de Débitos Estaduais</b> — No site da Secretaria da Fazenda do Estado de São Paulo (para verificar dívidas de ITR em imóveis rurais ou ICMS em imóveis comerciais)",
            "<b>Consulta ao CADIN</b> — O Cadastro Informativo de Créditos não Quitados do Setor Público Federal mostra se o vendedor tem pendências federais",
        ],
        "red_flag": (
            'Se o vendedor oferece "desconto para fechar rápido" e pede para não esperar as '
            "certidões, é quase certo que existe dívida. Quem não deve, não tem pressa. O "
            "desconto que ele oferece provavelmente é menor do que a dívida que você vai herdar."
        ),
    },
    {
        "num": 4,
        "title": "A Matrícula com Histórico Suspeito",
        "caso": [
            "A Fernanda e o Lucas encontraram um terreno em Caçapava, perfeito para construir "
            'a casa própria. Preço excelente, documentação "em ordem" segundo o vendedor. Eles '
            "verificaram a matrícula no cartório e viram que o terreno estava no nome de quem "
            "dizia ser o dono.",
            "O que eles não fizeram foi ler a matrícula <i>inteira</i>.",
            "Se tivessem lido, teriam visto que o terreno mudou de dono 4 vezes nos últimos 3 "
            "anos. Cada transferência foi feita por valores muito abaixo do mercado. E a primeira "
            "transferência — a que iniciou toda a cadeia — tinha uma assinatura questionável de "
            "uma senhora de 89 anos que, descobriram depois, sofria de Alzheimer e nunca "
            "autorizou a venda.",
            "Resultado: toda a cadeia de transferências foi anulada na Justiça. A Fernanda e o "
            "Lucas perderam o terreno e tiveram que entrar com processo para tentar recuperar "
            "o dinheiro de um vendedor que já tinha desaparecido.",
        ],
        "verificar": [
            "<b>Solicite a matrícula atualizada (inteiro teor)</b> — No Cartório de Registro de Imóveis da comarca onde o imóvel está localizado",
            "<b>Leia todas as transferências dos últimos 20 anos</b> — Quantas vezes o imóvel mudou de dono? Transferências frequentes em curto período são sinal de alerta",
            "<b>Verifique os valores das transferências</b> — Valores muito abaixo do mercado podem indicar fraude ou simulação (venda de fachada)",
            "<b>Confira se há averbações de penhora, hipoteca, usufruto ou cláusulas restritivas</b> — Essas informações aparecem na margem da matrícula",
            "<b>Observe se há cancelamentos de registros</b> — Isso pode indicar transações anteriores que foram anuladas judicialmente",
        ],
        "red_flag": (
            "Se a matrícula mostra 3 ou mais transferências nos últimos 5 anos, especialmente "
            "com valores baixos ou entre pessoas da mesma família, investigue a fundo. Isso pode "
            "ser lavagem de dinheiro, fraude contra credores ou tentativa de esconder o imóvel "
            "de uma execução judicial."
        ),
    },
    {
        "num": 5,
        "title": 'O Imóvel em Inventário que "Já Está Quase Pronto"',
        "caso": [
            "O Paulo encontrou uma casa incrível em Vila Adyana, bairro nobre de São José dos "
            "Campos. O preço estava 30% abaixo do mercado. O motivo: o proprietário faleceu, "
            "e os filhos queriam vender rápido para dividir a herança.",
            '"O inventário já está quase pronto", disse um dos herdeiros. "É só questão de semanas."',
            "O Paulo pagou um sinal de R$ 80 mil direto para os herdeiros, com um \"contrato de "
            'gaveta" (contrato particular sem registro). Esperou as semanas. Que viraram meses. '
            "Que viraram dois anos.",
            "O inventário travou porque um dos quatro herdeiros não concordava com o valor da "
            "venda. Outro apareceu — um filho de outro relacionamento que ninguém mencionou e "
            "que também tinha direito à herança. Enquanto isso, o Paulo não podia registrar o "
            "imóvel no nome dele. Não podia financiar. Não podia reformar. E o sinal de R$ 80 "
            "mil estava preso numa situação judicial que não tinha prazo para acabar.",
        ],
        "verificar": [
            '<b>Confirme se o inventário foi aberto</b> — Peça o número do processo e consulte no site do TJSP. "Vamos abrir" é diferente de "já está aberto"',
            "<b>Verifique se TODOS os herdeiros estão de acordo com a venda</b> — Exija uma ata de concordância assinada por cada um. Um único herdeiro que discorde pode travar tudo",
            "<b>Confirme se existe alvará judicial autorizando a venda</b> — Sem alvará, nenhum herdeiro pode vender legalmente o imóvel enquanto o inventário não terminar",
            "<b>Verifique se o ITCMD foi pago</b> — O Imposto de Transmissão Causa Mortis (imposto sobre herança) precisa estar quitado para a transferência ser concluída",
            "<b>Nunca pague sinal direto aos herdeiros</b> — Se for antecipar valores, use uma conta garantia (escrow) ou condicione o pagamento à lavratura da escritura",
        ],
        "red_flag": (
            'Se alguém diz que o inventário "está quase pronto" mas não consegue mostrar o '
            "número do processo ou o alvará de venda, o inventário não está quase pronto. "
            "Provavelmente nem começou. Não pague nenhum valor até ter documentos concretos "
            "nas mãos."
        ),
    },
    {
        "num": 6,
        "title": "A Área Construída que Não Existe no Papel",
        "caso": [
            "A Juliana comprou uma casa em Taubaté com 3 quartos, churrasqueira e uma edícula "
            "nos fundos (aquele cômodo extra que serve como quarto de hóspedes ou escritório). "
            "A edícula foi o diferencial — espaço perfeito para o home office dela.",
            "Na hora de financiar pelo banco, a avaliação ficou abaixo do esperado. Motivo: a "
            "edícula não estava averbada na matrícula do imóvel (ou seja, legalmente ela não "
            "existia). Para o banco e para a prefeitura, aquela construção era como se não "
            "estivesse ali.",
            "Resultado: o financiamento cobriu menos do que a Juliana precisava. Ela teve que "
            "desembolsar R$ 40 mil a mais do próprio bolso. E se quisesse regularizar a "
            "edícula, precisaria contratar um engenheiro, fazer um projeto, pagar taxas na "
            "prefeitura e arcar com a diferença do IPTU retroativo — mais uns R$ 15 mil.",
        ],
        "verificar": [
            "<b>Compare a matrícula com a realidade</b> — Veja na matrícula quantos metros quadrados de construção estão registrados. Depois, compare com o que você vê no imóvel",
            '<b>Peça o "habite-se" (auto de conclusão)</b> — Esse documento prova que a construção foi aprovada pela prefeitura. Sem ele, a construção é irregular',
            "<b>Verifique a planta aprovada na prefeitura</b> — Toda obra precisa ter projeto aprovado. Se a casa tem cômodos que não aparecem na planta, foram construídos sem autorização",
            "<b>Consulte o IPTU</b> — Compare a área tributada (que aparece no carnê do IPTU) com a área real. Se forem diferentes, há construção sem averbação",
            "<b>Cuidado com: puxadinhos, edículas, varandas fechadas, coberturas, mezaninos</b> — São as construções que mais frequentemente existem sem averbação",
        ],
        "red_flag": (
            'Se o vendedor diz "isso aqui eu fiz por conta, mas não mexi na documentação", '
            "você está comprando um problema. Qualquer construção não averbada pode gerar "
            "multa, embargo da prefeitura e, no pior caso, ordem de demolição. E o custo de "
            "regularizar será seu, não dele."
        ),
    },
    {
        "num": 7,
        "title": "A Zona de Restrição que Ninguém Te Contou",
        "caso": [
            "O Thiago comprou um terreno grande no Jardim Satélite, em São José dos Campos, "
            "com a ideia de construir uma casa e, no futuro, dividir o lote e vender a outra "
            'metade. O vendedor disse que "podia fazer o que quisesse" no terreno.',
            "Quando o Thiago procurou a prefeitura para aprovar o projeto, descobriu que o "
            "terreno ficava em uma <b>zona de proteção ambiental</b>. A margem do lote fazia "
            "divisa com uma APP (Área de Preservação Permanente) por causa de um córrego que "
            "passava nos fundos — um córrego que, no verão, quase seca e que ninguém mencionou.",
            "Resultado: o Thiago não podia construir nos 30 metros mais próximos do córrego "
            "(exigência do Código Florestal). Não podia desmembrar o lote (a prefeitura negou "
            "por restrição ambiental). E o terreno, que ele comprou para ser um investimento, "
            "virou um passivo — ele não consegue construir o que queria nem revender pelo "
            "preço que pagou.",
        ],
        "verificar": [
            "<b>Consulte o Plano Diretor e a Lei de Zoneamento</b> — Na prefeitura ou no site da Secretaria de Urbanismo. Cada zona da cidade tem regras sobre o que pode ser construído, altura máxima, taxa de ocupação e coeficiente de aproveitamento",
            "<b>Peça a Certidão de Uso e Ocupação do Solo</b> — Esse documento diz oficialmente o que pode e o que não pode ser feito no lote",
            "<b>Verifique a existência de APP</b> — Consulte na Secretaria de Meio Ambiente se o imóvel faz divisa com rios, córregos, nascentes, encostas ou topos de morro",
            "<b>Consulte o GRAPROHAB</b> — Para loteamentos no Estado de São Paulo, o Grupo de Análise e Aprovação de Projetos Habitacionais verifica a regularidade do empreendimento",
            "<b>Verifique se existem tombamentos ou restrições do patrimônio histórico</b> — Em regiões centrais de cidades como Taubaté e São José dos Campos, imóveis próximos a bens tombados têm restrições de reforma e demolição",
        ],
        "red_flag": (
            'Se o terreno é "barato demais para a localização", pode haver uma restrição '
            "ambiental, urbanística ou jurídica que o vendedor não está revelando. Terreno "
            'bom e barato sem motivo não existe. Sempre pergunte: "Por que esse preço?"'
        ),
    },
]


# ============================================================
# GERAÇÃO DO PDF
# ============================================================

def generate_pdf():
    """Gera o PDF completo."""
    print("\n=== Gerando PDF: 7 Armadilhas ===\n")

    # Setup fontes
    has_custom_fonts = setup_fonts()
    styles = create_styles(has_custom_fonts)

    # Criar diretório de saída
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Configurar documento
    doc = BaseDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        title="7 Armadilhas Escondidas em Imóveis Perfeitos",
        author="Joice Leite — Advogada Imobiliária",
        subject="Guia de proteção para compradores de imóveis",
        creator="Joice Leite",
    )

    # Frame para conteúdo
    content_frame = Frame(
        MARGIN, 20 * mm,
        CONTENT_W, PAGE_H - 45 * mm,
        id="content",
    )

    # Templates de página
    cover_template = PageTemplate(
        id="cover",
        frames=[content_frame],
        onPage=draw_cover_background,
    )

    body_template = PageTemplate(
        id="body",
        frames=[content_frame],
        onPage=draw_background,
    )

    doc.addPageTemplates([cover_template, body_template])

    # Construir conteúdo
    print("Construindo conteúdo...")
    story = []

    # Capa (usa template cover)
    story.extend(build_cover(styles))

    # Mudar para template body após a capa
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.insert(-1, NextPageTemplate("body"))

    # Introdução
    story.extend(build_intro(styles))

    # 7 Armadilhas
    for trap in TRAPS:
        story.extend(build_trap(
            trap["num"],
            trap["title"],
            trap["caso"],
            trap["verificar"],
            trap["red_flag"],
            styles,
        ))

    # Página final
    story.extend(build_final_page(styles))

    # Gerar PDF
    print("Gerando PDF...")
    doc.build(story)

    file_size = OUTPUT_PDF.stat().st_size / 1024
    print(f"\n  PDF gerado com sucesso!")
    print(f"  Arquivo: {OUTPUT_PDF}")
    print(f"  Tamanho: {file_size:.1f} KB")
    print(f"\n=== Concluído! ===\n")


if __name__ == "__main__":
    generate_pdf()
