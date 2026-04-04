#!/usr/bin/env node
/**
 * @hook notification
 * @event Notification
 * @matcher .*
 * @description Displays desktop notifications when Claude Code needs user attention.
 *              Supports macOS (osascript) and Linux (notify-send).
 * @dependencies Node.js, osascript (macOS) or notify-send (Linux)
 * @performance Low - Simple system notification call.
 */
const { exec } = require('child_process');
const fs = require('fs');
const logger = require('./utils/logger');

let output = { decision: "allow" };

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('notification', input);

    const notification = input.notification || {};
    const title = notification.title || 'Claude Code';
    const message = notification.message || 'Needs your attention';
    const subtitle = notification.subtitle || '';

    const platform = process.platform;
    let command;

    if (platform === 'darwin') {
        // macOS - use osascript with heredoc to avoid quoting issues
        const fullMessage = subtitle ? `${message}\n${subtitle}` : message;
        // Use a temp approach: write to a temp AppleScript file and execute it
        const appleScript = `display notification "${escapeAppleScriptString(fullMessage)}" with title "${escapeAppleScriptString(title)}"`;
        command = `osascript -e '${escapeForSingleQuotedShell(appleScript)}'`;
    } else if (platform === 'linux') {
        // Linux - use notify-send
        const fullMessage = subtitle ? `${message}\n${subtitle}` : message;
        command = `notify-send "${escapeShell(title)}" "${escapeShell(fullMessage)}"`;
    } else {
        // Windows or other - log and skip
        logger.warn(`Notifications not supported on platform: ${platform}`);
        process.exit(0);
    }

    logger.debug(`Executing: ${command}`);

    exec(command, { timeout: 5000 }, (error) => {
        if (error) {
            logger.error(`❌ Notification failed: ${error.message}`);
        } else {
            logger.info(`🔔 Notification sent: ${title} - ${message}`);
        }
        // Always exit successfully - notifications are non-critical
        process.exit(0);
    });

} catch (e) {
    logger.error(`Error in notification hook: ${e.message}`);
    // Fail-open: don't block on notification errors
}

/**
 * Escape special characters for AppleScript string literals
 * AppleScript uses backslash escaping inside double quotes
 */
function escapeAppleScriptString(str) {
    return str
        .replace(/\\/g, '\\\\')  // Backslashes first
        .replace(/"/g, '\\"')     // Double quotes
        .replace(/\n/g, ' ');     // Newlines to spaces
}

/**
 * Escape a string to be used inside single-quoted shell argument
 * The safest approach is to end the single quote, add escaped char, restart single quote
 */
function escapeForSingleQuotedShell(str) {
    return str
        .replace(/'/g, "'\"'\"'");  // End quote, add escaped quote, restart quote
}

/**
 * Escape special characters for shell double-quoted strings
 */
function escapeShell(str) {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/"/g, '\\"')
        .replace(/`/g, '\\`')
        .replace(/\$/g, '\\$')
        .replace(/\n/g, ' ');
}

// Output decision immediately (exec is async but we don't wait)
logger.finish(output);
process.stdout.write(JSON.stringify(output) + '\n');