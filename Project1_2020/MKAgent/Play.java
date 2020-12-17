package MKAgent;

import MKAgent.agents.ABPAgent;

public class Play {

    public static int getStartMove() {
        // TODO
        return 0;
    }

    private static final ABPAgent player = new ABPAgent(11, 2);

    public static int getMove(Board board, Side side) {
        return player.getMove(board, side);
    }

    // get swap (board, side)

}
