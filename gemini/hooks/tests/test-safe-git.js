#!/usr/bin/env node
/**
 * Robust test suite for safe-git-commit hook.
 * Synchronized with Gemini CLI official I/O (mutation at root).
 */
const { execSync } = require('child_process');
const path = require('path');

const HOOK_PATH = path.join(__dirname, '..', 'safe-git-commit.js');

function runHook(input) {
    const inputStr = JSON.stringify(input);
    const output = execSync(`node "${HOOK_PATH}"`, { input: inputStr, encoding: 'utf-8' });
    try {
        return JSON.parse(output);
    } catch (e) {
        console.error("Failed to parse hook output:", output);
        throw e;
    }
}

const testCases = [
    {
        name: "1. Normal commit (allow without change)",
        input: { tool_name: "run_shell_command", tool_input: { command: "git commit -m 'feat: no backticks'" } },
        validate: (out) => out.decision === "allow" && !out.tool_input
    },
    {
        name: "2. Backticks in double quotes (must escape)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: use `ls`"' } },
        validate: (out) => out.tool_input?.command === 'git commit -m "feat: use \\`ls\\`"'
    },
    {
        name: "3. Backticks in single quotes (now escapes for safety)",
        input: { tool_name: "run_shell_command", tool_input: { command: "git commit -m 'feat: use `ls` '" } },
        validate: (out) => out.tool_input?.command === "git commit -m 'feat: use \\`ls\\` '"
    },
    {
        name: "4. Already escaped backticks (must ignore/skip)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: use \\`ls\\`"' } },
        validate: (out) => out.decision === "allow" && !out.tool_input
    },
    {
        name: "5. No space after -m flag (must escape)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m"feat: `code`"' } },
        validate: (out) => out.tool_input?.command === 'git commit -m"feat: \\`code\\`"'
    },
    {
        name: "6. Double backslash before backtick (must escape unescaped backtick)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: \\\\`code` Resort to \\\\\\`code\\`"' } },
        validate: (out) => out.tool_input?.command.includes('\\\\\\`code\\`')
    },
    {
        name: "7. Using --message= syntax (must escape)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit --message="feat: `code`"' } },
        validate: (out) => out.tool_input?.command === 'git commit --message="feat: \\`code\\`"'
    },
    {
        name: "8. Apostrophes inside double quotes (Bug Fix Check)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "I\'m using `ls` and it\'s great"' } },
        validate: (out) => out.tool_input?.command === 'git commit -m "I\'m using \\`ls\\` and it\'s great"'
    },
    {
        name: "9. Not a commit command (must skip)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'ls -la' } },
        validate: (out) => out.decision === "allow" && !out.tool_input
    },
    {
        name: "10. Multi-line commit message (must escape)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: `ls` \n more lines"' } },
        validate: (out) => out.tool_input?.command.includes('\\`ls\\`')
    },
    {
        name: "11. Multiple -m flags (escape all)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "subject `s`" -m "body `b`"' } },
        validate: (out) => out.tool_input?.command.includes('\\`s\\`') && out.tool_input?.command.includes('\\`b\\`')
    },
    {
        name: "12. Backticks with other shell meta-characters",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: `ls` & $(whoami) | rm -rf /"' } },
        validate: (out) => out.tool_input?.command.includes('\\`ls\\`')
    },
    {
        name: "13. Backticks at start and end",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "`start` middle `end`"' } },
        validate: (out) => out.tool_input?.command.startsWith('git commit -m "\\`start\\`') && out.tool_input?.command.endsWith('\\`end\\`"')
    },
    {
        name: "14. Empty backticks (just in case)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: ``"' } },
        validate: (out) => out.tool_input?.command === 'git commit -m "feat: \\`\\`"'
    },
    {
        name: "15. Mixed quote types and backticks (Extreme case)",
        input: { tool_name: "run_shell_command", tool_input: { command: "git commit -m 'Double \" within single and `backtick`'" } },
        validate: (out) => out.tool_input?.command.includes('\\`backtick\\`')
    },
    {
        name: "16. Backslash-backtick sequence (already escaped)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "feat: \\`already escaped\\`"' } },
        validate: (out) => out.decision === "allow" && !out.tool_input
    },
    {
        name: "17. Markdown code blocks inside message",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "Here is some code:\n```javascript\nconst x = 1;\n```"' } },
        validate: (out) => {
            const count = (out.tool_input?.command.match(/\\`/g) || []).length;
            return count === 6;
        }
    },
    {
        name: "18. Commit with -am flag",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -am "hotfix: `urgent`"' } },
        validate: (out) => out.tool_input?.command.includes('\\`urgent\\`')
    },
    {
        name: "19. Environment variable prefix",
        input: { tool_name: "run_shell_command", tool_input: { command: 'LANG=en_US.UTF-8 git commit -m "feat: `ls`"' } },
        validate: (out) => out.tool_input?.command.includes('\\`ls\\`')
    },
    {
        name: "20. Command chaining (Security check)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "done"; ls `pwd`' } },
        validate: (out) => out.tool_input?.command.includes('\\`pwd\\`')
    },
    {
        name: "21. False positive check (git commit in echo)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'echo "git commit -m some-msg"; ls `pwd`' } },
        validate: (out) => out.tool_input?.command.includes('\\`pwd\\`')
    },
    {
        name: "22. Nested backticks in message",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "msg `ls \\`pwd\\``"' } },
        validate: (out) => {
            const cmd = out.tool_input?.command || "";
            return cmd.includes('\\`ls') && cmd.includes('\\`pwd');
        }
    },
    {
        name: "23. Backtick as part of a word (rare but possible)",
        input: { tool_name: "run_shell_command", tool_input: { command: 'git commit -m "don`t do this"' } },
        validate: (out) => out.tool_input?.command.includes('don\\`t')
    }
];

console.log("🧪 Running Synchronized Tests for Gemini safe-git-commit.js...");
let failed = 0;

testCases.forEach((tc, index) => {
    try {
        const output = runHook(tc.input);
        if (tc.validate(output)) {
            console.log(`  ✅ Test ${index + 1}: ${tc.name} Passed`);
        } else {
            console.log(`  ❌ Test ${index + 1}: ${tc.name} Failed`);
            console.log(`     Input Command:  ${tc.input.tool_input.command}`);
            console.log(`     Output Payload: ${JSON.stringify(output)}`);
            failed++;
        }
    } catch (e) {
        console.log(`  ❌ Test ${index + 1}: ${tc.name} Error: ${e.message}`);
        failed++;
    }
});

if (failed > 0) {
    console.log(`\n💔 ${failed} tests failed.`);
    process.exit(1);
} else {
    console.log("\n✨ Gemini safe-git-commit.js verified (Mutation at root)!");
}
