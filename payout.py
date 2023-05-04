from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")


def calculate_payouts(number_of_players, buy_in, pot_splash, number_of_winners):
    if number_of_players < 4:
        raise ValueError("At least 4 players are required.")
    if buy_in <= 0 or pot_splash < 0 or number_of_winners < 1:
        raise ValueError("Invalid input values.")
    if number_of_players < number_of_winners:
        raise ValueError(
            "Number of winners should be less than or equal to the total number of players."
        )

    prize_pool = number_of_players * buy_in + pot_splash
    payouts = {}

    base_ratios = [0.5, 0.3, 0.2]
    remaining_ratio = 1 - sum(base_ratios[: number_of_winners - 1])
    remaining_prize_pool = prize_pool - buy_in  # Deduct buy-in for the last place

    for i in range(number_of_winners - 1):  # Exclude last place winner
        ratio = base_ratios[min(i, 2)]
        remaining_ratio -= ratio
        payout = round(remaining_prize_pool * ratio / 5) * 5
        payouts[i + 1] = payout
        remaining_prize_pool -= payout

    # Set the last place winner payout to their buy-in
    payouts[number_of_winners] = buy_in

    # Distribute the remaining prize pool difference to the winners according to the desired ratio
    remaining_prize_pool_diff = prize_pool - sum(payouts.values())
    if remaining_prize_pool_diff > 0:
        i = 1
        while remaining_prize_pool_diff > 0:
            payouts[i] += 5
            remaining_prize_pool_diff -= 5
            i += 1
            if i > number_of_winners - 1:
                i = 1

    # Redistribute any remaining differences
    remaining_diff = prize_pool - sum(payouts.values())
    if remaining_diff > 0:
        for i, ratio in enumerate(base_ratios):
            if remaining_diff <= 0:
                break
            if i + 1 < number_of_winners:
                payouts[i + 1] += remaining_diff
                remaining_diff = 0

    return prize_pool, payouts


@app.route("/", methods=["GET", "POST"])
def payouts():
    error = None
    if request.method == "POST":
        num_players = request.form["num_players"]
        buy_in = request.form["buy_in"]
        pot_splash = request.form["pot_splash"]
        number_of_winners = request.form["number_of_winners"]

        if not num_players or not buy_in or not pot_splash or not number_of_winners:
            error = "Please fill in all fields."
        else:
            try:
                prize_pool, payouts = calculate_payouts(
                    int(num_players),
                    int(buy_in),
                    int(pot_splash),
                    int(number_of_winners),
                )
            except ValueError as e:
                error = str(e)
            if not error:
                return render_template(
                    "payouts.html",
                    prize_pool=prize_pool,
                    payouts=payouts,
                    num_players=num_players,
                    buy_in=buy_in,
                    pot_splash=pot_splash,
                    number_of_winners=number_of_winners,
                )
    return render_template("payouts.html", error=error)


@app.route("/contact_us", methods=["GET"])
def contact_us():
    return render_template("contact_us.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
