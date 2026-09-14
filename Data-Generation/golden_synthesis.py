from pathlib import Path
from deepeval.synthesizer import Synthesizer

BASE_DIR = Path(__file__).resolve().parent
# Documents live in research-agent/data/, not inside Data-Generation/
DATA_DIR = BASE_DIR.parent / "research-agent" / "data"
OUTPUT_DIR = BASE_DIR / "synthetic_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # create if not present

document_paths = [str(path) for path in DATA_DIR.glob("*.txt")]

if not document_paths:
    raise RuntimeError(f"No .txt files found in {DATA_DIR}")

synthesizer = Synthesizer()

single_turn_goldens = synthesizer.generate_goldens_from_docs(
    document_paths=document_paths,
    include_expected_output=True,
)

synthesizer.save_as(
    file_type="json",
    directory=str(OUTPUT_DIR),
    file_name="single_turn_goldens",
)

conversational_goldens = synthesizer.generate_conversational_goldens_from_docs(
    document_paths=document_paths,
    include_expected_outcome=True,
)

synthesizer.save_as(
    file_type="json",
    directory=str(OUTPUT_DIR),
    file_name="conversational_goldens",
)

print(f"Single-turn goldens generated: {len(single_turn_goldens)}")
print(f"Conversational goldens generated: {len(conversational_goldens)}")
print(f"Saved to: {OUTPUT_DIR}")
