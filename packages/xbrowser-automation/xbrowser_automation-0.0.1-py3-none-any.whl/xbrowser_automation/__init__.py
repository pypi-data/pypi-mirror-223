
import argparse

from importlib.resources import files as resources_files

from voila.app import main as voila_main


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ip',
        default='localhost',
        help='The IP address server will listen on.',
        required=False,
        type=str,
    )
    parser.add_argument(
        '--port',
        default=80,
        help='Port of the application',
        required=False,
        type=int,
    )
    parser.add_argument(
        '--show_tracebacks',
        default=True,
        help='Whether to send tracebacks to clients on exceptions.',
        required=False,
        type=bool,
    )
    parser.add_argument(
        '--enable_nbextensions',
        default=True,
        help='Set to True for Voilà to load notebook extensions',
        required=False,
        type=bool,
    )

    args = parser.parse_args(argv)
    voila_main([
        str(resources_files('xbrowser_automation') / 'xbrowser_automation.ipynb'),
        f'--show_tracebacks={args.show_tracebacks}',
        f'--enable_nbextensions={args.enable_nbextensions}',
        f'--Voila.ip={args.ip}',
        f'--Voila.port={args.port}',
    ])
