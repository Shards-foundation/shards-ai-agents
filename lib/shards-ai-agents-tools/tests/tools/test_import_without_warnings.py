from pydantic.warnings import PydanticDeprecatedSince20
import pytest


@pytest.mark.filterwarnings("error", category=PydanticDeprecatedSince20)
def test_import_tools_without_pydantic_deprecation_warnings():
    # This test is to ensure that the import of shards_ai_agents_tools does not raise any Pydantic deprecation warnings.
    import shards_ai_agents_tools

    assert shards_ai_agents_tools
