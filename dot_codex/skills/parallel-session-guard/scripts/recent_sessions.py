#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


SESSIONS_ROOT = Path.home() / '.codex' / 'sessions'


@dataclass
class SessionSummary:
    session_id: str
    last_seen: str
    cwd: str
    worktree: str
    agent: str
    parent_thread_id: str
    user_summary: str
    assistant_summary: str
    rollout_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Summarize recent Codex sessions for the current repo and its worktrees.'
    )
    parser.add_argument('--repo-root', required=True, help='Canonical repo root path')
    parser.add_argument('--days', type=int, default=14, help='How many recent days to scan')
    parser.add_argument('--limit', type=int, default=20, help='Max sessions to print')
    parser.add_argument(
        '--session-id',
        help='If provided, print the matching session even if it falls outside the day filter',
    )
    parser.add_argument(
        '--format',
        choices=('markdown', 'json'),
        default='markdown',
        help='Output format',
    )
    return parser.parse_args()


def run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ['git', '-C', str(repo_root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ''
    return result.stdout


def list_worktrees(repo_root: Path) -> list[Path]:
    output = run_git(repo_root, 'worktree', 'list', '--porcelain')
    worktrees: list[Path] = []
    for line in output.splitlines():
        if line.startswith('worktree '):
            worktrees.append(Path(line.split(' ', 1)[1]).resolve())
    if not worktrees:
        worktrees.append(repo_root.resolve())
    return worktrees


def is_under_any(path: Path, parents: list[Path]) -> bool:
    for parent in parents:
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            continue
    return False


def belonging_worktree(path: Path, worktrees: list[Path]) -> Path:
    matches = []
    for worktree in worktrees:
        try:
            path.relative_to(worktree)
            matches.append(worktree)
        except ValueError:
            continue
    if not matches:
        return path
    return max(matches, key=lambda item: len(str(item)))


def shorten(text: str, limit: int = 100) -> str:
    flat = ' '.join(text.split())
    if len(flat) <= limit:
        return flat
    return flat[: limit - 3] + '...'


def markdown_cell(text: str) -> str:
    return text.replace('|', '/')


def parse_session_file(path: Path, worktrees: list[Path]) -> SessionSummary | None:
    session_id = ''
    cwd = ''
    agent = ''
    parent_thread_id = ''
    user_summary = ''
    assistant_summary = ''
    last_seen = ''

    with path.open('r', encoding='utf-8') as handle:
        for line in handle:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            timestamp = item.get('timestamp')
            if timestamp and (not last_seen or timestamp > last_seen):
                last_seen = timestamp

            if item.get('type') == 'session_meta':
                payload = item.get('payload', {})
                session_id = payload.get('id', session_id)
                cwd = payload.get('cwd', cwd)
                agent = payload.get('agent_nickname', agent) or payload.get('agent_role', agent)
                source = payload.get('source', {})
                if not isinstance(source, dict):
                    source = {}
                subagent = source.get('subagent', {})
                if not isinstance(subagent, dict):
                    subagent = {}
                thread_spawn = subagent.get('thread_spawn', {})
                if not isinstance(thread_spawn, dict):
                    thread_spawn = {}
                parent_thread_id = thread_spawn.get('parent_thread_id', parent_thread_id)
                continue

            if item.get('type') == 'turn_context':
                payload = item.get('payload', {})
                cwd = payload.get('cwd', cwd)
                continue

            if item.get('type') == 'event_msg':
                payload = item.get('payload', {})
                if payload.get('type') == 'user_message' and payload.get('message'):
                    user_summary = shorten(payload['message'])
                elif payload.get('type') == 'agent_message' and payload.get('message'):
                    assistant_summary = shorten(payload['message'])
                elif payload.get('type') == 'task_complete' and payload.get('last_agent_message'):
                    assistant_summary = shorten(payload['last_agent_message'])
                continue

            if item.get('type') == 'response_item':
                payload = item.get('payload', {})
                if payload.get('type') != 'message':
                    continue
                role = payload.get('role')
                pieces = payload.get('content', [])
                text_parts = []
                for piece in pieces:
                    if piece.get('type') in ('input_text', 'output_text') and piece.get('text'):
                        text_parts.append(piece['text'])
                if not text_parts:
                    continue
                joined = shorten(' '.join(text_parts))
                if role == 'user':
                    user_summary = joined
                elif role == 'assistant':
                    assistant_summary = joined

    if not session_id or not cwd:
        return None

    cwd_path = Path(cwd).resolve()
    if not is_under_any(cwd_path, worktrees):
        return None

    worktree = belonging_worktree(cwd_path, worktrees)
    return SessionSummary(
        session_id=session_id,
        last_seen=last_seen,
        cwd=str(cwd_path),
        worktree=str(worktree),
        agent=agent,
        parent_thread_id=parent_thread_id,
        user_summary=user_summary,
        assistant_summary=assistant_summary,
        rollout_path=str(path),
    )


def iter_candidate_files(days: int, session_id: str | None) -> list[Path]:
    if not SESSIONS_ROOT.exists():
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    matched: list[Path] = []
    for path in SESSIONS_ROOT.rglob('rollout-*.jsonl'):
        if session_id and session_id in path.name:
            matched.append(path)
            continue
        if session_id:
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        if modified >= cutoff:
            matched.append(path)
    return matched


def render_markdown(items: list[SessionSummary]) -> str:
    lines = [
        '| last_seen | session_id | worktree | agent | last_user | last_assistant |',
        '| --- | --- | --- | --- | --- | --- |',
    ]
    for item in items:
        lines.append(
            '| {last_seen} | {session_id} | {worktree} | {agent} | {user} | {assistant} |'.format(
                last_seen=item.last_seen or '-',
                session_id=item.session_id,
                worktree=markdown_cell(item.worktree),
                agent=markdown_cell(item.agent or '-'),
                user=markdown_cell(item.user_summary or '-'),
                assistant=markdown_cell(item.assistant_summary or '-'),
            )
        )
    return '\n'.join(lines)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    worktrees = list_worktrees(repo_root)

    summaries: list[SessionSummary] = []
    for path in iter_candidate_files(args.days, args.session_id):
        summary = parse_session_file(path, worktrees)
        if summary:
            summaries.append(summary)

    summaries.sort(key=lambda item: item.last_seen, reverse=True)

    if args.session_id:
        summaries = [item for item in summaries if item.session_id == args.session_id]

    summaries = summaries[: args.limit]

    if args.format == 'json':
        payload = [item.__dict__ for item in summaries]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
        return 0

    print(render_markdown(summaries))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
