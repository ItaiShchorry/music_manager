/**
 * Pre-Commit Hook
 *
 * Purpose: Protect main branch and trigger code review before commits
 * Runs: Before every `git commit`
 * Blocking: Yes — prevents commits if checks fail
 *
 * Compatible with: Windows, macOS, Linux
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

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

function getCurrentBranch() {
  try {
    return execSync('git branch --show-current', { encoding: 'utf-8' }).trim();
  } catch (_) {
    return null;
  }
}

// ── Check 1: Protected branch ────────────────────────────────────────────────

function checkProtectedBranch() {
  const branch = getCurrentBranch();
  const protected_ = ['main', 'production'];

  if (protected_.includes(branch)) {
    log('❌ COMMIT BLOCKED', 'red');
    log(`Cannot commit directly to protected branch: "${branch}"`, 'yellow');
    log('\nCreate a feature branch first:', 'blue');
    log('  git checkout -b feature/your-feature-name\n', 'blue');
    return false;
  }

  log(`✓ Branch check passed (on "${branch}")`, 'green');
  return true;
}

// ── Check 2: Code review ─────────────────────────────────────────────────────

function runCodeReview() {
  log('\n🔍 Running automated code review...', 'blue');

  const reviewScript = path.join(__dirname, 'code-review.js');

  if (!fs.existsSync(reviewScript)) {
    log('⚠️  code-review.js not found in hooks directory — skipping', 'yellow');
    return true;
  }

  try {
    // Use `node` explicitly so this works on Windows (no shebang handling needed)
    execSync(`node "${reviewScript}"`, { stdio: 'inherit', shell: true });
    log('✓ Code review passed', 'green');
    return true;
  } catch (_) {
    log('❌ Code review failed — fix the issues above and try again', 'red');
    return false;
  }
}

// ── Check 3: Update STATUS.md ────────────────────────────────────────────────

function touchStatusFile() {
  const statusPath = path.join(process.cwd(), 'STATUS.md');

  if (!fs.existsSync(statusPath)) {
    log('⚠️  STATUS.md not found — skipping timestamp update', 'yellow');
    return;
  }

  try {
    let content = fs.readFileSync(statusPath, 'utf-8');
    const today = new Date().toISOString().split('T')[0];
    const updated = content.replace(
      /\*\*Last Updated:\*\*.*/,
      `**Last Updated:** ${today}`
    );

    if (updated !== content) {
      fs.writeFileSync(statusPath, updated, 'utf-8');
      execSync('git add STATUS.md', { shell: true });
      log('✓ STATUS.md timestamp updated and staged', 'green');
    }
  } catch (err) {
    log(`⚠️  Could not update STATUS.md: ${err.message}`, 'yellow');
    // Non-critical — don't block commit
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  log('\n═══════════════════════════════════', 'blue');
  log('   PRE-COMMIT HOOK', 'blue');
  log('═══════════════════════════════════\n', 'blue');

  if (!checkProtectedBranch()) process.exit(1);
  if (!runCodeReview()) process.exit(1);

  touchStatusFile();

  log('\n✅ All pre-commit checks passed — committing...\n', 'green');
}

main().catch((err) => {
  log(`\n❌ Pre-commit hook error: ${err.message}`, 'red');
  process.exit(1);
});
