# Asks the AI to write an insight about a pump through OpenRouter.
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def ask_ai(pump, service, result):
    """result = the analysis of the pump (see analysis.py)."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "The AI insight is unavailable. Add OPENROUTER_API_KEY to the project .env file."

    lines = []
    for parameter in result["parameters"].values():
        if parameter["hours"]:
            forecast = f"alarm in about {parameter['hours']} hours"
        else:
            forecast = "no alarm within 14 days"
        lines.append(
            f"- {parameter['name']}: now {parameter['value']} {parameter['unit']}, "
            f"alarm limit {parameter['limit']}, status {parameter['status']}, "
            f"forecast: {forecast}"
        )

    causes = ", ".join(
        f"{cause['name']} ({cause['score']}% match)" for cause in result["rca"][:2]
    ) or "none found"

    question = (
        f"You are a senior reliability engineer. Pump {pump} ({service}) is a centrifugal pump "
        "in an oil and gas plant. Readings with a time series forecast:\n"
        + "\n".join(lines)
        + f"\nThe rule-based root cause analysis suggests: {causes}.\n\n"
        "Answer in plain text (no markdown) with exactly these headings: "
        "What is happening, Root cause, What to do next, Urgency. "
        "Use simple words, under 150 words. If all is normal, say so."
    )

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            timeout=45,
            max_retries=0,
        )
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
        )
    except APITimeoutError:
        return "OpenRouter did not respond within 45 seconds. Check your connection and try again."
    except APIConnectionError:
        return "Could not connect to OpenRouter. Check your internet connection and try again."
    except APIStatusError as error:
        return f"OpenRouter returned HTTP {error.status_code}: {error.message}"

    answer = response.choices[0].message.content
    if not isinstance(answer, str) or not answer.strip():
        return "OpenRouter returned an empty AI response."
    return answer.strip()
