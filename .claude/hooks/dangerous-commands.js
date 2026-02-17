/**
 * Dangerous Commands Hook
 *
 * Purpose: Prevent destructive operations that could cause data or code loss
 * Runs: Before Claude executes a potentially dangerous shell command
 * Blocking: Yes for CRITICAL/HIGH severity; warns only for MEDIUM
 *
 * Compatible with: Windows, macOS, Linux
 * (Patterns cover both Unix and Windows destructive commands)
 */

const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// ── Dangerous pattern definitions ─────────────────────────────────────────────

const PATTERNS = [
  // ── Git ──────────────────────────────────────────────────────────────────
  {
    pattern: /git\s+push\s+.*--force/,
    reason: 'Force-push can permanently overwrite remote history',
    severity: 'high',
  },
  {
    pattern: /git\s+reset\s+--hard/,
    reason: 'Hard reset permanently discards uncommitted local changes',
    severity: 'high',
  },
  {
    pattern: /git\s+clean\s+-[a-zA-Z]*[fdx]/,
    reason: 'git clean permanently deletes untracked files/directories',
    severity: 'medium',
  },

  // ── Unix file deletion ───────────────────────────────────────────────────
  {
    pattern: /rm\s+-[rf]+\s+\/(?!\w)/,   // rm -rf / or rm -rf /  (root)
    reason: 'Recursive delete from root — EXTREMELY DANGEROUS',
    severity: 'critical',
  },
  {
    pattern: /rm\s+-[rf]+\s+~\//,
    reason: 'Recursive delete of home directory — EXTREMELY DANGEROUS',
    severity: 'critical',
  },
  {
    pattern: /rm\s+-[rf]+\s+\*/,
    reason: 'Recursive delete with wildcard — could wipe entire directory',
    severity: 'high',
  },
  {
    pattern: /rm\s+-[rf]+\s+\./,
    reason: 'Recursive delete of current directory',
    severity: 'high',
  },

  // ── Windows file deletion ────────────────────────────────────────────────
  {
    pattern: /rmdir\s+\/[sS]\s+\/[qQ]\s+[cC]:\\/,
    reason: 'Recursive delete of a root Windows path — EXTREMELY DANGEROUS',
    severity: 'critical',
  },
  {
    pattern: /rmdir\s+\/[sS]\s+\/[qQ]\s+\./,
    reason: 'Recursive delete of current directory on Windows',
    severity: 'high',
  },
  {
    pattern: /del\s+\/[fF]\s+\/[sS]\s+\/[qQ]\s+\*/,
    reason: 'Bulk forced-delete of all files in directory tree',
    severity: 'high',
  },
  {
    pattern: /Remove-Item\s+-Recurse\s+-Force\s+[cC]:\\/,
    reason: 'PowerShell recursive delete of a root Windows path',
    severity: 'critical',
  },
  {
    pattern: /Remove-Item\s+-Recurse\s+-Force\s+\./,
    reason: 'PowerShell recursive delete of current directory',
    severity: 'high',
  },

  // ── Database ─────────────────────────────────────────────────────────────
  {
    pattern: /DROP\s+DATABASE/i,
    reason: 'Drops the entire database — all data permanently lost',
    severity: 'critical',
  },
  {
    pattern: /DROP\s+TABLE/i,
    reason: 'Drops a table and all its data permanently',
    severity: 'high',
  },
  {
    pattern: /TRUNCATE\s+TABLE/i,
    reason: 'Truncate deletes all rows — cannot be rolled back without a transaction',
    severity: 'high',
  },
  {
    // DELETE FROM <table> with no WHERE clause
    pattern: /DELETE\s+FROM\s+\w+\s*;/i,
    reason: 'DELETE without a WHERE clause removes ALL rows from the table',
    severity: 'high',
  },

  // ── Alembic ──────────────────────────────────────────────────────────────
  {
    pattern: /alembic\s+downgrade/,
    reason: 'Downgrading migrations can cause irreversible data loss',
    severity: 'medium',
  },

  // ── Package management ───────────────────────────────────────────────────
  {
    pattern: /npm\s+publish/,
    reason: 'Publishing to npm registry — ensure this is intentional',
    severity: 'medium',
  },
  {
    pattern: /pip\s+uninstall\s+-y/,
    reason: 'Uninstalling Python packages without confirmation prompt',
    severity: 'low',
  },

  // ── Permissions (Unix) ───────────────────────────────────────────────────
  {
    pattern: /chmod\s+-R\s+777/,
    reason: 'Setting 777 permissions is a security risk',
    severity: 'medium',
  },
  {
    pattern: /sudo\s+rm/,
    reason: 'Using sudo with rm can bypass filesystem protections',
    severity: 'high',
  },
];

// ── Severity assessment ───────────────────────────────────────────────────────

function assess(matches) {
  if (!matches.length) return { threat: 'none', shouldBlock: false };
  const severities = matches.map((m) => m.severity);
  if (severities.includes('critical')) return { threat: 'critical', shouldBlock: true };
  if (severities.includes('high')) return { threat: 'high', shouldBlock: true };
  if (severities.includes('medium')) return { threat: 'medium', shouldBlock: false };
  return { threat: 'low', shouldBlock: false };
}

// ── Display ───────────────────────────────────────────────────────────────────

function display(command, matches, threat) {
  log('\n⚠️  DANGEROUS COMMAND DETECTED ⚠️', 'red');
  log('═══════════════════════════════════\n', 'red');
  log(`Command: ${command}\n`, 'yellow');
  log('Potential Issues:', 'yellow');

  matches.forEach(({ severity, reason }) => {
    const icon =
      severity === 'critical' ? '🚨' :
      severity === 'high'     ? '⛔' :
      severity === 'medium'   ? '⚠️ ' : 'ℹ️ ';
    log(`  ${icon} [${severity.toUpperCase()}] ${reason}`, 'yellow');
  });

  log('');

  if (threat.shouldBlock) {
    log('❌ COMMAND BLOCKED FOR SAFETY', 'red');
    log('\nIf you truly need to run this:', 'yellow');
    log('  1. Run it manually in your terminal', 'yellow');
    log('  2. Make sure you understand the consequences', 'yellow');
    log('  3. Have a backup if data is involved', 'yellow');
  } else {
    log('⚠️  COMMAND ALLOWED WITH WARNING — proceed carefully', 'yellow');
  }

  log('\n═══════════════════════════════════\n', 'red');
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main() {
  const command = process.argv.slice(2).join(' ');

  if (!command) {
    process.exit(0);
  }

  const matches = PATTERNS.filter(({ pattern }) => pattern.test(command));
  const threat = assess(matches);

  if (threat.threat === 'none') {
    process.exit(0);
  }

  display(command, matches, threat);
  process.exit(threat.shouldBlock ? 1 : 0);
}

main();
