package MKAgent;

import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

public class Utils {
    public static class Tuple<T1, T2, T3> {
        private final T1 first;
        private final T2 second;
        private final T3 third;

        private Tuple(T1 first, T2 second, T3 third) {
            this.first = first;
            this.second = second;
            this.third = third;
        }

        public T1 getFirst() {
            return first;
        }

        public T2 getSecond() {
            return second;
        }

        public static <T1, T2, T3> Tuple<T1, T2, T3> of(T1 first, T2 second, T3 third) {
            return new Tuple<>(first, second, third);
        }

        public T3 getThird() {
            return third;
        }
    }

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

    static String receiveMessage() {
        try {
            return recvMsg();
        } catch (IOException e) {
            System.err.println("Encountered IOException while receiving message: " + e);
            return "";
        }
    }
}
