#!/usr/bin/env node
/**
 * @hook py-quality-gate
 * @event AfterAgent
 * @description Scoped quality enforcement hook. Runs Ruff linting and
 *              Pyrefly typing checks on specific directories.
 *              Controlled by GEMINI_HOOKS_PY_QUALITY_DIRS or HOOKS_PY_QUALITY_DIRS.
 *              Blocks turn completion if errors found (with 3 auto-retries).
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

const ENV_VAR_GEMINI = 'GEMINI_HOOKS_PY_QUALITY_DIRS';
const ENV_VAR_SHARED = 'HOOKS_PY_QUALITY_DIRS';

let output = { decision: "allow" };

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
    output = { decision: "allow" }; // Fail-open
}

logger.finish(output);
console.log(JSON.stringify(output));

// If we have a deny and we haven't reached max retries, exit with 2 to trigger Gemini retry
if (output.decision === "deny") {
    process.exit(2);
}

// --- Retry persistence ---

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
    const raw = process.env[ENV_VAR_GEMINI] || process.env[ENV_VAR_SHARED] || '';
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
            `⚠️ py-quality-gate is DISABLED. Set ${ENV_VAR_GEMINI} or ${ENV_VAR_SHARED} ` +
            `to a comma-separated list of directories to enable linting.\n` +
            `   Example: export ${ENV_VAR_GEMINI}=src,tests`
        );
        try { fs.writeFileSync(sentinel, '1'); } catch (e) { /* fail-open */ }

        return {
            decision: "deny",
            reason: `The Python quality gate hook is currently disabled because the environment variables ${ENV_VAR_GEMINI} or ${ENV_VAR_SHARED} are not set. Recommend setting them to a comma-separated list of directories (e.g., 'src,tests') to enable linting and typing checks.`
        };
    }
    return { decision: "allow" };
}

// --- Diagnostics ---

function truncateOutput(text, limit) {
    if (!text || limit === -1 || isNaN(limit)) return text;
    const lines = text.split('\n');
    if (lines.length <= limit) return text;
    const truncated = lines.slice(0, limit).join('\n');
    const remaining = lines.length - limit;
    return `${truncated}\n\n...[AND ${remaining} MORE LINES HIDDEN TO SAVE CONTEXT]...`;
}

function runDiagnostics(paths) {
    let report = "";
    const pathArgs = paths.join(' ');
    const options = { stdio: 'pipe', timeout: 30000 };
    
    // Default limit is 10 lines
    const rawLimit = process.env.GEMINI_HOOKS_PY_QUALITY_LIMIT || process.env.HOOKS_PY_QUALITY_LIMIT || "10";
    const limit = parseInt(rawLimit, 10);

    // --- Ruff Check ---
    try {
        logger.info(`🧹 Running Ruff checks on: ${pathArgs}`);
        execSync(`uvx ruff check --fix --output-format grouped ${pathArgs}`, options);
    } catch (error) {
        let stdout = error.stdout?.toString() || "";
        let stderr = error.stderr?.toString() || "";
        const hasRealErrors = (stdout && !stdout.includes("No Python files found")) || stderr;

        if (hasRealErrors) {
            stdout = truncateOutput(stdout, limit);
            stderr = truncateOutput(stderr, limit);
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
        let stdout = error.stdout?.toString() || "";
        let stderr = error.stderr?.toString() || "";

        const isNoFiles = stdout.includes("No Python files matched pattern") || stderr.includes("No Python files matched pattern");
        const isZeroErrors = stdout.includes("0 errors") || stderr.includes("0 errors");
        const isExcluded = stdout.includes("is matched by `project-excludes` or ignore file") || stderr.includes("is matched by `project-excludes` or ignore file");

        const isNoise = (!stdout && !stderr) || isNoFiles || isZeroErrors || isExcluded;

        if (!isNoise) {
            stdout = truncateOutput(stdout, limit);
            stderr = truncateOutput(stderr, limit);
            report += `\n## Typing Errors (Pyrefly):\n`;
            if (stdout) report += `STDOUT:\n${stdout}\n`;
            if (stderr) report += `STDERR:\n${stderr}\n`;
        }
    }

    return report;
}

function handleSuccess(sessionId) {
    logger.info("✅ All scoped checks passed successfully.");
    deleteRetryFile(sessionId);
    return { decision: "allow" };
}

function handleFailure(sessionId, retryCount, errorReport) {
    if (retryCount >= MAX_RETRIES - 1) {
        logger.error("❌ Max retries reached. Allowing completion with errors.");
        console.error(`\n⚠️ QUALITY GATE FAILED after ${MAX_RETRIES} attempts:\n${errorReport}\n`);
        deleteRetryFile(sessionId);
        return { 
            decision: "allow",
            reason: "Quality gate failed after 3 attempts. Please review manually."
        };
    }

    saveRetryCount(sessionId, retryCount + 1);
    logger.warn(`🚫 Issues detected. Blocking stop (Attempt ${retryCount + 1}/${MAX_RETRIES}).`);

    const reason = [
        'Your changes introduced errors. Please fix them before finishing.',
        '',
        '**How to read errors:**',
        '- Ruff (linting): `file.py:line:col: RULE_CODE message` — attempt to fix the code. Only add `# noqa: RULE_CODE` to suppress if you are 100% sure it is a false positive.',
        '- Pyrefly (typing): `ERROR file.py:line:col-col: message [error-code]` — attempt to fix the type annotation. Only add `# pyrefly: ignore[error-code]` if it is a false positive.',
        '',
        errorReport,
    ].join('\n');
    
    return { decision: "deny", reason, retryCount: retryCount + 1 };
}
