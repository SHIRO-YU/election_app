#!/usr/bin/env python3
"""
election_data.json の構造を検証するスクリプト
Geminiが生成したデータが正しい形式かチェックします
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def validate_json_syntax(file_path: Path) -> tuple[bool, str]:
    """JSONファイルの構文をチェック"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "✅ JSON構文: 正常"
    except json.JSONDecodeError as e:
        return False, f"❌ JSON構文エラー: {e}"
    except Exception as e:
        return False, f"❌ ファイル読み込みエラー: {e}"


def validate_structure(data: Dict) -> List[str]:
    """データ構造を検証"""
    issues = []
    
    # トップレベルのキーをチェック
    if "parties" not in data:
        issues.append("❌ 'parties' キーが存在しません")
    if "districts" not in data:
        issues.append("❌ 'districts' キーが存在しません")
    
    # parties の検証
    if "parties" in data:
        parties = data["parties"]
        
        if not isinstance(parties, list):
            issues.append("❌ 'parties' はリストである必要があります")
        elif len(parties) == 0:
            issues.append("⚠️  'parties' が空です")
        else:
            for i, party in enumerate(parties):
                party_issues = validate_party(party, i)
                issues.extend(party_issues)
    
    # districts の検証
    if "districts" in data:
        districts = data["districts"]
        
        if not isinstance(districts, dict):
            issues.append("❌ 'districts' は辞書である必要があります")
        elif len(districts) == 0:
            issues.append("⚠️  'districts' が空です")
        else:
            for district_name, candidates in districts.items():
                district_issues = validate_district(district_name, candidates)
                issues.extend(district_issues)
    
    return issues


def validate_party(party: Dict, index: int) -> List[str]:
    """政党データを検証"""
    issues = []
    prefix = f"政党[{index}]"
    
    # 必須フィールド
    if "name" not in party:
        issues.append(f"❌ {prefix}: 'name' フィールドがありません")
    elif not party["name"]:
        issues.append(f"⚠️  {prefix}: 'name' が空です")
    
    party_name = party.get("name", f"インデックス{index}")
    
    # personalized_policies の検証
    if "personalized_policies" in party:
        pp = party["personalized_policies"]
        
        if not isinstance(pp, dict):
            issues.append(f"❌ {party_name}: 'personalized_policies' は辞書である必要があります")
        else:
            if len(pp) == 0:
                issues.append(f"⚠️  {party_name}: 'personalized_policies' が空です")
            
            for profession, policies in pp.items():
                # 文字列形式またはリスト形式の両方をサポート
                if not isinstance(policies, (list, str)):
                    issues.append(f"❌ {party_name} - {profession}: 政策は文字列またはリストである必要があります")
                elif isinstance(policies, list) and len(policies) == 0:
                    issues.append(f"⚠️  {party_name} - {profession}: 政策リストが空です")
                elif isinstance(policies, str) and not policies:
                    issues.append(f"⚠️  {party_name} - {profession}: 政策が空文字列です")
    else:
        issues.append(f"⚠️  {party_name}: 'personalized_policies' フィールドがありません")
    
    # personalized_explanations の検証（オプション）
    if "personalized_explanations" in party:
        pe = party["personalized_explanations"]
        
        if not isinstance(pe, dict):
            issues.append(f"❌ {party_name}: 'personalized_explanations' は辞書である必要があります")
        else:
            for profession, explanation in pe.items():
                # 文字列形式またはリスト形式の両方をサポート
                if not isinstance(explanation, (str, list)):
                    issues.append(f"❌ {party_name} - {profession}の解説: 文字列またはリストである必要があります")
    
    # general_policies の検証
    if "general_policies" in party:
        gp = party["general_policies"]
        
        if not isinstance(gp, dict):
            issues.append(f"❌ {party_name}: 'general_policies' は辞書である必要があります")
        else:
            if len(gp) == 0:
                issues.append(f"⚠️  {party_name}: 'general_policies' が空です")
            
            for topic, policy in gp.items():
                if not isinstance(policy, str):
                    issues.append(f"❌ {party_name} - {topic}: 政策は文字列である必要があります")
                elif not policy:
                    issues.append(f"⚠️  {party_name} - {topic}: 政策内容が空です")
    else:
        issues.append(f"⚠️  {party_name}: 'general_policies' フィールドがありません")
    
    # general_explanations の検証（オプション）
    if "general_explanations" in party:
        ge = party["general_explanations"]
        
        if not isinstance(ge, dict):
            issues.append(f"❌ {party_name}: 'general_explanations' は辞書である必要があります")
        else:
            for topic, explanation in ge.items():
                if not isinstance(explanation, str):
                    issues.append(f"❌ {party_name} - {topic}の解説: 文字列である必要があります")
    
    return issues


