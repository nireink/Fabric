# Phase 1 Classification Contract v1.0

CONTRACT_ID=PHASE-1-CLASSIFICATION-CONTRACT-v1.0
CATEGORIES_COUNT=12
MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=0.90
SAFETY_EXCLUSION_OVERRIDES_DUPLICATE_STATUS=YES
SAFETY_EXCLUSION_OVERRIDES_PERSISTENCE=YES
LOW_CONFIDENCE_OVERRIDES_FINAL_CLASSIFICATION=YES
ARTIFICIAL_CONFIDENCE_INCREASE=PROHIBITED
SOURCE_CONTENT_HASHING_STAGE=EACH_CLASSIFICATION_BATCH
COPY_AUTHORIZATION=NO
MOVE_AUTHORIZATION=NO
DELETE_AUTHORIZATION=NO

SECRET_VALUE_PERSISTENCE=PROHIBITED
AUTHENTICATION_VALUE_PERSISTENCE=PROHIBITED
PERSONAL_VALUE_PERSISTENCE=PROHIBITED
PRIVATE_KEY_CONTENT_PERSISTENCE=PROHIBITED
COOKIE_OR_SESSION_VALUE_PERSISTENCE=PROHIBITED
CONNECTION_STRING_CREDENTIAL_PERSISTENCE=PROHIBITED

SAFE_SENSITIVE_EVIDENCE=SENSITIVE_INDICATOR_DETECTED,SENSITIVE_INDICATOR_TYPE,VALUE_REDACTED

## 1. EXCLUDE_SECRET
DEFINITION=Operational secrets, private keys, API keys, tokens, passwords, or credential-bearing connection strings.
POSITIVE_CRITERIA=Verified secret indicator in batch content inspection.
NEGATIVE_CRITERIA=Authentication state without a standalone secret is handled by EXCLUDE_AUTHENTICATION.
PRECEDENCE=1
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Persist category and safe indicator type only; redact value.
DUPLICATE_BEHAVIOR=Safety is evaluated before duplicate status.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Any unresolved risk routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Safe indicator category, redaction flag, confidence, and rationale without value.

## 2. EXCLUDE_AUTHENTICATION
DEFINITION=Cookies, sessions, credential stores, OAuth tokens, and access state.
POSITIVE_CRITERIA=Verified authentication or session material.
NEGATIVE_CRITERIA=Standalone operational secrets use EXCLUDE_SECRET.
PRECEDENCE=2
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Never persist authentication values.
DUPLICATE_BEHAVIOR=Safety is evaluated before duplicate status.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Any unresolved authentication risk routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Safe authentication category, redaction flag, confidence, and value-free rationale.

## 3. EXCLUDE_PERSONAL_DATA
DEFINITION=Personal data unnecessary for legitimate durable technical knowledge.
POSITIVE_CRITERIA=Unnecessary names, emails, addresses, phones, or personal identifiers.
NEGATIVE_CRITERIA=Necessary technical context with safely minimized personal data requires separate evidence.
PRECEDENCE=3
CONFIDENCE_REQUIREMENT=MINIMUM_CONFIDENCE=0.90; lower confidence requires manual review.
SENSITIVITY_BEHAVIOR=Never persist detected personal values.
DUPLICATE_BEHAVIOR=Safety is evaluated before duplicate status.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Doubt or confidence below 0.90 routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Personal-data category, redaction flag, confidence, and value-free rationale.

## 4. EXCLUDE_REGENERABLE_CACHE
DEFINITION=Regenerable temporary or cache artifacts without durable context.
POSITIVE_CRITERIA=Artifact can be recreated automatically and contains no unique durable knowledge.
NEGATIVE_CRITERIA=Unique durable context is not a regenerable cache.
PRECEDENCE=4
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Apply sensitive categories first.
DUPLICATE_BEHAVIOR=Duplicate analysis follows safety and this exclusion.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Unclear regenerability routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Regeneration basis, confidence, and safe rationale.

## 5. EXCLUDE_BUILD_OR_DEPENDENCY
DEFINITION=Downloadable dependencies, build outputs, and reproducible generated artifacts.
POSITIVE_CRITERIA=Known dependency or reproducible build output.
NEGATIVE_CRITERIA=Source-authored durable context is not excluded solely by location.
PRECEDENCE=5
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Apply sensitive categories first.
DUPLICATE_BEHAVIOR=Duplicate analysis follows safety and this exclusion.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Unclear provenance routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Artifact role, reproducibility basis, confidence, safe rationale.

## 6. EXCLUDE_TELEMETRY
DEFINITION=Telemetry, metrics, automated diagnostics, and operational logs without durable context.
POSITIVE_CRITERIA=Automatically emitted operational observations lacking durable knowledge.
NEGATIVE_CRITERIA=Durable incident decisions or architecture evidence are not telemetry-only.
PRECEDENCE=6
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Apply sensitive and personal-data categories first.
DUPLICATE_BEHAVIOR=Duplicate analysis follows safety and this exclusion.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Potential durable value routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Telemetry basis, confidence, and value-free rationale.

## 7. EXCLUDE_IRRELEVANT
DEFINITION=Content without material relation to GYPPORT, its tracks, decisions, architecture, or agent collaboration.
POSITIVE_CRITERIA=No material relation after authorized inspection.
NEGATIVE_CRITERIA=Unclear relation is not sufficient for exclusion.
PRECEDENCE=7
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Apply all safety exclusions first.
DUPLICATE_BEHAVIOR=Duplicate analysis follows safety and this exclusion.
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Unclear relevance routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Relevance assessment, confidence, and safe rationale.

