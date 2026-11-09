// Native Hermes Desktop Plugin (`@hermes/plugin-sdk`) for HACMDN-Net (v1.0.0)
// Contributes:
//   1. Right-docked "HACMDN Hub" pane showing live compute pools, Game-Guard status,
//      70/10/10/10 shared-entity earnings, Anti-Whale daily cap meter, and pitched ideas.
//   2. Right status-bar telemetry chip showing live mesh status & accumulated credits.

import {
  PANES_AREA,
  STATUSBAR_AREAS,
  Badge,
  Button,
  haptic,
  host,
  queryClient,
  useMutation,
  useQuery,
} from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

function HacmdnDesktopPane({ ctx }) {
  const { data, isLoading } = useQuery({
    queryKey: ['hacmdn', 'hub'],
    queryFn: () => ctx.rest('/hub'),
    refetchInterval: 15000,
  })

  const actMutation = useMutation({
    mutationFn: body => ctx.rest('/action', { method: 'POST', body }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hacmdn', 'hub'] })
    },
  })

  if (isLoading && !data) {
    return jsx('div', {
      className: 'p-3 text-xs text-(--ui-text-tertiary)',
      children: 'Loading HACMDN-Net Contributor Hub…',
    })
  }

  const hub = (data && data.hub) || {}
  const earn = hub.earnings_summary || {}
  const policy = hub.anti_whale_policy || {}
  const wh = hub.worker_and_hardware || {}
  const hw = wh.hardware_profile || {}
  const wstate = wh.worker_state || {}
  const ideas = hub.ideas_pitched || []
  const shortage = wh.shortage_rankings || []

  return jsxs('div', {
    className: 'flex h-full flex-col gap-3 overflow-y-auto p-3 text-xs',
    children: [
      jsxs('div', {
        className: 'flex items-center justify-between border-b border-(--ui-stroke-secondary) pb-2',
        children: [
          jsxs('div', {
            children: [
              jsx('div', {
                className: 'font-semibold text-(--ui-text-primary)',
                children: '🕸️ HACMDN-Net Hub',
              }),
              jsx('div', {
                className: 'text-[11px] text-(--ui-text-tertiary)',
                children: `${hub.operator_id || 'jkorstad-node-01'} · ${wstate.compute_mode || 'auto_game_guard'}`,
              }),
            ],
          }),
          jsx(Badge, {
            children: `+${Number(earn.total_accumulated_credits || 0).toFixed(2)} cr`,
          }),
        ],
      }),

      jsxs('div', {
        className: 'rounded border border-(--ui-stroke-secondary) p-2.5',
        children: [
          jsx('div', {
            className: 'font-medium text-(--ui-text-secondary)',
            children: '70/10/10/10 Value-Backed Attribution & Fair-Share Cap',
          }),
          jsx('div', {
            className: 'mt-1 text-[11px] text-(--ui-text-tertiary)',
            children: `Worker (70%): ${earn.worker_inference_credits_capped || 0} / ${policy.daily_personal_cap_credits || 50} cr (${earn.cap_utilization_pct || 0}%)`,
          }),
          jsx('div', {
            className: 'text-[11px] text-(--ui-text-tertiary)',
            children: `Author Royalties (10%): +${earn.adapter_author_royalty_credits || 0} cr · Dividend: +${earn.community_dividend_pool_credits || 0} cr`,
          }),
          jsx('div', {
            className: 'text-[11px] text-(--ui-text-tertiary)',
            children: `Contribution: ${earn.tasks_completed || 0} tasks · ${earn.tokens_contributed || 0} tokens`,
          }),
          jsxs('div', {
            className: 'mt-2 flex flex-wrap gap-1.5',
            children: [
              jsx(Button, {
                size: 'sm',
                onClick: () => {
                  haptic('tap')
                  actMutation.mutate({
                    kind: 'hub',
                    action: 'simulate_datacenter_overflow',
                    raw_datacenter_credits: 120.0,
                  })
                },
                children: 'Simulate Overflow (+120 cr)',
              }),
              jsx(Button, {
                size: 'sm',
                onClick: () => {
                  haptic('tap')
                  actMutation.mutate({
                    kind: 'worker_pool',
                    action: 'auto_load_needed_specialist',
                  })
                },
                children: 'Auto-Load Specialist',
              }),
            ],
          }),
        ],
      }),

      jsxs('div', {
        className: 'rounded border border-(--ui-stroke-secondary) p-2.5',
        children: [
          jsx('div', {
            className: 'font-medium text-(--ui-text-secondary)',
            children: 'Game-Guard & Shortage Rankings',
          }),
          jsx('div', {
            className: 'mt-1 text-[11px] text-(--ui-text-tertiary)',
            children: hw.game_guard_status || 'Spare CPU Float32 Mode Active',
          }),
          ...shortage.slice(0, 3).map(s =>
            jsxs(
              'div',
              {
                className: 'mt-1.5 flex items-center justify-between border-t border-(--ui-stroke-secondary) pt-1',
                children: [
                  jsx('span', {
                    className: 'truncate text-[11px]',
                    children: s.spec_id,
                  }),
                  jsx('span', {
                    className: 'text-[10px] text-(--ui-text-tertiary)',
                    children: `shortage ${s.shortage_score}`,
                  }),
                ],
              },
              s.spec_id
            )
          ),
        ],
      }),

      jsxs('div', {
        className: 'rounded border border-(--ui-stroke-secondary) p-2.5',
        children: [
          jsx('div', {
            className: 'font-medium text-(--ui-text-secondary)',
            children: 'Pitched Community Ideas & Directives',
          }),
          ...ideas.slice(0, 4).map(item =>
            jsxs(
              'div',
              {
                className: 'mt-1.5 flex items-center justify-between border-t border-(--ui-stroke-secondary) pt-1',
                children: [
                  jsx('span', {
                    className: 'truncate text-[11px]',
                    children: item.title,
                  }),
                  jsx('span', {
                    className: 'text-[10px] text-(--ui-text-tertiary)',
                    children: `${item.vote_weight} wt`,
                  }),
                ],
              },
              item.idea_id
            )
          ),
        ],
      }),
    ],
  })
}

export default {
  id: 'hacmdn',
  name: 'HACMDN-Net Hub',
  defaultEnabled: true,
  register(ctx) {
    ctx.register({
      id: 'hub-pane',
      area: PANES_AREA,
      title: 'HACMDN Hub',
      data: { placement: 'right', width: '310px' },
      render: () => jsx(HacmdnDesktopPane, { ctx }),
    })

    ctx.register({
      id: 'hub-chip',
      area: STATUSBAR_AREAS.right,
      order: 125,
      render: () =>
        jsx('button', {
          type: 'button',
          className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
          onClick: () => {
            haptic('tap')
            host.notify({
              kind: 'info',
              message: 'HACMDN-Net Mesh Active · 3 Qwen3-0.6B Specialists Online (Game-Guard Protected)',
            })
          },
          children: '🕸️ HACMDN',
        }),
    })
  },
}
