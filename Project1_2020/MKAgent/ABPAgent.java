package MKAgent;

import static MKAgent.AlphaBetaPruning.alphaBetaPruning;

public class ABPAgent implements Agent {

    private final int DEPTH;
    private final int THREAD_DEPTH;

    public ABPAgent(int depth, int threadDepth) {
        this.DEPTH = depth;
        this.THREAD_DEPTH = threadDepth;
    }

    @Override
    public int getMove(Board board, Side side) {
        int maxReturn = board.getNoOfHoles() * board.getNoOfSeeds() + 1;
        AlphaBetaPruning.Result result = alphaBetaPruning(board, side, 0, -maxReturn, maxReturn, DEPTH, THREAD_DEPTH);
        return result.move;
    }
}
