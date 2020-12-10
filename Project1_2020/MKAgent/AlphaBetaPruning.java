package MKAgent;

import java.sql.SQLOutput;
import java.util.List;
import java.util.function.BiFunction;

public class AlphaBetaPruning {

    public static class Result {
        public int move;
        public int score;
        private Result(int move, int score) {
            this.move = move;
            this.score = score;
        }

        private static Result of(int move, int score) {
            return new Result(move, score);
        }
    }

    public static boolean isMaxNode(Side side) {
        return side == Side.SOUTH;
    }

    public static int getHeuristic(Board board) {
        return board.getSeedsInStore(Side.SOUTH) - board.getSeedsInStore(Side.NORTH);
    }

    private static boolean isTerminal(Board board) {
        return board.state().isGameOver;
    }

    public static Result alphaBetaPruning(Board board, Side side, int alpha, int beta, int depth) throws CloneNotSupportedException {
        if (depth == 0 || isTerminal(board)) {
            return Result.of(-1, getHeuristic(board));
        }
        BiFunction<Integer, Integer, Integer> order;
        BiFunction<Integer, Integer, Boolean> comparator;
        int optimalValue;
        if (isMaxNode(side)) {
            optimalValue = Integer.MIN_VALUE;
            order = Math::max;
            comparator = (a, b) -> a > b;
        } else {
            optimalValue = Integer.MAX_VALUE;
            order = Math::min;
            comparator = (a, b) -> a < b;
        }
        int optimalMove = 0;
        List<Integer> validMoves = board.getValidMoves(side);
        for (int move : validMoves) {
            Board nextBoard = board.clone();
            Side nextPlayer = nextBoard.step(side, move);
            Result result = alphaBetaPruning(nextBoard, nextPlayer, alpha, beta, depth-1);
            if (comparator.apply(result.score, optimalValue)) {
                optimalValue = result.score;
                optimalMove = move;
            }
            alpha = order.apply(alpha, optimalValue);
//            System.out.println("max player=" + isMaxNode(side) + ", depth="+depth + ", next move=" + move + ", score=" + result.score + ", optimal move="+optimalMove + ", optimal value=" + optimalValue + ", alpha=" + alpha + ", beta=" + beta);
            if (beta <= alpha) {
                break;
            }
        }
        return Result.of(optimalMove, optimalValue);
    }
}
