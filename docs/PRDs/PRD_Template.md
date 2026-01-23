# Product Requirements Document: [Feature Name]

## Version History

| Version | Date       | Author  | Changes |
|---------|------------|---------|---------|
| v1.0    | YYYY-MM-DD | [Name]  | Initial PRD draft |

---

## 1. Feature Name & Executive Summary

**Feature Name:** [Feature Name]

**Summary:**  
[Brief 2-3 sentence description of what this feature does, the problem it solves, and who benefits]

---

## 2. Business Justification / Problem Statement

### Current Problem
[Describe the current pain points or limitations that this feature addresses]

### Business Impact
- [Quantified impact if possible - e.g., "Reduces analysis time by X%"]
- [User impact - e.g., "Enables analysts to..."]
- [Stakeholder concerns addressed]

### User Stories
- **As an** [analyst/stakeholder], **I need to** [capability], **so that** [benefit]
- **As an** [user type], **I need to** [capability], **so that** [benefit]

### Success Criteria
- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]

---

## 3. Inputs

### Data Sources

#### Input Source 1: [Workbook/File Name]
- **Sheet/Location:** [Sheet name or file path]
- **Required Fields:**
  - `field_name` (data type, validation rules)
    - Description: [What this field represents]
    - Example values: [Examples]
  - `field_name_2` (data type, validation rules)
    - Description: [What this field represents]
    - Example values: [Examples]
- **Validation Rules:**
  - [Validation rule 1]
  - [Validation rule 2]

#### Input Source 2: [Workbook/File Name]
- **Sheet/Location:** [Sheet name or file path]
- **Required Fields:**
  - `field_name` (data type, validation rules)
- **Optional Fields:**
  - `optional_field` (data type, default value)

### Assumptions
- [Assumption 1 about input data]
- [Assumption 2 about input data]

---

## 4. Outputs

