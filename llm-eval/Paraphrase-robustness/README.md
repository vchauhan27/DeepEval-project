# Paraphrase Robustness Testing

Tests whether the agent's answer quality stays stable when the same question is asked in different words. This checks robustness of the system, not the judge's reliability (that's repeat-run variance, a different test).

## How It Works

1. For each question in `QUESTIONS`, the judge model generates `NUM_PARAPHRASES` reworded versions with the same meaning.
2. The original question plus all paraphrases are each run through the agent on a fresh `thread_id`.
3. Each answer is scored with `AnswerRelevancyMetric`.
4. Mean and standard deviation of the scores are reported per question.

A high standard deviation means the agent's answer quality is sensitive to surface wording rather than actual meaning, which points to a fragile prompt or retrieval step rather than a genuinely different answer being needed.

## Running

```bash
python paraphrase_robustness.py
```

## Configuration

- `QUESTIONS`: the base questions to test.
- `NUM_PARAPHRASES`: how many reworded versions to generate per question.
- Judge model comes from `config.get_judge_model()`, same as the rest of the eval suite.
