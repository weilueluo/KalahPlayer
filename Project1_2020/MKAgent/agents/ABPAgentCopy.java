package MKAgent.agents;

import MKAgent.Board;
import MKAgent.Side;
import MKAgent.alphaBetaPruning.AlphaBetaPruning;
import MKAgent.alphaBetaPruning.AlphaBetaPruningCopy;

import static MKAgent.alphaBetaPruning.AlphaBetaPruningCopy.alphaBetaPruning;

public class ABPAgentCopy implements Agent {

    private final int DEPTH;
    private final int THREAD_DEPTH;

    public ABPAgentCopy(int depth, int threadDepth) {
        this.DEPTH = depth;
        this.THREAD_DEPTH = threadDepth;
    }

    @Override
    public int getMove(Board board, Side side) {
        AlphaBetaPruningCopy.Result result = alphaBetaPruning(board, side, 0, Integer.MIN_VALUE, Integer.MAX_VALUE, DEPTH, THREAD_DEPTH);
        return result.move;
    }
}
