# Caesar API Documentation

This directory contains comprehensive documentation for Caesar Research AI API, including V2 exploration, testing, and migration guidance.

## Quick Start

1. **New to Caesar?** Start with [v2-introduction.md](v2-introduction.md)
2. **Migrating from V1?** Read [v1-vs-v2-comparison.md](v1-vs-v2-comparison.md)
3. **Optimizing quality?** See [COMPARISON-SUMMARY.md](COMPARISON-SUMMARY.md) for reasoning loops analysis
4. **Ready to implement?** See [PM-REPORT.md](PM-REPORT.md) for recommendations

## Documentation Index

### Overview & Introduction
- **[v2-introduction.md](v2-introduction.md)** - Caesar V2 capabilities, methodology, and advantages
- **[v2-versioning.md](v2-versioning.md)** - Version control, backward compatibility, and migration changes

### API Reference
- **[v2-create-research.md](v2-create-research.md)** - Create research object endpoint
  - Parameters, request format, response structure
- **[v2-get-research.md](v2-get-research.md)** - Get research object endpoint
  - Polling strategy, status states, response fields

### Analysis & Comparison
- **[v1-vs-v2-comparison.md](v1-vs-v2-comparison.md)** - Comprehensive V1/V2 comparison
  - Parameter differences, status states, response structure
  - Migration path, code examples, recommendations
- **[v2-test-summary.md](v2-test-summary.md)** - Test results and analysis
  - Performance metrics, content quality assessment
  - Source distribution, recommendations
- **[auto-mode-analysis.md](auto-mode-analysis.md)** - How auto and reasoning_loops actually work ⭐⭐ NEW
  - Critical findings on loop enforcement
  - auto=false vs auto=true comparison
  - Parameter behavior deep-dive
  - Revised mental model
- **[COMPARISON-SUMMARY.md](COMPARISON-SUMMARY.md)** - Quick comparison guide (3 configs tested) ⭐ UPDATED
  - auto=true loops=1 vs loops=2 vs auto=false loops=1
  - Why all consumed 2 loops
  - Configuration recommendations
- **[reasoning-loops-comparison.md](reasoning-loops-comparison.md)** - Initial loops comparison analysis
  - Loops=1 vs Loops=2 detailed comparison
  - Source quality analysis, ROI calculations
  - Use case recommendations

### Planning & Strategy
- **[PM-REPORT.md](PM-REPORT.md)** - Technical PM report
  - Executive summary, integration recommendations
  - Migration strategy, risk assessment, next steps

## Test Resources

### Test Scripts
- **Basic Test:** `../../mesh/test_scripts/test_caesar_v2_research.py`
  - End-to-end V2 API testing
  - Usage: `uv run python mesh/test_scripts/test_caesar_v2_research.py`
- **Comparison Test:** `../../mesh/test_scripts/test_caesar_v2_comparison.py`
  - Compare reasoning_loops=1 vs reasoning_loops=2 (both auto=true)
  - Usage: `uv run python mesh/test_scripts/test_caesar_v2_comparison.py`
- **Auto False Test:** `../../mesh/test_scripts/test_caesar_v2_auto_false.py` ⭐ NEW
  - Test auto=false with reasoning_loops=1
  - Usage: `uv run python mesh/test_scripts/test_caesar_v2_auto_false.py`

### Test Results
- **Location:** `../../mesh/test_scripts/caesar_v2_*.json`
- **Contents:** Raw API responses from test runs
- **Comparison Data:** `../../mesh/test_scripts/caesar_v2_comparison_*.json`

## Key Information

### Current API Version
- **Latest:** `2025-11-27`
- **Base URL:** `https://api.caesar.xyz`

### Authentication
```bash
Authorization: Bearer $CAESAR_API_KEY
API-Version: 2025-11-27
```

### V1 vs V2 Quick Reference

| Feature | V1 | V2 |
|---------|----|----|
| **Version Header** | Not required | `API-Version: 2025-11-27` |
| **Main Parameter** | `compute_units` | `reasoning_loops` |
| **Status States** | 4 | 7 |
| **Performance Metrics** | No | Yes |
| **Source Attribution** | Basic | Citation indices |
| **File Upload** | No | Yes |
| **Brainstorming** | No | Yes |

## Implementation Checklist

### Phase 1: Basic Migration
- [ ] Add `API-Version: 2025-11-27` header
- [ ] Rename `compute_units` to `reasoning_loops`
- [ ] Update status handling (4 → 7 states)
- [ ] Parse new metrics (`reasoning_loops_consumed`, `running_time`)
- [ ] Utilize `citation_index` in sources

