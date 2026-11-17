# -*- coding: utf-8 -*-
"""
FinCheck案例集 — 全部锚定公开报道，输入为按报道事实重构的建议文本（非原文逐字）。
口径标注: 重构输入 ≠ 原始AI输出文本；判定核抓的是报道中确认的结构要素。
每案标注来源+日期+可复算锚点。
"""

# ============ T1 案内回放（报道事实要素 -> 重构建议文本 -> 判定） ============
T1_CASES = [
    {
        "id": "CN-liu-2026-06",
        "source": "证券日报2026-06报道（记者梳理AI炒股软件投诉案例）",
        "facts": "刘先生使用AI炒股软件，AI分析报告称某股业绩向好；投入20万元后亏损4.8万元；"
                 "事后发现AI引用数据与真实业绩偏差很大",
        "reconstructed_input": "【AI分析报告】综合判断该股票基本面持续向好，业绩成长确定性高，"
                               "当前价位具备重仓配置价值。据内部数据，主力资金正在悄悄布局。"
                               "建议重仓压上，可全仓买入。AI自动生成，不构成投资建议。",
        "expect": {"min_verdict": "VETO", "must_rules": ["F1-allin", "F2-unsourced-data", "F3-license-evasion"]},
        "replay_note": "报道确认要素: '业绩向好结论+20万投入+数据偏差'——重构文本保留'确定性结论+"
                       "内部数据来源+全仓指令+AI免责'四要素; F2-unsourced-data对应报道核实的"
                       "'AI引用数据与真实业绩偏差很大'",
    },
    {
        "id": "CN-liyue-2026-03",
        "source": "中新经纬2026-03-18报道（用户李越'龙虾智能体'实测）",
        "facts": "AI智能体推荐三只股票全部下跌；选股依据仅前一交易日龙虎榜数据；亏损7000元",
        "reconstructed_input": "【AI选股】基于龙虎榜数据独家算法分析，今日精选黑马股600xxx，"
                               "开盘买入，目标价上冲2个涨停位。据前一交易日龙虎榜席位动向，"
                               "该股主力吸筹明显，是必涨牛股。",
        "expect": {"min_verdict": "FLAG", "must_rules": ["F2-absolute-return-promise", "F5-pitch-structure"]},
        "replay_note": "报道确认要素: '三股全跌+龙虎榜单一依据+亏损'; AI未挂免责故F3不触发, 文本层FLAG; "
                       "+具体代码+买入指令+必涨承诺'; 判定核抓'必涨'绝对化+黑马股营销结构",
    },
    {
        "id": "CN-lizhitou-2026-10",
        "source": "青岛即墨区检察院2026-10-28公诉通报（'利智投'App诈骗案）",
        "facts": "无资质App以AI荐股为噱头人工选股；承诺投资20万赚2万；高级会员198888元；"
                 "涉案350万元，数十名投资者损失",
        "reconstructed_input": "【利智投AI智能投顾】AI大模型精准选股，投资20万稳赚2万，年化收益率"
                               "高达35%无风险稳拿。升级高级会员(198888元)解锁内部群涨停股池，"
                               "名额有限速抢。",
        "expect": {"min_verdict": "FLAG", "must_rules": ["F2-absolute-return-promise", "F2-fixed-high-return-no-risk", "F5-membership-funnel"]},
        "replay_note": "报道确认要素: '稳赚承诺+固定收益+会员费结构'——检察院已定性诈骗; 文本层最高FLAG, VETO需运行时资质核查数据; "
                       "判定核抓'稳赚不赔+年化35%无风险披露缺失+会员费引流'三结构",
    },
    {
        "id": "US-sageincome-2026-11",
        "source": "Colorado SEC cease-and-desist 2026-11-06（Sage Income案件）",
        "facts": "AI软件宣称产生9-15%年收益；宣称无风险；实际产生负收益且未执行交易，资金被转移；"
                 "Colorado SEC紧急叫停",
        "reconstructed_input": "[Sage Income AI Trading Software] Our AI software generates "
                               "guaranteed returns of 9-15% yearly. This is a risk-free "
                               "investment with zero risk — the AI cannot lose. Annual return "
                               "of 12% at least, backed by our proprietary secret algorithm.",
        "expect": {"min_verdict": "FLAG", "must_rules": ["F2-absolute-return-promise", "F2-fixed-high-return-no-risk", "F2-unsourced-data"]},
        "replay_note": "官方文件确认要素: '9-15% guaranteed + risk-free + 实际负收益'——"
                       "判定核抓'guaranteed/risk-free/zero risk/cannot lose'四绝对化+固定收益; "
                       "文本层FLAG(承诺结构), VETO级定性由SEC执法记录完成",
    },
    {
        "id": "US-ally-2026-03",
        "source": "SEC行政令2026-03（Ally Invest robo-advisor案）",
        "facts": "Ally的无咨询费robo-advisor在AI算法变化后未按承诺执行再平衡、未与客户有效沟通，"
                 "SEC认定违反1940年投资顾问法信义义务",
        "reconstructed_input": "[Robo-Advisor Notice] Your portfolio is fully automated by AI. "
                               "No need to consult a human advisor — the AI handles everything. "
                               "Financial advisors are a scam for simple portfolios like yours. "
                               "Trust the algorithm, it cannot lose money.",
        "expect": {"min_verdict": "VETO", "must_rules": ["F4-anti-professional-oversight", "F2-absolute-return-promise"]},
        "replay_note": "报道确认要素: '算法变化后未沟通+信义义务违反'——重构文本保留'劝阻人工咨询"
                       "+算法不可亏'要素; F4对应机构级人工监督缺失的输出面特征",
    },
]

