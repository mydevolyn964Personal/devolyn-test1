from .agent import TrainBookingAgent


def main() -> None:
    agent = TrainBookingAgent()
    print(agent.explain_plan("Find a train from Delhi to Jaipur"))
    trains = agent.search_trains("Delhi", "Jaipur")
    print(trains)
    proposal = agent.propose_booking(trains[0]["train_id"], "traveler@example.test")
    print(proposal)
    print(agent.confirm_booking(proposal["booking_id"], "yes"))


if __name__ == "__main__":
    main()
