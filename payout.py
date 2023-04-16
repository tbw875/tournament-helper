from flask import Flask, request, render_template
app = Flask(__name__, template_folder='templates', static_folder='static')

def calculate_payouts(num_players, buy_in, pot_splash):
    prize_pool = num_players * buy_in + pot_splash
    payouts = {
        1: round(prize_pool * 0.5 / 5) * 5,
        2: round(prize_pool * 0.3 / 5) * 5,
        3: round(prize_pool * 0.15 / 5) * 5,
        4: buy_in
    }
    total_payout = sum(payouts.values())
    if total_payout > prize_pool:
        payouts[1] -= (total_payout - prize_pool)
    elif total_payout < prize_pool:
        remaining_amount = prize_pool - total_payout
        i = 1
        while remaining_amount > 0:
            payouts[1] += buy_in
            remaining_amount -= buy_in
            i+= 1
    return prize_pool,payouts

def place(num):
    if num == 1:
        return '1st Place'
    elif num == 2:
        return '2nd Place'
    elif num == 3:
        return '3rd Place'
    else:
        return f'{num}th Place'

@app.route('/', methods=["GET", "POST"])
def payouts():
    error = None
    if request.method == "POST":
        try:
            num_players = request.form["num_players"]
            buy_in = request.form["buy_in"]
            pot_splash = request.form["pot_splash"]
            prize_pool, payouts = calculate_payouts(int(num_players), int(buy_in), int(pot_splash))
        except ValueError:
            error = "Invalid Input. Please enter a valid number only."
        if not error:
            return render_template('payouts.html', prize_pool=prize_pool,payouts=payouts,num_players=num_players,buy_in=buy_in, pot_splash=pot_splash)
    return render_template('payouts.html', error=error)

@app.route('/contact_us', methods=["GET"])
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080)
