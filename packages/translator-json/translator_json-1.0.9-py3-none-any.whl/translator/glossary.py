import os
from typing import List

from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import translate_v3 as translate

location = 'us-central1'


class GlossaryModule:

    def __init__(self, credentials: service_account.Credentials, config):
        self.credentials = credentials
        self.config = config
        self.client = translate.TranslationServiceClient(
            credentials=credentials)

    def upload_glossary(self, path, credentials):
        """Uploads a file to the bucket."""

        # initialize the storage client and give it the bucket and the blob
        # name
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(self.config['bucket'])
        file_name = os.path.basename(path)
        blob = bucket.blob(file_name)

        # upload the file to the bucket
        blob.upload_from_filename(path)
        print(f"{file_name} is uploaded successfully !")

    def to_language_code_pair(self, pair):
        return {
            'source_language_code': pair['from'],
            'target_language_code': pair['to']
        }

    def create_glossary(self, parent, timeout: int = 180):
        """Creates a GCP glossary resource
        Assumes you've already manually uploaded a glossary to Cloud Storage
        ARGS
        languages: list of languages in the glossary
        project_id: GCP project id
        glossary_name: name you want to give this glossary resource
        glossary_uri: the uri of the glossary you uploaded to Cloud Storage
        RETURNS
        nothing
        """

        project_id = self.config['project_id']
        glossary_id = self.config['id']
        language_codes = self.config['languages']
        glossary_uri = self.config['uri']
        language_pairs = list(
            map(self.to_language_code_pair, self.config['code_pair']))

        name = self.client.glossary_path(project_id, 'us-central1',
                                         glossary_id)
        language_codes_set = translate.types.Glossary.LanguageCodesSet(
            language_codes=language_codes
        )

        gcs_source = translate.types.GcsSource(input_uri=glossary_uri)

        input_config = translate.types.GlossaryInputConfig(
            gcs_source=gcs_source)

        glossary = translate.types.Glossary(
            name=name,
            language_codes_set=language_codes_set,
            input_config=input_config
        )

        operation = self.client.create_glossary(parent=parent,
                                                glossary=glossary)

        result = operation.result(timeout)
        print(f"Created: {result.name}")
        print(f"Input Uri: {result.input_config.gcs_source.input_uri}")

    def list_glossaries(self) -> List[translate.Glossary]:
        """List Glossaries.

        Returns:
            The glossaries.
        """

        parent = f"projects/{self.credentials.project_id}/locations/{location}"

        result = []

        # Iterate over all results
        for glossary in self.client.list_glossaries(parent=parent):
            print(f"Name: {glossary.name}")
            print(f"Entry count: {glossary.entry_count}")
            print(f"Input uri: {glossary.input_config.gcs_source.input_uri}")

            # Note: You can create a glossary using one of two modes:
            # language_code_set or language_pair. When listing the information
            # for a glossary, you can only get information for the mode
            # you used when creating the glossary.
            for language_code in glossary.language_codes_set.language_codes:
                print(f"Language code: {language_code}")

            result.append(glossary)

        return result

    def delete_glossary(
            self,
            glossary_id: str,
            timeout: int = 180,
    ) -> translate.Glossary:
        """Delete a specific glossary based on the glossary ID.

        Args:
            glossary_id: The ID of the glossary to delete.
            timeout: The timeout for this request.

        Returns:
            The glossary that was deleted.
        """

        name = self.client.glossary_path(self.credentials.project_id,
                                         "us-central1", glossary_id)

        operation = self.client.delete_glossary(name=name)
        result = operation.result(timeout)
        print(f"Deleted: {result.name}")

        return result