def validate_district(district_name: str, candidates: List) -> List[str]:
    """選挙区データを検証"""
    issues = []
    
    if not isinstance(candidates, list):
        issues.append(f"❌ {district_name}: 候補者リストはリストである必要があります")
        return issues
    
    if len(candidates) == 0:
        issues.append(f"⚠️  {district_name}: 候補者が登録されていません")
    
    for i, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            issues.append(f"❌ {district_name} - 候補者[{i}]: 辞書である必要があります")
            continue
        
        # 必須フィールド
        if "name" not in candidate:
            issues.append(f"❌ {district_name} - 候補者[{i}]: 'name' フィールドがありません")
        elif not candidate["name"]:
            issues.append(f"⚠️  {district_name} - 候補者[{i}]: 'name' が空です")
        
        if "party" not in candidate:
            issues.append(f"❌ {district_name} - 候補者[{i}]: 'party' フィールドがありません")
        
        # オプションフィールド
        if "note" in candidate and not isinstance(candidate["note"], str):
            issues.append(f"❌ {district_name} - 候補者[{i}]: 'note' は文字列である必要があります")
    
    return issues


def get_statistics(data: Dict) -> Dict[str, Any]:
    """データの統計情報を取得"""
    stats = {
        "parties_count": 0,
        "professions": set(),
        "general_topics": set(),
        "districts_count": 0,
        "total_candidates": 0,
        "parties_with_explanations": 0
    }
    
    if "parties" in data and isinstance(data["parties"], list):
        stats["parties_count"] = len(data["parties"])
        
        for party in data["parties"]:
            if "personalized_policies" in party and isinstance(party["personalized_policies"], dict):
                stats["professions"].update(party["personalized_policies"].keys())
            
            if "general_policies" in party and isinstance(party["general_policies"], dict):
                stats["general_topics"].update(party["general_policies"].keys())
            
            # 解説の有無をカウント
            if "personalized_explanations" in party or "general_explanations" in party:
                stats["parties_with_explanations"] += 1
    
    if "districts" in data and isinstance(data["districts"], dict):
        stats["districts_count"] = len(data["districts"])
        
        for candidates in data["districts"].values():
            if isinstance(candidates, list):
                stats["total_candidates"] += len(candidates)
    
    return stats


def print_report(file_path: Path, data: Dict, issues: List[str], stats: Dict):
    """検証レポートを出力"""
    print("=" * 70)
    print(f"📊 election_data.json 検証レポート")
    print("=" * 70)
    print()
    
    # 統計情報
    print("📈 統計情報:")
    print(f"  政党数: {stats['parties_count']}")
    print(f"  💡 詳しい解説がある政党: {stats['parties_with_explanations']}/{stats['parties_count']}")
    print(f"  職種カテゴリ: {len(stats['professions'])}")
    if stats['professions']:
        print(f"    → {', '.join(sorted(stats['professions']))}")
    print(f"  一般政策トピック: {len(stats['general_topics'])}")
    if stats['general_topics']:
        print(f"    → {', '.join(sorted(stats['general_topics']))}")
    print(f"  選挙区数: {stats['districts_count']}")
    print(f"  総候補者数: {stats['total_candidates']}")
    print()
    
    # 検証結果
    print("🔍 検証結果:")
    
    if not issues:
        print("  ✅ すべての検証項目をパスしました!")
        print()
        if stats['parties_with_explanations'] == 0:
            print("  ℹ️  解説データがありませんが、アプリは動作します。")
            print("  💡 GEMINI_REQUEST.md の指示に従って、Geminiに解説データを生成してもらうと")
            print("     ユーザーにとってより分かりやすいアプリになります。")
        elif stats['parties_with_explanations'] < stats['parties_count']:
            print(f"  ℹ️  一部の政党（{stats['parties_count'] - stats['parties_with_explanations']}政党）に解説がありません。")
            print("     すべての政党に解説を追加すると、より親切なアプリになります。")
        else:
            print("  🎉 すべての政党に詳しい解説が含まれています！")
        print()
        print("  `streamlit run app.py` でアプリを起動してください。")
    else:
        errors = [i for i in issues if i.startswith("❌")]
        warnings = [i for i in issues if i.startswith("⚠️")]
        
        print(f"  エラー: {len(errors)}件")
        print(f"  警告: {len(warnings)}件")
        print()
        
        if errors:
            print("  【エラー】以下の問題を修正してください:")
            for issue in errors:
                print(f"    {issue}")
            print()
        
        if warnings:
            print("  【警告】以下は動作に影響しない可能性がありますが、確認推奨:")
            for issue in warnings:
                print(f"    {issue}")
            print()
        
        if errors:
            print("  ❌ エラーが存在するため、アプリが正常に動作しない可能性があります。")
        else:
            print("  ⚠️  警告のみです。アプリは動作しますが、データを確認してください。")
    
    print()
    print("=" * 70)


def main():
    """メイン処理"""
    # ファイルパスを取得
    script_dir = Path(__file__).parent
    json_file = script_dir / "election_data.json"
    
    if not json_file.exists():
        print(f"❌ ファイルが見つかりません: {json_file}")
        sys.exit(1)
    
    # JSON構文チェック
    is_valid, message = validate_json_syntax(json_file)
    if not is_valid:
        print(message)
        sys.exit(1)
    
    # データ読み込み
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 構造検証
    issues = validate_structure(data)
    
    # 統計情報取得
    stats = get_statistics(data)
    
    # レポート出力
    print_report(json_file, data, issues, stats)
    
    # 終了コード
    if any(issue.startswith("❌") for issue in issues):
        sys.exit(1)  # エラーあり
    else:
        sys.exit(0)  # 正常終了


if __name__ == "__main__":
    main()
