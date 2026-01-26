# Product Requirements Document: [Feasibility]

## Version History

| Version | Date       | Author  | Changes |
|---------|------------|---------|---------|
| v1.0    | 2026-01-26 | Andrew Johnson  | Initial PRD draft |

---

## 1. Feature Name & Executive Summary

**Feature Name:** Feasibility Constraints

**Summary:**  
This feature adds an input sheet that constrains measure adoption based on real-world physical limitations. Not all upgrades within a competition group can occur 100% of the time - for example, an electric resistance heater may not always be upgradeable to a ground source heat pump in certain building types due to space, infrastructure, or technical constraints. The feasibility input allows SMEs to specify a percentage (e.g., 90%) representing the portion of upgrades that can feasibly occur, with the remaining portion (10%) defaulting to baseline-to-baseline (no upgrade) scenarios. This produces more realistic adoption modeling.
---

## 2. Business Justification / Problem Statement

### Current Problem
currently it is assumed that all upgrades within a competition group can happen at 100% of the adoption models predicated demand. However physical limitation exist that would prevent 100% of market based upgrades from occurring

### Business Impact
- this process creates an additional input sheet
- User impact - Users can optionally add feasibility constraints to specific measures, not required for all measures
- Development time - Minimal increase (~2-4 hours for implementation)
- Stakeholder concerns addressed - Better representation of actual adoption and physical market constraints

### User Stories
- **As an** analyst **I need to** limit the adoption of certain measures based on physical limitations, **so that** adoption is better modeled
- **As an** stakeholder, **I need to** have better results, **so that** my reports are better

### Success Criteria
- Feasibility input sheet correctly reduces adoption for constrained measures
- Total competition group flow remains constant (reallocated to baseline, not lost)
- Measures with feasibility_constraint='n' are unaffected
- Manual calculations match model output within 0.1% tolerance
- Feasibility percentages between 0-100% work correctly

---

## 3. Inputs

### Data Sources
# 
#### Input Source 1: 35_feasibility_inputs
- **Sheet/Location:** 030_inputs/ and or master_inputs excel
- **Required Fields:**
  - `measure_name` (string, this will have to match from the template and measure database)
    - Description: this is the baseline to upgrade measure
    - Example values: same set up as what comes out of the measure database for linking purposes
  - `competition_group` (string, matches database)
    - Description: used by the adoption model so it knows what group this feasibility piece fits into
    - Example values: 
  - `efficiency_level` (int)
    - Description: efficiency level of the upgrade measure. this is needed so the adoption model can tell which relationship to limit
    - Example values: [Examples]
  - `building_type_feasibility` (float, needs to be a percentage generally higher than than 90%?)
    - Description: this is the percentage of the standard adoption model's yearly results that actually happen in a given year 
    - Example values: [.9]
- **Validation Rules:**
  - Feasibility percentages must be between 0.0 and 1.0 (or 0% to 100%)
  - measure_name must match existing measures in measure database
  - competition_group must match database values
  - efficiency_level must be 1 or 2 (efficient/top10 only)
  - building_type columns must match those used in the system

### Assumptions
- Values are given in .9 decimal format? - We can add data validation to the excel file
- we can limit the number of rows to only those that actually change values to reduce the storage load
- climate zones do not effect the feasibly adoption metric
---

## 4. Outputs

### Modified Files
#### File 1: 030_output/tech_adoption_results.csv, baseline_adoption_results.csv, competition_adoption_results.csv
- **Modified Columns:**
  - `yearly flow columns` (all year_XXXX columns)
    - Change: Flow results are redistributed - constrained measures have reduced adoption, with difference added to baseline measure
    - Total competition group flow remains constant

### New Files
#### File 1: 030_output/feasibility_applied_log.csv
- **Purpose:** Track which measures had feasibility constraints applied each year
- **Columns:** year, competition_group, measure_name, building_type, original_flow, feasibility_percent, adjusted_flow, reallocated_to_baseline


### Output Validation
- total flow numbers for each competition group are the same but the allocation is adjusted based on the input sheet
- 

---

## 5. Technical Specifications

### Algorithm / Logic Description

#### High-Level Flow
1. each time year in the adoption model there is a check to see if the measures that are being used have a feasibility metric
2. if the measures have a feasibility adjustment that is applied to the total amount allocated to that measure in that year. the total is adjusted down by (1-feasibility_percent) feasibility_percent is collected from the input sheet and the respective competition_group and building_type that the adoption model is running
3. the amount removed from the measure with the adjustment is allocated to the baseline measure (note:future enhancement) 
4. the total in the baseline to baseline measure now the adoption model regular value and the not feasible proportion. (Note we will not be doing existing to baseline in feasible in this iteration (future enhancement))
5. *Baseline to baseline generates zero savings 

#### Detailed Logic

