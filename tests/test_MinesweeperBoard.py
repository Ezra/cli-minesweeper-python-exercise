from MinesweeperBoard import KnowledgeState, EndState, MinesweeperBoard


def test_knowledge_state():
    state = KnowledgeState.FLAGGED
    assert str(state) == '#'


def test_init():
    board = MinesweeperBoard(3, 3, 1)
    assert(not board.end_state)


def test_victory():
    board = MinesweeperBoard(2, 1, 1)
    assert(not board.end_state)
    board.step(0, 0)
    assert(board.end_state == EndState.VICTORY)
    board.step(1, 0)
    assert(board.end_state == EndState.VICTORY)
