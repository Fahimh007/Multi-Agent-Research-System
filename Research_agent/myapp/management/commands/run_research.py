from django.core.management.base import BaseCommand
from myapp.pipelines.pipeline import run_research_pipeline


class Command(BaseCommand):
    help = 'Run the research pipeline from Django management command'

    def add_arguments(self, parser):
        parser.add_argument(
            'topic',
            nargs='?',
            default='The impact of AI on the job market in 2026',
            help='Topic to research',
        )

    def handle(self, *args, **options):
        topic = options['topic']
        result = run_research_pipeline(topic)
        self.stdout.write(self.style.SUCCESS(f"Research pipeline completed: {result}"))
