import sys
import pytest

from unittest.mock import MagicMock

# Mock modules before importing utils
for mod in ['lxml', 'lxml.etree', 'Evtx', 'Evtx.Evtx', 'pandas', 'sentence_transformers', 'lancedb', 'tqdm', 'ollama', 'evtx', 'matplotlib', 'seaborn', 'pyarrow', 'requests']:
    sys.modules[mod] = MagicMock()

sys.path.append('.')

from src.utils import clean_xml_to_string, etree

def test_clean_xml_to_string_disables_entities():
    # Setup mock parser and fromstring
    mock_parser_instance = MagicMock()
    etree.XMLParser.return_value = mock_parser_instance

    mock_elem1 = MagicMock()
    mock_elem1.text = "value1"
    mock_elem1.get.return_value = "Key1"

    mock_root = MagicMock()
    mock_root.iter.return_value = [mock_elem1]

    etree.fromstring.return_value = mock_root

    # Test
    xml = "<root><Event>Test</Event></root>"
    result = clean_xml_to_string(xml)

    # Verify XMLParser was created with resolve_entities=False
    etree.XMLParser.assert_called_once_with(resolve_entities=False)

    # Verify fromstring used the custom parser
    etree.fromstring.assert_called_once_with(xml, parser=mock_parser_instance)

    # Verify normal behavior works
    assert "Key1: value1" in result

if __name__ == "__main__":
    pytest.main([__file__])