**Step 1: Load Feasibility Constraints**
```python
feasibility_df = pd.read_excel('030_input/35_Feasibility_Inputs.xlsx')
# Create lookup dictionary by measure_name, competition_group, building_type
feasibility_lookup = create_feasibility_dict(feasibility_df)
```
- **Inputs:** 35_Feasibility_Inputs.xlsx
- **Outputs:** Feasibility lookup dictionary
- **Edge Cases:** Missing file = assume 100% feasibility for all measures

**Step 2: Apply Feasibility During Adoption Loop**
```python
FOR each year, competition_group, building_type:
    IF measure in feasibility_lookup:
        feasibility_pct = lookup_feasibility(measure, comp_group, bldg_type)
        adjusted_flow = original_flow × feasibility_pct
        reallocated_flow = original_flow × (1 - feasibility_pct)
        baseline_flow += reallocated_flow
    ELSE:
        adjusted_flow = original_flow  # No constraint
```
- **Inputs:** Adoption model flow, feasibility_lookup
- **Outputs:** Adjusted flow values
- **Edge Cases:** 
  - Feasibility = 0 → all flow goes to baseline
  - Feasibility = 1 → no adjustment
  - Missing building type in feasibility → use 100%

### Data Structures
- **DataFrame:** `df_feasibility`
  - Key columns: measure_name, competition_group, efficiency_level, [building_type]_feasibility columns
  - Index: None (natural index)
  - Shape expectations: ~50-200 rows (only constrained measures) × ~15 columns (3 metadata + ~10-12 building types)
- **Dict:** `feasibility_lookup`
  - Structure: {(measure_name, competition_group, building_type): feasibility_percentage}
  - Used for fast lookups during adoption loop

### Integration Points
- **Notebook/Module:** `030_Yearly_Full_Adoption_Model_competition.ipynb`
  - **Cell/Function:** After market adoption calculation, before writing results
  - **Modification Type:** Insert new cell to load feasibility and apply constraints
  - **Dependencies:** 
    - Requires 35_Feasibility_Inputs.xlsx to exist (can be empty)
    - Requires feasibility_constraint column in measure database
    - Must run after initial adoption calculations but before aggregation

### Performance Considerations
- **Expected Runtime:** [Estimate with typical data size]
- **Memory Usage:** [Approximate memory footprint]
- **Optimization Notes:** [Any performance concerns or optimizations needed]

---

## 6. User Interface / Workflow Changes

### Input Workflow Changes

**Current Workflow:**
1. Define measures in 00_Potential_Study_Input_Template (Measure_List sheet)
2. Run 000_Template_Creation to generate workpapers and input files
3. Fill out measure details in workpapers
4. Run adoption model (030_notebook)

**New Workflow:**
1. Define measures in 00_Potential_Study_Input_Template, set feasibility_constraint='y' for constrained measures
2. Run 000_Template_Creation to generate workpapers and 35_Feasibility_Inputs.xlsx
3. Fill out measure details in workpapers
4. **[NEW]** Fill out feasibility percentages by building type in 35_Feasibility_Inputs.xlsx
5. Run adoption model (030_notebook) - now applies feasibility constraints

### New Fields in Input Templates

**Workbook:** `00_potential_Study_Input_template.xlsx` (measure_list)
- **Row/Field:** add column to measure_list sheet names `feasibility_constraint`
  - **Type:** Dropdown
  - **Validation:** y or n
  - **Help Text:** y if we should add this measure to the feasibility input workbook
  - **Default Value:** N

### Output Visualization Changes

**New Report/Chart in:** `060_Reporting.ipynb`
 - Would it be worth having a note about feasibility here?

---

## 7. Tests & Validation

### Unit Tests

#### Test 1: Feasibility Constraint Applied Correctly
- **Given:** Measure with 80% feasibility, original flow = 100 units
- **When:** Apply feasibility constraint
- **Then:** Adjusted flow = 80 units, baseline flow increases by 20 units
- **Location:** Test cell in 030_notebook or separate test file

#### Test 2: No Constraint When Measure Not in Feasibility
- **Given:** Measure not in feasibility input file
- **When:** Run adoption model
- **Then:** Flow unchanged, 100% of original flow allocated to efficient measure

### Integration Tests

#### Test 3: End-to-End Feasibility Test
- **Input:** 2 measures (1 with 90% feasibility, 1 without)
- **Expected Output:** 
  - tech_adoption_results.csv with reduced flow for constrained measure
  - baseline_adoption_results.csv no change
  - Total flow per competition_group unchanged
- **Validation:** 
  - Manual Excel calculation of expected flows
  - Compare to: Manual calculation results
  - Tolerance: ±0.01% (within floating point precision)

### Edge Cases

#### Edge Case 1: Feasibility = 0%
- **Condition:** Measure has 0% feasibility (completely infeasible)
- **Expected Behavior:** All flow redirected to baseline, zero flow to efficient measure
- **Test Data:** Create row with all building_type columns = 0.0

#### Edge Case 2: Feasibility Input File Missing
- **Condition:** 35_Feasibility_Inputs.xlsx doesn't exist in 030_input/
- **Expected Behavior:** Model runs normally with 100% feasibility for all measures (no constraints applied)

