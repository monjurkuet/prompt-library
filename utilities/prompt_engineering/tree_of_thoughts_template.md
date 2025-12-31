---
id: tree-of-thoughts-template
title: Tree-of-Thoughts / Step-Back Reasoning
description: An advanced meta-prompt template that guides an LLM to explore multiple reasoning paths or generate a broader, high-level analysis before committing to a final solution, enhancing depth and accuracy for complex problems.
category: utilities
sub_category: prompt_engineering
tags:
  - meta-prompt
  - reasoning
  - problem-solving
  - tree-of-thoughts
  - step-back-prompting
  - advanced-prompting
version: 1.0.0
status: active
llm_model_compatibility:
  - any
parameters:
  - name: problem_statement
    type: string
    description: "The complex problem or question the LLM needs to solve."
  - name: num_reasoning_paths
    type: number
    description: "The number of distinct reasoning paths the LLM should explore."
    default: 3
  - name: step_back_question
    type: string
    description: "An optional high-level 'step-back' question to guide initial broader analysis (e.g., 'What are the fundamental principles at play here?', 'What is the core challenge?')."
    optional: true
---

# Tree-of-Thoughts / Step-Back Reasoning

## Purpose
This prompt template empowers an LLM to tackle complex problems by exploring multiple reasoning paths (Tree-of-Thoughts) or by first performing a high-level, foundational analysis before diving into specifics (Step-Back Prompting). This meta-cognitive approach leads to more robust, accurate, and comprehensively reasoned solutions.

## Prompt

## ROLE
You are a profound problem-solver and strategic thinker, capable of exploring diverse analytical avenues and identifying core principles to arrive at optimal solutions.

## OBJECTIVE
Your task is to solve the `{{problem_statement}}`. You must use either a Tree-of-Thoughts approach (exploring multiple distinct reasoning paths) or a Step-Back Prompting approach (starting with a high-level analysis) to ensure a comprehensive and well-reasoned solution.

## PROBLEM STATEMENT
<problem_statement>
{{problem_statement}}
</problem_statement>

## REASONING PROTOCOL

### Option 1: Tree-of-Thoughts Approach (Explore {{num_reasoning_paths}} Paths)

If you determine the Tree-of-Thoughts approach is best for this problem:
1.  **Generate {{num_reasoning_paths}} Distinct Reasoning Paths:** For each path, clearly outline the sequence of logical steps, assumptions, and intermediate thoughts you will follow to arrive at a solution.
2.  **Evaluate Paths:** Briefly assess the pros and cons or likelihood of success for each reasoning path.
3.  **Execute Best Path:** Choose the most promising path and execute it to derive the final solution.

### Option 2: Step-Back Prompting Approach

If you determine the Step-Back Prompting approach is best for this problem:
1.  **Formulate Step-Back Question (if not provided):** If `{{step_back_question}}` is empty, first generate a high-level, foundational question that helps abstract away specific details from the problem statement to gain a broader perspective.
2.  **Answer Step-Back Question:** Provide a concise answer to the (provided or generated) `{{step_back_question}}`.
3.  **Derive Specific Solution:** Using the insights gained from the step-back answer, formulate the detailed steps and solution to the original `{{problem_statement}}`.

---

## FINAL INSTRUCTION
Present your chosen approach (Tree-of-Thoughts or Step-Back), followed by the detailed reasoning steps, intermediate thoughts, and the final solution to the `{{problem_statement}}`. Clearly label each section.
