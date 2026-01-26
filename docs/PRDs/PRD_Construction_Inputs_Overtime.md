# Product Requirements Document: [Construction Inputs Overtime]

## Version History

| Version | Date       | Author  | Changes |
|---------|------------|---------|---------|
| v1.0    | 2026-01-26 | Andrew Johnson  | Initial PRD draft |

---

## 1. Feature Name & Executive Summary

**Feature Name:** [Construction Inputs Overtime]

**Summary:**  
This feature allows for the user to create a rate for the construction inputs (New construction, Demolition and Renovation) to change over time. It pulls in an excel input sheet and applies directly to the adoption model code.
---

## 2. Business Justification / Problem Statement

### Current Problem
The Current process assumes stagnant construction inputs in the model which is not realistic

### Business Impact
- This will increase development time requiring justification for the input metrics and the model will have to run longer as it will have to check more input data. 
- User impact - Users will have to make more inputs and have justification for them
- Stakeholder concerns addressed - A more precise result will be generated and the stakeholder could ask for certain laws or events planned in the future to be added here

### User Stories
- **As an** [stakeholder], **I need to** model future growth of the population in my service territory, **so that** future program growth is appropriately reflected. Specifically for the new construction market
- **As an** analyst, **I need to** better model renovation and new construction changes over time, **so that** we create believable results for these markets when split out by the stakeholders

### Success Criteria
- The user is able to quickly iterate on the rate of change inputs 
- Adding a linear or direct input function does not create issues with the rest of the model
- default values of no change step in when these are not filled out 

---

## 3. Inputs
THere will be two different strategies here: One a format similar to 30_Construction_Inputs.xlsx. Now called 030_input/31_CI_Rate_of_change.xlsx which has each competition group and building type but instead of percent of initial population added the values will be percent increase or decrease year over year, for example on value might be 1% meaning a linear growth of the inputs by 1% every year of the study. Note depending on which sheet it could be growth of new construction, demolition or renovation.
Strategy 2 is a much larger input file that has a individual sheet for each year but the format will be the same as the other files. The code will just prepopulate thing and 
### Data Sources

#### Input Source 1: 030_input/31_CI_Rate_of_change.xlsx
- **Sheet/Location:** 030_input/31_CI_Rate_of_change.xlsx
- **Required Fields:**
  - `competition_group` (string, need to match the competition groups from the workpapers)
    - Description: [the grouping that will be present in the adoption model]
    - Example values: [refrigeration]
  - `single_family` (string, this is each building type in the model)
    - Description: []
    - Example values: [single_family]
- **Validation Rules:**
  - all values are percentages
  - have a reasonability range for unit tests

#### Input Source 2: 030_input/32_CI_Manual_Rate_of_change.xlsx
- **Sheet/Location:** 030_input/32_CI_Manual_Rate_of_change.xlsx
- **Required Fields:**
  - same format just with a new sheet for each year in the study

### Assumptions
- values always in percentage of initial count (WIll have code make everything a percent so the user can enter a number and hve it converted to a percentage or a percentage)


---

## 4. Outputs

### Modified Files
#### File 1: [030_output]
- **this will effect the internal code and results values but not any formatting of results**
- We will want to present the assumptions to the client somehow...


### Output Validation
- [How to verify outputs are correct] - manual excel implementation of first row
- [Expected ranges or patterns in output data] - the ranges will change based on the input data focus on the markets where the input values effect things

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
- **DataFrame:** `31_CI_Rate_of_change`
  - Key columns: competition_group
  - Index: [competition_group]
  - Shape expectations: [approximate rows × columns] [unique competition_groups x unique_building_types]

### Integration Points - to be transferred to main system week of 1.26
- **Notebook/Module:** `030_adoption_model.ipynb`
  - **Cell/Function:** Cell XX, function `function_name()`
  - **Modification Type:** [Insert new logic / Modify existing / Add new cell]
  - **Dependencies:** Requires completion of [other feature/task]

### Performance Considerations - Will increase
- **Expected Runtime:** [Estimate with typical data size] will use time package to test
- **Memory Usage:** [Approximate memory footprint] from memory_profiler import profile
- **Optimization Notes:** [Any performance concerns or optimizations needed]

---

## 6. User Interface / Workflow Changes

### Input Workflow Changes

**Current Workflow:**
1. User fills out 30_Construction_Inputs
2. code runs

**New Workflow:**
1. User fills out 30 and 31 or 32
2. code has if statement that prefers 32 if both 31 and 32 filled out
3. if possible a mix of the two should be used
4. Also allow for user to enter nothing in 31 and 32 and just default to stagnant 30 values

### Input Templates ---> 31 and 32 generated but no new inputs needed from user



### Output Visualization Changes

**New Report/Chart in:** `060_Reporting.ipynb`
- **Chart Type:** [Line graph]
- **Purpose:** [Shows the change in construction inputs over time]
- **description:** line graph x axis is year Y axis is count of each construction input for each competition group. Make this generic so can fit for all scenarios
Future add - (can also make this a stacked bar graph with the stacks being the efficiency level added based on function used)

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
  - [31_CI_Rate_of_change.xlsx]
    - Owner: [AJ]
    - ETA: [1/26]
    - Status: [Test data added 0.01% growth]
      - [32_CI_Manual_Rate_of_change.xlsx]
    - Owner: [AJ]
    - ETA: [1/26]
    - Status: [Test data added 0.01% growth with Year 2030 at .05%]
- **Data Quality Requirements:**
  - [Just test data for now]

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

#### Phase 1: [Material Prep] (Week 1)
**Status:**  ✅ Complete

**Tasks:**
- [ ] [Add new sheets to template generation process]
  - Owner: [AJ]
  - ETA: [1/26]
- [ ] [add dummy data to inputs]
  - Owner: [AJ]
  - ETA: [1/26]

**Deliverables:**
- [new master input sheet and individual sheets]
- [dummy data as outlined]

#### Phase 2: [Psuedo code and testing plan] (Week 2)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] [AJ to review new adoption model]
- [ ] [Task 2]

**Blockers:**
- Blocked by: [Need new adoption model ready]

#### Phase 3: [Apply to adoption modele] (Week 3)
**Status:** ⏳ Not Started

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]


### Overall Status Dashboard

**Overall Completion:** 20%  
**Risk Level:** 🟢 Low  
**Current Phase:** [1]  
**Next Milestone:** [Milestone] on [Date]

### Recent Updates

**2026-01-26** - [Plan made and phase 1 completed]

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
- [Enhancement 1]: [Stacked bar graph for more specific reporting]
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
