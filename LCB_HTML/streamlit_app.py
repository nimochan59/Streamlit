import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components

import yaml
from yaml.loader import SafeLoader

## ユーザー設定読み込み
yaml_path = "/mount/src/streamlit/LCB_HTML/config.yaml"

with open(yaml_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

## UI 

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title id="pageTitle">{{pageTitle}}</title>
  <style>
    /* CSSは変更ありません。元のCSSをそのまま使用します */
    :root {
      --primary-color: #34a853;
      --primary-light: #dbf5e0;
      --secondary-color: #4285f4;
      --accent-color: #ea4335;
      --text-primary: #202124;
      --text-secondary: #5f6368;
      --text-tertiary: #80868b;
      --border-color: #dadce0;
      --background-light: #f8f9fa;
      --shadow-sm: 0 1px 2px rgba(60, 64, 67, 0.1);
      --shadow-md: 0 2px 6px rgba(60, 64, 67, 0.15);
      --shadow-lg: 0 4px 12px rgba(60, 64, 67, 0.2);
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 16px;
      --spacing-xs: 4px;
      --spacing-sm: 8px;
      --spacing-md: 16px;
      --spacing-lg: 24px;
      --spacing-xl: 32px;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    body {
      background-color: var(--background-light);
      color: var(--text-primary);
      line-height: 1.6;
      padding: var(--spacing-md);
      max-width: 100%;
      overflow-x: hidden;
    }

    /* ヘッダーセクション */
    .app-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background-color: white;
    }

    .status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--spacing-sm) var(--spacing-md);
      font-size: 14px;
      color: var(--text-secondary);
      background-color: white;
    }

    .battery-status {
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
    }

    .battery-icon {
      position: relative;
      width: 18px;
      height: 10px;
      border: 1px solid currentColor;
      border-radius: 2px;
    }

    .battery-icon::before {
      content: '';
      position: absolute;
      top: 2px;
      left: 2px;
      width: calc(45% - 4px);
      height: calc(100% - 4px);
      background-color: var(--accent-color);
      border-radius: 1px;
    }

    .battery-icon::after {
      content: '';
      position: absolute;
      width: 2px;
      height: 6px;
      background-color: currentColor;
      top: 2px;
      right: -3px;
      border-radius: 0 1px 1px 0;
    }

    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--spacing-md);
      background-color: white;
      box-shadow: var(--shadow-sm);
    }

    .page-title {
      font-size: 18px;
      font-weight: 600;
    }

    .back-button {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .back-button:hover {
      background-color: rgba(0, 0, 0, 0.05);
    }

    .actions {
      display: flex;
      gap: var(--spacing-md);
    }

    .action-button {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .action-button:hover {
      background-color: rgba(0, 0, 0, 0.05);
    }

    /* タブナビゲーション */
    .tab-container {
      display: flex;
      border-bottom: 1px solid var(--border-color);
      background-color: white;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }

    .tab-container::-webkit-scrollbar {
      display: none;
    }

    .tab {
      flex: 1;
      min-width: 80px;
      text-align: center;
      padding: var(--spacing-md) var(--spacing-sm);
      border-bottom: 3px solid transparent;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
    }

    .tab.active {
      border-bottom: 3px solid var(--primary-color);
      color: var(--primary-color);
      font-weight: 600;
    }

    .tab:not(.active):hover {
      background-color: rgba(0, 0, 0, 0.02);
    }

    .date {
      font-size: 16px;
      margin-bottom: 2px;
    }

    .day {
      font-size: 12px;
      color: var(--text-tertiary);
    }

    /* 交通手段セレクターとコスト情報 */
    .trip-info-container {
      margin: var(--spacing-lg) 0;
    }

    .transport-selector {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--spacing-md);
      background-color: white;
      border-radius: var(--radius-lg);
      padding: var(--spacing-md);
      margin: 0 auto var(--spacing-md);
      max-width: 300px;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
      transition: transform 0.2s, box-shadow 0.2s;
      border: 1px solid var(--border-color);
    }

    .transport-selector:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .transport-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: var(--primary-light);
      color: var(--primary-color);
    }

    .transport-label {
      font-weight: 500;
      flex-grow: 1;
    }

    .cost-info {
      display: flex;
      justify-content: center;
      gap: var(--spacing-xl);
      margin-bottom: var(--spacing-lg);
      color: var(--text-secondary);
    }

    .cost-item {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .cost-icon {
      font-size: 20px;
      margin-bottom: var(--spacing-xs);
    }

    .cost-value {
      font-weight: 500;
    }

    /* タイムライン */
    .timeline {
      display: flex;
      flex-direction: column;
      padding-left: var(--spacing-md);
      margin: var(--spacing-xl) auto;
      position: relative;
      max-width: 960px;
    }

    .timeline-line {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 35px;
      width: 3px;
      background-color: var(--border-color);
      z-index: 0;
    }

    .timeline-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: var(--spacing-xl);
      position: relative;
    }

    .timeline-item:last-child {
      margin-bottom: 0;
    }

    .timeline-marker-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-right: var(--spacing-lg);
      position: relative;
      z-index: 1;
    }

    .time-marker {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: var(--spacing-xs);
      font-weight: 500;
      text-align: right;
      width: 80px;
    }

    .point-number {
      background-color: var(--primary-color);
      color: white;
      border-radius: 50%;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 600;
      box-shadow: var(--shadow-sm);
      position: relative;
    }

    .timeline-details {
      background-color: white;
      padding: var(--spacing-lg);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      transition: transform 0.2s, box-shadow 0.2s;
      border: 1px solid var(--border-color);
    }

    .timeline-details:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .activity-info {
      flex: 1;
      margin-right: var(--spacing-lg);
    }

    .activity-label {
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      color: var(--primary-color);
      background-color: var(--primary-light);
      padding: 2px var(--spacing-sm);
      border-radius: var(--radius-sm);
      margin-bottom: var(--spacing-sm);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .activity-name {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: var(--spacing-sm);
      color: var(--text-primary);
    }

    .activity-location {
      font-size: 16px;
      color: var(--text-secondary);
      margin-bottom: var(--spacing-sm);
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
    }

    .activity-location::before {
      content: '📍';
      font-size: 16px;
    }

    .activity-detail {
      font-size: 14px;
      color: var(--text-tertiary);
      margin-top: var(--spacing-xs);
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
    }

    .activity-duration::before {
      content: '⏱️';
    }

    .activity-distance::before {
      content: '🔄';
    }

    .activity-notes {
      margin-top: var(--spacing-md);
      padding-top: var(--spacing-md);
      border-top: 1px dashed var(--border-color);
      font-size: 14px;
      color: var(--text-secondary);
      font-style: italic;
    }

    .activity-notes::before {
      content: '💡 ';
    }

    .reservation-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--spacing-xs);
      padding: var(--spacing-sm) var(--spacing-md);
      background-color: var(--primary-color);
      color: white;
      text-decoration: none;
      border-radius: var(--radius-md);
      font-size: 14px;
      font-weight: 500;
      white-space: nowrap;
      transition: background-color 0.2s, transform 0.2s;
      border: none;
      cursor: pointer;
      min-width: 100px;
    }

    .reservation-button:hover {
      background-color: #2c9147;
      transform: translateY(-2px);
    }

    .reservation-button::before {
      content: '🎟️';
    }

    /* 移動手段詳細 */
    .transport-detail {
      background-color: white;
      padding: var(--spacing-md);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      margin: var(--spacing-sm) 0 var(--spacing-lg) 55px;
      border: 1px solid #e0f2ff;
      background-color: #f0f8ff;
      max-width: 900px;
    }

    .transport-header {
      display: flex;
      align-items: center;
      gap: var(--spacing-md);
      color: var(--text-secondary);
      font-weight: 500;
      margin-bottom: var(--spacing-sm);
    }

    .transport-time-cost {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: var(--text-tertiary);
      margin-bottom: var(--spacing-sm);
    }

    .transport-icons {
      display: flex;
      align-items: center;
      gap: var(--spacing-sm);
      color: var(--text-tertiary);
      font-size: 14px;
    }

    .waiting-time {
      text-align: center;
      color: var(--text-tertiary);
      font-style: italic;
      margin: -10px 0 var(--spacing-lg) 55px;
      font-size: 14px;
      max-width: 900px;
    }

    /* フローティングボタン */
    .add-button {
      position: fixed;
      bottom: var(--spacing-xl);
      right: var(--spacing-xl);
      width: 60px;
      height: 60px;
      background-color: var(--primary-color);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      cursor: pointer;
      box-shadow: var(--shadow-lg);
      transition: transform 0.2s, background-color 0.2s;
      border: none;
      z-index: 10;
    }

    .add-button:hover {
      transform: scale(1.1);
      background-color: #2c9147;
    }

    /* 日付選択バッジ */
    .date-badge {
      position: fixed;
      bottom: var(--spacing-xl);
      left: var(--spacing-xl);
      background-color: white;
      border-radius: var(--radius-lg);
      padding: var(--spacing-sm) var(--spacing-md);
      box-shadow: var(--shadow-md);
      display: flex;
      align-items: center;
      gap: var(--spacing-sm);
      font-weight: 500;
      z-index: 10;
      border: 1px solid var(--border-color);
    }

    .date-badge-text {
      color: var(--text-primary);
    }

    .date-badge-day {
      color: var(--primary-color);
      font-weight: 600;
    }

    /* EV情報バッジ */
    .ev-status {
      position: fixed;
      bottom: calc(var(--spacing-xl) + 60px);
      right: var(--spacing-xl);
      background-color: white;
      border-radius: var(--radius-md);
      padding: var(--spacing-sm) var(--spacing-md);
      box-shadow: var(--shadow-md);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: var(--spacing-xs);
      z-index: 9;
      border: 1px solid var(--border-color);
    }

    .battery-level {
      display: flex;
      align-items: center;
      gap: var(--spacing-xs);
      font-weight: 500;
      color: var(--primary-color);
    }

    .range-info {
      font-size: 12px;
      color: var(--text-tertiary);
    }

    /* PC表示での調整 */
    @media screen and (min-width: 768px) {
      body {
        padding: var(--spacing-xl);
        max-width: 1200px;
        margin: 0 auto;
      }

      .app-container {
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: var(--spacing-xl);
      }

      .sidebar {
        position: sticky;
        top: var(--spacing-xl);
        height: calc(100vh - 2 * var(--spacing-xl));
        background-color: white;
        border-radius: var(--radius-md);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
      }

      .trip-info-container {
        margin-top: 0;
      }

      .timeline {
        padding-left: var(--spacing-xl);
      }

      .time-marker {
        font-size: 16px;
        width: 100px;
      }

      .point-number {
        width: 32px;
        height: 32px;
        font-size: 16px;
      }

      .timeline-details {
        padding: var(--spacing-xl);
      }

      .transport-detail, .waiting-time {
        margin-left: 75px;
      }

      .add-button {
        width: 70px;
        height: 70px;
      }

      .reservation-button {
        font-size: 16px;
        padding: var(--spacing-md) var(--spacing-lg);
      }

      .tab {
        flex: none;
        padding: var(--spacing-md) var(--spacing-lg);
      }

      /* サイドメニュー表示（PCのみ） */
      .overview-section {
        margin-bottom: var(--spacing-lg);
      }

      .section-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: var(--spacing-md);
        color: var(--text-primary);
      }

      .trip-overview {
        background-color: var(--primary-light);
        border-radius: var(--radius-md);
        padding: var(--spacing-md);
        margin-bottom: var(--spacing-lg);
      }

      .trip-title {
        font-weight: 600;
        font-size: 18px;
        margin-bottom: var(--spacing-xs);
      }

      .trip-date {
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: var(--spacing-sm);
      }

      .trip-summary {
        display: flex;
        justify-content: space-between;
        margin-bottom: var(--spacing-sm);
      }

      .summary-item {
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      .summary-value {
        font-weight: 600;
        font-size: 16px;
      }

      .summary-label {
        font-size: 12px;
        color: var(--text-tertiary);
      }

      .battery-status-card {
        background: linear-gradient(135deg, #34a853, #4285f4);
        color: white;
        border-radius: var(--radius-md);
        padding: var(--spacing-md);
        margin-bottom: var(--spacing-lg);
      }

      .battery-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-sm);
      }

      .battery-title {
        font-weight: 600;
      }

      .battery-percentage {
        font-size: 24px;
        font-weight: 700;
      }

      .battery-bar {
        height: 8px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: var(--spacing-sm);
      }

      .battery-fill {
        height: 100%;
        width: 45%;
        background-color: white;
        border-radius: 4px;
      }

      .battery-range {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
      }

      .charging-stations {
        margin-bottom: var(--spacing-lg);
      }

      .station-item {
        display: flex;
        justify-content: space-between;
        padding: var(--spacing-sm) 0;
        border-bottom: 1px solid var(--border-color);
      }

      .station-info {
        flex: 1;
      }

      .station-name {
        font-weight: 500;
        font-size: 14px;
      }

      .station-distance {
        font-size: 12px;
        color: var(--text-tertiary);
      }

      .station-status {
        font-size: 12px;
        color: var(--primary-color);
        background-color: var(--primary-light);
        padding: 2px var(--spacing-sm);
        border-radius: var(--radius-sm);
      }
    }
  </style>
