import csv
import json
from typing import Any, Optional, Dict, List, Set

from llm_friendly.aws import table_parser

MODE_CSV = 'csv'
MODE_JSON = 'json'
MODE_MARKDOWN = 'markdown'


def to_llm_output(textract_response: Dict[str, Any], mode=MODE_CSV) -> str:
    """
    Convert a Textract Response to CSV
    :param mode: MODE_CSV, MODE_JSON or MODE_MARKDOWN
    :param textract_response: JSON Response from Textract API
    :return: CSV String
    """
    blocks = textract_response.get('Blocks', [])
    analyze_document_text = ""
    blocks_to_ignore = set()

    for item in blocks:
        if item['BlockType'] == 'TABLE':
            blocks_to_ignore.update(_get_children_ids_recursively(blocks, item['Id']))

    for item in blocks:
        if item['BlockType'] == 'TABLE':
            csv_string = table_parser.get_table_as_csv(blocks, item)

            if mode == MODE_CSV:
                analyze_document_text += csv_string + '\n'
            elif mode == MODE_JSON:
                analyze_document_text += _csv_to_json(csv_string) + '\n'
            elif mode == MODE_MARKDOWN:
                analyze_document_text += _csv_to_markdown(csv_string) + '\n'

        already_analyzed_as_table = _is_id_in_set_or_children(blocks, item['Id'], blocks_to_ignore)

        if item['BlockType'] == 'LINE' and not already_analyzed_as_table:
            analyze_document_text += item['Text'] + '\n'

    return analyze_document_text


def _csv_to_json(csv_string: str) -> str:
    csv_string = csv_string.strip()

    csv_reader = csv.DictReader(csv_string.splitlines())
    csv_list = list(csv_reader)

    # delete empty headers
    for row_dict in csv_list:
        if "" in row_dict:
            del row_dict[""]

    return json.dumps(csv_list)


def _csv_to_markdown(csv_string: str) -> str:
    rows = csv_string.strip().splitlines()

    columns = rows[0].split(",")

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    # Convert each row of the CSV data into a row of the Markdown table
    md_rows = [header, separator]
    for row in rows[1:]:
        cells = row.split(",")
        md_row = "| " + " | ".join(cells) + " |"
        md_rows.append(md_row)

    md_table = "\n".join(md_rows)

    return md_table


def _get_children_ids_recursively(data: List[Dict[str, Any]], target_id: str) -> Set[str]:
    ids: Set[str] = set()
    index = _find_element_index(data, target_id)

    if index is not None:
        children_ids = []

        for rel in data[index].get('Relationships', []):
            if rel['Type'] == 'CHILD':
                children_ids.extend(rel['Ids'])

        for child_id in children_ids:
            ids.add(child_id)
            ids.update(_get_children_ids_recursively(data, child_id))

    return ids


def _is_id_in_set_or_children(data, target_id, id_set):
    index = _find_element_index(data, target_id)
    if index is not None:
        if data[index]['Id'] in id_set:
            return True
        children_ids = []
        for rel in data[index].get('Relationships', []):
            if rel['Type'] == 'CHILD':
                children_ids.extend(rel['Ids'])
        for child_id in children_ids:
            if _is_id_in_set_or_children(data, child_id, id_set):
                return True
    return False


def _find_element_index(data, target_id) -> Optional[int]:
    for i, elem in enumerate(data):
        if elem['Id'] == target_id:
            return i
    return None


# This is `module.exports` in the Python land
__all__ = [
    'to_llm_output'
]
