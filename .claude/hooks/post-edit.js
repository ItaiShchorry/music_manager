/**
 * Post-Edit Hook
 *
 * Purpose: Auto-format code after significant changes
 * Runs: After Claude makes major code changes
 * Blocking: No - runs in background
 *
 * Compatible with: Windows, macOS, Linux
 * (Uses Node.js fs instead of shell `find` / `which`)
 */

const { execSync, spawnSync } = require('child_process');
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

/**
 * Recursively collect files with given extensions, skipping ignored dirs.
 * Cross-platform — no `find` command needed.
 */
function collectFiles(rootDir, extensions, ignoreDirs = []) {
  const results = [];

  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (_) {
      return;
    }
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!ignoreDirs.includes(entry.name)) walk(fullPath);
      } else if (entry.isFile() && extensions.includes(path.extname(entry.name))) {
        results.push(fullPath);
      }
    }
  }

  if (fs.existsSync(rootDir)) walk(rootDir);
  return results;
}

/**
 * Check whether a CLI tool is available on PATH — cross-platform.
 * Uses `spawnSync` with shell:true so it works on Windows without `which`.
 */
function isToolAvailable(tool) {
  const result = spawnSync(tool, ['--version'], { stdio: 'ignore', shell: true });
  return result.status === 0;
}

function formatPythonFiles() {
  log('\n🔧 Formatting Python files with Black...', 'blue');

  if (!isToolAvailable('black')) {
    log('⚠️  Black not found. Install: pip install black', 'yellow');
    return;
  }

  const files = collectFiles(
    path.join(process.cwd(), 'backend'),
    ['.py'],
    ['venv', '.venv', '__pycache__']
  );

  if (files.length === 0) {
    log('No Python files to format yet', 'blue');
    return;
  }

  try {
    // Quote paths to handle spaces on Windows
    const quoted = files.map((f) => `"${f}"`).join(' ');
    execSync(`black --line-length 100 ${quoted}`, { stdio: 'inherit', shell: true });
    log(`✓ Formatted ${files.length} Python file(s)`, 'green');
  } catch (_) {
    log('⚠️  Python formatting failed', 'yellow');
  }
}

function formatTypeScriptFiles() {
  log('\n🔧 Formatting TypeScript/JS files with Prettier...', 'blue');

  if (!isToolAvailable('prettier')) {
    log('⚠️  Prettier not found. Install: npm install -g prettier', 'yellow');
    return;
  }

  const files = collectFiles(
    path.join(process.cwd(), 'frontend', 'src'),
    ['.ts', '.tsx', '.js', '.jsx'],
    ['node_modules']
  );

  if (files.length === 0) {
    log('No TypeScript/JavaScript files to format yet', 'blue');
    return;
  }

  try {
    const quoted = files.map((f) => `"${f}"`).join(' ');
    execSync(`prettier --write ${quoted}`, { stdio: 'inherit', shell: true });
    log(`✓ Formatted ${files.length} TypeScript/JavaScript file(s)`, 'green');
  } catch (_) {
    log('⚠️  TypeScript formatting failed', 'yellow');
  }
}

function organizeImports() {
  log('\n🔧 Organizing Python imports with isort...', 'blue');

  if (!isToolAvailable('isort')) {
    log('⚠️  isort not found (optional). Install: pip install isort', 'yellow');
    return;
  }

  const files = collectFiles(
    path.join(process.cwd(), 'backend'),
    ['.py'],
    ['venv', '.venv', '__pycache__']
  );

  if (files.length === 0) return;

  try {
    const quoted = files.map((f) => `"${f}"`).join(' ');
    execSync(`isort ${quoted}`, { stdio: 'inherit', shell: true });
    log('✓ Organized Python imports', 'green');
  } catch (_) {
    log('⚠️  isort failed', 'yellow');
  }
}

function removeTrailingWhitespace() {
  log('\n🔧 Removing trailing whitespace...', 'blue');

  const root = process.cwd();
  const sourceFiles = [
    ...collectFiles(path.join(root, 'backend'), ['.py'], ['venv', '.venv', '__pycache__']),
    ...collectFiles(path.join(root, 'frontend', 'src'), ['.ts', '.tsx', '.js', '.jsx'], ['node_modules']),
    ...collectFiles(root, ['.md'], ['.git', 'node_modules', 'venv', '.venv']),
  ];

  let modified = 0;
  for (const file of sourceFiles) {
    try {
      const original = fs.readFileSync(file, 'utf-8');
      const cleaned = original.replace(/ +$/gm, '');
      if (original !== cleaned) {
        fs.writeFileSync(file, cleaned, 'utf-8');
        modified++;
      }
    } catch (_) {}
  }

  log(modified > 0 ? `✓ Cleaned trailing whitespace in ${modified} file(s)` : '✓ No trailing whitespace found', 'green');
}

async function main() {
  log('\n═══════════════════════════════════', 'blue');
  log('   POST-EDIT FORMATTING', 'blue');
  log('═══════════════════════════════════', 'blue');

  formatPythonFiles();
  formatTypeScriptFiles();
  organizeImports();
  removeTrailingWhitespace();

  log('\n✅ Auto-formatting complete\n', 'green');
}

main().catch((err) => {
  log(`\n⚠️  Post-edit hook error: ${err.message}`, 'yellow');
  // Non-critical — don't block work
});
