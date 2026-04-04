#!/usr/bin/env node

/**
 * Parses json from stdin and validates it against Gemini CLI's expected schemas.
 * Exits with 0 if valid, 1 if invalid.
 */

const fs = require('fs');

const input = fs.readFileSync(0, 'utf-8').trim();

if (!input) {
  console.error("❌ Schema Validator Error: Empty output. Hooks MUST return a valid JSON object.");
  process.exit(1);
}

let parsed;
try {
  parsed = JSON.parse(input);
} catch (e) {
  console.error(`❌ Schema Validator Error: Output is not valid JSON.\nOutput received: ${input}`);
  process.exit(1);
}

// Allowed root keys
const allowedKeys = ['decision', 'reason', 'systemMessage', 'tool_input', 'suppressOutput', 'retryCount'];

const keys = Object.keys(parsed);
for (const key of keys) {
  if (!allowedKeys.includes(key)) {
     console.error(`❌ Schema Validator Error: Invalid key found: "${key}".`);
     process.exit(1);
  }
}

// If decision is provided, it must be allow or deny.
if (parsed.hasOwnProperty('decision')) {
    if (parsed.decision !== 'allow' && parsed.decision !== 'deny') {
        console.error(`❌ Schema Validator Error: 'decision' must be 'allow' or 'deny'. Got: "${parsed.decision}"`);
        process.exit(1);
    }

    if (parsed.decision === 'deny' && !parsed.reason) {
        console.error("⚠️ Schema Warning: It is highly requested to provide a 'reason' when decision is 'deny'.");
    }
} else {
    // If there is no decision, they might be mutating tool_input
    if (!parsed.hasOwnProperty('tool_input')) {
         console.error(`❌ Schema Validator Error: Missing 'decision' key. Every hook must output at least '{"decision": "allow"}'.`);
         process.exit(1);
    }
}

process.exit(0);
