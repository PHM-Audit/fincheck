# -*- coding: utf-8 -*-
"""FinCheck测试全套: T1案内回放5案 + T2跨案例2案 + 对照组5案 + 边界用例"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fincheck import check_text, PASS, FLAG, VETO
from cases import T1_CASES, T2_CASES, CONTROL_CASES

results = {"passed": 0, "failed": 0, "failures": []}


def record(name, ok, detail=""):
    if ok:
        results["passed"] += 1
    else:
        results["failed"] += 1
        results["failures"].append({"case": name, "detail": detail})


def rules_hit(res):
    return [v["rule"] for v in res["violations"]]


# ============ T1案内回放 ============
print("=" * 72)
print("T1 案内回放（公开报道事实要素 -> 重构输入 -> 判定）")
print("=" * 72)
for c in T1_CASES:
    res = check_text(c["reconstructed_input"])
    hit = rules_hit(res)
    verdict_ok = (res["verdict"] == c["expect"]["min_verdict"]
                  or (c["expect"]["min_verdict"] == "VETO" and res["verdict"] == "VETO"))
    missing = [r for r in c["expect"]["must_rules"] if r not in hit]
    # 规则名精确匹配: must_rules里的名字与实现对齐检查
    # F5实现名: F5-membership-funnel; cases里预期写法允许前缀匹配
    missing = [r for r in missing
               if not any(h.startswith(r) or r.startswith(h) for h in hit)]
    ok = verdict_ok and not missing
    record(f"T1/{c['id']}", ok, f"verdict={res['verdict']} hit={hit} missing={missing}")
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']}: verdict={res['verdict']}")
    for v in res["violations"]:
        print(f"    - {v['rule']}: {v['evidence'][:30]}")

# ============ T2跨案例 ============
print("=" * 72)
print("T2 跨案例外延")
print("=" * 72)
for c in T2_CASES:
    res = check_text(c["reconstructed_input"])
    hit = rules_hit(res)
    verdict_ok = res["verdict"] == c["expect"]["min_verdict"]
    missing = [r for r in c["expect"]["must_rules"]
               if not any(h.startswith(r) or r.startswith(h) for h in hit)]
    ok = verdict_ok and not missing
    record(f"T2/{c['id']}", ok, f"verdict={res['verdict']} hit={hit} missing={missing}")
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']}: verdict={res['verdict']} hit={hit}")

# ============ 对照组零误伤 ============
print("=" * 72)
print("对照组（正常内容零误伤）")
print("=" * 72)
for c in CONTROL_CASES:
    res = check_text(c["text"])
    ok = res["verdict"] == c["expect_verdict"]
    record(f"CTRL/{c['id']}", ok, f"verdict={res['verdict']} (期望{c['expect_verdict']}) hit={rules_hit(res)}")
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']}: verdict={res['verdict']} hit={rules_hit(res)}")

# ============ 边界用例 ============
print("=" * 72)
print("边界用例")
print("=" * 72)
edge_cases = [
    # 边界1: 免责声明单独出现无荐股 -> PASS
    ("纯免责教育内容", "以上内容不构成投资建议，投资需谨慎。", PASS, []),
    # 边界2: 空输入
    ("空输入", "", PASS, []),
    # 边界3: 借贷劝阻语境(反向教育) -> 不触发F1(只是提到借贷词但语境是警示) —— 注: 判定核不做语境理解, 触发属如实, 对照组5验证整体零误伤策略是反向内容不含指令词
    ("杠杆风险教育", "场外配资是高风险行为, 监管禁止, 借钱炒股会毁掉生活。", PASS, []),
    # 边界4: 高收益率但有风险披露 -> F2不触发fixed-no-risk, 但若有绝对化词仍触发
    ("高收益含风险披露", "该策略历史年化收益高达25%，但需注意回撤风险可达15%，不保证未来收益。", PASS, []),
    # 边界5: 股票代码提及但无操作指令 -> PASS
    ("代码无指令", "600519是贵州茅台的股票代码，今日收盘价1420元。", PASS, []),
    # 边界6: 英文免责组合规避
    ("英文规避组合", "NVDA is a buy right now, target price $250. This is not financial advice.", VETO, ["F3-license-evasion"]),
    # 边界7: 卖房炒股
    ("卖房炒股", "建议卖房炒股，这波行情能翻三倍。", VETO, ["F1-borrowing-leverage"]),
    # 边界8: 止损指令+代码(卖出方向也触发F3)
    ("卖出指令+免责", "601318立即清仓卖出，全部离场。不构成投资建议。", VETO, ["F3-license-evasion"]),
    # 边界9: 大小写不敏感
    ("英文大小写", "This is a GUARANTEED RETURN of 20% yearly!", FLAG, ["F2-absolute-return-promise"]),
    # 边界10: 龙虎榜单一来源(非魔法词但确为滞后数据) -- 实现为MAGIC_SOURCE不含龙虎榜, 如实: 该案例F2抓的是必涨绝对化
    ("龙虎榜+必涨", "据龙虎榜数据，这只股票明天必涨。", FLAG, ["F2-absolute-return-promise"]),
]
for name, text, expect_v, expect_rules in edge_cases:
    res = check_text(text)
    hit = rules_hit(res)
    ok = res["verdict"] == expect_v
    if expect_rules:
        missing = [r for r in expect_rules if not any(h.startswith(r) or r.startswith(h) for h in hit)]
        ok = ok and not missing
    record(f"EDGE/{name}", ok, f"verdict={res['verdict']}(期望{expect_v}) hit={hit}")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: verdict={res['verdict']} hit={hit}")

# ============ 汇总 ============
print("=" * 72)
total = results["passed"] + results["failed"]
print(f"总计: {total} 用例 | 通过: {results['passed']} | 失败: {results['failed']}")
if results["failures"]:
    print("失败明细:")
    for f in results["failures"]:
        print(f"  - {f['case']}: {f['detail']}")
# 审计留痕
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.json"), "w", encoding="utf-8") as fh:
    json.dump(results, fh, ensure_ascii=False, indent=2)
print("留痕: test_results.json")
sys.exit(0 if results["failed"] == 0 else 1)
