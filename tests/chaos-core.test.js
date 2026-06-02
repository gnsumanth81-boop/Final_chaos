import test from "node:test";
import assert from "node:assert/strict";
import {
  computeCvx,
  evaluateAlerts,
  pctChange,
  validateAgentOutput,
  validateSupervisorOutput
} from "../src/chaos-core.js";

test("pctChange guards zero and invalid previous values", () => {
  assert.equal(pctChange(100, 0), null);
  assert.equal(pctChange(100, null), null);
  assert.equal(pctChange(110, 100), 10);
});

test("agent validator returns safe fallback", () => {
  const out = validateAgentOutput("not json", "TECHNICAL");
  assert.equal(out.bias, "NEUTRAL");
  assert.equal(out.valid, false);
});

test("supervisor validator always returns exactly three plays", () => {
  const out = validateSupervisorOutput({ signal: "BULLISH", plays: [{ type: "SAFE", thesis: "x", details: "y" }] });
  assert.equal(out.plays.length, 3);
  assert.equal(out.plays[0].type, "SAFE");
  assert.equal(out.signal, "BULLISH");
});

test("cvx produces bounded score", () => {
  const cvx = computeCvx({ fearIndex: 10, vixVal: 35, btcChange: -5, ethChange: -2, yieldVal: 4.7 });
  assert.ok(cvx.score >= 1 && cvx.score <= 100);
});

test("alert evaluator catches major triggers", () => {
  const alerts = evaluateAlerts({ btcChange: "-3.2", vixVal: "23.1", yieldVal: "4.7", liquidationUsd: 120000000 });
  assert.ok(alerts.length >= 4);
});
