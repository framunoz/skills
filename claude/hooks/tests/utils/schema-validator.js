#!/usr/bin/env node
/**
 * Simple JSON Schema Validator for Claude Code Hooks
 * Used only in tests to ensure standard compliance.
 */
const fs = require('fs');

const EVENT_SCHEMAS = {
    'PreToolUse': {
        input: ['session_id', 'cwd', 'hook_event_name', 'tool_name', 'tool_input'],
        output: ['decision', 'reason', 'continue', 'hookSpecificOutput', 'tool_input', 'systemMessage', 'additionalContext']
    },
    'PostToolUse': {
        input: ['session_id', 'cwd', 'hook_event_name', 'tool_name', 'tool_input', 'tool_response'],
        output: ['decision', 'reason', 'continue', 'hookSpecificOutput', 'systemMessage', 'additionalContext']
    },
    'Stop': {
        input: ['session_id', 'cwd', 'hook_event_name'],
        output: ['decision', 'reason', 'continue', 'hookSpecificOutput', 'systemMessage', 'additionalContext']
    },
    'Notification': {
        input: ['session_id', 'cwd', 'hook_event_name', 'title', 'message', 'notification_type'],
        output: ['decision', 'reason', 'continue', 'hookSpecificOutput']
    }
};

function validate(json, type, eventName) {
    const schema = EVENT_SCHEMAS[eventName];
    if (!schema) {
        console.error(`❌ Validation Error: Unknown event "${eventName}"`);
        process.exit(1);
    }

    const fields = schema[type];
    const obj = JSON.parse(json);

    // Common check for output: {} is always valid
    if (type === 'output' && Object.keys(obj).length === 0) {
        return true;
    }

    // Check for unexpected fields in output (strict mode)
    if (type === 'output') {
        const keys = Object.keys(obj);
        for (const key of keys) {
            if (!fields.includes(key)) {
                console.error(`❌ Validation Error: Unexpected output field "${key}" for event "${eventName}". Expected among: [${fields.join(', ')}]`);
                return false;
            }
        }
    }

    // Check specifically for Notification field misplacement (common bug)
    if (type === 'input' && eventName === 'Notification') {
        if (obj.notification) {
            console.error(`❌ Validation Error: "Notification" event input should contain "title" and "message" at the root, NOT inside a "notification" object.`);
            return false;
        }
    }

    return true;
}

// CLI usage: node schema-validator.js <input|output> <eventName> <jsonString>
const [,, mode, event, data] = process.argv;

if (!mode || !event || !data) {
    console.log('Usage: node schema-validator.js <input|output> <eventName> <jsonString>');
    process.exit(1);
}

const isValid = validate(data, mode, event);
if (!isValid) process.exit(1);
console.log('✅ Validation Success');
process.exit(0);
