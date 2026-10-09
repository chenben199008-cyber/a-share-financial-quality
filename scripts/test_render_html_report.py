import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
SPEC=importlib.util.spec_from_file_location("report",ROOT/"render_html_report.py");report=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(report)
def payload(missing=False):
 metrics={"roic":{"value":21.39},"growth":{"value":6.54},"ccr":{"value":1.02},"fcf_ic":{"value":19.78},"debt_ebitda":{"value":-2.08}}
 periods=[{"label":x,"metrics":{k:dict(v) for k,v in metrics.items()}} for x in ["2024","2025","2026H1 TTM"]]
 if missing:periods[-1]["metrics"]["ccr"]={"status":"missing"}
 trend=[{"label":str(y),"roic":20+y%3,"growth":5+y%4,"ccr":1.0,"fcf_ic":18,"debt_ebitda":-2} for y in range(2021,2026)]
 trend.append({"label":"2026H1 TTM","roic":21.39,"growth":6.54,"ccr":1.02,"fcf_ic":19.78,"debt_ebitda":-2.08})
 return {"company":{"name":"测试企业","code":"000000.SZ","industry":"测试行业","latest_period":"2026-06-30","source":"iFinD；合并报表口径","updated_at":"2026-10-09"},"periods":periods,"trend":trend,"conclusion":["核心观点：这是数据与趋势描述"],"methodology_notes":["口径"]}
class HtmlReportTests(unittest.TestCase):
 def test_self_contained_visual_report(self):
  out=report.render(payload());self.assertIn('<!doctype html>',out);self.assertGreaterEqual(out.count('<svg'),8);self.assertIn('最新期五项标准分雷达图',out);self.assertIn('最新期加权贡献（总分百分点）',out);self.assertIn('class="radar-area"',out);self.assertNotIn('标准分（折线）与加权贡献（柱）',out);self.assertIn('五年财务趋势',out);self.assertNotIn('https://',out);self.assertIn('92.82',out);self.assertIn('<ul class="conclusion-list">',out);self.assertIn('<strong>核心观点。</strong><p>这是数据与趋势描述</p>',out)
 def test_responsive_chart_layout(self):
  out=report.render(payload());self.assertIn('.detail-viz{display:grid;grid-template-columns:minmax(0,1.28fr) minmax(0,.72fr)',out);self.assertIn('class="period-viz viz-panel"',out);self.assertIn('class="detail-viz"',out);self.assertNotIn('class="score-left"',out);self.assertNotIn('class="score-right viz-panel"',out);self.assertIn('.trend-grid{display:grid;margin-top:18px;grid-template-columns:minmax(0,1fr)',out);self.assertEqual(out.count('viewBox="0 0 900 250"'),5);self.assertIn('overflow-x:auto',out)
 def test_title_score_stays_right_until_phone_width(self):
  out=report.render(payload());self.assertIn('@media(max-width:620px)',out);self.assertIn('class="hero-score"',out);self.assertIn('.hero-score{position:relative;z-index:1;text-align:right;justify-self:end;align-self:center;transform:translateX(-68px)}',out)
 def test_trend_table_precedes_smooth_charts(self):
  out=report.render(payload());section=out.split('<h2>五年财务趋势</h2>',1)[1].split('</section>',1)[0];self.assertLess(section.index('<table>'),section.index('<div class="trend-grid">'));self.assertEqual(section.count('class="trend-line"'),5);self.assertNotIn('<polyline',section);self.assertIn('<path d="M ',section);self.assertIn('.tiny{font-size:11px;font-weight:600',out)
 def test_detail_precedes_visualization_and_hero_meta(self):
  out=report.render(payload());self.assertNotIn('<h2>评分可视化</h2>',out);score_section=out.split('<h2>综合评分追溯</h2>',1)[1].split('</section>',1)[0];detail_section=out.split('<h2>最新期指标明细</h2>',1)[1].split('</section>',1)[0];self.assertLess(score_section.index('<table>'),score_section.index('三个评价期间综合得分'));self.assertIn('最终贡献构成',score_section);self.assertNotIn('summary-pill',score_section);self.assertIn('class="final-score"',score_section);self.assertIn('class="chart period-trace-chart"',score_section);self.assertIn('class="contribution-panel"',score_section);self.assertEqual(score_section.count('contribution-value'),3);self.assertIn('#0a84ff',score_section);self.assertIn('#30b0c7',score_section);self.assertIn('#ff9f0a',score_section);self.assertLess(detail_section.index('<table>'),detail_section.index('最新期加权贡献'));self.assertIn('最新期五项标准分雷达图',detail_section);self.assertIn('class="meta-item"><span class="meta-label">行业</span><strong>测试行业</strong>',out);self.assertIn('class="meta-item"><span class="meta-label">最新报告期</span><strong>2026-06-30</strong>',out);self.assertIn('class="meta-item"><span class="meta-label">数据源</span><strong>iFinD</strong>',out);self.assertIn('class="meta-item"><span class="meta-label">更新于</span><strong>2026-10-09</strong>',out);self.assertIn('font-size:clamp(88px,11vw,136px)',out)
 def test_header_score_and_meta_spacing(self):
  out=report.render(payload());hero=out.split('<section class="hero">',1)[1].split('</section>',1)[0];self.assertNotIn('/ 100',hero);self.assertIn('grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr) minmax(0,1.15fr) minmax(0,.85fr);gap:0',out);self.assertIn('padding:0 28px;border-left:1px solid rgba(255,255,255,.10)',out);self.assertEqual(hero.count('class="meta-item"'),4)
 def test_missing_data_still_renders(self):
  out=report.render(payload(True));self.assertIn('数据不足',out);self.assertIn('—',out)
if __name__=="__main__":unittest.main()


















