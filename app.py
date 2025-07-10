import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import base64

# 日本語フォントの設定
try:
    # reportlab-japanese-fontsがインストールされている場合
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    JAPANESE_FONT = 'HeiseiMin-W3'
except ImportError:
    # フォールバック: システムフォントを使用
    try:
        # Windows の日本語フォント
        pdfmetrics.registerFont(TTFont('YuGothic', 'C:/Windows/Fonts/yu Gothic.ttc'))
        JAPANESE_FONT = 'YuGothic'
    except:
        # デフォルトフォント
        JAPANESE_FONT = 'Helvetica'

st.set_page_config(page_title="内部品質管理チェック：業務品質確認シート", layout="wide")
st.title("内部品質管理チェック：業務品質確認シート")

st.markdown("""
株式会社リジット  
コード作成責任者：品質管理担当者  
""")

auditor = st.text_input("品質管理責任者")
audit_date = st.date_input("記入日", value=date.today())

# チェック項目一覧（タイトル＋説明）
check_items = [
    {
        "title": "1. システムのバリデーション（CSV）",
        "desc": "新規または変更される情報システムについて、ベンダー信頼認証（FDAやCE認証）がない場合、バリデーションを実施し、その内容を記録として保管します。"
    },
    {
        "title": "2. 自動化システムの導入",
        "desc": "データ情報の分散を防ぎ、データ機密性と災害時のバックアップを強化するために、人為的過誤を最小限に抑える自動化システムを採用・構築しています。"
    },
    {
        "title": "3. RPAもしくは人工知能（AI)の活用",
        "desc": "ヒューマンエラーを最小限に抑えるため、RPA（Robotic Process Automation）および人工知能（AI）を導入しています。データ抽出や確認・削除も原則として担当者が一貫して行い、情報分散を防いでいます。"
    },
    {
        "title": "4. データの確認と管理",
        "desc": "画像データ受領時には、DICOMタグ情報（患者情報、施設情報、検査情報など）の秘匿化が適切に行われているかを確認します。ウィルス感染チェックは、受領した電子データについて、ウィルス対策ソフトを用いて実施し、ウィルスが発見された場合は駆除し、データ提供者に連絡します。解析結果の出力後、医療技術責任者は、被験者識別コードや撮像日などの項目を確認し、必要に応じて再解析を行います。"
    },
    {
        "title": "5. SOPの遵守と見直し",
        "desc": "SOPは、ICH-GCPガイドラインや関連法規等の改正の都度、または制定後少なくとも3年ごとに内容が見直されます。改訂の必要がないと判断された場合でも、その旨を明記し記録として保管されます。SOPの作成および改訂は、原則として信頼性保証・品質管理の担当者が行い、品質管理責任者が確認・承認します。"
    },
    {
        "title": "6. 是正措置と予防措置（CAPA）",
        "desc": "手順の逸脱があった場合は、そのレベルに応じて是正措置と予防措置を講じます。重大な逸脱（クラス1, 2）に対しては根本的な原因を改善する措置を講じ、品質管理責任者が過去の逸脱状況を調査し、再発防止のための教育訓練を実施します。"
    },
    {
        "title": "7. BCPの策定と訓練",
        "desc": "災害時においても事業を継続するための事業継続計画（BCP）が策定されており、従業員の安否確認、全業務の複数人カバー体制、データバックアップ、クラウドシステム利用などが含まれます。BCP訓練は、社員それぞれの地域防災訓練の中で定期的に実施されています。"
    }
]

# 入力記録
records = []

# 各チェック項目の表示と記録
for i, item in enumerate(check_items, 1):
    st.header(item["title"])
    st.markdown(item["desc"])
    col1, col2 = st.columns([1, 2])
    status = col1.radio("対応状況", ["未確認", "確認済", "要修正"], key=f"status_{i}")
    comment = col2.text_input("コメント", key=f"comment_{i}")
    records.append({
        "項目": item["title"],
        "説明": item["desc"],
        "対応状況": status,
        "コメント": comment
    })

# 特記事項
st.header("特記事項")
st.text_area("その他、記載すべき事項", height=100, key="special_notes")

def generate_pdf_report(records, auditor, audit_date, special_notes):
    """PDFレポートを生成する関数"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # 日本語フォントを使用したスタイル設定
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName=JAPANESE_FONT
    )
    
    # 日本語フォントを使用した通常スタイル
    normal_style = ParagraphStyle(
        'JapaneseNormal',
        parent=styles['Normal'],
        fontName=JAPANESE_FONT,
        fontSize=10
    )
    
    # 日本語フォントを使用した見出しスタイル
    heading_style = ParagraphStyle(
        'JapaneseHeading',
        parent=styles['Heading2'],
        fontName=JAPANESE_FONT,
        fontSize=14,
        spaceAfter=10
    )
    
    # ヘッダー情報
    story.append(Paragraph("内部品質管理チェック：業務品質確認シート", title_style))
    story.append(Spacer(1, 20))
    
    # 会社情報
    company_info = f"""
    <b>株式会社リジット</b><br/>
    コード作成責任者：品質管理担当者
    """
    story.append(Paragraph(company_info, normal_style))
    story.append(Spacer(1, 20))
    
    # 監査情報
    audit_info = f"""
    <b>品質管理責任者：</b>{auditor}<br/>
    <b>記入日：</b>{audit_date}
    """
    story.append(Paragraph(audit_info, normal_style))
    story.append(Spacer(1, 30))
    
    # 各チェック項目の結果
    for record in records:
        story.append(Paragraph(f"<b>{record['項目']}</b>", heading_style))
        story.append(Paragraph(record['説明'], normal_style))
        story.append(Spacer(1, 10))
        
        # 対応状況とコメント
        result_text = f"""
        <b>対応状況：</b>{record['対応状況']}<br/>
        <b>コメント：</b>{record['コメント']}
        """
        story.append(Paragraph(result_text, normal_style))
        story.append(Spacer(1, 15))
    
    # 特記事項
    story.append(Paragraph("<b>特記事項</b>", heading_style))
    story.append(Paragraph(special_notes, normal_style))
    story.append(Spacer(1, 20))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# 保存
if st.button("保存する"):
    df = pd.DataFrame(records)
    df["特記事項"] = st.session_state["special_notes"]
    
    # ファイル名のベース部分
    base_filename = f"品質管理チェック_{audit_date}_{auditor.replace(' ', '_')}"
    
    # CSVファイルの保存
    csv_filename = f"{base_filename}.csv"
    df.to_csv(csv_filename, index=False)
    
    # PDFファイルの生成
    pdf_buffer = generate_pdf_report(records, auditor, audit_date, st.session_state["special_notes"])
    pdf_filename = f"{base_filename}.pdf"
    
    st.success(f"保存しました: {csv_filename}, {pdf_filename}")
    
    # ダウンロードボタン
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "CSVをダウンロード", 
            data=df.to_csv(index=False), 
            file_name=csv_filename, 
            mime="text/csv"
        )
    with col2:
        st.download_button(
            "PDFをダウンロード", 
            data=pdf_buffer.getvalue(), 
            file_name=pdf_filename, 
            mime="application/pdf"
        )
