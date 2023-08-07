#  Copyright (c) 2023, Andreas Kirsch, Daedalus Lab Ltd
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

from langchain.schema import AIMessage, HumanMessage

from llm_strategy.chat_chain import ChatChain
from llm_strategy.structured_query import structured_query
from llm_strategy.testing.fake_chat_model import FakeChatModel


def test_structured_query():
    chat_model = FakeChatModel.from_messages(
        [
            [
                HumanMessage(
                    content=(
                        "Return 1 as string\n\nThe output should be formatted as a JSON instance that conforms to "
                        'the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": '
                        '"Foo", "description": "a list of strings", "type": "array", "items": {"type": '
                        '"string"}}}, "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a '
                        'well-formatted instance of the schema. The object {"properties": {"foo": ["bar", '
                        '"baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"properties": {'
                        '"result": {"title": "Result", "type": "string"}}, "required": ["result"]}\n```'
                    ),
                    additional_kwargs={},
                ),
                AIMessage(content='{"result": "1"}', additional_kwargs={}),
            ]
        ]
    )

    def f():
        chain = ChatChain(chat_model, [])
        result, new_chain = structured_query(chain, "Return 1 as string", str)
        assert result == "1"
        assert len(new_chain.messages) == 2

    f()


def test_structured_query_retry():
    chat_model = FakeChatModel.from_messages(
        [
            [
                HumanMessage(
                    content=(
                        "Return 1 as string\n\nThe output should be formatted as a JSON instance that conforms to "
                        'the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": '
                        '"Foo", "description": "a list of strings", "type": "array", "items": {"type": '
                        '"string"}}}, "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a '
                        'well-formatted instance of the schema. The object {"properties": {"foo": ["bar", '
                        '"baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"properties": {'
                        '"result": {"title": "Result", "type": "string"}}, "required": ["result"]}\n```'
                    ),
                    additional_kwargs={},
                ),
                AIMessage(content='The result is: "1".', additional_kwargs={}),
                HumanMessage(
                    content=(
                        "Tried to parse your last output but failed:\n\nFailed to parse StructuredOutput from "
                        'completion The result is: "1".. Got: Expecting value: line 1 column 1 (char 0)\n\nPlease '
                        "try again and avoid this issue."
                    ),
                    additional_kwargs={},
                ),
                AIMessage(content='My apologies. The result should be: {"result": "1"}', additional_kwargs={}),
            ]
        ]
    )

    def f():
        chain = ChatChain(chat_model, [])
        result, new_chain = structured_query(chain, "Return 1 as string", str)
        assert result == "1"
        assert len(new_chain.messages) == 4

    f()
