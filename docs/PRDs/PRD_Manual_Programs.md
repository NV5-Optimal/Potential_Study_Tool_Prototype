# Product Requirements Document: [Feature Name]

## Version History

| Version | Date       | Author  | Changes |
|---------|------------|---------|---------|
| v1.0    | 2026-01-29 | Andrew Johnson  | Initial PRD draft with Phase 1 implementation |

---

## 1. Feature Name & Executive Summary

**Feature Name:** Manual Programs

**Summary:**  
This feature adds the ability for users to define custom utility programs and assign measures to them with program-specific cost and benefit adjustments. This enables modeling of real-world utility programs beyond the default market-based assignments.

**Phase one** (COMPLETED): Adding programs to input sheets and workpapers
Phase two: Creating new condition rows in the database for each defined program
Phase three: Adjusting costs and benefits based on program assignments (Phase 3b: adjusting input global metrics)
Phase 4: Ensuring the adoption model correctly handles program-based adjustments
Phase 5: Creating reporting procedures to show program-specific costs and benefits 

Question do we will need to make sure that each condition in a competition group share programs? (I don't think so)
Question do all measures need at least one program?
Question does the adoption model care about programs?
Question does incentive values now need to change based on programs? - edit the incentives input sheet to have programs or add a new sheet that goes on top of the default incentives and edits based on the program selected (ex. have the standard incentives then another sheet by program with the percent adjustment up or down) (we might know the exact values...)
Question what else changes because of programs?
Question by moving away from default programs do we also move away from default building types (single_family vs single_family_li)
Adjacent PRD - Special predefined programs for Industrial and Behavioral where incentives only last a few years or are significantly smaller. This process's goal is to allow for that type of flexibility when creating programs. ideally we don't need this separate PRD
---

## 2. Business Justification / Problem Statement

### Current Problem
May utilities have their own programs they want to see in our model. Currently we just have programs assigned based on market and building type. However that does not map to most utility program. 

### Business Impact
- [Quantified impact] - This will increase runtime and complexity costs but increase the number of questions that can be answered
- [User impact - e.g., "Enables analysts to better model incentives and varying costs of conditions in different programs"]
- [Stakeholder concerns addressed] - Utilities can now see their actual programs and get a sense of incentive/metric sensitivity

### User Stories
- **As an** [analyst], **I need to** [model various program inputs that are beyond the default], **so that** [our stakeholders can have actionable data]


### Success Criteria
- ✅ Phase 1: Users can add any number of programs to the Programs sheet and see them dynamically added to workpapers with Y/N validation
- ✅ Phase 1: 18_program_adjustments.xlsx file is created with proper structure for measure/market/utility/program combinations
- Phase 2+: Users can adjust incentives and savings percentages by program without modifying core code
- Phase 2+: Program assignments correctly flow through to the measure database
- Phase 2+: Adoption model respects program-specific adjustments
- Phase 2+: Reporting shows program-level metrics and aggregations

---

## 3. Inputs

### Data Sources

#### Input Source 1: 00_Potential_Study_Input_Template.xlsx
- **Sheet/Location:** Programs
- **Required Fields:**
  - `program` (string, required, unique)
    - Description: User-defined program name. Can be any string value without restrictions on sector or market type.
    - Example values: "NLIRNC" (Non-Low Income Residential New Construction), "LIEE", "C&I_Retrofit", "Behavioral_Program"
    - Constraints: Must be unique within the sheet; no special Excel-invalid characters (: \ / ? * [ ])
- **Processing:** The template creation process reads this sheet, cleans values (lowercase, underscores), and creates a programs_list
- **Sheet/Location:** Global Inputs (Future Phase)
- **Required Fields:**
  - `program_type` (string, validation rules - Default or Custom)
    - Description: Determines whether to use default market-based programs or custom user-defined programs
    - Example values: "default", "custom"
- **Validation Rules:**
  - Program names must be valid Python identifiers (will be used as field names)
  - Only "default" or "custom" allowed for program_type


---

## 4. Outputs

### Modified Files
#### File 1: workpapers.xlsx
- **Location:** ./00_output/workpapers.xlsx
- **Modification Type:** Dynamic field addition
- **New Rows (dynamically generated):**
  - `{program_name}_applicable` (string with Y/N validation)
    - Description: For each program in programs_list, a field is dynamically added to the end of the workpapers field list
    - Values: Y or N (enforced by Excel data validation)
    - Example: If programs_list = ['nlirnc', 'liee', 'commercial'], three fields are added:
      - `nlirnc_applicable`
      - `liee_applicable`
      - `commercial_applicable`
- **Formula/Logic:** 
  ```python
  for program in programs_list:
      field_names.append(f'{program}_applicable')
  ```
- **Data Validation:** Y/N dropdown with type="list", formula1='"Y,N"', allow_blank=True
- **Implementation:** Cell #VSC-ed1d1a33 in 000_Template_Creation.ipynb


### New Files
# proposed additional sheet that has each program and how they effect the conditions in them - (ex. reduced incentive...)
# the default for now in 14_programs is just adjusting the overhead based on the program
# 13_incentives adjusts the incentives based on utility and fuel but not program
# 18_program_adjustments will adjust incentives, savings by program not utility
# question: how should we adjust savings (- reduce the individual measure savings produced by a percentage? (process same as incentives just inverse))

#### File 1: [18_program_adjustments]
- **Purpose:** This file contains values that show how programs effect the cost and savings of particular measures
- **Columns:**
  - `unique measure name` (str) - Description - unique measure name
  - `market` (str) - Description
  - `utility` (str) - Description
  - `utility_type` (str) - Description
  - `program` (str) - Description - all programs from 00
  - `incentive_adjustment_percent` (str) - Description - percent the incentive is adjusted by (should this be incremental cost adjustment?)
  - `savings_adjustment_percent` (str) - Description - percent the incremental savings is adjusted by?
- **Update Frequency:** [When initial template process is created] - might be worth filtering after workpapers creation when we know what programs the measure are applicable too

### Output Validation
- [How to verify outputs are correct]
- [Expected ranges or patterns in output data]

### Modified Files
#### File 1: [results]
- **Values** [some measure will have different results as thier cost and benefits have changed]

---

## 5. Technical Specifications - How will this effect the main pipeline???

### Algorithm / Logic Description

#### High-Level Flow (Phase 1 - Completed)
1. Read Programs sheet from input template
2. Clean and create programs_list
3. Dynamically append program_name_applicable fields to workpapers field_names list
4. For each measure sheet, add program fields with Y/N validation
5. Create unique measure/market tuples from df_expanded
6. Generate 18_program_adjustments.xlsx with all combinations of measure/market/utility/program

#### Detailed Logic

**Step 1: Load and Process Programs**
```python
df_programs = pd.read_excel('./00_input/00_Potential_Study_Input_Template.xlsx', 
                            sheet_name='Programs')
clean_column_names(df_programs)
clean_values(df_programs)
programs_list = df_programs['program'].unique().tolist()
```
- **Inputs:** 00_Potential_Study_Input_Template.xlsx, Programs sheet
- **Outputs:** programs_list (list of cleaned program names)
- **Edge Cases:** Empty Programs sheet will result in empty programs_list (no program fields added)

**Step 2: Add Dynamic Program Fields to Workpapers**
```python
# After static field_names list is defined
for program in programs_list:
    field_names.append(f'{program}_applicable')
```
- **Inputs:** programs_list, static field_names list
- **Outputs:** Extended field_names list with program fields appended
- **Edge Cases:** Special characters in program names are handled by clean_values() function

**Step 3: Apply Y/N Validation to Program Fields**
```python
elif field.endswith('_applicable') and field.replace('_applicable', '') in programs_list:
    dv = DataValidation(type="list", formula1='"Y,N"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(cell_ref)
```
- **Inputs:** field name, programs_list, cell reference
- **Outputs:** Excel data validation applied to cell
- **Edge Cases:** Validates that field suffix matches a program in programs_list

**Step 2: [Name]**
```
Formula:
  Result = Input_A × Factor + Adjustment
  
  Where:
    Factor = lookup from table X
    Adjustment = conditional based on Y
```

### Data Structures
- **DataFrame:** `df_programs`
  - Key columns: ['program']
  - Index: Default integer index
  - Shape expectations: Variable rows (user-defined) × 1 column minimum
  
- **List:** `programs_list`
  - Content: Unique program names after cleaning (lowercase, underscores)
  - Example: ['nlirnc', 'liee', 'commercial_retrofit']
  - Used in: Workpapers field generation, program_adjustments file creation
  
- **List:** `utility_list`
  - Content: List of tuples [(utility_name, utility_type), ...]
  - Example: [('test_utility_1', 'electric'), ('test_utility_1', 'gas')]
  - Used in: Program adjustments file for all utility combinations
  
- **List:** `unique_measure_market`
  - Content: List of tuples [(unique_measure_name, market), ...]
  - Generated from: df_expanded[['unique_measure_name', 'market']].drop_duplicates()
  - Used in: Creating rows in 18_program_adjustments.xlsx

### Integration Points
- **Notebook/Module:** `000_Template_Creation.ipynb`
  - **Cell:** #VSC-10adc1fd (NEW)
  - **Function:** Loads Programs sheet and creates programs_list
  - **Modification Type:** New cell added after vocabulary enums loading
  - **Dependencies:** Requires Programs sheet in input template
  
- **Notebook/Module:** `000_Template_Creation.ipynb`
  - **Cell:** #VSC-ed1d1a33 (MODIFIED)
  - **Function:** Creates workpapers.xlsx with dynamic program fields
  - **Modification Type:** Added loop to append program_applicable fields, added validation logic
  - **Dependencies:** Requires programs_list from Cell #VSC-10adc1fd
  
- **Notebook/Module:** `000_Template_Creation.ipynb`
  - **Cell:** #VSC-268a6817 (NEW)
  - **Function:** Creates 18_program_adjustments.xlsx
  - **Modification Type:** New cell for program adjustments file
  - **Dependencies:** Requires programs_list, utility_list, df_expanded
  
- **Future Integration Points (Phase 2+):**
  - 002_Initialization_Process.ipynb - Read workpapers and process program assignments
  - Measure database creation - Duplicate conditions for each applicable program
  - Cost/benefit calculations - Apply adjustment percentages from 18_program_adjustments

### Performance Considerations
- **Expected Runtime:** < 1 second for programs_list processing; adds ~0.1 seconds per program to workpapers creation
- **Memory Usage:** Negligible - programs_list typically < 20 entries, each < 50 characters
- **Optimization Notes:** 
  - No optimization needed for Phase 1
  - Phase 2: Consider indexing program assignments in database for faster lookups
  - 18_program_adjustments.xlsx can grow large (measures × markets × utilities × programs); typical size: 1000-10000 rows

---

## 6. User Interface / Workflow Changes

### Input Workflow Changes

**Current Workflow:**
1. User creates measure list in input template
2. User runs 000_Template_Creation.ipynb
3. Workpapers.xlsx is created with fixed set of fields
4. User manually fills in workpaper values for each measure

**New Workflow (Phase 1):**
1. User creates measure list in input template
2. **NEW:** User adds program names to Programs sheet in input template
3. User runs 000_Template_Creation.ipynb
4. **NEW:** Workpapers.xlsx is created with dynamic program_applicable fields
5. **NEW:** 18_program_adjustments.xlsx is created
6. User fills in workpaper values including Y/N for each program's applicability
7. **NEW:** User fills in incentive and savings adjustment percentages in 18_program_adjustments.xlsx

**Key Changes:**
- Step 2 (NEW): Requires adding Programs sheet with desired program names
- Step 4 (ENHANCED): Workpapers now include variable number of program fields
- Step 5 (NEW): Additional file to populate with adjustment percentages
1. [Modified step 1]
2. [New step added]
### New Fields in Input Templates

**Workbook:** `00_Potential_Study_Input_Template.xlsx`
- **Sheet:** Programs (NEW)
  - **Column:** program
  - **Type:** Text
  - **Validation:** None (user-defined)
  - **Help Text:** "Enter unique program names. These will be used to create program assignment fields in workpapers."
  - **Default Value:** None
  - **Example:** NLIRNC, LIEE, Commercial_Retrofit

**Workbook:** `workpapers.xlsx` (each measure sheet)
- **Row/Field:** {program_name}_applicable (dynamically generated, multiple fields)
  - **Type:** Dropdown (Y/N)
  - **Validation:** Data validation list with "Y,N", allow_blank=True
  - **Help Text:** "Select Y if this measure is applicable to the {program_name} program"
  - **Default Value:** Blank
  - **Location:** Appended to end of field list after 'reference' field
  - **Count:** One field per program in Programs sheet

**Workbook:** `18_program_adjustments.xlsx`
- **Sheet:** programs_adjustments
  - **Columns:** unique_measure_name, market, utility, utility_type, program, incentive_adjustment_percentage, savings_adjustment_percentage
  - **Type:** Text (identifiers), Decimal (adjustment percentages)
  - **Validation:** None (free-form entry for percentages)
  - **Help Text:** "Enter decimal values for adjustments (e.g., 0.10 for +10%, -0.20 for -20%)"
  - **Default Value:** Blank
  - **Purpose:** Define program-specific modifications to base incentives and savings

### Output Visualization Changes

**Phase 1:** No reporting changes

**Future (Phase 5):** New Report/Chart in `060_Reporting.ipynb`
- **Chart Type:** Stacked bar chart by program
- **Purpose:** Show total costs, benefits, and savings by program
- **Location:** New section "Program-Level Results"
- **Metrics:** Program costs, program incentives, net benefits, participant counts

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

#### Edge Case 1: Empty Programs Sheet
- **Condition:** Programs sheet exists but has no program entries
- **Expected Behavior:** 
  - programs_list is empty list []
  - No program fields added to workpapers
  - 18_program_adjustments.xlsx is created but has only headers, no data rows
- **Test Data:** Create Programs sheet with only headers, no data rows

#### Edge Case 2: Special Characters in Program Names
- **Condition:** Program name contains spaces, special characters, or mixed case (e.g., "C&I Retrofit Program")
- **Expected Behavior:** 
  - clean_values() converts to "c&i_retrofit_program"
  - Field name becomes "c&i_retrofit_program_applicable"
  - Excel sheet names and field names remain valid
- **Test Data:** Programs = ["Low-Income/Energy Efficiency", "C&I $aver"]

#### Edge Case 3: Duplicate Program Names
- **Condition:** Programs sheet has duplicate program entries
- **Expected Behavior:** 
  - programs_list.unique() ensures only unique programs
  - No duplicate fields created in workpapers
- **Test Data:** Programs sheet with "NLIRNC" appearing twice

#### Edge Case 4: Very Long Program Names
- **Condition:** Program name exceeds reasonable length (e.g., 50+ characters)
- **Expected Behavior:** 
  - Field name could become very long but still functional
  - Excel field names have no strict limit in value column format
  - Recommend: Document maximum suggested length (e.g., 30 chars)
- **Test Data:** Program = "Residential_Low_Income_Energy_Efficiency_New_Construction_Program_2025"

#### Edge Case 5: No Utility Combinations
- **Condition:** utility_list is empty
- **Expected Behavior:**
  - 18_program_adjustments.xlsx created with headers only
  - No data rows generated
- **Test Data:** Empty or invalid Utility_Combinations sheet

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
  - Clean functions (clean_column_names, clean_values) - Already implemented
    - Status: ✅ Complete
    - Impact: Required for consistent data cleaning across all sheets
  - openpyxl library - Already installed
    - Status: ✅ Complete
    - Impact: Required for Excel file creation and data validation
  - pandas - Already installed
    - Status: ✅ Complete
    - Impact: Required for data manipulation

### Data Dependencies
- **Required Data:**
  - Programs sheet in 00_Potential_Study_Input_Template.xlsx
    - Owner: User/Analyst
    - ETA: User-provided
    - Status: Template ready, users must populate
    - Format: Single column 'program' with program names
- **Data Quality Requirements:**
  - Program names should be unique
  - Program names should be descriptive (recommended 5-30 characters)
  - Avoid special characters that are invalid in Python variable names

### External Dependencies
- **Stakeholder Approvals:**
  - [Decision/assumption that needs approval]
    - Approver: [Name]
    - Target Date: [Date]
    - Approver: Project Lead/Product Owner
    - Target Date: N/A (assumed approved for Phase 1)
    - Status: ✅ Approved (Phase 1 implementation proceeded)

### Current Blockers

**Phase 1: No Active Blockers** ✅

**Phase 2+ Potential Blockers:**

#### BLOCKER 1: [Medium] - Database Schema for Program-Duplicated Conditions
- **Description:** Need to define how program-specific conditions are stored and indexed in the measure database
- **Impact:** Blocks Phase 2 implementation - cannot create program-specific conditions without schema
- **Owner:** Database architect/Lead developer
- **Mitigation:** Document current schema and propose extension with program_id field
- **Target Resolution:** Before Phase 2 start

#### BLOCKER 2: [Low] - Adjustment Percentage Application Logic
- **Description:** Need to clarify whether adjustments are additive, multiplicative, or sequential
- **Impact:** Affects Phase 3 cost/benefit calculations
- **Owner:** Business analyst/Product owner
- **Mitigation:** Document example calculations and get stakeholder sign-off
- **Target Resolution:** During Phase 2

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
- [ ] Read 18_program_adjustments.xlsx in cost/benefit calculation process
- [ ] Apply incentive_adjustment_percentage to base incentive calculations
- [ ] Apply savings_adjustment_percentage to measure savings
- [ ] Handle edge cases (missing adjustments, conflicting values)
- [ ] Add program-specific cost overhead from 14_programs.xlsx
- [ ] Validate calculation results against manual test cases

**Deliverables:**
- Program-adjusted cost calculations
- Program-adjusted benefit calculations
- Test cases with known correct results

**Blockers:**
- Blocked by: [Phase 1 completion / External dependency]

#### Phase 4: Adoption Model Integration
**Status:** ⏳ Not Started

**Tasks:**
- [ ] Review adoption model to understand program interactions
- [ ] Ensure program-specific conditions participate correctly in adoption calculations
- [ ] Test that competition logic works with program-duplicated measures
- [ ] Validate adoption results don't double-count across programs

**Deliverables:**
- Adoption model correctly processes program-specific conditions
- Validation test suite for program adoption scenarios

#### Phase 5: Reporting Enhancements 
**Status:** ⏳ Not Started

**Tasks:**
- [ ] Add program dimension to 060_Reporting.ipynb
- [ ] Create program-level summary tables (costs, benefits, savings by program)
- [ ] Add program comparison charts
- [ ] Create program-level cost-effectiveness metrics
- [ ] Document reporting methodology

**Deliverables:**
- Program-level reporting section in 060_Reporting.ipynb
- Program comparison visualizations

### Overall Status Dashboard

**Overall Completion:** 20% (Phase 1 of 5 complete)  
**Risk Level:** 🟢 Low  
**Current Phase:** Phase 1 Complete, Phase 2 Planning  
**Next Milestone:** Phase 2 - Database condition duplication (Date TBD)

### Recent Updates

**2026-01-29** - Phase 1 completed. Successfully implemented:
  - Programs sheet loading and processing
  - Dynamic program field generation in workpapers
  - 18_program_adjustments.xlsx file creation
  - Y/N validation on all program applicability fields

---

## 10. Open Questions & Decisions

### Open Questions

**Q1: Do all conditions in a competition group need to share the same programs?**
- **Context:** If one measure in a competition group is assigned to "NLIRNC" program, must all competing measures also be in that program?
- **Options:** 
  - Option A: Yes, enforce same programs within competition groups (simpler logic, less flexible)
  - Option B: No, allow different program assignments (more flexible, complex competition logic)
- **Decision Needed By:** Before Phase 2 (database creation)
- **Owner:** Product owner / Business analyst
- **Status:** 🔴 Open
- **Implication:** Affects database structure and validation rules

**Q2: Do all efficient measures require at least one program assignment?**
- **Context:** Should every efficient measure (non-baseline/existing) be required to have Y in at least one program_applicable field?
- **Options:**
  - Option A: Yes, require at least one program (ensures all measures are tracked)
  - Option B: No, allow measures with no programs (more flexible, may result in "orphan" measures)
- **Decision Needed By:** Before Phase 2
- **Owner:** Product owner
- **Status:** 🔴 Open

**Q3: How should the adoption model handle program assignments?**
- **Context:** When calculating market adoption, does the model need program awareness or just treat program-duplicated conditions as separate entities?
- **Options:**
  - Option A: Model is program-agnostic (treats program conditions as independent)
  - Option B: Model needs program logic (may aggregate or differentiate by program)
- **Decision Needed By:** Before Phase 4
- **Owner:** Lead developer / Model architect
- **Status:** 🟡 Under Discussion
- **Note:** Leaning toward Option A for simplicity

**Q4: Are incentive adjustments additive or multiplicative?**
- **Context:** If base incentive is $100 and adjustment is 0.10, is result $110 (additive) or $100 × 1.10 = $110 (multiplicative - same result but different for negative)?
- **Options:**
  - Option A: Additive: new_value = base_value × (1 + adjustment)
  - Option B: Multiplicative: new_value = base_value × adjustment_factor (where user enters 1.10 for +10%)
  - Option C: Percentage point adjustment: new_value = base_value + (base_value × adjustment)
- **Decision Needed By:** Before Phase 3
- **Owner:** Business analyst
- **Status:** 🔴 Open
- **Note:** Option A (additive) is most intuitive for percentage-based adjustments

**Q5: Should we move away from default building type programs (single_family_li)?**
- **Context:** Currently have default program logic based on building type suffixes. Does custom programs replace this?
- **Options:**
  - Option A: Replace entirely with custom programs
  - Option B: Keep default logic as fallback when program_type = "default"
  - Option C: Hybrid approach - both can coexist
- **Decision Needed By:** Before Phase 2
- **Owner:** Product owner
- **Status:** 🟡 Under Discussion
- **Note:** Option B provides backward compatibility

### Decisions Made

**✅ D1: Dynamic Program Field Generation in Workpapers** (Date: 2026-01-29)
- **Decision:** Programs will be dynamically added to workpapers based on Programs sheet, not hardcoded
- **Rationale:** Provides maximum flexibility for users to define any number of programs without code changes
- **Alternatives Considered:** Hardcoded list of common programs (rejected - too rigid)
- **Approved By:** Implementation team
- **Impact:** Requires programs_list to be populated before workpapers creation; enables user-driven program definition

**✅ D2: Use Y/N String Validation Instead of Boolean** (Date: 2026-01-29)
- **Decision:** Program applicability fields use Y/N dropdown strings, not TRUE/FALSE booleans
- **Rationale:** Consistent with existing applicable fields (RET_add_on_applicable, etc.); easier for users to understand
- **Alternatives Considered:** Boolean TRUE/FALSE (rejected - less intuitive)
- **Approved By:** Implementation team
- **Impact:** Data validation uses formula1='"Y,N"' pattern

**✅ D3: Separate File for Program Adjustments** (Date: 2026-01-29)
- **Decision:** Create 18_program_adjustments.xlsx as separate file rather than adding to existing files
- **Rationale:** Keeps workpapers focused on measure characteristics; allows granular program/utility/measure adjustments
- **Alternatives Considered:** 
  - Add to workpapers (rejected - too many fields)
  - Add to 14_programs.xlsx (rejected - different granularity)
- **Approved By:** Implementation team
- **Impact:** Users have additional file to populate; provides necessary granularity for program-specific adjustments
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
