from typing import Dict
import spacy


def analyze_tos(text: str) -> Dict:
    
	nlp = spacy.load("en_core_web_sm")
	doc = nlp(text)
	print(doc.text)
	for token in doc:
		print(token.text, token.pos, token.dep_)
		
	return {
		"score" : 0,
		"summary": "placeholder analysis - implement real checks",
		"length": len(text),
	}
