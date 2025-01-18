from gvet.gv.queries import QueryService, QueryResult
import pytest


class TestQueryService:
    @pytest.fixture
    def query_service(self) -> QueryService:
        return QueryService()

    def test_determines_default_template_location(self, query_service: QueryService):
        query_service.template_folder.exists()

    def test_loads_templates_on_init(self, query_service: QueryService):
        assert query_service.templates
        assert query_service.templates["get_notes"]

    def test_can_prepare_query(self, query_service: QueryService):
        query_service.set_template("test", "this is the @{id} for the template")
        query_text = query_service.prepare_named_query("test", id="aat:30022688")
        assert query_text == "this is the aat:30022688 for the template"

    def test_raises_exception_if_query_name_not_found(
        self, query_service: QueryService
    ):
        with pytest.raises(ValueError):
            query_service.prepare_named_query("popeye")

    def test_get_results(self, query_service: QueryService):
        result = query_service.execute_named_query(
            "get_ancestors", subject_id="aat:300226882"
        )
        assert type(result) is QueryResult
        assert result.execution_time_seconds < 1
