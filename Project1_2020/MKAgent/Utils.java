package MKAgent;

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
}