## 8. DUPLICATE_REFERENCE_ONLY
DEFINITION=Non-sensitive content hash-identical to an earlier canonical entry.
POSITIVE_CRITERIA=SHA-256 equals the first safe entry in frozen order.
NEGATIVE_CRITERIA=Sensitive duplicates retain their safety exclusion.
PRECEDENCE=8
CONFIDENCE_REQUIREMENT=Exact hash match and safety determination required.
SENSITIVITY_BEHAVIOR=Never override a safety exclusion.
DUPLICATE_BEHAVIOR=First safe frozen-order entry is canonical; later safe entries are references.
DESTINATION_KEY=REFERENCE_ONLY
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Any safety uncertainty routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Safe canonical identifier, hash status, confidence, no content fragment.

## 9. PERSIST_TRACK_SPECIFIC
DEFINITION=Durable knowledge applicable exclusively to the current track.
POSITIVE_CRITERIA=Verified durable and track-specific technical or decision context.
NEGATIVE_CRITERIA=Reusable multi-track context uses PERSIST_SHARED_CONTEXT.
PRECEDENCE=9
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Safety exclusions override persistence.
DUPLICATE_BEHAVIOR=Duplicate references are not persistence candidates.
DESTINATION_KEY=TRACK_CONTEXT_CANDIDATE
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Scope ambiguity routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Safe context type, track relevance, confidence, value-free rationale.

## 10. PERSIST_SHARED_CONTEXT
DEFINITION=Durable knowledge reusable by multiple tracks, agents, or GYPPORT components.
POSITIVE_CRITERIA=Verified reusable cross-track technical or decision context.
NEGATIVE_CRITERIA=Track-exclusive context uses PERSIST_TRACK_SPECIFIC.
PRECEDENCE=10
CONFIDENCE_REQUIREMENT=Final at confidence >=0.90; otherwise manual review.
SENSITIVITY_BEHAVIOR=Safety exclusions override persistence.
DUPLICATE_BEHAVIOR=Duplicate references are not persistence candidates.
DESTINATION_KEY=SHARED_CONTEXT_CANDIDATE
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Reuse ambiguity routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Safe context type, reuse basis, confidence, value-free rationale.

## 11. KEEP_UNCLASSIFIED
DEFINITION=Format or available evidence prevents technical evaluation without immediate sensitive risk.
POSITIVE_CRITERIA=Evidence is insufficient because format cannot be evaluated.
NEGATIVE_CRITERIA=Must not replace manual review when risk, ambiguity, or low confidence exists.
PRECEDENCE=11
CONFIDENCE_REQUIREMENT=Use only when format/evidence is unavailable and no unresolved risk exists.
SENSITIVITY_BEHAVIOR=Any sensitive risk routes to manual review or safety exclusion.
DUPLICATE_BEHAVIOR=Duplicate status requires content hash and cannot be assumed.
DESTINATION_KEY=UNCLASSIFIED_HOLD
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=Risk or material ambiguity routes to manual review.
SAFE_EVIDENCE_REQUIREMENTS=Format limitation, evidence limitation, and safe rationale.

## 12. MANUAL_OWNER_REVIEW_REQUIRED
DEFINITION=Fail-closed gate for unresolved conflicts, sensitive risk, material ambiguity, or confidence below 0.90.
POSITIVE_CRITERIA=CONFIDENCE_LT_0.90, AMBIGUITY_NOT_RESOLVED, SENSITIVE_RISK_NOT_RESOLVED, or non-unique precedence.
NEGATIVE_CRITERIA=Not used when a unique category is supported at confidence >=0.90 without unresolved risk.
PRECEDENCE=FAIL_CLOSED_GATE
CONFIDENCE_REQUIREMENT=Required whenever final confidence would be below 0.90.
SENSITIVITY_BEHAVIOR=Never persist the sensitive value causing review.
DUPLICATE_BEHAVIOR=Prevents unsafe duplicate or persistence conclusions.
DESTINATION_KEY=OWNER_REVIEW_QUEUE
COPY_AUTHORIZATION=NO
AMBIGUITY_BEHAVIOR=This category is the mandatory ambiguity behavior.
SAFE_EVIDENCE_REQUIREMENTS=Safe issue category, redaction flag, confidence, and value-free rationale.

## Global duplicate and destination rules
SAFETY_EVALUATED_BEFORE_DUPLICITY=YES
FIRST_SAFE_ENTRY_IN_FROZEN_ORDER_IS_CANONICAL=YES
LATER_SAFE_IDENTICAL_ENTRIES=DUPLICATE_REFERENCE_ONLY
PERSIST_TRACK_SPECIFIC=TRACK_CONTEXT_CANDIDATE
PERSIST_SHARED_CONTEXT=SHARED_CONTEXT_CANDIDATE
MANUAL_OWNER_REVIEW_REQUIRED=OWNER_REVIEW_QUEUE
KEEP_UNCLASSIFIED=UNCLASSIFIED_HOLD
DUPLICATE_REFERENCE_ONLY=REFERENCE_ONLY
ALL_EXCLUDE_CATEGORIES=NO_DESTINATION