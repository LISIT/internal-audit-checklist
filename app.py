import streamlit as st
import pandas as pd
from datetime import date

# チェックシートのデータ（カテゴリと項目）
data = {
    "1. 会社情報と体制": [
        "会社概要・所在地・人員構成",
        "組織図（最新版）と役割の明確化",
        "主要な受託業務と実績の記録"
    ],
    "2. 品質保証と監査体制": [
        "QA/QCの体制と人員",
        "SOPに基づく監査計画の有無",
        "監査結果とCAPA（是正措置）管理",
        "SOPの管理・改訂履歴の確認"
    ],
    "3. データ・文書管理": [
        "データのバックアップ体制（頻度、手段）",
        "電子データの保管場所・セキュリティ",
        "文書保管規定・旧版管理の有無"
    ],
    "4. 教育・訓練": [
        "教育研修SOPの整備状況",
        "教育訓練の記録・更新状況",
        "専門的スキル・資格の保有状況"
    ],
    "5. システムとセキュリティ": [
        "施設の入退室管理（物理的セキュリティ）",
        "システムバリデーション（CSV）の有無",
        "クラウドやNASの安全性とログ管理"
    ],
    "6. プロジェクト管理": [
        "プロジェクト指名書・責任者の明確化",
        "業務手順の一貫性と記録の整備"
    ]
}

st.title("Imaging CRO 内部監査チェックシート")

auditor = st.text_input("監査者名")
audit_date = st.date_input("監査日", value=date.today())

records = []

for section, items in data.items():
    st.header(section)
    for item in items:
        col1, col2 = st.columns([1, 3])
        checked = col1.checkbox("チェック済", key=item)
        comment = col2.text_input("コメント", key=f"comment_{item}")
        records.append({
            "カテゴリ": section,
            "項目": item,
            "チェック済": checked,
            "コメント": comment
        })

if st.button("保存する"):
    df = pd.DataFrame(records)
    filename = f"audit_{audit_date}_{auditor.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    st.success(f"保存しました: {filename}")