### Phase 2: V2 Features
- [ ] Add `exclude_social` parameter
- [ ] Add `auto` mode parameter
- [ ] Implement source filtering (`excluded_domains`)
- [ ] Add custom `system_prompt` support
- [ ] Add model selection

### Phase 3: Advanced Features
- [ ] Implement brainstorming workflow
- [ ] Add file upload support
- [ ] Create collections management
- [ ] Implement research chat
- [ ] Add event streaming

## Test Results Summary

### Test 1: End-to-End Research
**Query:** "Trump EU tariff impact on crypto"
**Config:** `reasoning_loops=2, auto=true`

**Results:**
- ✅ Processing Time: 148 seconds
- ✅ Reasoning Loops: 2/2
- ✅ Sources: 44 authoritative citations
- ✅ Quality: Comprehensive analysis with quantitative data
- ✅ Status: Completed successfully

### Test 2: Reasoning Loops Comparison ⭐ UPDATED
**Query:** "compare ethereum staking with solana staking yields"
**Configs Tested:** 3 configurations
- `auto=true, reasoning_loops=1`
- `auto=true, reasoning_loops=2`
- `auto=false, reasoning_loops=1` ⚠️ NEW

**Critical Findings:**
- 🔍 **All three consumed 2 loops** - even `auto=false` didn't force 1 loop!
- 🎯 **Query complexity determines minimum loops**, not settings
- ⚡ **auto=true is 21.9% faster** than auto=false (114s vs 139s)
- ✅ **auto=true loops=2**: Best quality (36 sources, 36 citations)
- ❌ **auto=false has no benefits** - slower, doesn't enforce loop count

**Key Discovery:** `reasoning_loops` is a quality signal, not a hard limit. `auto` optimizes execution but doesn't control loop count. Caesar enforces minimums based on query complexity.

See [auto-mode-analysis.md](auto-mode-analysis.md) and [COMPARISON-SUMMARY.md](COMPARISON-SUMMARY.md) for full analysis.

## Recommended Configuration

### ⭐ Default Configuration (Recommended)
Based on extensive testing (3 configurations), this provides optimal results:
```json
{
  "query": "Your research question",
  "reasoning_loops": 2,
  "auto": true,
  "exclude_social": false
}
```
**Why:**
- Best quality: 36 sources, 36 citations, 28 domains
- Fast execution: Only +9.6% vs fastest config
- Auto mode optimizes efficiency (21.9% faster than auto=false)
- Signals quality expectations to research engine

**Critical:** Always use `auto=true` - it's faster AND produces better results!

### For Crypto/Financial Research
```json
{
  "query": "Your research question",
  "reasoning_loops": 2,
  "exclude_social": false,
  "auto": true
}
```
**Note:** Keep social media for sentiment analysis

### For Professional/Academic Research
```json
{
  "query": "Your research question",
  "reasoning_loops": 2,
  "exclude_social": true,
  "auto": true,
  "source_timeout": 90
}
```
**Note:** Exclude social for authoritative sources only

### For Quick Research (Speed Priority)
```json
{
  "query": "Your research question",
  "reasoning_loops": 1,
  "auto": true,
  "allow_early_exit": true
}
```
**Note:**
- **Keep `auto=true`** - it's 21.9% faster than auto=false!
- Complex queries may still use 2+ loops (query complexity determines minimum)
- ❌ Don't use `auto=false` - no benefits, slower execution

## Related Files

### Current Implementation
- **V1 Agent:** `../../mesh/agents/caesar_research_agent.py`
- **Tests:** `../../mesh/tests/test_caesar_research_agent.yaml`

### External Resources
- **Official Docs:** https://docs.caesar.org/
- **API Reference:** https://docs.caesar.org/api-reference/
- **Changelog:** https://docs.caesar.org/changelog.mdx

## Questions?

Refer to:
1. **auto-mode-analysis.md** for how parameters actually work ⭐⭐ CRITICAL
2. **COMPARISON-SUMMARY.md** for quick comparison (3 configs) ⭐
3. **PM-REPORT.md** for strategic decisions
4. **v1-vs-v2-comparison.md** for V1→V2 migration
5. **v2-test-summary.md** for initial test evidence
6. Official Caesar docs for latest updates

---

**Last Updated:** 2026-01-21
**API Version Documented:** 2025-11-27
**Tests Completed:** 4 tests (basic + 3-way comparison)
**Critical Finding:** Query complexity determines loop count; always use `auto=true`
**Status:** Ready for implementation
