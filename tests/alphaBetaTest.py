import sys
sys.path.append('../alpha_beta_pruning')
import alpha_beta_pruning
from mancala import Mancala

def test_is_max_node():
    assert alpha_beta_pruning.is_max_node('north') == False
    assert alpha_beta_pruning.is_max_node('south') == True

def test_get_south_scores():
    mancala = Mancala()
    assert alpha_beta_pruning.get_south_scores(mancala) == 0
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.get_south_scores(mancala) == 2
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,4])
    assert alpha_beta_pruning.get_south_scores(mancala) == 4

def test_get_north_scores():
    mancala = Mancala()
    assert alpha_beta_pruning.get_north_scores(mancala) == 0
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.get_north_scores(mancala) == 2
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,8,1,1,10,10,10,9,9,4])
    assert alpha_beta_pruning.get_north_scores(mancala) == 8


def test_get_heuristics():
    mancala = Mancala()
    assert alpha_beta_pruning.get_heuristics(mancala) == 0
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.get_heuristics(mancala) == 0
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,8,1,1,10,10,10,9,9,4])
    assert alpha_beta_pruning.get_heuristics(mancala) == -4

def test_is_terminal_node():
    mancala = Mancala()
    assert alpha_beta_pruning.is_terminal_node(mancala) == False
    ancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.is_terminal_node(mancala) == False
    mancala = Mancala(7,7,[0,0,0,0,0,0,0,50,0,0,10,10,10,9,9,2])
    assert alpha_beta_pruning.is_terminal_node(mancala) == True

def test_is_empty_hole():
    mancala = Mancala()
    assert alpha_beta_pruning.is_empty_hole(mancala ,0) == False
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.is_empty_hole(mancala ,4) == True
    assert alpha_beta_pruning.is_empty_hole(mancala ,5) == False


def test_get_all_possible_moves():
    mancala = Mancala(7,7,[1,9,8,8,0,9,9,2,1,1,10,10,10,9,9,2])
    assert alpha_beta_pruning.get_all_possible_moves(mancala, 'south')== [1,2,3,4,5,6,7]
    assert alpha_beta_pruning.get_all_possible_moves(mancala, 'north')== [1,2,3,4,6,7]

test_is_max_node()
test_get_south_scores()
test_get_north_scores()
test_get_heuristics()
test_is_terminal_node()
test_is_empty_hole()
test_get_all_possible_moves()
