import streamlit as st
import json
from typing import Dict, List, Any
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="2026年衆院選 政策比較アプリ",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - スマートフォン対応のレスポンシブデザイン + ダークモード対応
st.markdown("""
    <style>
    /* 全体のフォント設定 */
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* ヘッダー */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: white !important;
    }
    
    .header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* ライトモード用の政党カード */
    [data-testid="stAppViewContainer"][data-theme="light"] .party-card {
        background: white;
        border-radius: 16px;
        padding: 0;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    /* ダークモード用の政党カード */
    [data-testid="stAppViewContainer"][data-theme="dark"] .party-card {
        background: #2d3748;
        border-radius: 16px;
        padding: 0;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
        border: 2px solid #4a5568;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .party-card:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transform: translateY(-4px);
    }
    
    /* ライトモード用の政党名 */
    [data-testid="stAppViewContainer"][data-theme="light"] .party-name {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        letter-spacing: 0.08em;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        text-align: center;
        border-bottom: 4px solid rgba(255, 255, 255, 0.3);
    }
    
    /* ダークモード用の政党名 */
    [data-testid="stAppViewContainer"][data-theme="dark"] .party-name {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        letter-spacing: 0.08em;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        text-align: center;
        border-bottom: 4px solid rgba(255, 255, 255, 0.2);
    }
    
    /* カードの内側のパディング */
    .party-card-content {
        padding: 1.5rem;
    }
    
    .policy-section {
        margin-bottom: 2rem;
    }
    
    /* ライトモード用のセクションタイトル */
    [data-testid="stAppViewContainer"][data-theme="light"] .policy-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 8px;
        border-left: 5px solid #667eea;
    }

    /* ライトモード用の政策カテゴリラベル */
    [data-testid="stAppViewContainer"][data-theme="light"] .policy-category-label {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        background-color: #e0e7ff;
        color: #3730a3;
        font-weight: 700;
        font-size: 0.95rem;
    }
    
    /* ダークモード用のセクションタイトル */
    [data-testid="stAppViewContainer"][data-theme="dark"] .policy-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f7fafc;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%);
        border-radius: 8px;
        border-left: 5px solid #667eea;
    }

    /* ダークモード用の政策カテゴリラベル */
    [data-testid="stAppViewContainer"][data-theme="dark"] .policy-category-label {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        background-color: #4338ca;
        color: #e0e7ff;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .explanation-label {
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    /* 長文の折り返し対策（政策・解説） */
    .party-card .policy-item {
        overflow-wrap: anywhere;
        word-break: break-word;
        white-space: normal;
    }

    .party-card [data-testid="stExpander"] summary {
        overflow-wrap: anywhere;
        word-break: break-word;
        white-space: normal;
    }

    .party-card [data-testid="stAlert"] {
        overflow-wrap: anywhere;
        word-break: break-word;
        white-space: normal;
    }
    
    /* ライトモード用の政策アイテム */
    [data-testid="stAppViewContainer"][data-theme="light"] .policy-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background-color: #f9fafb;
        border-left: 4px solid #667eea;
        border-radius: 6px;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #1f2937;
    }
    
    /* ダークモード用の政策アイテム */
    [data-testid="stAppViewContainer"][data-theme="dark"] .policy-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background-color: #1a202c;
        border-left: 4px solid #667eea;
        border-radius: 6px;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #f7fafc;
    }
    
    /* ライトモード用の候補者カード */
    [data-testid="stAppViewContainer"][data-theme="light"] .candidate-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* ダークモード用の候補者カード */
    [data-testid="stAppViewContainer"][data-theme="dark"] .candidate-card {
        background: #2d3748;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #4a5568;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    /* ライトモード用の候補者名 */
    [data-testid="stAppViewContainer"][data-theme="light"] .candidate-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
    }
    
    /* ダークモード用の候補者名 */
    [data-testid="stAppViewContainer"][data-theme="dark"] .candidate-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f7fafc;
    }
    
    .candidate-party {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: #dbeafe;
        color: #1e40af;
        border-radius: 12px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* ライトモード用の候補者メモ */
    [data-testid="stAppViewContainer"][data-theme="light"] .candidate-note {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* ダークモード用の候補者メモ */
    [data-testid="stAppViewContainer"][data-theme="dark"] .candidate-note {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* ライトモード用のセクション見出し */
    [data-testid="stAppViewContainer"][data-theme="light"] .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* ダークモード用のセクション見出し */
    [data-testid="stAppViewContainer"][data-theme="dark"] .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f7fafc;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4a5568;
    }
    
    /* レスポンシブ対応 */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.4rem;
        }
        
        .party-name {
            font-size: 1.6rem !important;
            padding: 1rem 1.5rem !important;
        }
        
        .section-header {
            font-size: 1.3rem;
        }
    }
    
    /* ライトモード用の空状態メッセージ */
    [data-testid="stAppViewContainer"][data-theme="light"] .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #6b7280;
    }
    
    /* ダークモード用の空状態メッセージ */
    [data-testid="stAppViewContainer"][data-theme="dark"] .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #94a3b8;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_election_data() -> Dict[str, Any]:
    """
    election_data.jsonを読み込む
    Geminiが生成したデータ構造に柔軟に対応
    """
    json_path = Path(__file__).parent / "election_data.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"データファイルが見つかりません: {json_path}")
        return {"parties": [], "districts": {}}
    except json.JSONDecodeError as e:
        st.error(f"JSONファイルの形式が正しくありません: {e}")
        return {"parties": [], "districts": {}}
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return {"parties": [], "districts": {}}


def get_all_profession_keys(parties: List[Dict]) -> List[str]:
    """
    全政党のpersonalized_policiesから職種キーを抽出
    """
    professions = set()
    for party in parties:
        if "personalized_policies" in party and isinstance(party["personalized_policies"], dict):
            professions.update(party["personalized_policies"].keys())
    return sorted(list(professions))


def get_all_general_policy_keys(parties: List[Dict]) -> List[str]:
    """
    全政党のgeneral_policiesから政策トピックを抽出
    """
    topics = set()
    for party in parties:
        if "general_policies" in party and isinstance(party["general_policies"], dict):
            topics.update(party["general_policies"].keys())
    return sorted(list(topics))


def display_party_card(party: Dict, selected_professions: List[str], selected_topics: List[str], 
                       show_explanations: bool = True):
    """
    政党カードを表示（選択された項目のみ）
    解説機能付き - 政党名を大きく目立たせる
    """
    def normalize_explanation(value: Any) -> str:
        if isinstance(value, list):
            items = [item.strip() for item in value if isinstance(item, str) and item.strip()]
            return "\n\n".join(items)
        if isinstance(value, str):
            return value.strip()
        return ""

    party_name = party.get("name", "不明な政党")
    
    # カード全体のHTML開始（政党名をヘッダーとして表示）
    card_html = f"""
    <div style="
        background: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 2px solid #e5e7eb;
        overflow: hidden;
    ">
        <div style="
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            padding: 0.9rem 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            text-align: center;
            border-bottom: 3px solid rgba(255, 255, 255, 0.3);
        ">
            {party_name}
        </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # コンテンツエリアの開始（政策がある場合のみパディングを追加）
    has_content = (selected_professions and "personalized_policies" in party) or \
                  (selected_topics and "general_policies" in party)
    
    if has_content:
        st.markdown('<div style="padding: 1.5rem;">', unsafe_allow_html=True)
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # 専門職向け政策の表示
    if selected_professions and "personalized_policies" in party:
        personalized = party["personalized_policies"]
        explanations = party.get("personalized_explanations", {}) if show_explanations else {}
        
        for profession in selected_professions:
            if profession in personalized:
                policies = personalized[profession]
                
                # セクションタイトル
                st.markdown(f"""
                <div style="
                    font-size: 1.1rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 1rem;
                    margin-top: 1rem;
                    padding: 0.75rem 1rem;
                    background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 100%);
                    border-radius: 8px;
                    border-left: 5px solid #667eea;
                ">
                    <span style="
                        display: inline-block;
                        padding: 0.15rem 0.6rem;
                        border-radius: 999px;
                        background-color: #e0e7ff;
                        color: #3730a3;
                        font-weight: 700;
                        font-size: 0.95rem;
                    ">🏥 {profession}向け政策</span>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(policies, list):
                    # リスト形式の政策
                    for i, policy in enumerate(policies):
                        explanation = None
                        if show_explanations and profession in explanations:
                            profession_explanations = explanations.get(profession)
                            if isinstance(profession_explanations, list) and i < len(profession_explanations):
                                explanation = normalize_explanation(profession_explanations[i])
                            elif isinstance(profession_explanations, str):
                                explanation = normalize_explanation(profession_explanations)

                        if explanation:
                            with st.expander(f"💡 {policy}", expanded=False):
                                st.markdown('<div style="font-weight: 700; margin-bottom: 0.25rem;">解説</div>', unsafe_allow_html=True)
                                st.info(explanation)
                        else:
                            st.markdown(f"""
                            <div style="
                                padding: 0.75rem 1rem;
                                margin: 0.5rem 0;
                                background-color: #f9fafb;
                                border-left: 4px solid #667eea;
                                border-radius: 6px;
                                font-size: 0.95rem;
                                line-height: 1.7;
                                color: #1f2937;
                            ">• {policy}</div>
                            """, unsafe_allow_html=True)
                
                elif isinstance(policies, str):
                    if show_explanations and profession in explanations:
                        profession_explanations = explanations.get(profession)
                        explanation = normalize_explanation(profession_explanations)

                        if explanation:
                            with st.expander(f"💡 {policies}", expanded=False):
                                st.markdown('<div style="font-weight: 700; margin-bottom: 0.25rem;">解説</div>', unsafe_allow_html=True)
                                st.info(explanation)
                        else:
                            st.markdown(f"""
                            <div style="
                                padding: 0.75rem 1rem;
                                margin: 0.5rem 0;
                                background-color: #f9fafb;
                                border-left: 4px solid #667eea;
                                border-radius: 6px;
                                font-size: 0.95rem;
                                line-height: 1.7;
                                color: #1f2937;
                            ">{policies}</div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            padding: 0.75rem 1rem;
                            margin: 0.5rem 0;
                            background-color: #f9fafb;
                            border-left: 4px solid #667eea;
                            border-radius: 6px;
                            font-size: 0.95rem;
                            line-height: 1.7;
                            color: #1f2937;
                        ">{policies}</div>
                        """, unsafe_allow_html=True)
    
    # 一般政策の表示
    if selected_topics and "general_policies" in party:
        general = party["general_policies"]
        general_explanations = party.get("general_explanations", {}) if show_explanations else {}
        
        # セクションタイトル
        st.markdown(f"""
        <div style="
            font-size: 1.1rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 1rem;
            margin-top: 1rem;
            padding: 0.75rem 1rem;
            background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 100%);
            border-radius: 8px;
            border-left: 5px solid #667eea;
        ">
            <span style="
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                background-color: #e0e7ff;
                color: #3730a3;
                font-weight: 700;
                font-size: 0.95rem;
            ">📋 一般政策</span>
        </div>
        """, unsafe_allow_html=True)
        
        for topic in selected_topics:
            if topic in general:
                policy = general[topic]
                
                if show_explanations and topic in general_explanations:
                    explanation = general_explanations[topic]
                    with st.expander(f"💡 {topic}: {policy}", expanded=False):
                        st.markdown('<div style="font-weight: 700; margin-bottom: 0.25rem;">解説</div>', unsafe_allow_html=True)
                        st.info(explanation)
                else:
                    st.markdown(f"""
                    <div style="
                        padding: 0.75rem 1rem;
                        margin: 0.5rem 0;
                        background-color: #f9fafb;
                        border-left: 4px solid #667eea;
                        border-radius: 6px;
                        font-size: 0.95rem;
                        line-height: 1.7;
                        color: #1f2937;
                    "><strong>{topic}:</strong> {policy}</div>
                    """, unsafe_allow_html=True)
    
    # カード終了
    if has_content:
        st.markdown('</div>', unsafe_allow_html=True)  # コンテンツエリア終了
    st.markdown('</div>', unsafe_allow_html=True)  # カード終了


def display_candidates(district_name: str, candidates: List[Dict]):
    """
    候補者リストを表示
    """
    st.markdown(f'<div class="section-header">📍 {district_name}の立候補者</div>', 
                unsafe_allow_html=True)
    
    if not candidates:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <p>この選挙区の候補者情報はまだ登録されていません</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    for candidate in candidates:
        name = candidate.get("name", "不明")
        party = candidate.get("party", "無所属")
        note = candidate.get("note", "")
        
        st.markdown(f"""
            <div class="candidate-card">
                <div class="candidate-name">{name}</div>
                <div class="candidate-party">{party}</div>
                {f'<div class="candidate-note">{note}</div>' if note else ''}
            </div>
        """, unsafe_allow_html=True)


def main():
    # ヘッダー
    st.markdown("""
        <div class="header">
            <h1>🗳️ 2026年衆議院議員総選挙 政策比較</h1>
            <p>2026年2月8日投開票 | あなたと家族のための政策ガイド</p>
        </div>
    """, unsafe_allow_html=True)
    
    # データ読み込み
    data = load_election_data()
    parties = data.get("parties", [])
    districts = data.get("districts", {})
    
    if not parties:
        st.warning("政党データが読み込めませんでした。election_data.jsonを確認してください。")
        return
    
    # 利用可能な職種と一般トピックを動的に取得
    available_professions = get_all_profession_keys(parties)
    available_topics = get_all_general_policy_keys(parties)
    
    # サイドバー - ユーザー属性と関心事の選択
    with st.sidebar:
        st.markdown("### 👤 あなたの属性を選択")
        st.markdown("*複数選択可能です*")
        
        selected_professions = st.multiselect(
            "職種・立場",
            options=available_professions,
            default=[],
            help="あなたやご家族に該当する職種を選択してください"
        )
        
        st.markdown("---")
        st.markdown("### 📌 関心のある政策")
        
        selected_topics = st.multiselect(
            "政策トピック",
            options=available_topics,
            default=[],
            help="比較したい政策分野を選択してください"
        )
        
        st.markdown("---")
        st.markdown("### 💡 表示設定")
        
        show_explanations = st.checkbox(
            "詳しい解説を表示",
            value=False,
            help="政策の詳しい説明を展開可能な形式で表示します（オンにすると表示項目が増えます）"
        )
        
        st.markdown("---")
        st.markdown("### 🗺️ 選挙区検索")
        
        district_list = ["選択してください"] + sorted(list(districts.keys()))
        selected_district = st.selectbox(
            "お住まいの選挙区",
            options=district_list,
            help="選挙区を選択すると候補者情報が表示されます"
        )
    
    # メインコンテンツ
    if not selected_professions and not selected_topics:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">👈</div>
                <p>左のサイドバーから、あなたの属性や関心のある政策を選択してください</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # 政策比較セクション
    st.markdown('<div class="section-header">🎯 政党別政策比較</div>', unsafe_allow_html=True)
    
    # 選択された項目の表示
    col1, col2 = st.columns(2)
    with col1:
        if selected_professions:
            st.info(f"**選択中の属性:** {', '.join(selected_professions)}")
    with col2:
        if selected_topics:
            st.info(f"**選択中のトピック:** {', '.join(selected_topics)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 政党カードをカラム表示（レスポンシブ対応）
    # PC: 2カラム、タブレット: 2カラム、スマホ: 1カラム（自動調整）
    num_parties = len(parties)
    
    if num_parties == 0:
        st.warning("表示できる政党がありません")
        return
    
    # 2カラムレイアウト
    for i in range(0, num_parties, 2):
        cols = st.columns(2)
        
        # 左カラム
        with cols[0]:
            display_party_card(parties[i], selected_professions, selected_topics, show_explanations)
        
        # 右カラム（存在する場合のみ）
        if i + 1 < num_parties:
            with cols[1]:
                display_party_card(parties[i + 1], selected_professions, selected_topics, show_explanations)
    
    # 候補者情報セクション
    if selected_district and selected_district != "選択してください":
        st.markdown("<br><br>", unsafe_allow_html=True)
        candidates = districts.get(selected_district, [])
        display_candidates(selected_district, candidates)
    
    # フッター
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.85rem;">
            <p>このアプリは各政党の公約を比較するための参考情報です。<br>
            投票の際は、必ず公式情報もご確認ください。</p>
            <p style="margin-top: 1rem;">💡 <strong>データ更新:</strong> 最新の公約情報は election_data.json で管理されています</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
