import importlib.util,unittest
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("scorer",Path(__file__).with_name("score_financial_quality.py"));scorer=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(scorer)
class ScorerTests(unittest.TestCase):
 def test_anchor_and_interpolation(self):
  self.assertEqual(scorer.interpolate(18,*scorer.ANCHORS["roic"]),90);self.assertEqual(scorer.interpolate(0,*scorer.ANCHORS["debt_ebitda"]),100);self.assertEqual(scorer.interpolate(7,*scorer.ANCHORS["debt_ebitda"]),0)
 def test_complete_score(self):
  values={"roic":18,"growth":12.5,"ccr":1.1,"fcf_ic":8,"debt_ebitda":1.5};metrics={k:{"value":v} for k,v in values.items()};result=scorer.score({"periods":[{"label":str(i),"metrics":metrics} for i in range(3)]});self.assertEqual(result["final_score"],83.0);self.assertEqual(result["result"]["grade"],"B")
 def test_missing_blocks_final_score(self):
  metrics={k:{"value":1} for k in scorer.METRIC_WEIGHTS};periods=[{"label":str(i),"metrics":dict(metrics)} for i in range(3)];periods[2]["metrics"]["ccr"]={"status":"missing"};result=scorer.score({"periods":periods});self.assertIsNone(result["final_score"]);self.assertEqual(result["status"],"数据不足")
 def test_turnaround_override(self):self.assertEqual(scorer.metric_score("growth",{"status":"turnaround","score_override":60})["score"],60)
if __name__=="__main__":unittest.main()

