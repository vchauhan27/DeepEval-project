Running single-turn MCP-Use eval...
✨ You're running DeepEval's latest MCP Use Metric! (using 
dots-studio/dots-3-note-preview:free, strict=False, async_mode=True)...

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric      ┃ Average Score        ┃ Pass Rate                                  ┃ Total    │
│ ━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━ │
│  MCP Use     │ 1.00                 │ 100.00% | passed=1 | failed=0              │ 1        │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================
✓ Done 🎉! View results on 
https://app.confident-ai.com/project/cmtyaseol003amy0tvr2de0bp/test-runs/cmu12cown003vr00tgazdj
j62

Running multi-turn MCP-Use + MCP Task Completion eval...
✨ You're running DeepEval's latest Multi-Turn MCP Use Metric! (using 
dots-studio/dots-3-note-preview:free, strict=False, async_mode=True)...
✨ You're running DeepEval's latest MCP Task Completion Metric! (using 
dots-studio/dots-3-note-preview:free, strict=False, async_mode=True)...
Evaluating 1 test case(s) in parallel ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0:00:42
    🎯 Evaluating test case #0        ━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━  50% 0:00:42Warning: Could not update test run on disk: [Errno 2] No such file or directory:

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                             │
│  ❌ conversational_test_case_0                                                              │
│  ├── Conversation Turns                                                                     │
│  │   ├── User: Give me an MLA citation for a 2021 book titled 'Deep Learning Basics' by     │
│  │   │   Doe, Jane, published by O'Reilly.                                                  │
│  │   ├── Assistant:                                                                         │
│  │   │                                                                                      │
│  │   │   Here is the MLA citation for the book:                                             │
│  │   │                                                                                      │
│  │   │   Doe, Jane. *Deep Learning Basics*. O'Reilly, 2021.                                 │
│  │   ├── User: Now count the words in this sentence: 'Short and to the point.'              │
│  │   ├── Assistant:                                                                         │
│  │   │                                                                                      │
│  │   │   There are 5 words in the sentence "Short and to the point."                        │
│  │   ├── User: Thanks, that's all I needed.                                                 │
│  │   └── Assistant:                                                                         │
│  │                                                                                          │
│  │       You're welcome! Feel free to reach out if you need any more help in the future.    │
│  │       Goodbye!                                                                           │
│  └── Metrics                                                                                │
│       Status ┃ Metric              ┃ Score ┃ Threshold ┃ Reason                             │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Multi-Turn MCP Use  │ 0.00  │ 0.50      │ The score is 0.0 because the       │
│              │                     │       │           │ application failed to achieve      │
│              │                     │       │           │ any successful interactions, as    │
│              │                     │       │           │ no positive reasons were           │
│              │                     │       │           │ recorded and the metric did not    │
│              │                     │       │           │ pass.                              │
│        FAIL  │ MCP Task Completion │ 0.00  │ 0.50      │ The score is 0.0 because the       │
│              │                     │       │           │ application failed to achieve      │
│              │                     │       │           │ any successful outcomes, as        │
│              │                     │       │           │ indicated by the empty list of     │
│              │                     │       │           │ reasons and the absence of a       │
│              │                     │       │           │ success status, implying that no   │
│              │                     │       │           │ interactions were completed        │
│              │                     │       │           │ correctly.                         │
│                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                   ┃ Average Score     ┃ Pass Rate                         ┃ Total   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━ │
│  Multi-Turn MCP Use       │ 0.00              │ 0.00% | passed=0 | failed=1       │ 1       │
│  MCP Task Completion      │ 0.00              │ 0.00% | passed=0 | failed=1       │ 1       │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯

Warning: Could not load test run from disk: [Errno 2] No such file or directory:
'D:\\DeepEval-project\\.deepeval\\.temp_test_run_data.json'

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================
✓ Done 🎉! View results on 
https://app.confident-ai.com/project/cmtyaseol003amy0tvr2de0bp/test-runs/cmu12dus8002eo30tsy4j8
mv9