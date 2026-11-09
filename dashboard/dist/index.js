(function () {
  "use strict";

  const SDK = window.__HERMES_PLUGIN_SDK__;
  if (!SDK || !window.__HERMES_PLUGINS__) return;

  const { React } = SDK;
  const { useState, useEffect, useCallback } = SDK.hooks;
  const { Card, CardHeader, CardTitle, CardContent, Badge, Button } = SDK.components;

  function HacmdnDashboardPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [ideaTitle, setIdeaTitle] = useState("");

    const refresh = useCallback(() => {
      setLoading(true);
      SDK.fetchJSON("/api/plugins/hacmdn/hub")
        .then((res) => {
          setData(res);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }, []);

    useEffect(() => {
      refresh();
    }, [refresh]);

    const runAction = (payload) => {
      SDK.fetchJSON("/api/plugins/hacmdn/action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then((res) => {
        if (res && res.hub) {
          setData((prev) => ({ ...(prev || {}), hub: res.hub }));
        } else {
          refresh();
        }
      });
    };

    if (loading && !data) {
      return React.createElement("div", { className: "p-6 text-sm text-muted-foreground" }, "Loading HACMDN-Net Contributor Hub...");
    }

    const hub = (data && data.hub) || {};
    const earn = hub.earnings_summary || {};
    const policy = hub.anti_whale_policy || {};
    const wh = hub.worker_and_hardware || {};
    const hw = wh.hardware_profile || {};
    const ideas = hub.ideas_pitched || [];
    const bounties = hub.open_bounties || [];

    return React.createElement(
      "div",
      { className: "space-y-4 p-4" },
      React.createElement(
        Card,
        null,
        React.createElement(
          CardHeader,
          null,
          React.createElement(
            CardTitle,
            null,
            "🕸️ HACMDN-Net Contributor & Node Operator Hub (v0.3.0)"
          )
        ),
        React.createElement(
          CardContent,
          { className: "space-y-3 text-sm" },
          React.createElement(
            "div",
            { className: "flex flex-wrap gap-4" },
            React.createElement(Badge, null, "Total Earned: +" + (earn.total_accumulated_credits || 0) + " cr"),
            React.createElement(Badge, null, "Worker (70%): " + (earn.worker_inference_credits_capped || 0) + " / " + (policy.daily_personal_cap_credits || 50) + " cr cap"),
            React.createElement(Badge, null, "Author Royalties (10%): +" + (earn.adapter_author_royalty_credits || 0) + " cr"),
            React.createElement(Badge, null, "Community Dividend: +" + (earn.community_dividend_pool_credits || 0) + " cr"),
            React.createElement(Badge, null, "Tasks: " + (earn.tasks_completed || 0) + " (" + (earn.tokens_contributed || 0) + " tok)")
          ),
          React.createElement(
            "p",
            { className: "text-xs text-muted-foreground" },
            "Game-Guard Status: " + (hw.game_guard_status || "Active") + " · " + (policy.overflow_policy || "")
          ),
          React.createElement(
            "div",
            { className: "flex flex-wrap gap-2 pt-2" },
            React.createElement(
              Button,
              {
                onClick: () =>
                  runAction({
                    kind: "hub",
                    action: "simulate_datacenter_overflow",
                    raw_datacenter_credits: 120.0,
                  }),
              },
              "Simulate Datacenter Overflow (+120 cr)"
            ),
            React.createElement(
              Button,
              {
                onClick: () =>
                  runAction({
                    kind: "flywheel",
                    action: "run_idle_pool_task",
                    idle_pool_category: "open-science",
                  }),
              },
              "Run Idle Open-Science Task"
            ),
            React.createElement(
              Button,
              {
                onClick: () =>
                  runAction({
                    kind: "worker_pool",
                    action: "auto_load_needed_specialist",
                  }),
              },
              "Auto-Load Needed Specialist"
            )
          )
        )
      ),
      React.createElement(
        Card,
        null,
        React.createElement(CardHeader, null, React.createElement(CardTitle, null, "💡 Pitched Community Directives & Open Bounties")),
        React.createElement(
          CardContent,
          { className: "space-y-2 text-xs" },
          ideas.map((item) =>
            React.createElement(
              "div",
              { key: item.idea_id, className: "flex justify-between border-b py-1" },
              React.createElement("span", null, item.title + " (" + item.category + ")"),
              React.createElement("span", null, item.vote_weight + " vote wt · " + item.status)
            )
          ),
          bounties.map((b) =>
            React.createElement(
              "div",
              { key: b.bounty_id, className: "flex justify-between border-b py-1 text-muted-foreground" },
              React.createElement("span", null, "Bounty: " + b.gap_domain + " (" + b.suggested_base + ")"),
              React.createElement("span", null, "+" + b.reward_credits + " cr · " + b.status)
            )
          )
        )
      )
    );
  }

  window.__HERMES_PLUGINS__.register("hacmdn", HacmdnDashboardPage);
})();
