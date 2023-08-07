#  Copyright (c) 2023, Andreas Kirsch, Daedalus Lab Ltd
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

import typing
from typing import Tuple

from langchain.output_parsers import PydanticOutputParser
from langchain.schema import OutputParserException
from pydantic import create_model

from llm_strategy.chat_chain import ChatChain

T = typing.TypeVar("T")


def structured_query(chain: ChatChain, question: str, return_type: type[T]) -> Tuple[T, ChatChain]:
    """Asks a question and returns the result in a single block."""
    # TOOD: deduplicate
    if typing.get_origin(return_type) is typing.Annotated:
        return_info = typing.get_args(return_type)
    else:
        return_info = (return_type, ...)

    output_model = create_model("StructuredOutput", result=return_info)  # type: ignore
    parser = PydanticOutputParser(pydantic_object=output_model)
    question_and_formatting = question + "\n\n" + parser.get_format_instructions()

    num_retries = 3
    prompt = question_and_formatting
    for _ in range(num_retries):
        try:
            reply_content, chain = chain.query(prompt)
            parsed_reply = parser.parse(reply_content)
            break
        except OutputParserException as e:
            prompt = (
                "Tried to parse your last output but failed:\n\n"
                + str(e)
                + "\n\nPlease try again and avoid this issue."
            )
    else:
        raise OutputParserException(f"Failed to parse output after {num_retries} retries.")

    result = parsed_reply.result  # type: ignore
    return result, chain
