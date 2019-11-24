import MinesweeperBoard


def test_knowledge_state():
    state = MinesweeperBoard.KnowledgeState.FLAGGED
    assert str(state) == '#'