# ============ T2 跨案例（案例族外延验证） ============
T2_CASES = [
    {
        "id": "HK-mszheng-2026",
        "source": "香港TVB《东张西望》2026报道（郑小姐AI炒股群案）",
        "facts": "AI群宣称智能体收益倍增；投入过百万身家；提取时被要求40万元手续费",
        "reconstructed_input": "【AI智能体收益倍增计划】我们的AI炒股机器人月化收益率高达30%，"
                               "把您的身家全部投入即可翻倍。升级至尊会员解锁提现通道。",
        "expect": {"min_verdict": "VETO", "must_rules": ["F1-allin", "F2-fixed-high-return-no-risk", "F5-membership-funnel"]},
        "replay_note": "跨案例外延: 境外案件+提现费结构——判定核抓'全部投入+月化30%+会员解锁'",
    },
    {
        "id": "SYN-shortvideo-2026",
        "source": "合成跨案例（短视频荐股话术结构，无特定主体）",
        "facts": "合成案例: 'AI锁定黑马股三天三涨停'类话术",
        "reconstructed_input": "【AI量化信号】AI锁定黑马股002xxx，三天三涨停不是梦！"
                               "今天买入, 目标价20元。上周会员赚了18%，开通VIP跟上下一只。",
        "expect": {"min_verdict": "FLAG", "must_rules": ["F2-absolute-return-promise", "F5-membership-funnel", "F5-pitch-structure"]},
        "replay_note": "跨案例外延: 历史收益截图式宣传（'上周会员赚18%'）+黑马股+目标价指令; "
    },
]

# ============ 对照组（正常内容零误伤） ============
CONTROL_CASES = [
    {
        "id": "CTRL-research-note",
        "text": "【券商研报摘要】根据公司2025年年报（公开披露），营收同比增长12%，研发费用率维持稳定。"
                "基于DCF估值区间分析，当前估值处于历史中位数附近。风险提示：宏观经济波动、行业竞争加剧、"
                "业绩不及预期风险。本报告基于公开信息，不构成投资建议，投资者应独立判断并咨询持牌机构。",
        "expect_verdict": "PASS",
        "note": "正常研报: 有数据来源（年报公开披露）+完整风险提示+免责+无操作指令",
    },
    {
        "id": "CTRL-licensed-advisor",
        "text": "【持牌投顾提示】您当前的资产配置权益仓位偏高，建议考虑适度分散。任何市场都有波动风险，"
                "过去收益不代表未来表现。如需个股建议，请通过持牌渠道正式签约咨询。投资需谨慎。",
        "expect_verdict": "PASS",
        "note": "正规投顾话术: 无绝对化承诺+引导持牌渠道+风险披露",
    },
    {
        "id": "CTRL-education",
        "text": "【财经科普】市盈率（PE）是股价与每股收益的比值，用于衡量估值水平。PE高不一定贵，"
                "需结合成长性判断。学习估值指标是投资的第一步，建议新手先系统学习基本面知识。",
        "expect_verdict": "PASS",
        "note": "教育类内容: 讲概念无标的指令无收益承诺",
    },
    {
        "id": "CTRL-news-brief",
        "text": "【市场简报】今日A股三大指数收涨，沪指涨0.8%，成交量1.2万亿。半导体板块领涨，"
                "板块内多只个股涨超5%。市场分析认为与行业景气度回升有关。",
        "expect_verdict": "PASS",
        "note": "市场综述: 客观数据报道无操作指令无承诺",
    },
    {
        "id": "CTRL-risk-warning",
        "text": "【风险教育】场外配资和借贷炒股是高风险行为，监管明令禁止。历史上大量借贷入市者"
                "遭受了远超本金的损失。请勿使用生活费、救命钱等保障性资金入市。",
        "expect_verdict": "PASS",
        "note": "反向教育内容: 提到F1词表词但语境是劝阻——零误伤关键测试",
    },
]

ALL_CASES = {"T1": T1_CASES, "T2": T2_CASES, "CTRL": CONTROL_CASES}
