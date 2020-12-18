package MKAgent;

import MKAgent.agents.ABPAgent;
import java.util.List;
import java.util.Random;

public class Play {

    public static int getStartMove() {
        return 4;
    }

    private static final ABPAgent player = new ABPAgent(14, 2);

    public static int getMove(Board board, Side side, long secondsSpent) {
        if (Kalah.gameOver(board).over) {
            List<Integer> validMoves = Kalah.getAllValidMoves(board, side);
            return validMoves.get(new Random().nextInt(validMoves.size()));
        }
        return player.getMove(board, side);
    }

    public static boolean getSwap(int oppMove) {
        return oppMove != 1 && oppMove != 2 && oppMove != 6;
    }
}
