from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace GitHub URL placeholders in the manuscript and README using the repo's origin remote."
    )
    parser.add_argument(
        "--repo",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the khinchin-signature-pslq repository root.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the two-pass pdflatex verification step.",
    )
    return parser.parse_args()


def normalize_remote(url: str) -> str:
    url = url.strip()
    if url.startswith("git@github.com:"):
        path = url.split(":", 1)[1]
        if path.endswith(".git"):
            path = path[:-4]
        return f"https://github.com/{path}"
    if url.startswith("https://") or url.startswith("http://"):
        return url[:-4] if url.endswith(".git") else url
    return url


def get_origin_url(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("No origin remote is configured for this repository yet.")
    return normalize_remote(result.stdout)


def replace_in_file(path: Path, replacements: list[tuple[str, str]]) -> str:
    original = path.read_text(encoding="utf-8")
    updated = original
    for old, new in replacements:
        updated = updated.replace(old, new)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path),
        )
    )


def build_paper(repo: Path) -> None:
    paper_dir = repo / "paper"
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "khinchin_signature_expmath_note.tex"],
            cwd=paper_dir,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            raise RuntimeError("pdflatex build failed")


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()

    try:
        public_url = get_origin_url(repo)
    except RuntimeError as exc:
        print({"status": "blocked", "reason": str(exc)})
        return 1

    readme = repo / "README.md"
    tex = repo / "paper" / "khinchin_signature_expmath_note.tex"

    readme_diff = replace_in_file(
        readme,
        [("<INSERT_PUBLIC_GITHUB_URL_HERE>", public_url)],
    )
    tex_diff = replace_in_file(
        tex,
        [
            (r"\url{<INSERT_GITHUB_URL_HERE>}", rf"\url{{{public_url}}}"),
            ("<INSERT_GITHUB_URL_HERE>", public_url),
        ],
    )

    if not args.skip_build:
        build_paper(repo)

    print({"status": "ok", "public_url": public_url})
    if readme_diff:
        print(readme_diff)
    if tex_diff:
        print(tex_diff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
