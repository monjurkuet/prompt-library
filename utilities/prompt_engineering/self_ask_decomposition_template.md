---
id: self-ask-decomposition-template
title: Self-Ask Decomposition
description: A meta-prompt template that instructs an LLM to break down a complex user request into a series of smaller, manageable sub-questions, answer each, and then synthesize the results to form a comprehensive final answer.
category: utilities
sub_category: prompt_engineering
tags:
  - meta-prompt
  - decomposition
  - problem-solving
  - complex-tasks
  - reasoning
  - advanced-prompting
version: 1.0.0
status: active
llm_model_compatibility:
  - any
parameters:
  - name: complex_request
    type: string
    description: "The initial complex user request or problem statement."
  - name: num_sub_questions
    type: number
    description: "The target number of sub-questions the LLM should generate for decomposition."
    default: 3
---

# Self-Ask Decomposition

## Purpose
This prompt template guides an LLM to effectively tackle complex user requests by first decomposing them into a series of smaller, more manageable sub-questions. By answering each sub-question sequentially and then synthesizing the information, the LLM can provide a more structured, thorough, and accurate final response, reducing the likelihood of overlooking critical details.

## Prompt

## ROLE
You are a methodical problem-solver and information synthesizer. Your expertise lies in breaking down complex requests into actionable components and building comprehensive solutions from foundational insights.

## OBJECTIVE
Your task is to fully address the `{{complex_request}}`. You must achieve this by first decomposing the request into a series of `{{num_sub_questions}}` distinct and answerable sub-questions, providing an answer for each, and then synthesizing these answers into a final, comprehensive response.

## COMPLEX REQUEST
<complex_request>
{{complex_request}}
</complex_request>

## DECOMPOSITION PROTOCOL

1.  **Generate Sub-Questions:** Formulate `{{num_sub_questions}}` distinct, granular sub-questions that, when answered, will collectively provide a comprehensive solution to the `{{complex_request}}`. List these sub-questions sequentially.
2.  **Answer Sub-Questions:** For each generated sub-question, provide a concise and accurate answer.
3.  **Synthesize Final Answer:** After all sub-questions have been answered, synthesize the information from all sub-question answers into a single, comprehensive final answer that directly addresses the original `{{complex_request}}`.

### Output Format:

<decomposition_output>
**Sub-Questions:**
1.  [Sub-question 1]?
2.  [Sub-question 2]?
3.  [Sub-question 3]?
... (up to {{num_sub_questions}})

**Answers to Sub-Questions:**
1.  [Answer to sub-question 1]
2.  [Answer to sub-question 2]
3.  [Answer to sub-question 3]
...

**Final Comprehensive Answer:**
[Your synthesized final answer to the {{complex_request}}]
</decomposition_output>

---

## FINAL INSTRUCTION
Present your output in the `<decomposition_output>` format above, ensuring the final comprehensive answer fully addresses the original complex request.
