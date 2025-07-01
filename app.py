import streamlit as st
import pandas as pd
from datetime import date

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

# 保存
if st.button("保存する"):
    df = pd.DataFrame(records)
    df["特記事項"] = st.session_state["special_notes"]
    filename = f"品質管理チェック_{audit_date}_{auditor.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    st.success(f"保存しました: {filename}")
    st.download_button("CSVをダウンロード", data=df.to_csv(index=False), file_name=filename, mime="text/csv")
