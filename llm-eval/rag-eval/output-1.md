Q: What embedding model is used in this research agent, and how many dimensions does it produce?
Tools called: ['retrieve_documents']
Retrieved chunks: 1

✨ You're running DeepEval's latest Answer Relevancy Metric! (using 
gemini-flash-lite-latest (Gemini), strict=False, async_mode=False)...
✨ You're running DeepEval's latest Faithfulness Metric! (using 
gemini-flash-lite-latest (Gemini), strict=False, async_mode=False)...
✨ You're running DeepEval's latest Contextual Relevancy Metric! (using 
gemini-flash-lite-latest (Gemini), strict=False, async_mode=False)...
✨ You're running DeepEval's latest Contextual Precision Metric! (using 
gemini-flash-lite-latest (Gemini), strict=False, async_mode=False)...
✨ You're running DeepEval's latest Contextual Recall Metric! (using
gemini-flash-lite-latest (Gemini), strict=False, async_mode=False)...
Direct use of automatic function calling (AFC) in Models.generate_content is not      
recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct 
use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend
to use AFC in Chat.send_message_stream.

╭────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                     │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 5 metrics)                                                  │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                  │
│                                                                                    │
│  Metric                 ┃ Average Score  ┃ Pass Rate                      ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Answer Relevancy       │ 0.75           │ 100.00% | passed=1 | failed=0  │ 1      │
│  Faithfulness           │ 1.00           │ 100.00% | passed=1 | failed=0  │ 1      │
│  Contextual Relevancy   │ 1.00           │ 100.00% | passed=1 | failed=0  │ 1      │
│  Contextual Precision   │ 1.00           │ 100.00% | passed=1 | failed=0  │ 1      │
│  Contextual Recall      │ 1.00           │ 100.00% | passed=1 | failed=0  │ 1      │
╰────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.