#!/usr/bin/env node
/**
 * @hook notification
 * @event Notification
 * @matcher .*
 * @description Displays desktop notifications when Gemini CLI needs user attention.
 *              Synchronized with Gemini CLI Reference (notification_type, message).
 * @dependencies Node.js, osascript (macOS) or notify-send (Linux)
 * @performance Low - Simple system notification call.
 */
const { exec } = require('child_process');
const fs = require('fs');
const logger = require('./utils/logger');

let output = { decision: "allow" };

try {
    const inputString = fs.readFileSync(0, 'utf-8');
    if (!inputString.trim()) {
        process.exit(0);
    }
    const input = JSON.parse(inputString);
    logger.init('notification', input);

    // Gemini Spec: notification_type, message, details
    const notificationType = input.notification_type || 'General';
    const rawMessage = input.message || 'Needs your attention';
    
    // Map notification types to user-friendly titles
    const titleMap = {
        'ToolPermission': '🔒 Permission Required',
        'SessionStart': '🚀 Session Started',
        'SessionEnd': '🏁 Session Ended',
        'General': '♊ Gemini CLI'
    };
    
    const title = titleMap[notificationType] || `♊ Gemini: ${notificationType}`;
    const message = rawMessage;

    const platform = process.platform;
    let command;

    if (platform === 'darwin') {
        // macOS - use osascript
        const appleScript = `display notification "${escapeAppleScriptString(message)}" with title "${escapeAppleScriptString(title)}"`;
        command = `osascript -e '${escapeForSingleQuotedShell(appleScript)}'`;
    } else if (platform === 'linux') {
        // Linux - use notify-send
        command = `notify-send "${escapeShell(title)}" "${escapeShell(message)}"`;
    } else {
        logger.warn(`Notifications not supported on platform: ${platform}`);
        process.stdout.write(JSON.stringify(output) + '\n');
        process.exit(0);
    }

    logger.debug(`Executing: ${command}`);

    // Notifications are observability-only in Gemini, but we still run the command
    exec(command, { timeout: 5000 }, (error) => {
        if (error) {
            logger.error(`❌ Notification failed: ${error.message}`);
        } else {
            logger.info(`🔔 Notification sent: [${notificationType}] ${message}`);
        }
        process.exit(0);
    });

} catch (e) {
    logger.error(`Error in notification hook: ${e.message}`);
    process.stdout.write(JSON.stringify(output) + '\n');
    process.exit(0);
}

function escapeAppleScriptString(str) {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/"/g, '\\"')
        .replace(/\n/g, ' ');
}

function escapeForSingleQuotedShell(str) {
    return str
        .replace(/'/g, "'\"'\"'");
}

function escapeShell(str) {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/"/g, '\\"')
        .replace(/`/g, '\\`')
        .replace(/\$/g, '\\$')
        .replace(/\n/g, ' ');
}

logger.finish(output);
process.stdout.write(JSON.stringify(output) + '\n');
