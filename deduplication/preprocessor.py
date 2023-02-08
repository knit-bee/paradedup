import re
from dataclasses import dataclass
from typing import Set


@dataclass
class Preprocessor:
    shingle_size: int = 3
    case_insensitive: bool = False
    ignore_nums: bool = False
    normalize_whitespace: bool = False
    ignore_interpunctuation: bool = False
    use_token: bool = True

    def preprocess_document(self, document: str) -> str:
        text = re.sub("\n", " ", document)
        if self.case_insensitive:
            text = text.lower()
        if self.ignore_nums:
            text = re.sub(r"\d", "", text)
        if self.normalize_whitespace:
            text = re.sub(r"\s+", " ", text)
        if self.ignore_interpunctuation:
            text = re.sub(r"[^\w\s\dÄÖÜäöüẞß]", "", text)
        return text

    def create_shingle_set(self, document: str) -> Set[str]:
        if self.use_token:
            pattern = r"(\w)([^\w\d\sÄÖÜöäüẞß])"
            text = re.sub(pattern, r"\1 \2", document)
            tokens = text.split()
            if self.shingle_size > 1 and len(tokens) % self.shingle_size != 0:
                tokens.extend(
                    [""] * (self.shingle_size - (len(tokens) % self.shingle_size))
                )
            return {
                "~".join(tokens[i : i + self.shingle_size])
                for i in range(len(tokens) - (self.shingle_size - 1))
            }
        return {
            document[i : i + self.shingle_size]
            for i in range(len(document) - (self.shingle_size) - 1)
        }