### Modified Files
#### File 1: [Path/to/output/file.csv]
- **New Columns:**
  - `new_column_name` (data type)
    - Description: [What this column contains]
    - Formula/Logic: [How it's calculated]
- **Modified Columns:**
  - `existing_column` 
    - Change: [What changes to existing data]

### New Files
#### File 1: [Path/to/new/file.csv]
- **Purpose:** [Why this file is created]
- **Columns:**
  - `column_1` (data type) - Description
  - `column_2` (data type) - Description
  - `column_3` (data type) - Description
- **Update Frequency:** [When this file is regenerated]

### Output Validation
- [How to verify outputs are correct]
- [Expected ranges or patterns in output data]

---

## 5. Technical Specifications

### Algorithm / Logic Description

#### High-Level Flow
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

#### Detailed Logic

**Step 1: [Name]**
```
Pseudocode or formula:
  IF condition THEN
    perform calculation
  ELSE
    alternative calculation
```
- **Inputs:** [What data this step uses]
- **Outputs:** [What this step produces]
- **Edge Cases:** [Special scenarios to handle]

**Step 2: [Name]**
```
Formula:
  Result = Input_A × Factor + Adjustment
  
  Where:
    Factor = lookup from table X
    Adjustment = conditional based on Y
```

### Data Structures
- **DataFrame:** `df_name`
  - Key columns: [column list]
  - Index: [what serves as index]
  - Shape expectations: [approximate rows × columns]

### Integration Points
- **Notebook/Module:** `XXX_Notebook_Name.ipynb`
  - **Cell/Function:** Cell XX, function `function_name()`
  - **Modification Type:** [Insert new logic / Modify existing / Add new cell]
  - **Dependencies:** Requires completion of [other feature/task]

### Performance Considerations
- **Expected Runtime:** [Estimate with typical data size]
- **Memory Usage:** [Approximate memory footprint]
- **Optimization Notes:** [Any performance concerns or optimizations needed]

---

## 6. User Interface / Workflow Changes

### Input Workflow Changes

**Current Workflow:**
1. [Current step 1]
2. [Current step 2]

**New Workflow:**
1. [Modified step 1]
2. [New step added]
3. [Modified step 3]

### New Fields in Input Templates

**Workbook:** `workpapers.xlsx` (each measure sheet)
- **Row/Field:** [row number/field name]
  - **Type:** Dropdown / Numeric / Text
  - **Validation:** [Validation rule]
  - **Help Text:** [User guidance]
  - **Default Value:** [If applicable]

### Output Visualization Changes

**New Report/Chart in:** `060_Reporting.ipynb`
- **Chart Type:** [Bar chart / Line graph / Heatmap]
- **Purpose:** [What insight this provides]
- **Location:** [Cell number or section]

---

## 7. Tests & Validation

### Unit Tests

#### Test 1: [Test Name]
- **Given:** [Initial conditions/input data]
- **When:** [Action or function called]
- **Then:** [Expected result]
- **Location:** [Where test code lives]

#### Test 2: [Test Name]
- **Given:** [Initial conditions]
- **When:** [Action]
- **Then:** [Expected result]

### Integration Tests

#### Test 3: [End-to-End Test Name]
- **Input:** [Real or realistic test dataset]
- **Expected Output:** [Specific file/results expected]
- **Validation:** [How to verify correctness]
  - Compare to: [Baseline/historical data]
  - Tolerance: [Acceptable variance]

### Edge Cases

#### Edge Case 1: [Scenario Name]
- **Condition:** [What makes this an edge case]
- **Expected Behavior:** [How system should handle it]
- **Test Data:** [How to replicate]

#### Edge Case 2: [Scenario Name]
- **Condition:** [Description]
- **Expected Behavior:** [Handling]

### Performance Tests

#### Test 4: [Performance Test Name]
- **Measure:** [Runtime / Memory usage]
- **Acceptable Threshold:** [X seconds / Y MB]
- **Test Dataset:** [Size and characteristics]

### Validation Checklist
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Edge cases handled
- [ ] Performance within acceptable limits
- [ ] Output validation checks pass
- [ ] Documentation updated

---

## 8. Dependencies & Blockers

### Code Dependencies
- **Depends On:**
  - [Feature/Issue #X] - [Brief description]
    - Status: [Not Started / In Progress / Complete]
    - Impact: [What this feature needs from it]
  - [Library/Package] version [X.Y.Z]
    - Required for: [Functionality]

### Data Dependencies
- **Required Data:**
  - [Data source name]
    - Owner: [Person/Team]
    - ETA: [Date]
    - Status: [Status]
- **Data Quality Requirements:**
  - [Requirement 1]
  - [Requirement 2]

### External Dependencies
- **Stakeholder Approvals:**
  - [Decision/assumption that needs approval]
    - Approver: [Name]
    - Target Date: [Date]
    - Status: [Pending / Approved / Rejected]

### Current Blockers

#### BLOCKER 1: [High/Medium/Low] - [Blocker Title]
- **Description:** [What is blocked and why]
- **Impact:** [How this affects the feature]
- **Owner:** [Who is responsible for resolution]
- **Mitigation:** [Workaround or plan to unblock]
- **Target Resolution:** [Date]

#### BLOCKER 2: [Priority] - [Blocker Title]
- **Description:** [Details]
- **Impact:** [Impact]
- **Owner:** [Owner]

---

## 9. Implementation Plan & Status

### Implementation Phases

#### Phase 1: [Phase Name] (Week 1)
**Status:** ⏳ Not Started / 🔄 In Progress / ✅ Complete

**Tasks:**
- [ ] [Task 1 description]
  - Owner: [Name]
  - ETA: [Date]
- [ ] [Task 2 description]
  - Owner: [Name]
  - ETA: [Date]

**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

#### Phase 2: [Phase Name] (Week 2)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]

**Blockers:**
- Blocked by: [Phase 1 completion / External dependency]

#### Phase 3: [Phase Name] (Week 3)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]

#### Phase 4: [Phase Name] (Week 4)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]

### Overall Status Dashboard

**Overall Completion:** 0%  
**Risk Level:** 🟢 Low / 🟡 Medium / 🔴 High  
**Current Phase:** [Phase name]  
**Next Milestone:** [Milestone] on [Date]

### Recent Updates

**YYYY-MM-DD** - [Update description]

---

## 10. Open Questions & Decisions

### Open Questions

**Q1: [Question]**
- **Context:** [Why this question matters]
- **Options:** 
  - Option A: [Description]
  - Option B: [Description]
- **Decision Needed By:** [Date]
- **Owner:** [Who will decide]
- **Status:** 🔴 Open / 🟡 Under Discussion / 🟢 Resolved

**Q2: [Question]**
- **Context:** [Context]
- **Options:**
  - [Option list]
- **Decision Needed By:** [Date]

### Decisions Made

**✅ D1: [Decision Title]** (Date: [YYYY-MM-DD])
- **Decision:** [What was decided]
- **Rationale:** [Why this was chosen]
- **Alternatives Considered:** [What else was evaluated]
- **Approved By:** [Name/Team]
- **Impact:** [How this affects implementation]

**✅ D2: [Decision Title]** (Date: [YYYY-MM-DD])
- **Decision:** [Decision]
- **Rationale:** [Reasoning]

---

## 11. Related Work & References

### Related Features
- **[Feature Name]** (Issue #XX, PRD tag: prd-feature-vX.X)
  - Relationship: [How they relate - shares data structures / potential conflict / builds upon]
  - Coordination: [What needs to be coordinated]

### References & Research
- [Document/Study Name] - [Link or location]
  - Relevance: [Why this is referenced]
- [Internal Documentation] - [Path or link]
  - Key Findings: [Summary]

### Codebase References
- **File:** [path/to/file.ipynb]
  - **Cells:** [Cell numbers]
  - **Description:** [Existing logic this relates to]

### Future Enhancements (Out of Scope)

**Phase 2 Candidates:**
- [Enhancement 1]: [Brief description]
- [Enhancement 2]: [Brief description]

**Deferred Items:**
- [Item]: [Why deferred and when to revisit]

---

## 12. Stakeholder Communication

### Review Schedule
- **Design Review:** [Date] with [Team/People]
- **Technical Review:** [Date] with [Team/People]  
- **Stakeholder Demo:** [Date] with [Team/People]

### Communication Plan
- **Weekly Updates:** [To whom, what format]
- **Blocker Escalation:** [To whom, when]
- **Completion Notification:** [To whom]

---

## Appendix

### Glossary
- **Term 1:** Definition
- **Term 2:** Definition

### Examples
[Include concrete examples, sample data, or screenshots if helpful]

### Change Log (Detailed)
- **v1.0 (YYYY-MM-DD):** Initial PRD created
  - Added all sections
  - Identified key dependencies
  - Created initial implementation plan

---

## Quick Reference

### Git Commands for This PRD
```bash
# Tag this version
git tag -a "prd-[feature-name]-v1.0" -m "Initial PRD draft"
git push origin prd-[feature-name]-v1.0

# Update and tag new version
git add docs/PRDs/PRD_[Feature_Name].md
git commit -m "PRD v1.1: [Brief description of changes]"
git tag -a "prd-[feature-name]-v1.1" -m "[What changed]"
git push origin feature/[feature-name] --follow-tags
```

### PRD Checklist
- [ ] All placeholder text replaced with actual content
- [ ] Version history updated
- [ ] Success criteria are measurable
- [ ] All inputs documented with validation rules
- [ ] All outputs documented with examples
- [ ] Algorithm/logic is clear and testable
- [ ] Tests defined with specific expected results
- [ ] Dependencies identified with owners
- [ ] Implementation phases have realistic estimates
- [ ] Open questions documented with decision owners
- [ ] Related features cross-referenced
- [ ] Git tag created for this version
