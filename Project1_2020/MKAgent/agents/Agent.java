package MKAgent.agents;

import MKAgent.Board;
import MKAgent.Side;

public interface Agent {
    int getMove(Board board, Side side);
}
