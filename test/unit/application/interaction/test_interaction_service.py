import unittest
from mock import MagicMock

from src.application.interaction.interaction_service import InteractionService
from src.domain.input_text.input_text_processor import InputTextProcessor
from src.domain.interaction.interaction_context import InteractionContext


class TestInteractionService(unittest.TestCase):

    _SOME_INPUT_TEXT = "input text"
    _SOME_OUTPUT_TEXT = "output text"

    def setUp(self):
        self.interaction_context_mock = MagicMock(spec=InteractionContext)
        self.input_text_processor_mock = MagicMock(spec=InputTextProcessor)
        self.interaction_service = InteractionService(self.interaction_context_mock, self.input_text_processor_mock)

    def test__when__processing_input_text__then__fetch_next_interaction_phase_according_to_given_input_text(self):
        self.interaction_service.process_input_text(self._SOME_INPUT_TEXT)

        self.interaction_context_mock.fetch_next_interaction_phase.assert_called_once_with(self._SOME_INPUT_TEXT)

    def test__when__processing_input_text__then__fetched_interaction_phase_is_processing_input_text_with_input_text_processor(
        self
    ):
        next_interaction_phase_mock = MagicMock()
        self.interaction_context_mock.fetch_next_interaction_phase.return_value = next_interaction_phase_mock
        self.interaction_service.process_input_text(self._SOME_INPUT_TEXT)

        next_interaction_phase_mock.process_input_text.assert_called_once_with(
            self._SOME_INPUT_TEXT, self.input_text_processor_mock
        )

    def test__when__processing_input_text__then__returns_output_from_processing_in_tuple_with_next_interaction_phase(
        self
    ):
        next_interaction_phase_mock = MagicMock()
        self.interaction_context_mock.fetch_next_interaction_phase.return_value = next_interaction_phase_mock
        next_interaction_phase_mock.process_input_text.return_value = self._SOME_OUTPUT_TEXT
        expected_response = self._SOME_OUTPUT_TEXT, next_interaction_phase_mock

        actual_response = self.interaction_service.process_input_text(self._SOME_INPUT_TEXT)

        self.assertEqual(expected_response, actual_response)

