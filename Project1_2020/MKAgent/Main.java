package MKAgent;

import MKAgent.agents.ABPAgent;
import MKAgent.agents.Agent;
import MKAgent.agents.RandomAgent;

import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;
import java.util.stream.IntStream;

/**
 * The main application class. It also provides methods for communication
 * with the game engine.
 */
public class Main {
    /**
     * Input from the game engine.
     */
    private static Reader input = new BufferedReader(new InputStreamReader(System.in));

    /**
     * Sends a message to the game engine.
     *
     * @param msg The message.
     */
    public static void sendMsg(String msg) {
        System.out.print(msg);
        System.out.flush();
    }

    /**
     * Receives a message from the game engine. Messages are terminated by
     * a '\n' character.
     *
     * @return The message.
     * @throws IOException if there has been an I/O error.
     */
    public static String recvMsg() throws IOException {
        StringBuilder message = new StringBuilder();
        int newCharacter;

        do {
            newCharacter = input.read();
            if (newCharacter == -1)
                throw new EOFException("Input ended unexpectedly.");
            message.append((char) newCharacter);
        } while ((char) newCharacter != '\n');

        return message.toString();
    }

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


    private static void evaluate() {
        Board board = new Board(7, 7);
        Kalah game = new Kalah(board);
        boolean gameFinished = false;
        Side nextPlayer = Side.values()[new Random().nextInt(Side.values().length)];

        Agent player1 = new ABPAgent(11, 1);
        Agent player2 = new RandomAgent();
        Side winner = null;

        List<Long> player1MoveTimes = new ArrayList<>();
        List<Long> player2MoveTimes = new ArrayList<>();
        Instant startTime = Instant.now();
        while (!gameFinished) {
            int move;
            Instant moveStartTime = Instant.now();
            System.err.println("Player: " + nextPlayer + " is making a move ...");
            if (nextPlayer == Side.NORTH) {
                move = player1.getMove(board, Side.NORTH);
                player1MoveTimes.add(Duration.between(moveStartTime, Instant.now()).getSeconds());
            } else {
                move = player2.getMove(board, Side.SOUTH);
                player2MoveTimes.add(Duration.between(moveStartTime, Instant.now()).getSeconds());
            }
            System.err.println("move: " + move);
            nextPlayer = game.makeMove(Move.of(nextPlayer, move));
            System.err.println(board);
            Kalah.State state = game.gameOver();
            if (state.over) {
                gameFinished = true;
                winner = state.winner;
            }
        }
        System.err.println("Game Finished, winner: " + winner);
        System.err.println("Player 1 move times: " + Arrays.toString(player1MoveTimes.toArray()));
        long player1AvgMoveTime = (long) player1MoveTimes.stream().mapToLong(i -> i).average().orElse(0);
        System.err.println("Player 1 avg move times: " + player1AvgMoveTime + "s");

        System.err.println("Player 2 move times: " + Arrays.toString(player2MoveTimes.toArray()));
        long player2AvgMoveTime = (long) player2MoveTimes.stream().mapToLong(i -> i).average().orElse(0);
        System.err.println("Player 2 avg move times: " + player2AvgMoveTime + "s");

        System.err.println("Total Time taken: " + Duration.between(startTime, Instant.now()).getSeconds() + "s");
    }


//    private static String msToPrettyString(long durationInMillis) {
//        long millis = durationInMillis % 1000;
//        long second = (durationInMillis / 1000) % 60;
//        long minute = (durationInMillis / (1000 * 60)) % 60;
//        long hour = (durationInMillis / (1000 * 60 * 60)) % 24;
//
//        return String.format("%02d:%02d:%02d.%d", hour, minute, second, millis);
//    }
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