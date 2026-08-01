import argparse, json, re, sys
from collections import Counter, defaultdict

RULES = [
    ('auth', re.compile(r'\b(401|403|unauthori[sz]ed|forbidden|permission denied|login required)\b', re.I), 'Refresh credentials or reduce requested scope.'),
    ('rate_limit', re.compile(r'\b(429|rate limit|too many requests|quota exceeded)\b', re.I), 'Add backoff, batching, or a cheaper fallback route.'),
    ('network', re.compile(r'\b(timeout|timed out|ECONN|ENOTFOUND|TLS|SSL|connection reset)\b', re.I), 'Retry with jitter and capture endpoint health.'),
    ('schema', re.compile(r'\b(JSONDecodeError|invalid json|schema|validation|expected .* got)\b', re.I), 'Save raw output and add contract tests.'),
    ('filesystem', re.compile(r'\b(no such file|not found|EACCES|read-only|path does not exist)\b', re.I), 'Check working directory, allowlist, and path assumptions.'),
    ('unsafe_command', re.compile(r'\b(rm -rf|git reset --hard|checkout --|DROP TABLE|destructive)\b', re.I), 'Require explicit human approval before execution.'),
]

def classify(line):
    for key, rx, fix in RULES:
        if rx.search(line):
            return key, fix
    return 'unknown', 'Group with neighboring lines and add a new classifier rule.'

def analyze(text):
    events=[]
    for i,line in enumerate(text.splitlines(),1):
        if re.search(r'\b(error|failed|exception|traceback|denied|timeout|429|403|401|jsondecodeerror|invalid json)\b', line, re.I):
            kind, fix = classify(line)
            events.append({'line':i,'type':kind,'message':line.strip()[:220],'suggested_fix':fix})
    counts=Counter(e['type'] for e in events)
    return {'total_events':len(events),'counts':dict(counts),'events':events}

def markdown(report):
    out=['# Agent Tool Error Taxonomy','',f"Total events: {report['total_events']}",'']
    for k,v in sorted(report['counts'].items(), key=lambda x:(-x[1],x[0])):
        out.append(f'- {k}: {v}')
    out.append('')
    for e in report['events'][:50]:
        out.append(f"- L{e['line']} `{e['type']}`: {e['message']} Fix: {e['suggested_fix']}")
    return '\n'.join(out)+'\n'

def main(argv=None):
    ap=argparse.ArgumentParser(description='Build a taxonomy of AI agent tool errors from logs.')
    ap.add_argument('logfile')
    ap.add_argument('--format', choices=['json','markdown'], default='markdown')
    ns=ap.parse_args(argv)
    text=open(ns.logfile, encoding='utf-8').read()
    report=analyze(text)
    print(json.dumps(report, indent=2) if ns.format=='json' else markdown(report))
if __name__=='__main__': main()
