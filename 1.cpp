#pragma once
#include <cmath>
#include <stdexcept>
#include <utility>

class Elo {
public:
    explicit Elo(int kFactor = 32, int cValue = 400, int lFactor = 16)
        : k_(static_cast<double>(kFactor)),
          c_(static_cast<double>(cValue)),
          l_(static_cast<double>(lFactor)) {}

    // Returns {newRatingA, newRatingB}
    std::pair<double, double> elo(double ratingA, double ratingB, int outcome) const {
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
            throw std::invalid_argument("outcome must be 0 (draw), 1 (A wins), or 2 (B wins)");
        }

        double eA = expectedScore(ratingA, ratingB);
        double eB = 1.0 - eA;

        double newA = ratingA + k_ * (sA - eA);
        double newB = ratingB + k_ * (sB - eB);

        return { newA, newB };
    }

    // Returns {newRatingA, newRatingB}
    std::pair<double, double> eloWithPoints(
        double ratingA,
        double ratingB,
        double pointsA,
        double pointsB,
        int method = 2,
        int outcome = -1 // -1 = auto-detect from points
    ) const {
        if (outcome == -1) {
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
            throw std::invalid_argument("outcome must be 0, 1, or 2");
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
            newA = ratingA + k_ * (sA - eA);
            newB = ratingB + k_ * (sB - eB);
            break;

        case 1:
            // Use score fraction
            newA = ratingA + k_ * (fracA - eA);
            newB = ratingB + k_ * (fracB - eB);
            break;

        case 2: {
            // Bonus with L factor
            double diffA = sA - eA;
            double pA;
            if (diffA > 0.0) {
                pA = 1.0;
            } else if (diffA < 0.0) {
                pA = -1.0;
            } else {
                pA = 0.0;
            }

            double diffB = sB - eB;
            double pB;
            if (diffB > 0.0) {
                pB = 1.0;
            } else if (diffB < 0.0) {
                pB = -1.0;
            } else {
                pB = 0.0;
            }

            newA = ratingA + k_ * diffA + pA * l_ * fracA;
            newB = ratingB + k_ * diffB + pB * l_ * fracB;
            break;
        }

        default:
            throw std::invalid_argument("method must be 0, 1, or 2");
        }

        return { newA, newB };
    }

private:
    double expectedScore(double ratingA, double ratingB) const {
        double exponent = (ratingB - ratingA) / c_;
        return 1.0 / (1.0 + std::pow(10.0, exponent));
    }

    double k_;
    double c_;
    double l_;
};
