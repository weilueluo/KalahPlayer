package MKAgent;

import static MKAgent.AlphaBetaPruning.alphaBetaPruning;

public class ABPAgent implements Agent {

    private final int DEPTH;
    public ABPAgent(int depth) {
        this.DEPTH = depth;
    }

    @Override
    public int getMove(Board board, Side side) {
        try {
            int maxReturn = board.getNoOfHoles() * board.getNoOfSeeds() + 1;
            AlphaBetaPruning.Result result = alphaBetaPruning(board, side, -maxReturn, maxReturn, DEPTH);
            return result.move;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}
