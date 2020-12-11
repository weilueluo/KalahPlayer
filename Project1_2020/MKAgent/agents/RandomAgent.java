package MKAgent.agents;

import MKAgent.Board;
import MKAgent.Kalah;
import MKAgent.Side;
import MKAgent.agents.Agent;

import java.util.List;
import java.util.Random;

public class RandomAgent implements Agent {

    private static final Random random = new Random();

    @Override
    public int getMove(Board board, Side side) {
        List<Integer> validMoves = Kalah.getAllValidMoves(board, side);
        return validMoves.get(random.nextInt(validMoves.size()));
    }
}
