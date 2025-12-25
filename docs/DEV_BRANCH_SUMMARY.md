# Dev Branch Summary

**Branch:** `dev`
**Compared to:** `main`
**Date:** 2025-12-26

---

## What This Branch Is About

### 1. 13 New Languages

Main branch has: **elixir**, **python** (2 languages)

Dev branch adds **13 new languages**:

| Language | Type | Tool |
|----------|------|------|
| Erlang | tree-sitter | built-in |
| TypeScript | SCIP | scip-typescript |
| JavaScript | SCIP | scip-typescript |
| Rust | SCIP | rust-analyzer |
| Go | SCIP | scip-go |
| Java | SCIP | scip-java (coursier) |
| Scala | SCIP | scip-java (coursier) |
| C | SCIP | scip-clang |
| C++ | SCIP | scip-clang |
| Ruby | SCIP | scip-ruby |
| C# | SCIP | scip-dotnet |
| VB | SCIP | scip-dotnet |
| Dart | SCIP | scip_dart |

### 2. SCIP Moved to Separate Package

- `cicada-scip` is now an optional dependency
- Enables monorepo split architecture
- Lighter base installation without SCIP tooling

### 3. Removed KeyBERT and GloVe

- Removed heavy ML dependencies (`keybert`, `glove`)
- Simpler, lighter keyword extraction
- Faster installation, smaller footprint

---

## Docker Testing Infrastructure

Complete E2E testing in `tests/docker/`:

```
Dockerfile.base     # Minimal Python + Cicada
Dockerfile.go       # Go + scip-go
Dockerfile.java     # JDK + Gradle + coursier
Dockerfile.scala    # JDK + sbt + coursier
Dockerfile.ruby     # Ruby + scip-ruby
Dockerfile.dart     # Dart SDK + scip_dart
Dockerfile.c        # GCC + CMake + scip-clang
Dockerfile.dotnet   # .NET SDK + scip-dotnet
test-complete.sh    # 3-phase comprehensive test
```

---

## Test Fixtures

| Fixture | index.scip | .gitignore |
|---------|------------|------------|
| sample_go | ❌ Pending | ✅ |
| sample_java | ❌ Pending | ✅ |
| sample_scala | ❌ Pending | ✅ |
| sample_ruby | ❌ Pending | ✅ |
| sample_dart | ❌ Pending | ✅ |
| sample_c | ❌ Pending | ✅ |
| sample_cpp | ❌ Pending | ✅ |
| sample_csharp | ❌ Pending | ✅ |
| sample_vb | ❌ Pending | ✅ |

---

## What's Left

1. Run Docker tests to generate missing `index.scip` files
2. Validate all 13 new languages work end-to-end
