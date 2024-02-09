import argparse
import json
import pathlib

from .const import FRONTEND_BACKEND_TRANSLATIONS, DOWNLOAD_DIR
from .download import run_download_docker
from .util import get_base_arg_parser, load_json_from_path


def get_arguments() -> argparse.Namespace:
    """Get parsed passed-in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--skip-download", action="store_true", help="Skip downloading translations."
    )
    return parser.parse_args()


def update_frontend_translations():
    """Update frontend translations with backend data."""
    args = get_arguments()

    if not args.skip_download:
        run_download_docker()

    for lang_file in DOWNLOAD_DIR.glob("*.json"):
        translations = load_json_from_path(lang_file)

        to_write_translations = {"component": {}}

        for domain, domain_translations in translations["component"].items():
            if "state" not in domain_translations:
                continue

            to_write_translations["component"][domain] = {
                "state": domain_translations["state"]
            }

        frontend_translation_path = FRONTEND_BACKEND_TRANSLATIONS / lang_file.name

        with open(frontend_translation_path, "w", encoding="utf-8") as f:
            json.dump(to_write_translations, f, indent=2)
            

def run():
    """Run the script."""
    update_frontend_translations()
