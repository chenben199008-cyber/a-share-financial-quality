# A股企业财务质量评估 Skill

基于固定的 V4.0 规则，对A股非金融类上市企业进行可追溯的财务质量评估，并生成包含表格、柱状图、雷达图和五年趋势图的单文件 HTML 报告。

## 核心指标

- ROIC
- 扣非归母净利润增长率
- 现金利润比
- FCF资本回报率
- 净负债/EBITDA

## 目录

- `SKILL.md`：Skill入口与工作流
- `references/model-v4.md`：评分公式、锚点、权重和异常处理
- `references/html-report.md`：HTML报告结构与视觉规范
- `scripts/score_financial_quality.py`：确定性评分器
- `scripts/render_html_report.py`：离线单文件HTML生成器
- `scripts/test_*.py`：回归测试

## 使用

本Skill依赖同花顺 iFinD 数据能力获取实际披露数据。准备符合 `references/html-report.md` 约定的JSON后，可运行：

```bash
python scripts/score_financial_quality.py --input report.json
python scripts/render_html_report.py --input report.json --output report.html
```

运行测试：

```bash
python -m unittest discover -s scripts -p "test_*.py"
```

本模型仅用于企业财务质量评价，不等同于股票投资价值判断或买卖建议。
