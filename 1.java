public class Elo {
    private final double k;
    private final double c;
    private final double l;

    public Elo(int kFactor, int cValue, int lFactor) {
        this.k = kFactor;
        this.c = cValue;
        this.l = lFactor;
    }

    public Elo() {
        this(32, 400, 16);
    }

    private double expectedScore(double ratingA, double ratingB) {
        double exponent = (ratingB - ratingA) / c;
        return 1.0 / (1.0 + Math.pow(10.0, exponent));
    }

    public double[] elo(double ratingA, double ratingB, int outcome) {
        double sA, sB;

        if (outcome == 0) {
            sA = 0.5;
            sB = 0.5;
        } else if (outcome == 1) {
            sA = 1.0;
            sB = 0.0;
        } else if (outcome == 2) {
            sA = 0.0;
            sB = 1.0;
        } else {
            throw new IllegalArgumentException("outcome must be 0 (draw), 1 (A wins), or 2 (B wins)");
        }

        double eA = expectedScore(ratingA, ratingB);
        double eB = 1.0 - eA;

        double newA = ratingA + k * (sA - eA);
        double newB = ratingB + k * (sB - eB);

        return new double[]{ newA, newB };
    }

    public double[] eloWithPoints(
            double ratingA,
            double ratingB,
            double pointsA,
            double pointsB,
            int method,
            Integer outcome // can be null
    ) {
        // If outcome not provided, infer from points
        if (outcome == null) {
            if (pointsA > pointsB) {
                outcome = 1;
            } else if (pointsB > pointsA) {
                outcome = 2;
            } else {
                outcome = 0;
            }
        }

        double sA, sB;
        if (outcome == 0) {
            sA = 0.5;
            sB = 0.5;
        } else if (outcome == 1) {
            sA = 1.0;
            sB = 0.0;
        } else if (outcome == 2) {
            sA = 0.0;
            sB = 1.0;
        } else {
            throw new IllegalArgumentException("outcome must be 0, 1, or 2");
        }

        double eA = expectedScore(ratingA, ratingB);
        double eB = 1.0 - eA;

        double totalPoints = pointsA + pointsB;
        double fracA, fracB;
        if (totalPoints > 0.0) {
            fracA = pointsA / totalPoints;
            fracB = pointsB / totalPoints;
        } else {
            fracA = fracB = 0.5;
        }

        double newA, newB;

        switch (method) {
            case 0:
                // Classic ELO
                newA = ratingA + k * (sA - eA);
                newB = ratingB + k * (sB - eB);
                break;

            case 1:
                // Use score fraction instead of S
                newA = ratingA + k * (fracA - eA);
                newB = ratingB + k * (fracB - eB);
                break;

            case 2:
                // Bonus with L factor
                double diffA = sA - eA;
                double pA;
                if (diffA > 0) {
                    pA = 1.0;
                } else if (diffA < 0) {
                    pA = -1.0;
                } else {
                    pA = 0.0;
                }

                double diffB = sB - eB;
                double pB;
                if (diffB > 0) {
                    pB = 1.0;
                } else if (diffB < 0) {
                    pB = -1.0;
                } else {
                    pB = 0.0;
                }

                newA = ratingA + k * diffA + pA * l * fracA;
                newB = ratingB + k * diffB + pB * l * fracB;
                break;

            default:
                throw new IllegalArgumentException("method must be 0, 1, or 2");
        }

        return new double[]{ newA, newB };
    }
}
