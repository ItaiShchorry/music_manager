/**
 * Code Review Hook
 *
 * Purpose: Automated code quality checks before commits
 * Runs: Called by pre-commit hook and after major code changes
 * Blocking: Yes — prevents commits if critical issues found
 *
 * Compatible with: Windows, macOS, Linux
 */

const { execSync } = require('child_process');
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

function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only', { encoding: 'utf-8' }).trim();
    if (!output) return [];
    return output
      .split('\n')
      .map((f) => f.trim())
      .filter((f) => f.length > 0 && ['.py', '.ts', '.tsx', '.js', '.jsx'].includes(path.extname(f)));
  } catch (_) {
    return [];
  }
}

function getStagedDiff(file) {
  try {
    // Use -- to safely handle filenames with spaces or special chars
    return execSync(`git diff --cached -- "${file}"`, { encoding: 'utf-8' });
  } catch (_) {
    return '';
  }
}

function analyzeFile(file, diff) {
  const issues = [];
  const warnings = [];
  const suggestions = [];

  const addedLines = diff.split('\n').filter((l) => l.startsWith('+') && !l.startsWith('+++'));

  // Helper to check if any added line matches a pattern
  const anyAdded = (pattern) => addedLines.some((l) => pattern.test(l));

  // 1. console.log / print statements
  if (anyAdded(/console\.log\(/) || anyAdded(/^\+\s*print\(/)) {
    warnings.push('Found console.log / print statements — use a proper logger instead');
  }

  // 2. TODO / FIXME in new code
  if (anyAdded(/\/\/\s*(TODO|FIXME)/i) || anyAdded(/#\s*(TODO|FIXME)/i)) {
    suggestions.push('Found TODO/FIXME comments — consider resolving before committing');
  }

  // 3. Overly long lines
  const maxLen = file.endsWith('.py') ? 120 : 100;
  const longLines = addedLines.filter((l) => l.length - 1 > maxLen); // subtract the leading '+'
  if (longLines.length > 0) {
    suggestions.push(`${longLines.length} line(s) exceed ${maxLen} characters`);
  }

  // 4. Leftover debug/breakpoint code
  const debugPatterns = [/debugger;/, /breakpoint\(\)/, /import pdb/, /pdb\.set_trace/];
  if (debugPatterns.some((p) => anyAdded(p))) {
    issues.push('Leftover debug code found (debugger / pdb) — remove before committing');
  }

  // 5. Hardcoded credentials (simple heuristic)
  const credentialPatterns = [
    /password\s*=\s*["'][^"']{4,}["']/i,
    /api[_-]?key\s*=\s*["'][^"']{4,}["']/i,
    /secret\s*=\s*["'][^"']{4,}["']/i,
  ];
  if (credentialPatterns.some((p) => anyAdded(p))) {
    issues.push('⚠️  CRITICAL: Possible hardcoded credentials detected — use environment variables');
  }

  // 6. Large blocks of commented-out code
  const commentedCount = addedLines.filter((l) => {
    const content = l.slice(1).trim();
    return content.startsWith('//') || content.startsWith('#');
  }).length;
  if (commentedCount > 10) {
    warnings.push(`Large block of commented code (${commentedCount} lines) — consider removing`);
  }

  return { issues, warnings, suggestions };
}

function performCodeReview() {
  const files = getStagedFiles();

  if (files.length === 0) {
    log('No source files staged for review', 'blue');
    return { passed: true };
  }

  log(`\nReviewing ${files.length} staged file(s):\n`, 'blue');

  let totalIssues = 0;
  let totalWarnings = 0;
  let totalSuggestions = 0;

  for (const file of files) {
    const diff = getStagedDiff(file);
    if (!diff) continue;

    const { issues, warnings, suggestions } = analyzeFile(file, diff);

    if (!issues.length && !warnings.length && !suggestions.length) {
      log(`  ✓ ${file}`, 'green');
      continue;
    }

    log(`  ${file}:`, 'yellow');
    issues.forEach((m) => { log(`    ❌ ISSUE: ${m}`, 'red'); totalIssues++; });
    warnings.forEach((m) => { log(`    ⚠️  WARNING: ${m}`, 'yellow'); totalWarnings++; });
    suggestions.forEach((m) => { log(`    💡 SUGGESTION: ${m}`, 'blue'); totalSuggestions++; });
    log('');
  }

  log('─────────────────────────────────', 'blue');
  log('CODE REVIEW SUMMARY:', 'blue');
  log(`  Issues:      ${totalIssues}`, totalIssues > 0 ? 'red' : 'green');
  log(`  Warnings:    ${totalWarnings}`, totalWarnings > 0 ? 'yellow' : 'green');
  log(`  Suggestions: ${totalSuggestions}`, 'blue');
  log('─────────────────────────────────\n', 'blue');

  if (totalIssues > 0) {
    log('❌ Code review FAILED — fix critical issues before committing', 'red');
    return { passed: false };
  }

  if (totalWarnings > 0) {
    log('⚠️  Code review PASSED with warnings', 'yellow');
  } else {
    log('✅ Code review PASSED', 'green');
  }

  return { passed: true };
}

function main() {
  try {
    const result = performCodeReview();
    process.exit(result.passed ? 0 : 1);
  } catch (err) {
    log(`\nError during code review: ${err.message}`, 'red');
    log('Allowing commit to proceed (review errored)', 'yellow');
    process.exit(0);
  }
}

main();
