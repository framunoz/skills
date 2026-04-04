/**
 * @module state-manager
 * @description Handles session-specific JSON state for Gemini CLI hooks.
 */
const fs = require('fs');
const path = require('path');
const logger = require('./logger');

const TMP_DIR = path.join(__dirname, '..', '..', 'tmp', 'hooks');

/**
 * Ensures the temporary directory exists.
 */
function ensureTmpDir() {
    if (!fs.existsSync(TMP_DIR)) {
        fs.mkdirSync(TMP_DIR, { recursive: true });
    }
}

/**
 * Returns the path to the state file for a given session.
 */
function getStatePath(sessionId) {
    return path.join(TMP_DIR, `state_${sessionId || 'default'}.json`);
}

/**
 * Loads the state for a session. Returns a default state if not found.
 */
function loadState(sessionId) {
    const stateFile = getStatePath(sessionId);
    let state = { files: [], retryCount: 0, lastModified: Date.now() };

    if (fs.existsSync(stateFile)) {
        try {
            state = JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
        } catch (e) {
            logger.warn(`Failed to parse state file for ${sessionId}: ${e.message}`);
        }
    }
    return state;
}

/**
 * Saves the state for a session.
 */
function saveState(sessionId, state) {
    ensureTmpDir();
    const stateFile = getStatePath(sessionId);
    state.lastModified = Date.now();
    try {
        fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
    } catch (e) {
        logger.error(`Failed to save state for ${sessionId}: ${e.message}`);
    }
}

/**
 * Deletes the state file for a session.
 */
function deleteState(sessionId) {
    const stateFile = getStatePath(sessionId);
    try {
        if (fs.existsSync(stateFile)) {
            fs.unlinkSync(stateFile);
        }
    } catch (e) {
        logger.warn(`Failed to delete state file for ${sessionId}: ${e.message}`);
    }
}

/**
 * Removes state files older than the specified threshold (default 24h).
 */
function cleanupStaleStates(thresholdMs = 24 * 3600 * 1000) {
    try {
        if (!fs.existsSync(TMP_DIR)) return;

        const now = Date.now();
        fs.readdirSync(TMP_DIR).forEach(file => {
            if (file.startsWith('state_') && file.endsWith('.json')) {
                const fullPath = path.join(TMP_DIR, file);
                const stats = fs.statSync(fullPath);
                if (now - stats.mtimeMs > thresholdMs) {
                    fs.unlinkSync(fullPath);
                    logger.debug(`Deleted stale state file: ${file}`);
                }
            }
        });
    } catch (e) {
        logger.warn(`Stale state cleanup failed: ${e.message}`);
    }
}

module.exports = {
    loadState,
    saveState,
    deleteState,
    cleanupStaleStates,
    getStatePath
};
