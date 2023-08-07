#  Copyright (c) 2023, Andreas Kirsch, Daedalus Lab Ltd
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

import langchain
import pytest

from llm_strategy.testing import fake_llm

langchain.llm_cache = None


def test_fake_llm_query():
    """Test that the fake LLM returns the correct query."""
    llm = fake_llm.FakeLLM(texts={"foobar"})
    assert llm("foo") == "bar"


def test_fake_llm_query_with_stop():
    """Test that the fake LLM returns the correct query."""
    llm = fake_llm.FakeLLM(texts={"foobar"})
    assert llm("foo", stop=["a"]) == "b"


def test_fake_llm_missing_query():
    """Test that the fake LLM raises an error if the query is missing."""
    llm = fake_llm.FakeLLM(texts=set())
    with pytest.raises(NotImplementedError):
        raise ValueError(llm("foo"))
