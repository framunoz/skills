#!/usr/bin/env node
/**
 * @hook py-quality-gate
 * @event Stop
 * @description Scoped quality enforcement hook. Runs Ruff linting and
 *              Pyrefly typing checks on specific directories.
 *              Controlled by CLAUDE_HOOKS_PY_QUALITY_DIRS or HOOKS_PY_QUALITY_DIRS.
 *              Blocks agent stop if errors found (with 3 auto-retries).
 * @dependencies Node.js, uv (ruff, pyrefly), fs, path, child_process
 * @performance Medium - Runs diagnostics on specified paths; fast when skipped.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const logger = require('./utils/logger');

const RETRY_DIR = '/tmp';
const RETRY_PREFIX = 'py-quality-retry-';
const SKIP_SENTINEL_PREFIX = 'py-quality-skip-';
const MAX_RETRIES = 3;
const STALE_THRESHOLD_MS = 24 * 3600 * 1000;

const ENV_VAR_CLAUDE = 'CLAUDE_HOOKS_PY_QUALITY_DIRS';
const ENV_VAR_SHARED = 'HOOKS_PY_QUALITY_DIRS';

let output = {};

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('py-quality-gate', input);

    const sessionId = input.session_id;
    const cwd = input.cwd || process.cwd();

    cleanupStaleRetryFiles();

    const targetPaths = resolveTargetPaths(cwd);
    if (!targetPaths) {
        output = handleNotConfigured(sessionId);
    } else {
        const retryCount = loadRetryCount(sessionId);
        logger.info(`🔍 Starting diagnostics on [${targetPaths.join(', ')}] (Attempt ${retryCount + 1}/${MAX_RETRIES})...`);

        const errorReport = runDiagnostics(targetPaths);

        if (errorReport.trim().length > 0) {
            output = handleFailure(sessionId, retryCount, errorReport);
        } else {
            output = handleSuccess(sessionId);
        }
    }
} catch (e) {
    logger.error(`Error in hook logic: ${e.message}`);
    output = {}; // Fail-open
}

logger.finish(output);
console.log(JSON.stringify(output));

// --- Retry persistence (inline, no state-manager) ---

function getRetryFilePath(sessionId) {
    return path.join(RETRY_DIR, `${RETRY_PREFIX}${sessionId || 'default'}`);
}

function loadRetryCount(sessionId) {
    const retryFile = getRetryFilePath(sessionId);
    try {
        if (fs.existsSync(retryFile)) {
            return parseInt(fs.readFileSync(retryFile, 'utf-8'), 10) || 0;
        }
    } catch (e) {
        logger.warn(`Failed to read retry file: ${e.message}`);
    }
    return 0;
}

function saveRetryCount(sessionId, count) {
    try {
        fs.writeFileSync(getRetryFilePath(sessionId), String(count));
    } catch (e) {
        logger.warn(`Failed to save retry file: ${e.message}`);
    }
}

function deleteRetryFile(sessionId) {
    try {
        const retryFile = getRetryFilePath(sessionId);
        if (fs.existsSync(retryFile)) fs.unlinkSync(retryFile);
    } catch (e) {
        logger.warn(`Failed to delete retry file: ${e.message}`);
    }
}

function cleanupStaleRetryFiles() {
    try {
        const tmpDir = RETRY_DIR;
        const now = Date.now();
        fs.readdirSync(tmpDir).forEach(file => {
            if (file.startsWith(RETRY_PREFIX) || file.startsWith(SKIP_SENTINEL_PREFIX)) {
                const fullPath = path.join(tmpDir, file);
                const stats = fs.statSync(fullPath);
                if (now - stats.mtimeMs > STALE_THRESHOLD_MS) {
                    fs.unlinkSync(fullPath);
                    logger.debug(`Deleted stale retry/skip file: ${file}`);
                }
            }
        });
    } catch (e) {
        logger.warn(`Stale retry cleanup failed: ${e.message}`);
    }
}

// --- Scoping & Configuration ---

function resolveTargetPaths(cwd) {
    const raw = process.env[ENV_VAR_CLAUDE] || process.env[ENV_VAR_SHARED] || '';
    if (!raw.trim()) return null;

    const entries = raw.split(',').map(p => p.trim()).filter(Boolean);
    const valid = [];
    for (const entry of entries) {
        const resolved = path.isAbsolute(entry) ? entry : path.resolve(cwd, entry);
        if (fs.existsSync(resolved) && fs.statSync(resolved).isDirectory()) {
            valid.push(resolved);
        } else {
            logger.warn(`⚠️ Path does not exist or is not a directory: "${entry}" (resolved: ${resolved})`);
        }
    }
    return valid.length > 0 ? valid : null;
}

function handleNotConfigured(sessionId) {
    const sentinel = path.join(RETRY_DIR, `${SKIP_SENTINEL_PREFIX}${sessionId || 'default'}`);
    if (!fs.existsSync(sentinel)) {
        logger.warn(
            `⚠️ py-quality-gate is DISABLED. Set ${ENV_VAR_CLAUDE} or ${ENV_VAR_SHARED} ` +
            `to a comma-separated list of directories to enable linting.\n` +
            `   Example: export ${ENV_VAR_CLAUDE}=src,tests`
        );
        try { fs.writeFileSync(sentinel, '1'); } catch (e) { /* fail-open */ }

        return {
            decision: "block",
            reason: `The Python quality gate hook is currently disabled because the environment variables ${ENV_VAR_CLAUDE} or ${ENV_VAR_SHARED} are not set. Recommend setting them to a comma-separated list of directories (e.g., 'src,tests') to enable linting and typing checks.`
        };
    }
    return {};
}

