def simulate(blueprint, minutes):
    # Initialize resources and robots
    resources = {
        "ore": 1,  # You start with 1 ore-collecting robot
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
    robots = {
        "ore": 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }

    # Simulate the process for the given number of minutes
    for minute in range(minutes):
        # Have each robot collect its respective resource
        resources["ore"] += robots["ore"]
        resources["clay"] += robots["clay"]
        resources["obsidian"] += robots["obsidian"]
        resources["geode"] += robots["geode"]

        # Check if we can build any new robots
        for robot_type, cost in blueprint.items():
            # Check if we have enough resources to build at least one robot
            if all(resources[r] >= cost[r] for r in cost):
                # Calculate the maximum number of robots we can build
                max_robots = min(resources[r] // cost[r] for r in cost)
                # Build the maximum number of robots
                robots[robot_type] += max_robots
                # Deduct the resources used to build the robots
                for r in cost:
                    resources[r] -= cost[r] * max_robots

    # Return the maximum number of geode-cracking robots built
    return robots["geode"]


# Define the list of blueprints
blueprints = [
    {
        "ore": 4,
        "clay": 2,
        "obsidian": { "ore": 3, "clay": 14 },
        "geode": { "ore": 2, "obsidian": 7 },
    },
    {
        "ore": 2,
        "clay": 3,
        "obsidian": { "ore": 3, "clay": 8 },
        "geode": { "ore": 3, "obsidian": 12 },
    },
    # Add more blueprints here...
]

# Set the number of minutes to simulate
minutes = 24

# Find the best blueprint
best_blueprint = max(blueprints, key=lambda b: simulate(b, minutes))

# Print the result
print(f"The best blueprint is {best_blueprint}")
