# BAAD Rule Query Note

Prefer the `baad-rule-update` skill for BAAD / BAAQMD rule questions.

Reason:
- it checks the BAAQMD website for rule updates,
- downloads updated rule PDFs,
- regenerates rule JSON,
- rebuilds the Markdown corpus and RAG index,
- then runs the query against the refreshed rule corpus.

Primary command:

`python scripts/baaqmd_rule_update.py query --question "<QUESTION>"`

Use the generic `agentic-rag-indexer` directly only if you explicitly do **not** want a rule refresh first.

When answering BAAD / BAAQMD rule questions, also check whether key terms are formally defined:
- first in the definitions section of the same rule;
- then in `Regulation 1`, if relevant.

If a term is defined and that definition affects interpretation, include the definition text explicitly in the answer.

If the answer depends on a specific cited rule section, excerpt the relevant rule language in addition to summarizing it.

For any question about `Regulation 2`, `NSR`, `permitting`, or `New Source Review`, also consult the local `NSR guidance` folder. 
- Treat the rule text as primary authority.
- Use the NSR guidance documents as interpretive / procedural support. This can be done using `agentic-rag-indexer` from the index.pkl stored in `NSR guidance\.rag_cache\` folder.
- Additionally consider `Barr Approach.docx` as an overall summary of the appropriate appraoch. 
