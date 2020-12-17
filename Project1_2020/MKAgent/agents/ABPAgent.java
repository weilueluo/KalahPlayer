package MKAgent.agents;

import MKAgent.Utils;
import MKAgent.alphaBetaPruning.AlphaBetaPruning;
import MKAgent.Board;
import MKAgent.Side;
import java.util.function.BiFunction;

import static MKAgent.alphaBetaPruning.AlphaBetaPruning.alphaBetaPruning;

public class ABPAgent implements Agent {

    private final int DEPTH;
    private final int THREAD_DEPTH;

    public ABPAgent(int depth, int threadDepth) {
        this.DEPTH = depth;
        this.THREAD_DEPTH = threadDepth;
    }

    @Override
    public int getMove(Board board, Side side) {
        AlphaBetaPruning.Result result = alphaBetaPruning(board, side, 0, Integer.MIN_VALUE, Integer.MAX_VALUE, DEPTH, THREAD_DEPTH);
        return result.move;
    }
}
