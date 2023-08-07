from typing import Dict, Any, List


# Source:
# https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html

def _get_rows_columns_map(table_result, blocks_map):
    rows = {}
    scores = []
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get confidence score
                    scores.append(str(cell['Confidence']))

                    # get the text value
                    rows[row_index][col_index] = _get_text(cell, blocks_map)
    return rows, scores


def _get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        if "," in word['Text'] and word['Text'].replace(",", "").isnumeric():
                            text += '"' + word['Text'] + '"' + ' '
                        else:
                            text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
    return text


def get_table_as_csv(blocks: List[Dict[str, Any]], table_block: Dict[str, Any], index=1) -> str:
    # Prepare Hashmap: blockId => Block
    blocks_map = {}
    for block in blocks:
        blocks_map[block['Id']] = block

    return _generate_table_csv(table_block, blocks_map, index)


def _generate_table_csv(table_result: Dict[str, Any], blocks_map: Dict[str, Any], table_index=1):
    rows, scores = _get_rows_columns_map(table_result, blocks_map)

    # get cells.
    csv = ''

    for row_index, cols in rows.items():
        for col_index, text in cols.items():
            csv += '{}'.format(text.strip()) + ","
        csv += '\n'

    csv += '\n\n\n'
    return csv
