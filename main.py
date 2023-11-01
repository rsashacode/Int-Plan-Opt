class Event:
    def __init__(self, duration, revenue, cost, resources):
        self.duration = duration
        self.revenue = revenue
        self.cost = cost
        self.resources = resources


def objective_function(event):
    return event.revenue - event.cost


def simple_genetic_algorithm(events):
    return events


if __name__ == "__main__":
    meeting = Event(duration=2, revenue=200, cost=50, resources=["Conference Room", "Projector"])
    optimized_schedule = simple_genetic_algorithm([meeting])
    print(f"Optimized Schedule: {optimized_schedule}")