### Performance Tests

#### Test 4: Performance Test with Large Dataset
- **Measure:** Runtime increase and memory usage
- **Acceptable Threshold:** <15 seconds additional runtime, <10 MB additional memory
- **Test Dataset:** 100 constrained measures × 10 building types × 10 years = 10,000 constraint checks

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
- **Depends On:** need new system running
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
#### BLOCKER 1: [High] - [New System]
- **Description:** [What is blocked and why]
- **Impact:** [How this affects the feature]
- **Owner:** mike
- **Mitigation:** [Workaround or plan to unblock]
- **Target Resolution:** [1/27]

---

## 9. Implementation Plan & Status

### Implementation Phases

#### Phase 1: [input generation] (Week 1)
**Status:**  ✅ Complete

**Tasks:**
- [ ] Edit 00_potential_Study_Input_Template
  - Owner: [AJ]
  - ETA: [1/26]
- [ ] [Create Input sheet for Feasibility in master_input Excel]
  - Owner: [AJ]
  - ETA: [1/26]

**Deliverables:**
- 35_Feasibility_Input.xlsx
- [Deliverable 2]

#### Phase 2: Complete PRD Review (Week of 1/27)
**Status:** 🔄 In Progress

**Tasks:**
- [ ] Review PRD with Mike for technical approach
- [ ] Confirm feasibility calculation logic
- [ ] Validate that existing-to-existing is out of scope
- [ ] Confirm output file structure

**Deliverables:**
- Approved PRD with stakeholder sign-off

#### Phase 3: Implementation (Week of 2/3)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] Add feasibility load function to 030_notebook
- [ ] Implement feasibility constraint logic in adoption loop
- [ ] Create feasibility_applied_log output
- [ ] Add unit tests
- [ ] Run integration test with sample data
- [ ] Update documentation

**Deliverables:**
- Working implementation in 030_notebook
- Test results showing correct behavior
- Updated user documentation



### Overall Status Dashboard

**Overall Completion:** 20%  
**Risk Level:** 🟢 Low  
**Current Phase:** [2]  
**Next Milestone:** [Milestone] on [Date]

### Recent Updates

**2026-01-26** - [PRD and input template created]

---

## 10. Open Questions & Decisions

### Open Questions

**Q1: [We will not be doing existing to baseline in feasible in this iteration?]**
- **Context:** [we will be tracking real efficiency in another PRD ] tracking existing staying as existing is an interesting thought and possible with this tool
- **Options:** 
  - Option A: add this to inputs and track like all the others
  - Option B: [Description]
- **Decision Needed By:** [Date]
- **Owner:** Stakeholders
- **Status:** 🔴 Open

**Q2: [Values are given in .9 decimal format?]**
- **Context:** [Is this specific enough]
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
- **[Construction_Inputs]** (Issue #10, PRD tag: prd-feature-vX.X)
  - Relationship: [This feature will check things each year like the construction inputs did]
  - Coordination: [none]

### References & Research
- [Document/Study Name] - [Link or location] - Previous study on feasibility 
  - Relevance: [Why this is referenced]
- [Internal Documentation] - [Path or link]
  - Key Findings: [Summary]

### Future Enhancements (Out of Scope)

**Phase 2 Candidates:**
- Existing-to-existing feasibility tracking (measures that stay at existing efficiency)
- Time-varying feasibility (feasibility changes year-over-year)
- Building-type-specific feasibility overrides per climate zone
- Feasibility dashboard/visualization in reporting notebook

**Deferred Items:**
- Existing-to-baseline feasibility constraints: Deferred to PRD for "Real Efficiency Tracking" - will be handled in separate feature focused on tracking existing equipment retention

---

## 12. Stakeholder Communication

### Review Schedule
- **Design Review:** Week of 1/27 with Cliff and Griff (advisors)
- **Technical Review:** Week of 1/27 with Mike Fink (database SME/main developer)  
- **Stakeholder Demo:** Week of 2/10 with Matt (main SME) after implementation

### Communication Plan
- **Weekly Updates:** Matt (SME) - email summary of progress and blockers
- **Blocker Escalation:** To Mike Fink for technical issues, to Matt for business/requirements questions
- **Completion Notification:** Matt, Cliff, Griff, and Mike upon Phase 3 completion

### Team Roles
- **Andrew Johnson (AJ):** Project Manager, prototype development, simple implementations
- **Michael Fink (Mike):** Database SME, main system developer, technical lead
- **Cliff & Griff:** Design review advisors
- **Matt:** Main Subject Matter Expert, requirements owner

---

## Appendix

### Glossary
- **Term 1:** Definition
- **Term 2:** Definition

### Examples
[Include concrete examples, sample data, or screenshots if helpful]

### Change Log (Detailed)
- **v1.0 (2026-01-26):** Initial PRD created
  - Added all sections
  - Identified key dependencies
  - Created initial implementation plan
  - made initial templates

---

