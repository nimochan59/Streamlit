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
  <title>電気自動車 旅程プラン</title>
  <style>
    /* リセットCSSと基本スタイル (前回のコードから変更なし) */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
      background-color: #f5f5f5;
      color: #333;
      line-height: 1.6;
      padding: 20px; /* body padding を追加 */
    }

    /* ヘッダー (ステータスバー、ナビゲーションバー) (前回のコードから変更なし) */
    .status-bar, .nav-bar, .tab-container, .transport-selector, .cost-info {
      background-color: white;
      padding: 10px 15px;
      margin-bottom: 10px;
    }

    .status-bar, .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .left-status {
      font-weight: bold;
      font-size: 18px;
    }

    .right-status {
      display: flex;
      gap: 10px;
    }

    .back-button {
      font-size: 24px;
      cursor: pointer;
    }

    .actions {
      display: flex;
      gap: 20px;
    }

    .actions span {
      cursor: pointer;
    }

    /* タブコンテナ (前回のコードから変更なし) */
    .tab-container {
      display: flex;
      border-bottom: 1px solid #eee;
    }

    .tab {
      flex: 1;
      text-align: center;
      padding: 10px 0;
      border-bottom: 3px solid transparent;
      cursor: pointer;
    }

    .tab.active {
      border-bottom: 3px solid #3b82f6;
      color: #3b82f6;
    }

    .date {
      font-size: 16px;
    }

    .day {
      font-size: 12px;
      color: #666;
    }

    /* 交通手段セレクター (前回のコードから変更なし) */
    .transport-selector {
      display: flex;
      align-items: center;
      gap: 10px;
      background-color: #e0f7fa;
      border-radius: 25px;
      padding: 10px 20px;
      margin: 15px auto;
      max-width: 300px;
      cursor: pointer;
    }

    /* 費用情報 (前回のコードから変更なし) */
    .cost-info {
      display: flex;
      justify-content: center;
      gap: 30px;
      margin-bottom: 20px;
      color: #777;
    }

    /* タイムライン (前回のコードから微修正) */
    .timeline {
      display: flex;
      flex-direction: column;
      padding-left: 20px;
      margin-top: 20px;
      position: relative;
      max-width: 960px; /* timeline の最大幅を設定 */
      margin: 20px auto; /* 中央寄せ */
    }

    .timeline-line {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 35px;
      width: 2px;
      background-color: #ccc;
      z-index: -1;
    }

    .timeline-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: 20px;
    }

    .timeline-item:last-child {
      margin-bottom: 0;
    }

    .timeline-marker-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-right: 20px;
    }

    .time-marker {
      font-size: 14px;
      color: #777;
      margin-bottom: 5px;
      text-align: right;
      width: 80px; /* 時間マーカーの幅を広げました */
    }

    .point-marker {
      width: 12px;
      height: 12px;
      background-color: white;
      border: 2px solid #aaa;
      border-radius: 50%;
      z-index: 1;
    }

    .point-number {
      background-color: #3b82f6;
      color: white;
      border-radius: 50%;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
      margin-top: 5px;
    }


    .timeline-details {
      background-color: #fff;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.05);
      width: 100%;
      display: flex; /* Flexbox を適用 */
      justify-content: space-between; /* 左右に要素を配置 */
      align-items: flex-start; /* 上揃え */
    }

    .activity-info {
      flex: 1; /* activity-info が残り幅を占める */
      margin-right: 15px; /* reservation-button との間隔 */
    }


    .activity-label {
      font-size: 12px;
      color: #888;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .activity-name {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 10px;
      color: #333;
    }

    .activity-location {
      font-size: 16px;
      color: #555;
      margin-bottom: 0; /* activity-location の margin-bottom を 0 に */
    }

    .activity-duration, .activity-distance, .activity-reason, .activity-notes {
      font-size: 14px;
      color: #666;
      margin-top: 5px;
    }

    .activity-notes {
      margin-top: 10px;
      border-top: 1px dashed #eee;
      padding-top: 10px;
    }

    /* reservation-button スタイル */
    .reservation-button {
      display: inline-block;
      padding: 10px 15px;
      background-color: #4caf50; /* 緑色 */
      color: white;
      text-decoration: none;
      border-radius: 5px;
      font-size: 14px;
      white-space: nowrap; /* ボタンテキストを折り返さない */
      margin-top: 10px; /* 上マージンを追加 */
    }

    .reservation-button:hover {
      background-color: #43a047; /* ホバー時、少し暗い緑 */
    }


    /* transport-detail, waiting-time (前回のコードから変更なし) */
    .transport-detail, .waiting-time {
      background-color: #fff;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.05);
      margin-left: 55px;
      margin-bottom: 20px;
      max-width: 940px; /* transport-detail の最大幅を timeline に合わせる */
    }

    .waiting-time {
      text-align: center;
      color: #777;
      font-style: italic;
    }

    .transport-detail > div {
      margin-bottom: 10px;
    }

    .transport-detail > div:last-child {
      margin-bottom: 0;
    }

    .transport-header {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #555;
    }

    .transport-time-cost {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: #666;
    }

    .transport-icons {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #777;
      font-size: 14px;
    }


    /* フローティングボタン (前回のコードから変更なし) */
    .add-button {
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 60px;
      height: 60px;
      background-color: #3b82f6;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      cursor: pointer;
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* PC表示での調整 (前回のコードから微修正) */
    @media screen and (min-width: 768px) {
      body {
        padding: 30px; /* body padding を大きく */
        max-width: 1200px; /* 最大幅を広げる */
        margin: 0 auto;
      }

      .status-bar, .nav-bar, .tab-container, .transport-selector, .cost-info {
        padding: 15px 20px;
        margin-bottom: 15px;
      }

      .timeline {
        padding-left: 30px;
        max-width: 1180px; /* timeline の最大幅を body に合わせる */
      }

      .time-marker {
        font-size: 16px;
        width: 100px; /* 時間マーカーの幅を広げました */
      }

      .point-marker {
        width: 14px;
        height: 14px;
      }

      .point-number {
        width: 28px;
        height: 28px;
        font-size: 14px;
      }

      .timeline-details {
        padding: 20px;
        max-width: 1000px; /* timeline-details の最大幅を広げる */
      }

      .transport-detail, .waiting-time {
         padding: 20px;
         margin-left: 75px;
         max-width: 980px; /* transport-detail の最大幅を timeline-details に合わせる */
      }

      .add-button {
        width: 70px;
        height: 70px;
        bottom: 40px;
        right: 40px;
      }

      .reservation-button {
        font-size: 16px; /* PC表示で予約ボタンのフォントサイズを大きく */
        padding: 12px 20px; /* PC表示で予約ボタンの padding を大きく */
      }
    }
  </style>
</head>
<body>
  <div class="status-bar">
    <div class="left-status">10:40 ◀</div>
    <div class="right-status">
      <span>●●● ≡</span>
      <span>📶</span>
      <span>🔋45%</span>
    </div>
  </div>

  <div class="nav-bar">
    <div class="back-button">←</div>
    <div class="actions">
      <span>❓</span>
      <span>👤+</span>
      <span>📊</span>
      <span>⋮</span>
    </div>
  </div>

  <div class="tab-container">
    <div class="tab">
      <div>📅</div>
      <div class="day">プラン</div>
    </div>
    <div class="tab active">
      <div class="date">3/9</div>
      <div class="day">日</div>
    </div>
    <div class="tab">
      <div class="date">3/10</div>
      <div class="day">月</div>
    </div>
  </div>

  <div class="transport-selector">
    <span>⚡️</span>
    <span>電気自動車</span>
    <span>▼</span>
  </div>

  <div class="cost-info">
    <div>🚶 ¥1,500</div>
    <div>充電 ¥500</div>
  </div>

  <div class="timeline" id="timeline-container">
    <div class="timeline-line"></div>
    <!-- 旅程プランがここに動的に生成されます -->
  </div>

  <div class="add-button">
    <span>📍+</span>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
      renderItinerary(dummyItineraryData); // ダミーデータで初期表示
    });

    const dummyItineraryData = [
      {
        "time": "10:00",
        "label": "出発",
        "activity": "自宅を出発",
        "location": "自宅",
        "duration": "0分",
        "distance": "0km",
      },
      {
        "time": "11:00",
        "label": "充電",
        "activity": "急速充電",
        "location": "海老名SA(下り)充電ステーション",
        "duration": "30分",
        "distance": "約50km",
        "notes": "EXPASA海老名(下り)に到着。急速充電30分",
        "transport_detail": {
          "transport_type": "car",
          "time": "約1時間",
          "icons": ["🚗", "⚡️"]
        }
      },
      {
        "time": "11:30",
        "label": "移動",
        "activity": "箱根へドライブ",
        "location": "箱根",
        "duration": "30分",
        "distance": "約20km",
        "notes": "充電後、箱根に向けて出発",
        "transport_detail": {
          "transport_type": "car",
          "time": "約30分",
          "icons": ["🚗"]
        }
      },
      {
        "time": "12:00",
        "label": "食事",
        "activity": "EV充電対応レストラン検索",
        "location": "箱根周辺",
        "duration": "30分",
        "distance": " ",
        "notes": "ランチ場所を検索",
        "has_reservation_button": false, // 予約ボタンなし
      },
      {
        "time": "12:30",
        "label": "食事",
        "activity": "仙石原 すすき草原",
        "location": "仙石原",
        "duration": "1時間30分",
        "distance": " ",
        "notes": "すすきヶ原を散策",
        "has_reservation_button": false, // 予約ボタンなし
      },
      {
        "time": "14:00",
        "label": "レジャー",
        "activity": "箱根ガラスの森美術館",
        "location": "箱根ガラスの森美術館",
        "duration": "2時間",
        "distance": " ",
        "notes": "ヴェネチアン・グラス美術館",
        "has_reservation_button": true, // 予約ボタンあり
        "reservation_url": "https://www.hakone-garasunomori.jp/" // 予約URL
      },
      {
        "time": "16:00",
        "label": "移動",
        "activity": "ホテルへ移動",
        "location": "ホテル",
        "duration": "30分",
        "distance": "約10km",
        "notes": "ホテルへ移動",
        "transport_detail": {
          "transport_type": "car",
          "time": "約30分",
          "icons": ["🚗"]
        }
      },
      {
        "time": "16:30",
        "label": "ホテル",
        "activity": "ホテルチェックイン",
        "location": "箱根ホテル",
        "duration": "30分",
        "distance": " ",
        "notes": "チェックイン",
        "has_reservation_button": false, // 予約ボタンなし
      },
      {
        "time": "17:00",
        "label": "休憩",
        "activity": "ホテルで休憩",
        "location": "ホテル",
        "duration": "1時間",
        "distance": " ",
        "notes": "温泉に入る",
        "has_reservation_button": false, // 予約ボタンなし
      },
      {
        "time": "18:00",
        "label": "夕食",
        "activity": "ホテル内レストラン",
        "location": "ホテル内",
        "duration": "2時間",
        "distance": " ",
        "notes": "夕食",
        "has_reservation_button": true, // 予約ボタンあり
        "reservation_url": "https://www.hakone-hotel.jp/restaurant/" // 予約URL
      }
    ];


    function renderItinerary(itinerary) {
      const timelineContainer = document.getElementById('timeline-container');
      timelineContainer.innerHTML = ''; // 既存の表示をクリア

      if (!itinerary || !Array.isArray(itinerary)) {
        displayErrorMessage('無効な旅程プランデータです。');
        return;
      }

      itinerary.forEach((item, index) => {
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item';

        // マーカーコンテナ
        const markerContainer = document.createElement('div');
        markerContainer.className = 'timeline-marker-container';

        const timeMarker = document.createElement('div');
        timeMarker.className = 'time-marker';
        timeMarker.textContent = item.time;
        markerContainer.appendChild(timeMarker);

        const pointMarker = document.createElement('div');
        pointMarker.className = 'point-marker';
        markerContainer.appendChild(pointMarker);

        const pointNumber = document.createElement('div');
        pointNumber.className = 'point-number';
        pointNumber.textContent = index + 1;
        markerContainer.appendChild(pointNumber);

        timelineItem.appendChild(markerContainer);

        // タイムライン詳細
        const timelineDetails = document.createElement('div');
        timelineDetails.className = 'timeline-details';

        // アクティビティ情報コンテナ
        const activityInfo = document.createElement('div');
        activityInfo.className = 'activity-info';

        const label = document.createElement('div');
        label.className = 'activity-label';
        label.textContent = item.label;
        activityInfo.appendChild(label);

        const name = document.createElement('div');
        name.className = 'activity-name';
        name.textContent = item.activity;
        activityInfo.appendChild(name);

        const location = document.createElement('div');
        location.className = 'activity-location';
        location.textContent = item.location;
        activityInfo.appendChild(location);

        if (item.duration) {
          const duration = document.createElement('div');
          duration.className = 'activity-duration';
          duration.textContent = `所要時間: ${item.duration}`;
          activityInfo.appendChild(duration);
        }
        if (item.distance) {
          const distance = document.createElement('div');
          distance.className = 'activity-distance';
          distance.textContent = `距離: ${item.distance}`;
          activityInfo.appendChild(distance);
        }
        if (item.notes) {
          const notes = document.createElement('div');
          notes.className = 'activity-notes';
          notes.textContent = `備考: ${item.notes}`;
          activityInfo.appendChild(notes);
        }

        timelineDetails.appendChild(activityInfo); // activityInfo を timelineDetails に追加


        // 予約ボタン
        if (item.has_reservation_button) {
          const reservationButton = document.createElement('a');
          reservationButton.className = 'reservation-button';
          reservationButton.href = item.reservation_url;
          reservationButton.textContent = '予約';
          reservationButton.target = '_blank'; // 別タブで開く
          timelineDetails.appendChild(reservationButton); // 予約ボタンを timelineDetails に追加
        }


        timelineItem.appendChild(timelineDetails);
        timelineContainer.appendChild(timelineItem);

        // transport-detail (変更なし)
        if (item.transport_detail) {
          const transportDetailDiv = document.createElement('div');
          transportDetailDiv.className = 'transport-detail';

          const transportHeader = document.createElement('div');
          transportHeader.className = 'transport-header';
          transportHeader.innerHTML = `<span>🚇</span><span>公共交通機関</span><span>▼</span>`;
          if (item.transport_detail.transport_type === 'car') {
             transportHeader.innerHTML = `<span>🚗</span><span>自家用車</span><span>▼</span>`;
          } else if (item.transport_detail.transport_type === 'train') {
             transportHeader.innerHTML = `<span>🚄</span><span>電車</span><span>▼</span>`;
          }


          const transportTimeCost = document.createElement('div');
          transportTimeCost.className = 'transport-time-cost';
          transportTimeCost.innerHTML = `<div class="transport-time">${item.transport_detail.time}</div><div class="transport-cost">${item.transport_detail.cost}</div>`;

          const transportIcons = document.createElement('div');
          transportIcons.className = 'transport-icons';
          if (item.transport_detail.icons && Array.isArray(item.transport_detail.icons)) {
              transportIcons.innerHTML = item.transport_detail.icons.join('<span></span>');
          } else {
              transportIcons.innerHTML = `<span></span><span></span><span></span>`;
          }


          transportDetailDiv.appendChild(transportHeader);
          transportDetailDiv.appendChild(transportTimeCost);
          transportDetailDiv.appendChild(transportIcons);

          timelineContainer.appendChild(transportDetailDiv);
        }

        // waiting-time (変更なし)
        if (item.waiting_time) {
          const waitingTimeDiv = document.createElement('div');
          waitingTimeDiv.className = 'waiting-time';
          waitingTimeDiv.textContent = item.waiting_time;
          timelineContainer.appendChild(waitingTimeDiv);
        }
      });
    }

    function displayErrorMessage(message) {
      const timelineContainer = document.getElementById('timeline-container');
      const errorElement = document.createElement('div');
      errorElement.style.color = 'red';
      errorElement.textContent = message;
      timelineContainer.appendChild(errorElement);
    }
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
    st.write('# ログインしました!')
    
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
