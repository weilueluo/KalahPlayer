package MKAgent;

import com.sun.javaws.IconUtil;

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
    public static void main(String[] args) {
//        Board board = new Board(7, 7);
//        System.out.println(board);
//        Agent player1 = new ABPAgent(6);
//        int move = player1.getMove(board, Side.SOUTH);
//        System.out.println("Player 1 get move: " + move);
        evaluateMain();
    }

    private static void evaluateMain() {
        Board board = new Board(7, 7);
        boolean gameFinished = false;
        Side nextPlayer = Side.values()[new Random().nextInt(Side.values().length)];
        Agent player1 = new ABPAgent(9);
        Agent player2 = new RandomAgent();

        List<Long> player1MoveTimesMs = new ArrayList<>();
        List<Long> player2MoveTimesMs = new ArrayList<>();
        Instant startTime = Instant.now();
        while (!gameFinished) {
            int move;
            Instant moveStartTime = Instant.now();
            if (nextPlayer == Side.NORTH) {
                move = player1.getMove(board, Side.NORTH);
                player1MoveTimesMs.add(Duration.between(moveStartTime, Instant.now()).toMillis());
            } else {
                move = player2.getMove(board, Side.SOUTH);
                player2MoveTimesMs.add(Duration.between(moveStartTime, Instant.now()).toMillis());
            }
            nextPlayer = board.step(nextPlayer, move);
            Board.GameState state = board.state();
            if (state.isGameOver) {
                gameFinished = true;
                System.out.println("Game Finished, winner: " + state.winner);
            }
        }
        System.out.println("Player 1 move times: " + Arrays.toString(player1MoveTimesMs.toArray()));
        long player1AvgMoveTimeInMs = (long) player1MoveTimesMs.stream().mapToLong(i -> i).average().orElse(0);
        System.out.println("Player 1 avg move times: " + msToPrettyString(player1AvgMoveTimeInMs));

        System.out.println("Player 2 move times: " + Arrays.toString(player2MoveTimesMs.toArray()));
        long player2AvgMoveTimeInMs = (long) player2MoveTimesMs.stream().mapToLong(i -> i).average().orElse(0);
        System.out.println("Player 2 avg move times: " + msToPrettyString(player2AvgMoveTimeInMs));

        System.out.println("Total Time taken: " + msToPrettyString(Duration.between(startTime, Instant.now()).toMillis()));
    }


    private static String msToPrettyString(long durationInMillis) {
        long millis = durationInMillis % 1000;
        long second = (durationInMillis / 1000) % 60;
        long minute = (durationInMillis / (1000 * 60)) % 60;
        long hour = (durationInMillis / (1000 * 60 * 60)) % 24;

        return String.format("%02d:%02d:%02d.%d", hour, minute, second, millis);
    }
}
