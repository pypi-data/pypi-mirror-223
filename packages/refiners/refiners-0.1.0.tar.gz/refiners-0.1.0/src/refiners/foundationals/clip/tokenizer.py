import gzip
from pathlib import Path
from functools import lru_cache
from itertools import islice
import re
from torch import Tensor, tensor
from refiners.fluxion import pad


class CLIPTokenizer:
    def __init__(
        self,
        vocabulary_path: str | Path = Path(__file__).resolve().parent / "bpe_simple_vocab_16e6.txt.gz",
    ):
        self.vocabulary_path = vocabulary_path
        self.byte_to_unicode_mapping = self.get_bytes_to_unicode_mapping()
        self.byte_decoder = {v: k for k, v in self.byte_to_unicode_mapping.items()}
        merge_tuples = [
            tuple(merge.split())
            for merge in gzip.open(vocabulary_path).read().decode("utf-8").split("\n")[1 : 49152 - 256 - 2 + 1]
        ]
        vocabulary = (
            list(self.byte_to_unicode_mapping.values())
            + [v + "</w>" for v in self.byte_to_unicode_mapping.values()]
            + ["".join(merge) for merge in merge_tuples]
            + ["", ""]
        )
        self.token_to_id_mapping = {token: i for i, token in enumerate(vocabulary)}
        self.byte_pair_encoding_ranks = {merge: i for i, merge in enumerate(merge_tuples)}
        self.byte_pair_encoding_cache = {"": ""}
        # Note: this regular expression does not support Unicode. It was changed so
        # to get rid of the dependence on the `regex` module. Unicode support could
        # potentially be added back by leveraging the `\w` character class.
        self.token_pattern = re.compile(
            r"""<\|startoftext\|>|<\|endoftext\|>|'s|'t|'re|'ve|'m|'ll|'d|[a-zA-Z]+|[0-9]|[^\s\w]+""",
            re.IGNORECASE,
        )
        self.start_of_text_token_id: int = 49406
        self.end_of_text_token_id: int = 49407

    def __call__(self, text: str, sequence_length: int) -> Tensor:
        tokens = self.encode(text=text, max_length=sequence_length).unsqueeze(0)
        assert (
            tokens.shape[1] <= sequence_length
        ), f"Text is too long: tokens.shape[1] > sequence_length: {tokens.shape[1]} > {sequence_length}"
        return pad(tokens, (0, sequence_length - tokens.shape[1]), value=self.end_of_text_token_id)

    @lru_cache()
    def get_bytes_to_unicode_mapping(self) -> dict[int, str]:
        initial_byte_values = (
            list(range(ord("!"), ord("~") + 1))
            + list(range(ord("¡"), ord("¬") + 1))
            + list(range(ord("®"), ord("ÿ") + 1))
        )
        extra_unicode_values = (byte for byte in range(2**8) if byte not in initial_byte_values)
        byte_values = initial_byte_values + list(extra_unicode_values)
        unicode_values = [chr(value) for value in byte_values]
        return dict(zip(byte_values, unicode_values))

    def byte_pair_encoding(self, token: str) -> str:
        if token in self.byte_pair_encoding_cache:
            return self.byte_pair_encoding_cache[token]

        def recursive_bpe(word: tuple[str, ...]) -> tuple[str, ...]:
            if len(word) < 2:
                return word
            pairs = {(i, (word[i], word[i + 1])) for i in range(len(word) - 1)}
            min_pair = min(
                pairs,
                key=lambda pair: self.byte_pair_encoding_ranks.get(pair[1], float("inf")),
            )
            if min_pair[1] not in self.byte_pair_encoding_ranks:
                return word
            new_word: list[str] = []
            i = 0
            while i < len(word):
                if i == min_pair[0]:
                    new_word.append(min_pair[1][0] + min_pair[1][1])
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            return recursive_bpe(tuple(new_word))

        word = tuple(token[:-1]) + (token[-1] + "</w>",)
        result = " ".join(recursive_bpe(word))
        self.byte_pair_encoding_cache[token] = result
        return result

    def encode(self, text: str, max_length: int | None = None) -> Tensor:
        text = re.sub(r"\s+", " ", text.lower())
        tokens = re.findall(self.token_pattern, text)
        upper_bound = None
        if max_length:
            assert max_length >= 2
            upper_bound = max_length - 2
        encoded_tokens = islice(
            (
                self.token_to_id_mapping[subtoken]
                for token in tokens
                for subtoken in self.byte_pair_encoding(
                    "".join(self.byte_to_unicode_mapping[character] for character in token.encode("utf-8"))
                ).split(" ")
            ),
            0,
            upper_bound,
        )
        return tensor([self.start_of_text_token_id, *encoded_tokens, self.end_of_text_token_id])
