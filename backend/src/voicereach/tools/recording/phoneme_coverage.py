"""Japanese phoneme coverage tracker for voice preservation recordings.

Tracks which Japanese morae have been covered in recording sessions,
ensuring comprehensive phoneme coverage for TTS model training.

Coverage targets (from docs/08_VOICE_PRESERVATION.md):
- All 46 basic kana
- Dakuten (voiced), handakuten (semi-voiced)
- Yoon (contracted sounds)
- Sokuon (double consonants)
- Hatsuon (nasal sounds in context)
- Pitch accent types: atamadaka, nakadaka, odaka, heiban
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Basic Japanese morae (gojuon)
BASIC_MORAE = [
    "あ", "い", "う", "え", "お",
    "か", "き", "く", "け", "こ",
    "さ", "し", "す", "せ", "そ",
    "た", "ち", "つ", "て", "と",
    "な", "に", "ぬ", "ね", "の",
    "は", "ひ", "ふ", "へ", "ほ",
    "ま", "み", "む", "め", "も",
    "や", "ゆ", "よ",
    "ら", "り", "る", "れ", "ろ",
    "わ", "を", "ん",
]

# Dakuten (voiced)
DAKUTEN_MORAE = [
    "が", "ぎ", "ぐ", "げ", "ご",
    "ざ", "じ", "ず", "ぜ", "ぞ",
    "だ", "ぢ", "づ", "で", "ど",
    "ば", "び", "ぶ", "べ", "ぼ",
]

# Handakuten (semi-voiced)
HANDAKUTEN_MORAE = [
    "ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
]

# Yoon (contracted sounds)
YOON_MORAE = [
    "きゃ", "きゅ", "きょ",
    "しゃ", "しゅ", "しょ",
    "ちゃ", "ちゅ", "ちょ",
    "にゃ", "にゅ", "にょ",
    "ひゃ", "ひゅ", "ひょ",
    "みゃ", "みゅ", "みょ",
    "りゃ", "りゅ", "りょ",
    "ぎゃ", "ぎゅ", "ぎょ",
    "じゃ", "じゅ", "じょ",
    "びゃ", "びゅ", "びょ",
    "ぴゃ", "ぴゅ", "ぴょ",
]

# All target morae
ALL_MORAE = BASIC_MORAE + DAKUTEN_MORAE + HANDAKUTEN_MORAE + YOON_MORAE

# Sentence-final particles
FINAL_PARTICLES = ["よ", "ね", "か", "な", "ぞ", "わ", "の", "さ"]


@dataclass
class CoverageReport:
    """Coverage analysis results."""
    total_morae: int
    covered_morae: int
    coverage_percent: float
    missing_morae: list[str]
    basic_coverage: float
    dakuten_coverage: float
    handakuten_coverage: float
    yoon_coverage: float
    particle_coverage: float
    missing_particles: list[str]


@dataclass
class PhonemeCoverageTracker:
    """Tracks which Japanese morae have been covered in recordings."""

    covered: set[str] = field(default_factory=set)
    covered_particles: set[str] = field(default_factory=set)

    def add_text(self, text: str) -> None:
        """Register text content to update coverage.

        Extracts hiragana characters from text and marks them as covered.
        For yoon, checks consecutive character pairs.
        """
        # Convert katakana to hiragana
        normalized = ""
        for ch in text:
            cp = ord(ch)
            if 0x30A1 <= cp <= 0x30F6:  # Katakana range
                normalized += chr(cp - 0x60)
            else:
                normalized += ch

        # Check single morae
        for ch in normalized:
            if ch in set(BASIC_MORAE + DAKUTEN_MORAE + HANDAKUTEN_MORAE):
                self.covered.add(ch)

        # Check yoon (2-char sequences)
        for i in range(len(normalized) - 1):
            pair = normalized[i : i + 2]
            if pair in YOON_MORAE:
                self.covered.add(pair)

        # Check sentence-final particles (last char before punctuation)
        stripped = normalized.rstrip("。！？、…")
        if stripped and stripped[-1] in FINAL_PARTICLES:
            self.covered_particles.add(stripped[-1])

    def report(self) -> CoverageReport:
        """Generate a coverage report."""
        total = len(ALL_MORAE)
        covered_count = sum(1 for m in ALL_MORAE if m in self.covered)

        basic_covered = sum(1 for m in BASIC_MORAE if m in self.covered)
        dakuten_covered = sum(1 for m in DAKUTEN_MORAE if m in self.covered)
        handakuten_covered = sum(1 for m in HANDAKUTEN_MORAE if m in self.covered)
        yoon_covered = sum(1 for m in YOON_MORAE if m in self.covered)
        particle_covered = sum(1 for p in FINAL_PARTICLES if p in self.covered_particles)

        missing = [m for m in ALL_MORAE if m not in self.covered]
        missing_particles = [p for p in FINAL_PARTICLES if p not in self.covered_particles]

        return CoverageReport(
            total_morae=total,
            covered_morae=covered_count,
            coverage_percent=round(covered_count / total * 100, 1) if total > 0 else 0.0,
            missing_morae=missing,
            basic_coverage=round(basic_covered / len(BASIC_MORAE) * 100, 1),
            dakuten_coverage=round(dakuten_covered / len(DAKUTEN_MORAE) * 100, 1),
            handakuten_coverage=round(handakuten_covered / len(HANDAKUTEN_MORAE) * 100, 1),
            yoon_coverage=round(yoon_covered / len(YOON_MORAE) * 100, 1),
            particle_coverage=round(particle_covered / len(FINAL_PARTICLES) * 100, 1),
            missing_particles=missing_particles,
        )
