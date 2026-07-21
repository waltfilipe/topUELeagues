#!/usr/bin/env python3
"""Build cached parquet artifacts for European leagues season passes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import passes_engine as pe
import xp_engine as xe


def main() -> None:
    print("Building europe_season_passes.parquet from CSV sources...")
    if pe.EUROPE_SEASON_PARQUET.exists():
        pe.EUROPE_SEASON_PARQUET.unlink()
    pe._load_season_pass_frame.cache_clear()
    frame = pe._load_season_pass_frame()
    print(f"  rows: {len(frame):,}")
    print(f"  players: {frame['player_id'].nunique():,}")

    print(f"Building xP season artifacts ({xe.XP_MODEL_VERSION})...")
    if xe.XP_PASSES_PARQUET.exists():
        xe.XP_PASSES_PARQUET.unlink()
    season = xe.build_serie_b_season_passes(force_artifacts=False)
    print(f"  xp rows: {len(season):,}")
    print(f"  threat passes: {int(season[xe.THREAT_COL].sum()):,}")

    _, players = xe.build_xp_analytics()
    print(f"  players with xP metrics: {len(players)}")
    print(f"  cached metrics parquet: {xe.XP_PLAYER_METRICS_PARQUET}")
    if players:
        top = players[0]
        print(f"  top xP: {top['player_name']} ({top['xp_m4_total']:.1f})")


if __name__ == "__main__":
    main()
