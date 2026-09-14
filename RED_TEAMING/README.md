# Fault-Injection Red-Teaming

Tests whether the agent degrades gracefully or breaks under adversarial inputs, using [DeepTeam](https://github.com/confident-ai/deepteam), the red-teaming package built on DeepEval.

This is different from paraphrase robustness testing: paraphrasing changes the *surface form* of a normal question, fault injection changes the *input itself* adversarially to try to make the agent misbehave.

## Vulnerability and Attacks

- **`Robustness`** - the vulnerability being probed: does the agent hold its role and instructions under adversarial pressure?
- **`PromptInjection`** - attempts to override the agent's system prompt or instructions from within the user input.
- **`ContextPoisoning`** - attempts to plant false or misleading context that the agent might treat as ground truth.

Both attacks are run against the same `Robustness` vulnerability in a single `red_team()` call, since they're two strategies for the same underlying test, not separate concerns.

## How It Works

1. `model_callback` wraps `agent.invoke`, giving each adversarial call its own `thread_id` so conversations don't leak into each other.
2. `red_team()` generates adversarial prompts using the configured attacks, sends them through `model_callback`, and scores the agent's responses.
3. A `risk_assessment` report is returned showing pass/fail rates per vulnerability.

## Running

```bash
python fault_injection_redteam.py
```

## Notes

- `weight` on each attack controls how often that attack strategy is sampled relative to the others - it does not affect scoring.
- This only probes *behavior* (did the agent comply with something it shouldn't have). It does not check tool-definition provenance (e.g. whether a tool's definition silently changed) - that's a separate concern, sometimes called "rug-pull" testing.
