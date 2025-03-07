


# Load API key from environment variable
HF_API_KEY = "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"

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from huggingface_hub import InferenceClient

TEMPLATES = {
    "job_application": " In 300 tokens Write a professional email applying for a software engineer position.",
    "business_proposal": "in 300 tokens Write a formal email proposing a business collaboration.",
    "client_followup": "in 300 tokens Write a polite follow-up email to a client about a previous discussion."
}

@csrf_exempt  # Disable CSRF for simplicity (only for development)
def generate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            template = data.get("template", "custom")
            custom_prompt = data.get("customPrompt", "").strip()

            prompt = TEMPLATES.get(template, custom_prompt) if template != "custom" else custom_prompt
            if not prompt:
                return JsonResponse({"error": "Prompt cannot be empty"}, status=400)

            client = InferenceClient(api_key=HF_API_KEY)
            response = client.text_generation(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                prompt=prompt,
                max_new_tokens=300
            )

            return JsonResponse({"response": response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

def home(request):
    return render(request, "generator/index.html")