import unittest
import mastermind_ai

class TestMastermindAI(unittest.TestCase):
    def setUp(self):
        self.pieces = mastermind_ai.toutes_pieces()
        self.empty_board = [None]*16

    def test_toutes_pieces(self):
        self.assertEqual(len(self.pieces), 16**1)  # 16 pièces uniques
        self.assertEqual(len(set(self.pieces)), 16)

    def test_coups_possibles(self):
        board = [None]*16
        self.assertEqual(mastermind_ai.coups_possibles(board), list(range(16)))
        board[0] = 'BSDF'
        self.assertNotIn(0, mastermind_ai.coups_possibles(board))

    def test_simule(self):
        board = [None]*16
        new_board = mastermind_ai.simule(board, 0, 'BSDF')
        self.assertEqual(new_board[0], 'BSDF')
        self.assertIsNot(board, new_board)

    def test_victoire_ligne(self):
        board = [None]*16
        for i in range(4):
            board[i] = 'BSDF'
        self.assertTrue(mastermind_ai.victoire(board))

    def test_victoire_colonne(self):
        board = [None]*16
        for i in range(0, 16, 4):
            board[i] = 'BSDF'
        self.assertTrue(mastermind_ai.victoire(board))

    def test_victoire_diagonale(self):
        board = [None]*16
        for i in range(0, 16, 5):
            board[i] = 'BSDF'
        self.assertTrue(mastermind_ai.victoire(board))

    def test_choose_move_first(self):
        state = {'board': [None]*16}
        move = mastermind_ai.choose_move(state)
        self.assertIn('piece', move)

    def test_choose_move_gagnant(self):
        board = [None]*16
        for i in range(3):
            board[i] = 'BSDF'
        state = {'board': board, 'piece': 'BSDF'}
        move = mastermind_ai.choose_move(state)
        self.assertEqual(move['pos'], 3)

    def test_pieces_disponibles(self):
        board = [None]*16
        board[0] = 'BSDF'
        dispo = mastermind_ai.pieces_disponibles(board, None)
        self.assertNotIn('BSDF', dispo)

if __name__ == '__main__':
    unittest.main()
