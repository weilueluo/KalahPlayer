package MKAgent.alphaBetaPruning;

import MKAgent.*;
import MKAgent.Utils.Tuple;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.function.BiFunction;
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

        @Override
        public String toString() {
            return "Result{" +
                    "move=" + move +
                    ", score=" + score +
                    ", seq=" + seq +
                    '}';
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

    public static Result alphaBetaPruning(Board board, Side side, int seq, int alpha, int beta, int depth,
                                          int threadDepth) {
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

        if (threadDepth >= 1) {
            return _multiThreadAlphaBetaPruning(boardAndMoves, comparator, order, optimalValue, optimalMove,
                    seq, alpha, beta, depth, threadDepth, side);
        } else {
            return _normalAlphaBetaPruning(boardAndMoves, comparator, order, optimalValue, optimalMove,
                    seq, alpha, beta, depth, threadDepth, side);
        }
    }

    private static Result _normalAlphaBetaPruning(List<Tuple<Board, Side, Integer>> boardAndMoves,
                                                  BiFunction<Integer, Integer, Boolean> comparator,
                                                  BiFunction<Integer, Integer, Integer> order,
                                                  int optimalValue, int optimalMove, int seq, int alpha, int beta,
                                                  int depth, int threadDepth, Side side) {
        for (Tuple<Board, Side, Integer> boardSideTuple : boardAndMoves) {
            Result result = alphaBetaPruning(boardSideTuple.getFirst(), boardSideTuple.getSecond(), seq, alpha, beta,
                    depth - 1, threadDepth);
            if (comparator.apply(result.score, optimalValue)) {
                optimalValue = result.score;
                optimalMove = boardSideTuple.getThird();
            }
            if (isMaxNode(side)) {
                alpha = order.apply(alpha, optimalValue);
            } else {
                beta = order.apply(beta, optimalValue);
            }
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
                                                       int threadDepth, Side side) {

        ExecutorService executorService = Executors.newFixedThreadPool(boardAndMoves.size());
        ExecutorCompletionService<Result> executor = new ExecutorCompletionService<>(executorService);
        List<Future<Result>> results = new ArrayList<>();

        for (int i = 0; i < boardAndMoves.size(); i++) {
            results.add(executor.submit(createAlphaPruningTask(
                    boardAndMoves.get(i), i, alpha, beta, depth, threadDepth)));
        }
        for (Future<Result> future : results) {
            try {
                Result result = future.get();
                if (comparator.apply(result.score, optimalValue)) {
                    optimalValue = result.score;
                    optimalMove = boardAndMoves.get(result.seq).getThird();
                }
                if (isMaxNode(side)) {
                    alpha = order.apply(alpha, optimalValue);
                } else {
                    beta = order.apply(beta, optimalValue);
                }
                if (beta <= alpha) {
                    break;
                }
            } catch (InterruptedException | ExecutionException ignored) {
                // ignore
            }
        }
        // cancel any remaining tasks
        for (Future<Result> future : results) {
            future.cancel(true);
        }
        executorService.shutdownNow();
        return Result.of(optimalMove, optimalValue, seq);
    }

    private static List<Tuple<Board, Side, Integer>> getAllPossibleNextBoards(Board board, Side side) {
        return Kalah.getAllValidMoves(board, side)
                .stream()
                .map(move -> getNextBoard(board, side, move))
                // sort by heuristic desc, because it is more likely to be pruned
                .sorted((tuple1, tuple2) -> {
                    int heuDiff = getHeuristic(tuple2.getFirst()) - getHeuristic(tuple1.getFirst());
                    return heuDiff == 0 ? tuple1.getThird() - tuple2.getThird() : heuDiff;
                })
                .collect(Collectors.toList());
    }

    // return tuple of next_moved_board, next_player, move_made
    private static Tuple<Board, Side, Integer> getNextBoard(Board board, Side side, int move) {
        Board boardCopy = board.uncheckedClone();
        Side nextPlayer = Kalah.makeMove(boardCopy, Move.of(side, move));
        return Utils.Tuple.of(boardCopy, nextPlayer, move);
    }

    private static Callable<Result> createAlphaPruningTask(Utils.Tuple<Board, Side, Integer> tuple, int seq, int alpha,
                                                           int beta, int depth, int threadDepth) {
        Board boardCopy = tuple.getFirst();
        Side nextPlayer = tuple.getSecond();
        return () -> alphaBetaPruning(boardCopy, nextPlayer, seq, alpha, beta, depth - 1, threadDepth - 1);
    }
}
