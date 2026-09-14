import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Agent model (used by research-agent/agent.py)
# =============================================================================

agent_model_name = "dots-studio/dots-3-note-preview:free"

# =============================================================================
# Embedding model (used by research-agent/agent.py for Chroma)
# =============================================================================

embedding_model = "baai/bge-m3"

# =============================================================================
# Eval model names
# =============================================================================

eval_model_name_openrouter = "dots-studio/dots-3-note-preview:free"
eval_model_name_gemini     = "gemini-flash-lite-latest"

# Keep the old name as an alias so legacy references don't break
eval_model_name = eval_model_name_openrouter

# =============================================================================
# Judge model factory
# =============================================================================
# Active provider: "gemini"
# Switch to "openrouter" to use the OpenRouter judge instead.
# The OpenRouter option is kept but commented out in the factory below.

JUDGE_PROVIDER = "gemini"   # change to "openrouter" to switch providers


def get_judge_model():
    """
    Return a DeepEval-compatible judge model instance.

    Active provider  : Gemini  (gemini-flash-lite-latest)
    Alternate provider: OpenRouter (dots-studio/dots-3-note-preview:free)
                        — has no structured-output support on the free tier,
                          which causes DAG/GEval/Safety metrics to mis-score.

    To switch providers, change JUDGE_PROVIDER above.
    """
    if JUDGE_PROVIDER == "gemini":
        from deepeval.models import GeminiModel
        return GeminiModel(
            model=eval_model_name_gemini,
            api_key=os.environ.get("GOOGLE_API_KEY"),
            temperature=0,
        )

    # ------------------------------------------------------------------
    # OpenRouter provider (commented out — no structured-output support
    # on free-tier models, leading to unreliable metric scoring)
    # ------------------------------------------------------------------
    # if JUDGE_PROVIDER == "openrouter":
    #     from deepeval.models import OpenRouterModel
    #     return OpenRouterModel(
    #         model=eval_model_name_openrouter,
    #         api_key=os.environ.get("OPENROUTER_API_KEY"),
    #     )

    raise ValueError(f"Unknown JUDGE_PROVIDER: {JUDGE_PROVIDER!r}")