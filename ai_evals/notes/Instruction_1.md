These techniqeus have to be applied causiously:

## 1. LLM As A Judge

- Using one model to judge the output of another is a common design pattern.
- Considerations:
    - Label good/bad answers manually first
    - Compare AI-judge scores to human scores
    - Automate only after alignment with human experts

## 2. Review Traces

- Looking only at answers/responses hides failures
- Wrong source + right answer = slient bug
- Log step-by-step reasoning: (request -> search -> tool call -> response)
- Use a trace viewer to inspect quickly

## 3. Test Failure Cases

- A few perfect cases create false confidence
- Real users push systems into edge cases
- Hence:
    - Generate lots of variations
    - Add failure cases from production
    - Continously grow your test set

## 4. Vage Metrics

- Use meaningful metrics
    - Use binary pass/fail checks
    - Tie metrics directly to user outcomes
    - eg: "Return exactly 1 correct contact when asked"

## 5. Tool Reliance

- Write your own success criteria
- Start simple, add tools later if you need scale