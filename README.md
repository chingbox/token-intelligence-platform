# Token Intelligence Platform

免費、純前端、繁體中文的 AI 開發 Token 預算工作台。

## 功能

- 階段式 WBS Token 預算：輸入與輸出 Token、模型單價、緩衝、匯率
- SKILL.md 投資報酬與損益兩平試算
- Prompt／Skill／RAG／Agent／Script 方法比較
- 實測用量 CSV 匯入、偏差分析、比較表匯出
- 自訂模型費率、日期與參考來源
- 下載可修改的 SKILL.md 範本

## 使用方式

開啟 `index.html` 即可使用，或部署整個目錄到任何靜態網站服務。無需安裝依賴、建置、API 金鑰、資料庫或註冊帳號。

## GitHub Pages 部署

1. 將全部檔案推送至 GitHub Repository 的預設分支。
2. Repository → Settings → Pages。
3. Build and deployment → Deploy from a branch；選擇預設分支與 `/ (root)`。
4. 存檔，等待 GitHub Pages 顯示發布網址。

## 本機資料與隱私

程式沒有 fetch、第三方腳本、追蹤器或 AI API 呼叫。參數存入瀏覽器 `localStorage`；使用者選取的 CSV 只在瀏覽器解析，不上傳。清除網站的瀏覽器資料即可清除儲存的預算與實測資訊。從 GitHub Pages 載入靜態檔案本身仍需一般 HTTP 連線。

## 計算定義

每個 WBS 階段：

- Input = 呼叫次數 × 每輪 Input Tokens
- Output = 呼叫次數 × 每輪 Output Tokens
- 預估總量 = (ΣInput + ΣOutput) × (1 + 緩衝%)
- API 費用 USD = 緩衝後 Input / 1,000,000 × Input 單價 + 緩衝後 Output / 1,000,000 × Output 單價

Skill ROI：

- Prompt 總量 = 任務數 × Prompt 每次 Token
- Skill 總量 = 建置 Token + 任務數 × Skill 每次 Token
- 淨節省 = Prompt 總量 − Skill 總量
- 損益兩平次數 = ceil(建置 Token / (Prompt 單次 − Skill 單次))；若每次沒有節省則無法回本

CSV 匯入必須包含 `phase,input_tokens,output_tokens`，同名階段多列自動加總。比較偏差使用**未加緩衝的原始預算**，以免緩衝掩蓋開發超支。未提供實測資料不當作零。

## 限制

- 此工具不是 Tokenizer，不會讀取你的 AI 開發環境，無法精確預測未來 Token；估算數字完全由使用者假設決定。
- 沒有自動抓取官方最新價格；預設示例費率是**假設價格**，非任何供應商報價。
- 尚未區分 Prompt Cache、推理 Tokens、特殊工具計價、訂閱方案與其他可能費用。
- 實測可信度標籤由使用者自行負責。
- CSV 公式注入風險：檔案供下載後若要在試算表開啟，請留意使用者輸入的階段名稱；目前 CSV 匯出將前置 `'=+-@` 特殊字元轉為一般文字的保護請參閱程式實作。

## License

MIT。參見 `LICENSE`。