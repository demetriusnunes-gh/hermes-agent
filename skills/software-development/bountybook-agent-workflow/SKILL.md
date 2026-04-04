---
name: bountybook-agent-workflow
description: Complete workflow for interacting with BountyBook agent bounty platform - wallet generation, authentication, job claiming, work submission, and payment verification
category: software-development
---
# BountyBook Agent Workflow

## Trigger Conditions
When user wants to:
- Attempt a job posted on BountyBook (or similar agent bounty platform)
- Earn cryptocurrency by having an AI agent complete tasks
- Test autonomous agent capabilities on bounty platforms
- Need a reusable pattern for wallet-signature authenticated API interactions

## Overview
This skill provides a complete workflow for interacting with BountyBook:
1. Generate Ethereum wallet (private key + address)
2. Authenticate via wallet signature nonce
3. Find and claim open jobs
4. Complete work (can be customized)
5. Submit output for verification
6. Check verification status and payment

The workflow handles common pitfalls like nonce expiration, already-claimed jobs, and verification delays.

## Prerequisites
- Node.js installed (for wallet generation and signing)
- Access to BountyBook API (https://api.bountybook.ai)
- Understanding that this is experimental software - only use funds you can afford to lose

## Step-by-Step Instructions

### 1. Generate Wallet
```bash
# Generate random Ethereum private key and address
node -e "console.log('Private key: 0x'+require('crypto').randomBytes(32).toString('hex'))"
node -e "const { ethers } = require('ethers'); const wallet = new ethers.Wallet('YOUR_PRIVATE_KEY'); console.log('Address:', wallet.address)"
```

### 2. Authenticate
```bash
# Get nonce
curl -s "https://api.bountybook.ai/auth/nonce?address=YOUR_ADDRESS"

# Sign nonce with private key (using Node.js with ethers)
# Save this as sign.js:
const { ethers } = require('ethers');
const nonce = "NONCE_FROM_STEP_1";
const privateKey = "YOUR_PRIVATE_KEY";
const wallet = new ethers.Wallet(privateKey);
wallet.signMessage(nonce).then(signature => console.log(signature));

# Verify to get token
curl -s -X POST https://api.bountybook.ai/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"address": "YOUR_ADDRESS", "signature": "SIGNATURE_FROM_STEP_2"}'
```

### 3. Find Unclaimed Job
```bash
curl -s "https://api.bountybook.ai/jobs?status=open&limit=20"
# Look for jobs with "executor_address": null
```

### 4. Claim Job
```bash
curl -s -X POST "https://api.bountybook.ai/jobs/JOB_ID/claim" \
  -H "Authorization: Bearer YOUR_TOKEN_FROM_STEP_2" \
  -H "Content-Type: application/json" \
  -d '{"executorAddress": "YOUR_ADDRESS"}'
```

### 5. Complete Work
(This step is task-dependent - examples):
- **Writing**: Create story, document, etc.
- **Code**: Write script, fix bug, implement feature
- **Data**: Research, transform, extract information
- **Monitoring**: Set up checks, collect data over time

Save output to file for submission.

### 6. Submit Output
```bash
# For plain text/data (outputData method)
curl -s -X POST "https://api.bountybook.ai/jobs/JOB_ID/submit" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"executorAddress": "YOUR_ADDRESS", "outputData": {"key": "value"}}'

# For file/IPFS (outputCID method)
# First upload to IPFS, then submit CID
```

### 7. Check Verification & Payment
```bash
# Check job status
curl -s "https://api.bountybook.ai/jobs/JOB_ID"

# Check agent earnings
curl -s "https://api.bountybook.ai/agents/YOUR_ADDRESS"
curl -s "https://api.bountybook.ai/agents/YOUR_ADDRESS/timeline"

# Verification typically completes within minutes
# Payment appears in agent profile once verified
```

## Common Pitfalls and Solutions

### Pitfall: "Invalid or expired nonce/signature"
**Solution**: Nonces expire quickly. Always get a fresh nonce immediately before signing.

### Pitfall: Job already claimed
**Solution**: Check `executor_address` is null before claiming. If claimed, check queue or find another job.

### Pitfall: Verification stuck or failed
**Solution**: 
- Check job endpoint for verification_result
- Read failure reason carefully
- For creative work: ensure it genuinely matches requirements
- For code: ensure it passes the test script provided in spec
- You can re-submit improved work before deadline

### Pitfall: Payout shows failed but earnings appear
**Solution**: 
- Trust agent profile/timeline over job endpoint payout status
- There may be display delays in the job endpoint
- Check Basescan for actual USDC transfer to your address on Base

### Pitfall: Need ETH for gas on Base
**Solution**: 
- Claiming and submitting jobs is FREE (no gas)
- Only needed if you want to transfer USDC out
- Very small amounts needed (~$0.0001 per tx)
- Use Base bridge or exchange withdrawals

## Verification of Success
- Job status changes to `verified`
- Agent profile shows increased `total_earned`
- Timeline shows completed job with earnings
- Success rate updates

## Safety Notes
- BountyBook is experimental proof-of-concept
- Smart contracts and oracle unaudited
- Platform explicitly states: "do not deposit funds you cannot afford to lose"
- Treat as educational/experimental, not guaranteed income
- Oracle verification is probabilistic (92% confidence example seen)
- You assume all risk for funds and outcomes

## Customization Notes
- Work completion step (5) can be replaced with delegated AI agent work (using claude-code, codex, etc. skills)
- For automated looping: add job scanning, claiming, working, submitting cycle
- Can adapt for other similar platforms with wallet-signature auth

## Example: Snail Love Story (from actual session)
- Job: "Write a love story about snails" (5 USDC)
- Work: 2,327 character original story about snails Luna and Sol
- Verification: Passed with 92% AI confidence ("genuine, well-crafted love story...")
- Result: 5 USDC credited to agent profile

## Related Skills
- `claude-code` / `codex` / `opencode` - for delegating coding work
- `hermes-agent` - for spawning subagents to do work
- `browser-research-bot-workarounds` - for research-intensive jobs
- `google-workspace` - for Docs/Sheets output

## Reference
BountyBook API docs: https://api.bountybook.ai/docs
Terms of Service: https://www.bountybook.ai/terms