/**
 * @module logger
 * @description Centralized logging utility for Gemini CLI hooks.
 *              Supports ISO 8601 timestamps, log levels, size-based
 *              rotation (1MB), and mirroring to stderr for
 *              the Debug Drawer.
 * @dependencies Node.js, fs, path
 */
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, '..', 'logs');
const LOG_FILE = path.join(LOG_DIR, 'hooks.log');
const OLD_LOG_FILE = path.join(LOG_DIR, 'hooks.old.log');
const MAX_SIZE = 1 * 1024 * 1024; // 1MB

const LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
};

const getLogLevel = () => {
    const level = (process.env.CLAUDE_HOOKS_LOG_LEVEL || 'INFO').toUpperCase();
    return LEVELS[level] !== undefined ? LEVELS[level] : LEVELS.INFO;
};

let currentHookName = 'unknown';
let currentSessionId = 'no-session';

const rotateLogs = () => {
    try {
        if (fs.existsSync(LOG_FILE)) {
            const stats = fs.statSync(LOG_FILE);
            if (stats.size > MAX_SIZE) {
                fs.renameSync(LOG_FILE, OLD_LOG_FILE);
            }
        }
    } catch (e) {
        console.error(`[logger] Failed to rotate logs: ${e.message}`);
    }
};

const writeToLog = (levelName, msg) => {
    const levelValue = LEVELS[levelName];
    if (levelValue < getLogLevel()) return;

    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] [${currentSessionId}] [${currentHookName}] [${levelName}] ${msg}\n`;

    // Always mirror to stderr for the Debug Drawer
    console.error(`[${currentHookName}] ${msg}`);

    try {
        if (!fs.existsSync(LOG_DIR)) {
            fs.mkdirSync(LOG_DIR, { recursive: true });
        }
        rotateLogs();
        fs.appendFileSync(LOG_FILE, line);
    } catch (e) {
        // Fail-open: don't crash the hook if logging fails
        console.error(`[logger] Failed to write to log file: ${e.message}`);
    }
};

const logger = {
    init: (hookName, input) => {
        currentHookName = hookName;
        currentSessionId = (input?.session_id || 'no-session').slice(0, 8);
        writeToLog('INFO', '--- Hook Started ---');
        if (input) {
            writeToLog('DEBUG', `Input: ${JSON.stringify(input)}`);
        }
    },
    debug: (msg) => writeToLog('DEBUG', msg),
    info: (msg) => writeToLog('INFO', msg),
    warn: (msg) => writeToLog('WARN', msg),
    error: (msg) => writeToLog('ERROR', msg),
    finish: (output) => {
        if (output) {
            writeToLog('DEBUG', `Output: ${JSON.stringify(output)}`);
        }
        writeToLog('INFO', '--- Hook Finished ---');
    }
};

module.exports = logger;
