"""HuggingFace Text Generation Algorithm."""
from typing import Any, ClassVar, Dict, Mapping, Optional

from marshmallow import fields
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.types import T_FIELDS_DICT

DEFAULT_MAX_LENGTH = 50
DEFAULT_NUM_RETURN_SEQUENCES = 1
DEFAULT_SEED = 42

logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the TransformerTextGeneration algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any]) -> Dict[str, Any]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the TransformerTextGeneration algorithm."""

    def __init__(
        self,
        model_id: str,
        text_column_name: str,
        max_length: int,
        num_return_sequences: int,
        seed: int,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences
        self.seed = seed

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the model and tokenizer."""
        # TODO: [BIT-3097] Resolve initialise without DP
        if pod_dp:
            logger.warning("The use of DP is not supported, ignoring set `pod_dp`.")
        self.datasource = datasource
        set_seed(self.seed)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, trust_remote_code=True
        )

    def run(self) -> Any:
        """Runs the pipeline to generate text."""
        generator = pipeline(
            "text-generation",
            model=self.model,
            pad_token_id=self.tokenizer.eos_token_id,
            device_map="auto",
            tokenizer=self.tokenizer,
            return_full_text=False,
        )
        results = generator(
            self.datasource.get_column(self.text_column_name).tolist(),
            max_length=self.max_length,
            num_return_sequences=self.num_return_sequences,
        )
        return results


class TransformerTextGeneration(BaseAlgorithmFactory):
    """HuggingFace Text Generation Algorithm.

    Args:
        model_id: The model id to use for text generation.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The signle column to query against. Should contain
            text for generation.
        max_length: The maximum length of the sequence to be generated. Defaults to 50.
        num_return_sequences: The number of sequence candidates to return
            for each input. Defaults to 1.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.

    Attributes:
        model_id: The model id to use for text generation.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The signle column to query against. Should contain
            text for generation.
        max_length: The maximum length of the sequence to be generated. Defaults to 50.
        num_return_sequences: The number of sequence candidates to return
            for each input. Defaults to 1.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
    """

    def __init__(
        self,
        model_id: str,
        text_column_name: str,
        max_length: int = DEFAULT_MAX_LENGTH,
        num_return_sequences: int = DEFAULT_NUM_RETURN_SEQUENCES,
        seed: int = DEFAULT_SEED,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences
        self.seed = seed

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "text_column_name": fields.Str(required=True),
        "max_length": fields.Int(required=False, missing=DEFAULT_MAX_LENGTH),
        "num_return_sequences": fields.Int(
            required=False, missing=DEFAULT_NUM_RETURN_SEQUENCES
        ),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the TransformerTextGeneration algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the TransformerTextGeneration algorithm."""
        return _WorkerSide(
            model_id=self.model_id,
            text_column_name=self.text_column_name,
            max_length=self.max_length,
            num_return_sequences=self.num_return_sequences,
            seed=self.seed,
            **kwargs,
        )
