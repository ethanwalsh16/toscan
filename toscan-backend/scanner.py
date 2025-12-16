"""Heuristic spaCy-based scanner for common TOS clauses.

Start small with a few high-signal patterns using spaCy's Matcher and
PhraseMatcher, plus simple sentence-level heuristics. This is designed
to be easy to extend with more rules over time.
"""
from typing import Dict, List, Tuple

import spacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.language import Language


def _load_nlp() -> Tuple["Language", bool]:
	"""Load an English pipeline, preferring en_core_web_sm.

	Returns a tuple (nlp, has_model) where has_model indicates if a
	trained model with tagger/lemmatizer is available. If not, falls
	back to a blank pipeline with a sentencizer, which still supports
	tokenization and sentence segmentation for simpler rules.
	"""
	has_model = True
	try:
		nlp = spacy.load("en_core_web_sm")
	except Exception:
		nlp = spacy.blank("en")
		if "sentencizer" not in nlp.pipe_names:
			nlp.add_pipe("sentencizer")
		has_model = False
	return nlp, has_model


NLP, HAS_MODEL = _load_nlp()


def _build_matchers(nlp: "Language") -> Tuple[Matcher, PhraseMatcher]:
	matcher = Matcher(nlp.vocab)
	pmatcher = PhraseMatcher(nlp.vocab, attr="LOWER")

	# 1) Arbitration clauses
	matcher.add(
		"ARBITRATION",
		[
			[{"LOWER": {"IN": ["binding", "mandatory"]}}, {"LOWER": "arbitration"}],
			[{"LOWER": "arbitration"}],
			[{"LEMMA": "arbitrate"}] if HAS_MODEL else [{"LOWER": "arbitrate"}],
		],
	)

	# 2) Class action waiver
	pmatcher.add(
		"CLASS_ACTION",
		[
			nlp.make_doc("class action"),
			nlp.make_doc("class arbitration"),
			nlp.make_doc("collective action"),
			nlp.make_doc("waiver of class action"),
		],
	)

	# 3) Limitation of liability
	pmatcher.add(
		"LIMITATION_OF_LIABILITY",
		[
			nlp.make_doc("limitation of liability"),
			nlp.make_doc("liability is limited"),
			nlp.make_doc("maximum liability"),
			nlp.make_doc("to the fullest extent permitted by law"),
		],
	)

	# 4) Unilateral changes to terms
	# e.g., "we may modify/change/update/amend these terms at any time"
	verbs = ["modify", "change", "update", "amend", "revise"]
	for v in verbs:
		pattern = [
			{"LOWER": {"IN": ["we", "company", "provider"]}},
			{"LOWER": "may"},
			({"LEMMA": v} if HAS_MODEL else {"LOWER": v}),
		]
		matcher.add("UNILATERAL_CHANGES", [pattern])

	# 5) Data sharing/sale with third parties (heuristic via phrases)
	pmatcher.add(
		"DATA_SHARING",
		[
			nlp.make_doc("share your data"),
			nlp.make_doc("share your personal information"),
			nlp.make_doc("sell your data"),
			nlp.make_doc("sell your personal information"),
			nlp.make_doc("third-party partners"),
			nlp.make_doc("third party partners"),
		],
	)

	return matcher, pmatcher


MATCHER, PHRASE_MATCHER = _build_matchers(NLP)


def _collect_matches(doc, matcher: Matcher, pmatcher: PhraseMatcher) -> List[Dict]:
	hits: List[Dict] = []

	for rule_id, start, end in matcher(doc):
		label = doc.vocab.strings[rule_id]
		span = doc[start:end]
		sent = span.sent.text if span.sent is not None else span.text
		hits.append(
			{
				"label": label,
				"text": span.text,
				"start": span.start_char,
				"end": span.end_char,
				"sentence": sent,
			}
		)

	for rule_id, start, end in PHRASE_MATCHER(doc):
		label = doc.vocab.strings[rule_id]
		span = doc[start:end]
		sent = span.sent.text if span.sent is not None else span.text
		hits.append(
			{
				"label": label,
				"text": span.text,
				"start": span.start_char,
				"end": span.end_char,
				"sentence": sent,
			}
		)

	return hits


def _score(hits: List[Dict]) -> Dict:
	weights = {
		"ARBITRATION": 5,
		"CLASS_ACTION": 6,
		"LIMITATION_OF_LIABILITY": 5,
		"UNILATERAL_CHANGES": 4,
		"DATA_SHARING": 3,
	}
	per_label = {}
	total = 0
	for h in hits:
		lbl = h["label"]
		per_label[lbl] = per_label.get(lbl, 0) + 1
		total += weights.get(lbl, 1)

	risk = min(100, int(total * 5))
	return {"risk_score": risk, "by_category": per_label}


def analyze_tos(text: str) -> Dict:
	"""Analyze TOS text and return a structured score object."""
	if not isinstance(text, str):
		text = str(text)

	doc = NLP(text)
	hits = _collect_matches(doc, MATCHER, PHRASE_MATCHER)
	score = _score(hits)
	result = {
		**score,
		"matches": hits,
		"meta": {
			"length": len(text),
			"model": "en_core_web_sm" if HAS_MODEL else "blank",
		},
	}
	return result
