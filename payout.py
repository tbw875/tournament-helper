while True:
  try:
    num_players = int(input("Enter the number of players: "))
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")

while True:
  try:
    buy_in = int(input("Enter the buy-in amount: "))
    break
  except ValueError:
    print("Invalid input. Please enter a valid number.")


def calculate_payouts(num_players, buy_in):
    prize_pool = num_players * buy_in
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
    print(f'Total prize pool: ${prize_pool}')
    return payouts

payouts = calculate_payouts(num_players, buy_in)
print(f"First place: ${payouts[1]}")
print(f"Second place: ${payouts[2]}")
print(f"Third place: ${payouts[3]}")
print(f"Fourth place: ${payouts[4]}")