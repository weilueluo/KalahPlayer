package MKAgent.alphaBetaPruning;

import MKAgent.*;
import MKAgent.Utils.Tuple;

import java.sql.Array;
import java.sql.SQLOutput;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;

public class AlphaBetaPruning {

    public static class Result {
        public final int move;
        public final int score;
        public final int seq;

        private Result(int move, int score, int seq) {
            this.move = move;
            this.score = score;
            this.seq = seq;
        }

        private static Result of(int move, int score, int seq) {
            return new Result(move, score, seq);
        }
    }

    public static boolean isMaxNode(Side side) {
        return side == Side.SOUTH;
    }

    public static int getHeuristic(Board board) {
        return board.getSeedsInStore(Side.SOUTH) - board.getSeedsInStore(Side.NORTH);
    }

    private static boolean isTerminal(Board board) {
        return Kalah.gameOver(board).over;
    }

    public static Result alphaBetaPruning(Board board, Side side, int seq, int alpha, int beta, int depth, int threadDepth) {
        if (depth == 0 || isTerminal(board)) {
            return Result.of(-1, getHeuristic(board), seq);
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
        int optimalMove = -1;
        List<Tuple<Board, Side, Integer>> boardAndMoves = getAllPossibleNextBoards(board, side);

        if (threadDepth > 1) {
            return _multiThreadAlphaBetaPruning(boardAndMoves, comparator, order, optimalValue, optimalMove,
                    seq, alpha, beta, depth, threadDepth);
        } else {
            return _normalAlphaBetaPruning(boardAndMoves, comparator, order, optimalValue, optimalMove,
                    seq, alpha, beta, depth, threadDepth);
        }
    }

    private static Result _normalAlphaBetaPruning(List<Tuple<Board, Side, Integer>> boardAndMoves, BiFunction<Integer, Integer, Boolean> comparator, BiFunction<Integer, Integer, Integer> order, int optimalValue, int optimalMove, int seq, int alpha, int beta, int depth, int threadDepth) {
        for (Tuple<Board, Side, Integer> boardSideTuple : boardAndMoves) {
            Result result = alphaBetaPruning(boardSideTuple.getFirst(), boardSideTuple.getSecond(), seq, alpha, beta,
                    depth - 1, threadDepth);
            if (comparator.apply(result.score, optimalValue)) {
                optimalValue = result.score;
                optimalMove = boardSideTuple.getThird();
            }
            alpha = order.apply(alpha, optimalValue);
            if (beta <= alpha) {
                break;
            }
        }
        return Result.of(optimalMove, optimalValue, seq);
    }

    private static Result _multiThreadAlphaBetaPruning(List<Tuple<Board, Side, Integer>> boardAndMoves,
                                                       BiFunction<Integer, Integer, Boolean> comparator,
                                                       BiFunction<Integer, Integer, Integer> order, int optimalValue,
                                                       int optimalMove, int seq, int alpha, int beta, int depth,
                                                       int threadDepth) {

        ExecutorCompletionService<Result> executor = getExecutor();
        List<Future<Result>> results = new ArrayList<>();

        for (int i = 0; i < boardAndMoves.size(); i++) {
            results.add(executor.submit(
                    createAlphaPruningTask(boardAndMoves.get(i), i, alpha, beta, depth, threadDepth)));
        }
        int resultCount = 0;
        boolean needMoreResult = true;
        while (needMoreResult || resultCount < boardAndMoves.size()) {
            try {
                Result result = executor.take().get();
                if (comparator.apply(result.score, optimalValue)) {
                    optimalValue = result.score;
                    optimalMove = boardAndMoves.get(result.seq).getThird();
                }
                alpha = order.apply(alpha, optimalValue);
                if (beta <= alpha) {
                    needMoreResult = false;
                }
            } catch (InterruptedException | ExecutionException ignore) {
                // ignore
            } finally {
                resultCount++;
            }
        }
        // cancel any remaining tasks
        for (Future<Result> future : results) {
            future.cancel(true);
        }
        return Result.of(optimalMove, optimalValue, seq);
    }

    private static List<Tuple<Board, Side, Integer>> getAllPossibleNextBoards(Board board, Side side) {
        return Kalah.getAllValidMoves(board, side)
                .stream()
                .map(move -> getNextBoard(board, side, move))
                // sort by heuristic desc, because it is more likely to be pruned
                .sorted((tuple1, tuple2) -> getHeuristic(tuple2.getFirst()) - getHeuristic(tuple1.getFirst()))
                .collect(Collectors.toList());
    }

    // return tuple of next_moved_board, next_player, move_made
    private static Tuple<Board, Side, Integer> getNextBoard(Board board, Side side, int move) {
        Board boardCopy = board.uncheckedClone();
        Side nextPlayer = Kalah.makeMove(boardCopy, Move.of(side, move));
        return Utils.Tuple.of(boardCopy, nextPlayer, move);
    }

    private static <T> ExecutorCompletionService<T> getExecutor() {
        int processors = Runtime.getRuntime().availableProcessors() / 2;
        ExecutorService executorService = Executors.newFixedThreadPool(processors);
        return new ExecutorCompletionService<>(executorService);
    }

    private static Callable<Result> createAlphaPruningTask(Utils.Tuple<Board, Side, Integer> tuple, int seq, int alpha, int beta, int depth, int threadDepth) {
        Board boardCopy = tuple.getFirst();
        Side nextPlayer = tuple.getSecond();
        return () -> alphaBetaPruning(boardCopy, nextPlayer, seq, alpha, beta, depth - 1, threadDepth - 1);
    }
}
