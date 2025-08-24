
# Vibe Finance Allocator
Streamlit 工具：輸入「目前金額」與「理想比例」，即時計算「差距金額」，並可匯出 CSV 給 Notion。

## 使用
```bash
pip install -r requirements.txt
streamlit run vibe_portfolio_app.py
```

## 功能
- 輸入 TWD / USD（自動換匯）
- 你自行輸入理想比例（四大類：固定收益/成長/避險/現金）
- 小計算機：比例↔金額即時對應
- 容忍區與鎖定規則（例如固定收益不賣）
- 一鍵匯出 CSV（丟進 Notion Database）

## 檔案
- `vibe_portfolio_app.py`：主程式
- `assets_template.csv`：明細→大類 mapping（可選）
- `requirements.txt`：套件清單
