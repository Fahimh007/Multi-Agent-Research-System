import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from myapp.pipelines.pipeline import run_research_pipeline


def home(request):
    """Render the main research assistant page."""
    return render(request, "home.html", {})


@csrf_exempt
@require_http_methods(["POST"])
def run_research_view(request):
    """API endpoint that runs the research pipeline.

    Expects JSON body: {"topic": "..."}
    Returns JSON with the full pipeline result.
    """
    try:
        body = json.loads(request.body)
        topic = body.get("topic", "").strip()
    except (json.JSONDecodeError, AttributeError):
        topic = ""

    if not topic:
        return JsonResponse(
            {"status": "error", "message": "Please provide a research topic."},
            status=400,
        )

    try:
        result = run_research_pipeline(topic)
        return JsonResponse(result)
    except Exception as exc:
        traceback.print_exc()
        return JsonResponse(
            {"status": "error", "message": f"Pipeline error: {exc}"},
            status=500,
        )
