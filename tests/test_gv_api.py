import pytest

from gvet import create_app
from gvet.gv.api import Vocabulary
from gvet.gv.queries import QueryService


class TestGettyVocabularyApi:
    @pytest.mark.skip
    @pytest.mark.integration
    def test_get_subject_by_id_with_cache(self):
        qs = QueryService()
        v = Vocabulary(qs)

        app = create_app()
        with app.app_context():
            subject = v.get_subject_detail("aat:300254607")
            assert subject.id == "aat:300254607"
            assert subject.name == "sponge boats"
            assert subject.record_type == "Concept"
            assert subject.terms
            assert subject.ancestors

    @pytest.mark.integration
    def test_get_subject_by_id_without_cache(self):
        qs = QueryService()
        v = Vocabulary(qs)

        subject = v.get_subject_detail("aat:300254607")
        assert subject.id == "aat:300254607"
        assert subject.name == "sponge boats"
        assert subject.record_type == "Concept"
        assert subject.terms
        assert subject.ancestors

    @pytest.mark.integration
    def test_search(self):
        v = Vocabulary()
        result = v.search("bear")
        assert result
