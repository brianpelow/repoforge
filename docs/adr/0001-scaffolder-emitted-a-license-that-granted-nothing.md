# ADR 0001: The scaffolder emitted a license that granted nothing

**Status:** Accepted
**Date:** 2026-08-21

## Context

A portfolio-wide remediation replaced defective LICENSE files across 44
repositories with the canonical 11,358-byte Apache-2.0 text, and added an
auditor rule identifying license content by git blob SHA.

The artifacts were fixed. The generator that produces them was not.

`RepoGenerator.write_configs()` wrote a 73-byte LICENSE: three lines naming
the license and linking to apache.org. Apache-2.0 section 4(a) requires that
recipients receive a copy of the License itself. A pointer conveys no terms,
and automated detection reports the project as unlicensed, which a visitor
reads as all rights reserved.

Every repository this tool scaffolds would have reintroduced the defect that
took a full session to remediate.

The defect had a second half. `RepoAuditor` ran ten checks and all ten were
presence tests. `_check_file("LICENSE", "LICENSE present")` returns
`Path.exists()` and nothing more, so it passed on the stub the generator
itself wrote. `tests/test_auditor.py` wrote `"Apache 2.0"` to a temp file and
asserted the check passed -- encoding the defect as correct behaviour.

The scaffolder produced a defective artifact, its own auditor certified it,
and its own test suite ratified the certification.

None of this surfaced because nothing ran. The repository had no CI workflow,
despite shipping a `write_workflows()` that installs one into every repo it
creates.

## Decision

Ship the canonical Apache-2.0 text as package data
(`src/repoforge/data/apache-2.0.txt`, blob
`d645695673349e3947e8e5ae42332d0ac3164cd7`) and write it with `newline="\n"`,
so Windows CRLF translation cannot alter the bytes. Move copyright to a
per-repo NOTICE so the license text stays byte-identical across every
scaffolded repository and remains machine-detectable.

Add `_check_license_content` alongside the presence check rather than
replacing it. A missing file and a defective file are distinct findings with
distinct remediations -- the same split as CMP002 and CMP011 in
code-compliance-auditor. Recognition is by operative marker phrase for
Apache-2.0, MIT, and BSD-3, plus a length floor a pointer cannot clear.

Invert the test fixture. It now asserts that presence passes and content
fails.

Add CI: lint, types, tests, and an encoding guard.

## Consequences

Tests assert the git blob SHA of the generated file, not a marker phrase. A
CRLF translation produces a file that still reads as a license but hashes
differently and matches no detector. Only the object store answers the
question the license actually poses.

The inverted fixture is what proves the new check fires. The repository
corpus is already remediated, so nothing in it would trigger the rule
naturally -- a rule that flags zero repositories is indistinguishable from a
rule that does not work. Reconstructing the defect is the test.

`RepoGenerator` had no tests before this change. It now has three.

Enabling CI surfaced four further defects that had been invisible: a `mypy
strict` config that had never run (8 errors), a `uv.lock` listing packages
absent from the manifest, BOMs in 14 of 16 source files, and 27 ruff
violations. `uv sync --locked` now fails the build on lockfile drift.

The generalisable lesson: remediating a corpus does not remediate the
generator that produces it. After fixing a class of artifact, find what emits
it. And existence is not a property -- a check that passes on the presence of
an artifact certifies nothing about it. This is the third instance of that
failure in this portfolio, after CMP002 and SECURITY.md.