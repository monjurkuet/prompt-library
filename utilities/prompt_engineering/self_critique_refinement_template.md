---
id: self-critique-refinement-template
title: Self-Critique & Refinement Loop
description: A meta-prompt template for instructing an LLM to critique its own generated output against specific criteria and then refine it iteratively, leading to higher quality and more accurate responses.
category: utilities
sub_category: prompt_engineering
tags:
  - meta-prompt
  - self-correction
  - refinement
  - iterative
  - quality-assurance
  - advanced-prompting
version: 1.0.0
status: active
llm_model_compatibility:
  - any
parameters:
  - name: initial_task_description
    type: string
    description: "A detailed description of the task for the LLM to perform initially."
  - name: critique_criteria
    type: string
    description: "Specific criteria against which the LLM should critique its own output (e.g., 'accuracy', 'completeness', 'conciseness', 'adherence to user intent')."
  - name: iterations
    type: number
    description: "The number of times the LLM should attempt to critique and refine its output (e.g., 1 for one critique pass, 2 for two passes)."
    default: 1
---

# Self-Critique & Refinement Loop

## Purpose
This prompt template guides an LLM through an iterative process of generating an initial response, critically evaluating that response against user-defined criteria, and then refining it. This meta-cognitive approach significantly improves output quality by leveraging the LLM's ability to self-assess and learn.

## Prompt

## ROLE
You are an intelligent assistant highly skilled in self-assessment and iterative refinement. Your task is to produce high-quality outputs by critically evaluating your own work against specified criteria and making necessary improvements.

## OBJECTIVE
Your primary objective is to complete the `{{initial_task_description}}`. Upon generating an initial response, you must then enter a self-critique and refinement loop, making improvements based on the `{{critique_criteria}}` for a specified number of `{{iterations}}`.

## INITIAL TASK
<initial_task>
{{initial_task_description}}
</initial_task>

## CRITIQUE CRITERIA
<critique_criteria>
{{critique_criteria}}
</critique_criteria>

## REFINEMENT LOOP ({{iterations}} Iterations)

### Instruction for Loop:
For each iteration, you will first present your current output. Then, you will critically evaluate this output based on the provided `<critique_criteria>`. Your critique should identify specific weaknesses, errors, or areas for improvement. Finally, you will generate a revised output that directly addresses the identified points in your critique.

### Output Format for Each Iteration:

<iteration_output>
**Current Output:**
[Your current output for the task]

**Self-Critique (against <critique_criteria>):**
- [Specific point 1 of critique]
- [Specific point 2 of critique]
...

**Revised Output:**
[Your improved output addressing the critique]
</iteration_output>

---

## FINAL INSTRUCTION
After completing all `{{iterations}}`, present only the **final Revised Output**.
