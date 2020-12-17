package MKAgent;

import MKAgent.agents.ABPAgent;
import MKAgent.agents.Agent;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;

import static MKAgent.Utils.receiveMessage;
import static MKAgent.Utils.sendMsg;


/**
 * The main application class. It also provides methods for communication
 * with the game engine.
 */
public class Main {


    /**
     * The main method, invoked when the program is started.
     *
     * @param args Command line arguments.
     */

    // map: first move -> boolean
    // hard code main

    // time estimate: moves made, board, time -> alpha pruning depth, >= 3
    // read: requirements & protocol
    public static void main(String[] args) throws ExecutionException, InterruptedException, IOException, InvalidMessageException {
        evaluate();
//        while (true) {
//            String message = recvMsg();
//            MsgType type = Protocol.getMessageType(message);
//            switch (type) {
//                case START:
//                    // if our turn: send normal move
//                    // if their turn, do nothing
//                case STATE:
//                    // it is our turn:
//                    //     state == swap:
//                    //         send swap or not according to table
//                    //     state == change:
//                    //         if have enough time: send alpha pruning result
//                    //         if do not have enough time: send alpha pruning with less depth result
//                case END:
//                    // do nothing
//                default:
//                    throw new RuntimeException();
//            }
//        }
    }

    private static Optional<MsgType> getMessageType(String message) {
        try {
            return Optional.of(Protocol.getMessageType(message));
        } catch (InvalidMessageException e) {
            System.err.println("Cannot infer message type from message: " + e);
        }
        return Optional.empty();
    }

    private static void handleStartMessage(String message) {
        try {
            boolean ourStart = Protocol.interpretStartMsg(message);
            if (ourStart) {
                sendMsg(Protocol.createMoveMsg(Play.getStartMove()));
            }  // else do nothing, opponent first move
        } catch (InvalidMessageException e) {
            System.err.println("Failed to interpret start message: " + e);
        }
    }

    private static void handleStateMessage(String message, long secondsSpent) {
        Board board = new Board(7, 7);
        try {
            Protocol.MoveTurn moveTurn = Protocol.interpretStateMsg(message, board);
        } catch (InvalidMessageException e) {
            System.err.println("Failed to interpret state message: " + e);
        }
    }

    private static void handleEndMessage(String message) {

    }

    private static void _main(String[] args) throws IOException {
        boolean gameFinished = false;
        long secondsSpent = 0;
        while (!gameFinished) {
            String message = receiveMessage();
            // start 1 seconds early, ensure we do not over-estimate time left.
            Instant thisMoveStartTime = Instant.now().minus(1, ChronoUnit.SECONDS);
            Optional<MsgType> messageType = getMessageType(message);
            if (messageType.isPresent()) {
                switch (messageType.get()) {
                    case START:
                        handleStartMessage(message);
                        break;
                    case STATE:
                        handleStateMessage(message, secondsSpent);
                        break;
                    case END:
                        handleEndMessage(message);
                        gameFinished = true;
                        break;
                    default:
                        System.err.println("Unexpected message type encountered: " + messageType.get());
                        break;
                }
            }
            // add time spent for this move
            secondsSpent += Duration.between(thisMoveStartTime, Instant.now()).getSeconds();
        }
    }

    private static void evaluate() {
        Agent player1 = new ABPAgent(8, 2);
        Agent player2 = new ABPAgent(8, 0);

        int south_side_win = 0;
        int north_side_win = 0;

        for (int i = 0; i < 100; i++) {
            Board board = new Board(7, 7);
            Kalah game = new Kalah(board);
            boolean gameFinished = false;
            Side winner = null;
            Side nextPlayer = Side.NORTH;
            System.err.println("Game: " + (i + 1));

            List<Long> player1MoveTimes = new ArrayList<>();
            List<Long> player2MoveTimes = new ArrayList<>();
            Instant startTime = Instant.now();
            long moveSeconds;

            while (!gameFinished) {
                int move;

                Instant moveStartTime = Instant.now();

                if (nextPlayer == Side.NORTH) {
                    move = player1.getMove(board, Side.NORTH);

                    moveSeconds = Duration.between(moveStartTime, Instant.now()).getSeconds();
                    player1MoveTimes.add(moveSeconds);
                } else {
                    move = player2.getMove(board, Side.SOUTH);

                    moveSeconds = Duration.between(moveStartTime, Instant.now()).getSeconds();
                    player2MoveTimes.add(moveSeconds);
                }

                System.err.println("move: " + move + ", took " + moveSeconds + "s, board after move:");

                nextPlayer = game.makeMove(Move.of(nextPlayer, move));
                Kalah.State state = game.gameOver();
                if (state.over) {
                    gameFinished = true;
                    winner = state.winner;
                }
            }
            System.err.println("winner: " + winner);
            if (winner == Side.NORTH)
                north_side_win++;
            if (winner == Side.SOUTH)
                south_side_win++;
        }
        System.err.println("North:" + north_side_win);
        System.err.println("South:" + south_side_win);
    }
}

// Game Finished, winner: NORTH
//Player 1 move times: [35, 33, 35, 37, 39, 41, 43, 46, 49, 52, 54, 56, 59, 65, 69, 76, 78, 83, 84, 21, 0, 0, 0, 0]
//Player 1 avg move times: 43s
//Player 2 move times: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
//Player 2 avg move times: 0s
//Total Time taken: 1063s

// sort desc
//Game Finished, winner: NORTH
//Player 1 move times: [34, 31, 33, 33, 33, 34, 35, 36, 37, 38, 38, 39, 39, 42, 44, 47, 49, 52, 55, 58, 62, 46, 10, 0, 0, 0]
//Player 1 avg move times: 35s
//Player 2 move times: [0, 0, 0]
//Player 2 avg move times: 0s
//Total Time taken: 937s
//
//Process finished with exit code 0

// optimized pruning
// Game Finished, winner: NORTH
//Player 1 move times: [23, 21, 18, 16, 10, 11, 9, 13, 9, 6, 5, 4, 4, 9, 6, 5, 5, 4, 4, 2, 3, 2, 0]
//Player 1 avg move times: 8s
//Player 2 move times: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
//Player 2 avg move times: 0s
//Total Time taken: 200s