</head>
<body>
  <div class="app-container" id="appContainer">
    <!-- コンテンツはJavaScriptで生成されます -->
  </div>

  <script>
    const templateData = {
      pageTitle: "電気自動車 箱根旅行プラン",
      tripTitle: "箱根温泉旅行",
      tripDate: "2025年3月9日（日）- 3月10日（月）",
      tripSummary: {
        distance: "80km",
        chargeCount: 2,
        chargeCost: "2,000"
      },
      batteryStatus: {
        percentage: 45,
        remainingRange: 112,
        rangeToCharge: 40
      },
      chargingStations: [
        { name: "海老名SA 充電ステーション", distance: "3km先 / 11:00到着予定", status: "利用可能" },
        { name: "箱根町観光案内所 充電スポット", distance: "28km先", status: "混雑中" },
        { name: "箱根ホテル 充電スポット", distance: "40km先", status: "予約済み" }
      ],
      activeDate: { date: "3/9", dayOfWeek: "日" },
      date2: { date: "3/10", dayOfWeek: "月" },
      date3: { date: "3/11", dayOfWeek: "火" },
      date4: { date: "3/12", dayOfWeek: "水" },
      timelineItems: [
        {
          time: "10:00",
          activityLabel: "出発",
          activityName: "自宅を出発",
          activityLocation: "自宅",
          duration: "0分",
          distance: "0km",
          actionButtonText: "AC起動"
        },
        {
          time: "11:00",
          activityLabel: "充電",
          activityName: "急速充電",
          activityLocation: "海老名SA(下り)充電ステーション",
          duration: "30分",
          distance: "約50km",
          reservationButtonText: "充電器予約",
          reservationUrl: "#" // 予約URLをAI生成情報から取得
        },
        {
          time: "12:00",
          activityLabel: "食事",
          activityName: "レストラン「お食事処大和」",
          activityLocation: "箱根周辺",
          duration: "30分",
          distance: "", // 距離はAI生成情報から取得
          reservationButtonText: "レストラン予約",
          reservationUrl: "#" // 予約URLをAI生成情報から取得
        },
        {
          time: "12:30",
          activityLabel: "レジャー",
          activityName: "仙石原 すすき草原",
          activityLocation: "仙石原",
          duration: "1時間30分",
          distance: "" // 距離はAI生成情報から取得
        },
        {
          time: "14:00",
          activityLabel: "レジャー",
          activityName: "箱根ガラスの森美術館",
          activityLocation: "箱根ガラスの森美術館",
          duration: "2時間",
          distance: "", // 距離はAI生成情報から取得
          reservationButtonText: "予約",
          reservationUrl: "https://www.hakone-garasunomori.jp/"
        },
        {
          time: "16:30",
          activityLabel: "ホテル",
          activityName: "ホテル天成園チェックイン",
          activityLocation: "ホテル内",
          duration: "30分",
          distance: "", // 距離はAI生成情報から取得
          reservationButtonText: "ホテル予約",
          reservationUrl: "#" // 予約URLをAI生成情報から取得
        },
        {
          time: "17:00",
          activityLabel: "休憩",
          activityName: "温泉「天空大露天風呂」",
          activityLocation: "ホテル内",
          duration: "1時間",
          distance: "" // 距離はAI生成情報から取得
        },
        {
          time: "18:00",
          activityLabel: "夕食",
          activityName: "レストラン「瀧見亭」",
          activityLocation: "ホテル内",
          duration: "2時間",
          distance: "", // 距離はAI生成情報から取得
          reservationButtonText: "レストラン予約",
          reservationUrl: "https://www.hakone-hotel.jp/restaurant/"
        }
      ],
      evStatus: {
        batteryLevel: 45,
        remainingRange: 112
      }
    };

    function renderHTML(data) {
      return `
        <!-- サイドバー (PCのみ表示) -->
        <aside class="sidebar" id="sidebar">
          <section class="overview-section">
            <h2 class="section-title">旅程概要</h2>
            <div class="trip-overview">
              <h3 class="trip-title">${data.tripTitle}</h3>
              <div class="trip-date">${data.tripDate}</div>
              <div class="trip-summary">
                <div class="summary-item">
                  <div class="summary-value">${data.tripSummary.distance}</div>
                  <div class="summary-label">走行距離</div>
                </div>
                <div class="summary-item">
                  <div class="summary-value">${data.tripSummary.chargeCount}回</div>
                  <div class="summary-label">充電</div>
                </div>
                <div class="summary-item">
                  <div class="summary-value">¥${data.tripSummary.chargeCost}</div>
                  <div class="summary-label">充電費用</div>
                </div>
              </div>
            </div>

            <div class="battery-status-card">
              <div class="battery-header">
                <div class="battery-title">バッテリー残量</div>
                <div class="battery-percentage">${data.batteryStatus.percentage}%</div>
              </div>
              <div class="battery-bar">
                <div class="battery-fill" style="width: ${data.batteryStatus.percentage}%;"></div>
              </div>
              <div class="battery-range">
                <span>残り ${data.batteryStatus.remainingRange}km</span>
                <span>次の充電まで ${data.batteryStatus.rangeToCharge}km</span>
              </div>
            </div>

            <section class="charging-stations">
              <h3 class="section-title">近くの充電スポット</h3>
              ${data.chargingStations.map(station => `
              <div class="station-item">
                <div class="station-info">
                  <div class="station-name">${station.name}</div>
                  <div class="station-distance">${station.distance}</div>
                </div>
                <div class="station-status">${station.status}</div>
              </div>
              `).join('')}
            </section>
          </section>
        </aside>

        <!-- メインコンテンツ -->
        <main class="main-content">
          <header class="app-header">
            <div class="nav-bar">
              <button class="back-button">←</button>
              <h1 class="page-title">${data.pageTitle}</h1>
              <div class="actions">
                <button class="action-button">👤</button>
                <button class="action-button">⋮</button>
              </div>
            </div>

            <nav class="tab-container">
              <div class="tab">
                <div>📅</div>
                <div class="day">プラン</div>
              </div>
              <div class="tab active">
                <div class="date">${data.activeDate.date}</div>
                <div class="day">${data.activeDate.dayOfWeek}</div>
              </div>
              <div class="tab">
                <div class="date">${data.date2.date}</div>
                <div class="day">${data.date2.dayOfWeek}</div>
              </div>
              <div class="tab">
                <div class="date">${data.date3.date}</div>
                <div class="day">${data.date3.dayOfWeek}</div>
              </div>
              <div class="tab">
                <div class="date">${data.date4.date}</div>
                <div class="day">${data.date4.dayOfWeek}</div>
              </div>
            </nav>
          </header>

          <div class="timeline" id="timeline-container">
            <div class="timeline-line"></div>
            ${data.timelineItems.map((item, index) => `
            <section class="timeline-item">
              <div class="timeline-marker-container">
                <time class="time-marker">${item.time}</time>
                <div class="point-marker"></div>
                <div class="point-number">${index + 1}</div>
              </div>
              <div class="timeline-details">
                <div class="activity-info">
                  <span class="activity-label">${item.activityLabel}</span>
                  <h2 class="activity-name">${item.activityName}</h2>
                  <div class="activity-location">${item.activityLocation}</div>
                  <div class="activity-detail activity-duration">所要時間: ${item.duration}</div>
                  <div class="activity-detail activity-distance">距離: ${item.distance}</div>
                  ${item.notes ? `<p class="activity-notes">${item.notes}</p>` : ''}
                </div>
                ${item.reservationUrl ? `<a class="reservation-button" href="${item.reservationUrl}" target="_blank">${item.reservationButtonText}</a>` : ''}
                ${item.actionButtonText ? `<button class="reservation-button">${item.actionButtonText}</button>` : ''}
              </div>
            </section>
            `).join('')}
          </div>

          <!-- フローティングボタン -->
          <button class="add-button">+</button>

          <!-- 固定日付バッジ -->
          <div class="date-badge">
            <div>📅</div>
            <div class="date-badge-text">今日</div>
            <div class="date-badge-day">${data.activeDate.date}</div>
          </div>

          <!-- EV情報バッジ -->
          <div class="ev-status">
            <div class="battery-level">
              🔋 ${data.evStatus.batteryLevel}%
            </div>
            <div class="range-info">
              ${data.evStatus.remainingRange} km走行可能
            </div>
          </div>
        </main>
      `;
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('pageTitle').textContent = templateData.pageTitle;
      document.getElementById('appContainer').innerHTML = renderHTML(templateData);
    });
  </script>
</body>
</html>
"""

authenticator.login()
if st.session_state["authentication_status"]:
    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    
    # HTML埋め込み
    # st.markdown(HTML, unsafe_allow_html=True)
    components.html(
        HTML,
        height=800,
        scrolling=True,
        )

elif st.session_state["authentication_status"] is False:
    ## ログイン成功ログイン失敗
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    ## デフォルト
    st.warning('Please enter your username and password')
