from django.core.management import BaseCommand
from django.urls import URLPattern, URLResolver
from django.urls import resolvers


class Command(BaseCommand):

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **kwargs):

        urls = resolvers.get_resolver()
        all_urls = list()

        def func_for_sorting(i):
            if i.name is None:
                i.name = ''
            return i.name

        def show_urls(urls):
            for url in urls.url_patterns:
                if isinstance(url, URLResolver):
                    show_urls(url)
                elif isinstance(url, URLPattern):
                    all_urls.append(url)
        show_urls(urls)

        all_urls.sort(key=func_for_sorting, reverse=False)

        print('-' * 100)
        for url in all_urls:
            print('| {0.pattern} | {0.name} | {0.lookup_str} | {0.default_args} |'.format(url))
        print('-' * 100)