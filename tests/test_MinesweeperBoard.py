import MinesweeperBoard

def test_knowledge_stat():
    state = MinesweeperBoard.KnowledgeState.FLAGGED
    assert str(state) == '#'
