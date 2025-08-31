# Technical Design Rationale

## **`Topic 01`**: Reference Variable Removal in Final Report Writer

### Problem Statement

The `write_final_report` function previously maintained a `reference` variable that concatenated all search result references in sequential order. This approach was fundamentally flawed and contradicted the service's core responsibility.

> **TL;DR**: *References should not be generated at the report-writer level; they must reflect only the sources actually cited in the final content, not all outputs from work agents.*


### Design Issues

#### 1. **Misaligned Responsibility**
The `final_report_writer` service receives a research brief that defines the specific content requirements for the final report. This means the service should synthesize information based on the brief's requirements, not simply aggregate all search results from individual work agents.

#### 2. **Irrelevant Content Inclusion**
Concatenating references from all spawned work agents creates a reference list that may include sources not actually utilized in the final report generation. This violates the principle of reference integrity - references should only include sources that directly contributed to the final content.

#### 3. **Sequential Reference Ordering Problems**
The original approach maintained numerical reference ordering `[1], [2], [3]` based on the order of work agent results, but this ordering becomes meaningless when:
- Not all agent results are used in the final report
- The final report may reference sources in a different order than they were retrieved
- Some sources may be combined or synthesized, making individual attribution unclear

### Technical Implementation Details

#### Previous Problematic Implementation
```python
# In write_final_report function
reference = ""
for i, result in enumerate(state.get("queries_results", [])):
    reference += f"[{i+1}] - {result.title} ({result.url})\n"
```

This approach:
- Assumes all search results are relevant to the final report
- Maintains artificial ordering based on agent execution sequence
- Creates references that may not correspond to actual content usage

### Benefits of This Design Decision

1. **Reference Integrity**: Only sources actually used in the final report are referenced
2. **Logical Ordering**: References can be ordered based on their actual usage in the content
3. **Content Quality**: The final report focuses on brief requirements rather than agent output aggregation

### Impact on System Architecture

This change reinforces the principle that the `final_report_writer` service should be a content synthesis engine that:
- Processes the research brief requirements
- Selectively uses relevant information from search results
- Generates coherent, focused content
- Maintains accurate reference attribution

The removal of the reference concatenation mechanism ensures that the final report's reference list accurately reflects the sources that contributed to the actual content, rather than simply listing all sources that were retrieved during the research process.

---