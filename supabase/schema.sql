-- Chaos Intelligence 14x signal ledger.
-- Run this in Supabase SQL editor or via migrations.

create extension if not exists pgcrypto;

create table if not exists public.chaos_runs (
  id uuid primary key default gen_random_uuid(),
  run_at timestamptz not null default now(),
  session_label text,
  status text not null default 'SUCCESS',
  partial_data boolean not null default false,
  source_summary jsonb not null default '{}'::jsonb,
  error_message text
);

create table if not exists public.chaos_signals (
  id text primary key,
  run_id uuid references public.chaos_runs(id) on delete set null,
  issued_at timestamptz not null,
  session_label text not null,
  headline text not null,
  signal text not null check (signal in ('BULLISH','BEARISH','NEUTRAL','VOLATILE')),
  confidence numeric not null check (confidence >= 0 and confidence <= 100),
  active_regime text not null,
  forces text[] not null default '{}',
  signal_hash text not null,
  btc_entry numeric,
  spx_entry numeric,
  vix_entry numeric,
  payload jsonb not null,
  resolved boolean not null default false,
  resolved_at timestamptz,
  result text check (result in ('WIN','LOSS','FLAT','VOID')),
  pnl_percent numeric,
  created_at timestamptz not null default now()
);

create table if not exists public.chaos_plays (
  id uuid primary key default gen_random_uuid(),
  signal_id text not null references public.chaos_signals(id) on delete cascade,
  play_type text not null check (play_type in ('SAFE','AGGRESSIVE','CONTRARIAN')),
  thesis text not null,
  details text not null,
  asset text,
  direction text check (direction in ('LONG','SHORT','HEDGE','WAIT','MIXED')),
  entry_level numeric,
  target_level numeric,
  stop_level numeric,
  timeframe text,
  created_at timestamptz not null default now()
);

create table if not exists public.agent_outputs (
  id uuid primary key default gen_random_uuid(),
  signal_id text references public.chaos_signals(id) on delete cascade,
  agent text not null,
  bias text not null,
  confidence numeric not null,
  thesis text not null,
  raw_output jsonb not null default '{}'::jsonb,
  valid boolean not null default true,
  created_at timestamptz not null default now()
);

create index if not exists chaos_signals_issued_at_idx on public.chaos_signals (issued_at desc);
create index if not exists chaos_signals_result_idx on public.chaos_signals (result);
create index if not exists chaos_plays_signal_idx on public.chaos_plays (signal_id);

create or replace view public.chaos_performance_summary as
select
  count(*) filter (where resolved) as resolved_signals,
  count(*) filter (where result = 'WIN') as wins,
  count(*) filter (where result = 'LOSS') as losses,
  round(
    100.0 * count(*) filter (where result = 'WIN') / nullif(count(*) filter (where resolved and result in ('WIN','LOSS')), 0),
    2
  ) as win_rate,
  round(avg(pnl_percent) filter (where resolved), 2) as avg_pnl_percent,
  round(max(pnl_percent) filter (where resolved), 2) as best_pnl_percent,
  round(min(pnl_percent) filter (where resolved), 2) as worst_pnl_percent
from public.chaos_signals;

-- Optional public read policy.
-- Enable RLS only after you decide what should be public.
-- alter table public.chaos_signals enable row level security;
-- create policy "public read resolved signals" on public.chaos_signals for select using (true);