// --- Diagnostics ---

function runDiagnostics(paths) {
    let report = "";
    const pathArgs = paths.join(' ');
    const options = { stdio: 'pipe', timeout: 30000 };

    // --- Ruff Check ---
    try {
        logger.info(`🧹 Running Ruff checks on: ${pathArgs}`);
        execSync(`uvx ruff check --fix --output-format grouped ${pathArgs}`, options);
    } catch (error) {
        const stdout = error.stdout?.toString() || "";
        const stderr = error.stderr?.toString() || "";
        const hasRealErrors = (stdout && !stdout.includes("No Python files found")) || stderr;

        if (hasRealErrors) {
            report += `\n## Linting Errors (Ruff):\n`;
            if (stdout) report += `STDOUT:\n${stdout}\n`;
            if (stderr) report += `STDERR:\n${stderr}\n`;
        }
    }

    // --- Pyrefly Check ---
    try {
        logger.info(`🔥 Running Pyrefly checks on: ${pathArgs}`);
        execSync(`uvx pyrefly check --output-format min-text ${pathArgs}`, options);
    } catch (error) {
        const stdout = error.stdout?.toString() || "";
        const stderr = error.stderr?.toString() || "";

        const isNoFiles = stdout.includes("No Python files matched pattern");
        const isZeroErrors = stdout.includes("0 errors");
        const isExcluded = stderr.includes("is matched by `project-excludes` or ignore file");

        const isNoise = (!stdout && !stderr) || isNoFiles || isZeroErrors || isExcluded;

        if (!isNoise) {
            report += `\n## Typing Errors (Pyrefly):\n`;
            if (stdout) report += `STDOUT:\n${stdout}\n`;
            if (stderr) report += `STDERR:\n${stderr}\n`;
        }
    }

    return report;
}

// --- Result handlers ---

function handleSuccess(sessionId) {
    logger.info("✅ All scoped checks passed successfully.");
    deleteRetryFile(sessionId);
    return {};
}

function handleFailure(sessionId, retryCount, errorReport) {
    if (retryCount >= MAX_RETRIES) {
        logger.error("❌ Max retries reached. Allowing completion with errors.");
        console.error(`\n⚠️ QUALITY GATE FAILED after ${MAX_RETRIES} attempts:\n${errorReport}\n`);
        deleteRetryFile(sessionId);
        return {};
    }

    saveRetryCount(sessionId, retryCount + 1);
    logger.warn(`🚫 Issues detected. Blocking stop (Attempt ${retryCount + 1}/${MAX_RETRIES}).`);

    const reason = [
        'Your changes introduced errors. Please fix them before finishing.',
        '',
        '**How to read errors:**',
        '- Ruff (linting): `file.py:line:col: RULE_CODE message` — fix the code or add `# noqa: RULE_CODE` to suppress (ask to the user first).',
        '- Pyrefly (typing): `ERROR file.py:line:col-col: message [error-code]` — fix the type annotation or logic, or add `# pyrefly: ignore[error-code]` to suppress (ask to the user first).',
        '',
        errorReport,
    ].join('\n');
    return { decision: "block", reason };
}
