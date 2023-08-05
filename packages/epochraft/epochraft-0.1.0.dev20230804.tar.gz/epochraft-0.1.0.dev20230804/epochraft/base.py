from __future__ import annotations

import abc
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
)

import numpy as np
import torch


if TYPE_CHECKING:
    import streaming
    from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast

    Tokenizer = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]


Sample = Dict[str, Any]
StateDict = Dict[str, Any]
TokenArray = Union[List[int], np.ndarray, torch.Tensor]
FilterMapFn = Callable[[Sample], Optional[Sample]]
CollateFn = Callable[[List[Sample]], Sample]
ParallelExecutorType = Literal["process", "thread"]


class CheckpointableIterator(abc.ABC):
    def __iter__(self) -> CheckpointableIterator:
        return self

    @abc.abstractmethod
    def __next__(self) -> Sample:
        raise NotImplementedError()

    @abc.abstractmethod
    def state_dict(self) -> StateDict:
        raise NotImplementedError


class CheckpointableDataset(torch.utils.data.IterableDataset, abc.ABC):
    def __iter__(self) -> CheckpointableIterator:
        return self.iter(state_dict=None)

    @abc.abstractmethod
    def iter(self, state_dict: Optional[StateDict] = None) -> CheckpointableIterator:
        raise NotImplementedError()

    @staticmethod
    def from_sequence(
        sequence: Sequence[Sample],
        repeat: bool = False,
        shuffle: bool = False,
        shuffle_seed: int = 42,
    ) -> CheckpointableDataset:
        from .sources import SequenceDataset

        return SequenceDataset(
            sequence=sequence, repeat=repeat, shuffle=shuffle, shuffle_seed=shuffle_seed
        )

    @staticmethod
    def from_iterable(
        iterable: Iterable[Sample],
        repeat: bool = False,
    ) -> CheckpointableDataset:
        """
        Create a CheckpointableDataset from an iterable.

        This static method creates a new CheckpointableDataset instance from an iterable.
        Each item in the iterable should be a `Sample` instance.

        The iterable should be a 're-iterable' and 'deterministic', i.e., it should return a new
        iterator each time `iter` is invoked and generate the same sequence of samples every time.
        This allows the successful resumption.
        """

        from .sources import IterableDataset

        return IterableDataset(iterable, repeat=repeat)

    @staticmethod
    def from_mosaicml(
        mosaicml_dataset: streaming.StreamingDataset,
        repeat: bool = False,
    ) -> CheckpointableDataset:
        from .sources import MosaicmlDataset

        return MosaicmlDataset(mosaicml_dataset, repeat=repeat)

    def filter_map(self, fn: FilterMapFn) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        return FilterMapDataset(self, fn)

    def map(self, fn: Callable[[Sample], Sample]) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        return FilterMapDataset(self, fn)

    def filter(self, fn: Callable[[Sample], bool]) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        def _fn(sample: Sample) -> Optional[Sample]:
            return sample if fn(sample) else None

        return FilterMapDataset(self, _fn)

    def parallel_filter_map(
        self,
        fn: FilterMapFn,
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms import ParallelFilterMapDataset

        return ParallelFilterMapDataset(
            self,
            fn,
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def parallel_map(
        self,
        fn: Callable[[Sample], Sample],
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms import ParallelFilterMapDataset

        return ParallelFilterMapDataset(
            self,
            fn,
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def parallel_filter(
        self,
        fn: Callable[[Sample], bool],
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms import ParallelFilterMapDataset

        def _fn(sample: Sample) -> Optional[Sample]:
            return sample if fn(sample) else None

        return ParallelFilterMapDataset(
            self,
            _fn,
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def enumerate(self, count_column: str = "step") -> CheckpointableDataset:
        from .transforms import CountDataset

        return CountDataset(self, count_column=count_column)

    def take(
        self,
        max_count: int,
    ) -> CheckpointableDataset:
        from .transforms import CountDataset

        return CountDataset(self, max_count=max_count)

    def batch(
        self,
        batch_size: int,
        collate_fn: CollateFn = torch.utils.data.default_collate,
        drop_last: bool = False,
    ) -> CheckpointableDataset:
        from .transforms import BatchDataset

        return BatchDataset(
            self, batch_size=batch_size, collate_fn=collate_fn, drop_last=drop_last
        )

    def concat_chunk(
        self,
        chunk_length: int,
        column: str = "input_ids",
        bos_tokens: Optional[TokenArray] = None,
        eos_tokens: Optional[TokenArray] = None,
    ) -> CheckpointableDataset:
        from .transforms import ConcatChunkDataset

        return ConcatChunkDataset(
            self,
            chunk_length=chunk_length,
            column=column,
            bos_tokens=bos_tokens,
            eos_tokens=eos_tokens,
        )

    def tokenize(
        self,
        tokenizer: Tokenizer,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        target_column: str = "text",
        parallel: bool = True,
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        tokenizer_kwargs = tokenizer_kwargs or {}

        def _fn(sample: Sample) -> Sample:
            sample.update(tokenizer(sample[target_column], **tokenizer_kwargs))
            return sample

        if parallel:
            # TODO: show some warning on this
            os.environ["TOKENIZERS_PARALLELISM"] = "false"

            return self.parallel_map(
                _fn,
                max_workers=max_workers,
                prefetch_factor=prefetch_factor,
                ordered=ordered,
                executor_type=executor_type,
            )
        else:
            return self.map(_fn)

    # `__add__` is implemented in PyTorch's `IterableDataset`,
    # so we need to override it here for prevent unexpected behavior
    def __add__(self, other: CheckpointableDataset) -> CheckpointableDataset:  # type: ignore
        from .combinations import concat_datasets

        return concat_datasets([self, other])
