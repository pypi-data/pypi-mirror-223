import json
import os
import re
import uuid
from typing import Any, Dict, List, Optional, Union

import requests

from orkg.common import OID
from orkg.out import OrkgResponse


def _validate_doi(doi: str) -> bool:
    """Check if a string is a valid DOI or a complete DOI URL."""
    if doi is None:
        return False

    # DOI pattern.
    doi_pattern = re.compile(r"^10.\d{4,9}/[-._;()/:A-Z0-9]+$", re.I)

    # DOI URL pattern.
    url_pattern = re.compile(r"^https?://doi\.org/10.\d{4,9}/[-._;()/:A-Z0-9]+$", re.I)

    return bool(doi_pattern.match(doi) or url_pattern.match(doi))


def _process_contribution(
    contribution_json: Union[Dict, List, str],
    resulting_object: Union[Dict, List],
    global_ids: Dict,
    context: Dict,
):
    if isinstance(contribution_json, List):
        for item in contribution_json:
            _process_contribution(item, resulting_object, global_ids, context)
    elif isinstance(contribution_json, Dict):
        if isinstance(resulting_object, List):
            current_object = {}
            resulting_object.append(current_object)
            resulting_object = current_object
        for key, value in contribution_json.items():
            if key == "@id":
                global_ids[value] = "_" + str(uuid.uuid4())
                resulting_object["@temp"] = global_ids[value]
            elif key == "@type":
                resulting_object["classes"] = [
                    clazz.rsplit("/", 1)[-1] for clazz in contribution_json[key]
                ]
            elif key == "label":
                resulting_object["label"] = str(contribution_json[key])
            elif key == "@context":
                continue
            else:
                orkg_predicate_id = context[key].rsplit("/", 1)[-1]
                # other keys
                if "values" not in resulting_object:
                    resulting_object["values"] = {}
                if isinstance(value, List) and all(
                    isinstance(item, str) for item in value
                ):
                    resulting_object["values"][orkg_predicate_id] = [
                        {"text": str(item)} for item in value
                    ]
                elif isinstance(value, List) or isinstance(value, Dict):
                    predicate_values = []
                    resulting_object["values"][orkg_predicate_id] = predicate_values
                    _process_contribution(value, predicate_values, global_ids, context)
                else:
                    # Check if the value starts with "_:"
                    # FIXME: Workaround because the descriptions aren't up to date!!
                    if key not in context:
                        orkg_predicate_id = f"CSVW_{key.title()}"
                    resulting_object["values"][orkg_predicate_id] = []
                    if isinstance(value, str) and value.startswith("_:"):
                        resulting_object["values"][orkg_predicate_id].append(
                            {"@id": global_ids[value]}
                        )
                    else:
                        resulting_object["values"][orkg_predicate_id].append(
                            {"text": str(value)}
                        )


def harvest(
    orkg_client: Any,
    doi: Optional[str],
    orkg_rf: Union[str, OID],
    directory: Optional[str],
) -> OrkgResponse:
    if doi is None and directory is None:
        raise ValueError("Either doi or directory must be provided.")

    contributions_urls = []
    doi_response = None

    # Check if directory is provided and all is valid
    if directory is not None:
        if not os.path.isdir(directory):
            raise ValueError(f"The directory {directory} does not exist.")
        if doi is None and not os.path.isfile(os.path.join(directory, "doi.json")):
            raise ValueError(
                f"The directory {directory} does not contain the file doi.json."
            )
        if os.path.isfile(os.path.join(directory, "doi.json")):
            with open(os.path.join(directory, "doi.json")) as f:
                doi_response = json.load(f)
    if doi_response is None:
        doi_response, contributions_urls = _get_doi_response(doi)

    if isinstance(orkg_rf, str):
        rf_response = orkg_client.resources.get(q=orkg_rf, exact=True, size=1)
        if not rf_response.succeeded or len(rf_response.content) == 0:
            raise ValueError(
                f"Unable to find the ORKG research field with the given string value {orkg_rf}"
            )
        orkg_rf = OID(rf_response.content[0]["id"])

    doi_content = doi_response["data"]
    paper_json = {
        # TODO: handle multiple titles
        "title": doi_content["attributes"]["titles"][0]["title"],
        "doi": doi_content["attributes"]["doi"],
        "authors": [
            {"label": f'{creator["givenName"]} {creator["familyName"]}'}
            for creator in doi_content["attributes"]["creators"]
        ],
        "publicationYear": int(doi_content["attributes"].get("publicationYear"))
        if doi_content["attributes"].get("publicationYear")
        else None,
        "publishedIn": doi_content["attributes"].get("publisher", None),
        "researchField": f"{orkg_rf}",
    }

    if "contributions" not in paper_json:
        paper_json["contributions"] = []

    # Get the contribution content and override if directory is provided
    contribution_content = [requests.get(url).json() for url in contributions_urls]
    if directory is not None:
        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f != "doi.json"
        ]
        contribution_content = []
        for file in files:
            with open(os.path.join(directory, file)) as f:
                contribution_content.append(json.load(f))

    for contribution_json in contribution_content:
        orkg_contribution_json = {}
        global_ids = {}
        context = contribution_json["@context"]
        _process_contribution(
            contribution_json, orkg_contribution_json, global_ids, context
        )
        # replace the key "label" with "name"
        orkg_contribution_json["name"] = orkg_contribution_json.pop("label")
        paper_json["contributions"].append(orkg_contribution_json)
    # Now that we have everything, let's finalize the paper object and add it to the graph
    paper_json = {"paper": paper_json}
    return orkg_client.papers.add(paper_json)


def _get_doi_response(doi: str):
    # TODO: activate after stable DOIs are used
    # # Check if the doi is a valid DOI string
    # if not _validate_doi(doi):
    #     raise ValueError(f'{doi} is not a valid DOI string')

    # Get the content behind the DOI
    url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.status_code != 200:
        raise ValueError(f"Unable to retrieve the content behind the DOI {doi}")
    response = response.json()

    # get contribution info
    contributions_urls = [
        url["relatedIdentifier"]
        for url in filter(
            lambda x: x["relationType"] == "IsSupplementedBy"
            and x["relatedIdentifierType"] == "URL",
            response["data"]["attributes"]["relatedIdentifiers"],
        )
    ]
    return response, contributions_urls
