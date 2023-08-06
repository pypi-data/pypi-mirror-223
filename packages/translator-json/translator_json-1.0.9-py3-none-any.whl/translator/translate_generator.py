import json
import os
import re

import click
from google.cloud import translate
from google.cloud import translate_v3 as translate
from google.cloud.translate_v3.types import translation_service
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

from translator.glossary import GlossaryModule
from translator.utils import read_json_file, get_all_files

source = 'fr'
DEFAULT_LANGUAGES = ['en', 'de', 'ko']
location = 'us-central1'

credentials = None
glossary_conf = None

"""
    Translate text to a target language
    exclude params
    :arg text - text to translate
    :arg target - target language
    :return translated text
"""


def translate_text(text, target, translate_client, glossary,
                   parent) -> translation_service.TranslateTextResponse:
    # Find translate params
    params = re.findall(r"{{\w+}}", text)
    for param in params:
        parsedParam = param.replace(
            '{{', '<span translate="no">').replace('}}', '</span>')
        # no translate params
        text = text.replace(param, parsedParam)

    if glossary is not None:
        glossary_config = translate.TranslateTextGlossaryConfig(
            glossary=glossary
        )

        return translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "fr",
                "target_language_code": target,
                "glossary_config": glossary_config,
            }
        )

    return translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "fr",
            "target_language_code": target,
        }
    )


"""
    Translate all values from dictionary data to language dest
    :argument
        data: dictionary
        language: language dest
    :return
        translated dictionary
"""


def translate_language(data, language, translate_client, glossary, parent):
    for key in data.keys():
        if isinstance(data[key], str):
            value = data[key]

            if not value:
                data[key] = value
            else:
                translation = translate_text(
                    value,
                    language,
                    translate_client,
                    glossary,
                    parent
                )
                if translation.glossary_translations[0]:
                    t = translation.glossary_translations[0]
                else:
                    t = translation.translations[0]
                data[key] = t.translated_text.replace(
                    '<span translate="no">', '{{').replace('</span>', '}}')
        else:
            translate_language(
                data[key],
                language,
                translate_client,
                glossary,
                parent
            )


def silent_remove(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")


def write_translate_file(file_name, data, language):
    # output file
    output_file = os.path.dirname(file_name)
    # delete old version file
    silent_remove(f"{output_file}/{language}.json")
    with open(
            f"{output_file}/{language}.json",
            'w',
            encoding='utf-8'
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_json_file(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


@click.command(help=f"""
Translate all the value of a json file in a language given in
argument using the google translate
API. The supported language are English, Deutsch, Korean and French.
""")
@click.option('--credentials', '-c', type=str,
              help='google key credentials file')
@click.option('--input', '-i', type=str, default=None,
              help='path to the json file to translate')
@click.option('--output', '-o', type=str, default='.',
              help='path to the json file translated')
@click.option('--languages', '-l', default=None,
              help="""the language to translate
              must be 'en', 'de' or 'ko'""")
@click.option('--available', '-a',
              is_flag=True, default=False,
              help="List available languages")
@click.option('--glossary', '-g', default=None,
              help='Id of the glossary to be used for the translation')
@click.option('--folder', '-f', type=str, default=None,
              help='path to a folder and the program'
                   'will try to translate every file in it.')
def json_translator(
        credentials,
        input=None,
        output='.',
        languages=None,
        available=False,
        glossary=None,
        folder=None
):
    to_translate = []
    credentials = read_json_file(credentials)

    credentials_dist = service_account.Credentials.from_service_account_info(
        credentials
    )

    projectId = credentials['project_id']
    if not projectId:
        raise Exception('Project id not found')

    translate_client = translate.TranslationServiceClient(
        credentials=credentials_dist
    )

    if glossary is not None:
        glossary = translate_client.glossary_path(
            project=credentials['project_id'],
            location='us-central1',
            glossary=glossary
        )

    if available:
        response = translate_client.get_supported_languages(
            parent=f"projects/{projectId}/locations/{location}"
        )

        for language in response.languages:
            print("Language Code: {}".format(language.language_code))

        return

    if languages is None:
        languages = DEFAULT_LANGUAGES
    else:
        languages = languages.split(",")

    if input is not None:
        to_translate.append(input)

    if folder is not None:
        to_translate = get_all_files(folder, source)

    for file in to_translate:
        print(f"translate file {file} ...")
        for language in languages:
            f = open(file)
            data = json.load(f)
            f.close()
            translate_language(
                data,
                language,
                translate_client,
                glossary,
                f"projects/{projectId}/locations/{location}"
            )
            write_translate_file(file, data, language)


@click.command(help=f"""
    Provide a tool for create, update, list and delete google glossary
"""
               )
@click.option('--credentials', '-c', is_flag=False, type=str,
              help='Set the credentials file', required=True,
              default=None)
@click.option('--config', is_flag=False, type=str,
              help='Set the credentials file', default=None)
@click.option('--list', '-l', is_flag=True,
              help='List all glossary from json config file', default=False)
@click.option('--upload', '-u', type=str,
              help='Upload the glossary file to google storage', default=None)
@click.option('--create', '-a', is_flag=True, default=False,
              help='create the glossary file using the glossary config file '
                   'and the path of this option'
              )
@click.option('--remove', '-r', type=str, default=None,
              help='delete the glossary file according to this id')
def google_glossary(
        credentials=None,
        config=None,
        list=False,
        upload=None,
        create=False,
        remove=None
):
    credentials_file = read_json_file(credentials)

    glossary_config = read_json_file(config)

    credentials_dist: Credentials = Credentials.from_service_account_info(
        credentials_file
    )

    glossary_module = GlossaryModule(credentials=credentials_dist,
                                     config=glossary_config)

    if list:
        glossary_module.list_glossaries()

    if upload:
        glossary_module.upload_glossary(upload, credentials_dist)
        return

    if create:
        glossary_module.create_glossary(
            f"projects/{credentials_dist.project_id}/locations/us-central1")
        return

    if remove:
        glossary_module.delete_glossary(remove)


@click.group()
def cli():
    pass


if __name__ == '__main__':
    cli()
