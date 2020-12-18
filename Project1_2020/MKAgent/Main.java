package MKAgent;

import MKAgent.agents.ABPAgent;
import MKAgent.agents.Agent;

import java.io.IOException;
import java.io.PrintWriter;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
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
    public static void main(String[] args) throws IOException, InvalidMessageException {
        boolean gameFinished = false;
        long secondsSpent = 0;
        Side ourSide = null;
        boolean isFirstMove = true;
//        PrintWriter writer = new PrintWriter("log.txt", "UTF-8");
        while (!gameFinished) {
//            writer.append("Waiting for message ...\n");
//            writer.flush();
            String message = receiveMessage();
//            writer.append("Received Message: ").append(message);
//            writer.flush();
            // start 1 seconds early, ensure we do not over-estimate time left.
            Instant thisMoveStartTime = Instant.now().minus(1, ChronoUnit.SECONDS);
            MsgType messageType = Protocol.getMessageType(message);
            String messageToSend = null;
            switch (messageType) {
                case START:
                    boolean ourStart = Protocol.interpretStartMsg(message);
                    if (ourStart) {
                        messageToSend = Protocol.createMoveMsg(Play.getStartMove());
                        isFirstMove = false;
                        ourSide = Side.SOUTH;
                    } else {
                        ourSide = Side.NORTH;
                    }
                    break;
                case STATE:
                    // move == -1: enemy swapped
                    // end == true: game ended
                    // again == true: make a move
                    // again == false: do nothing
                    // first move: make a swap / make a move
                    Board board = new Board(7, 7);
                    Protocol.MoveTurn state = Protocol.interpretStateMsg(message, board);
//                    writer.append(board.toString());
//                    writer.append(ourSide.toString()).append("\n");
                    if (state.end) {
//                        writer.append("state.end\n");
                        gameFinished = true;
                    } else if (state.move == -1) {
//                        writer.append("state.move == -1\n");
                        ourSide = ourSide.opposite();
                        messageToSend = Protocol.createMoveMsg(Play.getMove(board, ourSide, secondsSpent));
                    } else if (isFirstMove) {
//                        writer.append("isFirstMove\n");
                        if (Play.getSwap(state.move)) {
                            messageToSend = Protocol.createSwapMsg();
                            ourSide = ourSide.opposite();
                        } else {
                            messageToSend = Protocol.createMoveMsg(Play.getMove(board, ourSide, secondsSpent));
                        }
                        isFirstMove = false;
                    } else if (state.again) {
//                        writer.append("state.again\n");
                        messageToSend = Protocol.createMoveMsg(Play.getMove(board, ourSide, secondsSpent));
                    } // else {
//                        writer.append("none\n");
//                        writer.append(state.toString()).append("\n");
//                    }
                    break;
                case END:
                    gameFinished = true;
                    break;
                default:
                    System.err.println("Unexpected message type encountered: " + messageType);
                    break;
            }
            if (messageToSend != null) {
//                writer.append("Message Sent: ").append(messageToSend);
//                writer.flush();
                sendMsg(messageToSend);
            }
            // add time spent for this move
            secondsSpent += Duration.between(thisMoveStartTime, Instant.now()).getSeconds();
        }
//        writer.close();
        System.err.println("Game has ended");
    }

    private static void evaluate() {
        Agent player1 = new ABPAgent(15, 2);
        Agent player2 = new ABPAgent(15, 2);

        int south_side_win = 0;
        int north_side_win = 0;

        for (int i = 0; i < 1; i++) {
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
                System.err.print("Player " + nextPlayer + " is making a move... ");
                if (nextPlayer == Side.NORTH) {
                    move = player1.getMove(board, Side.NORTH);
                    moveSeconds = Duration.between(moveStartTime, Instant.now()).getSeconds();
                    player1MoveTimes.add(moveSeconds);
                } else {
                    move = player2.getMove(board, Side.SOUTH);
                    moveSeconds = Duration.between(moveStartTime, Instant.now()).getSeconds();
                    player2MoveTimes.add(moveSeconds);
                }
                System.err.println(", move: " + move + ", took " + moveSeconds + "s, board:");
                nextPlayer = game.makeMove(Move.of(nextPlayer, move));
                System.err.println(board);
                Kalah.State state = game.gameOver();
                if (state.over) {
                    gameFinished = true;
                    winner = state.winner;
                }
            }
            System.err.println("winner: " + winner);
            System.err.println("player 1 times: " + Arrays.toString(player1MoveTimes.toArray()));
            System.err.println("player 2 times: " + Arrays.toString(player2MoveTimes.toArray()));
            System.err.println("Match Time Taken: " + Duration.between(startTime, Instant.now()).getSeconds());
            System.err.println(board);
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
