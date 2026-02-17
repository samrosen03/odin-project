class Exercise:
    def __init__(self, name):
        self.name = name
        self.best_reps = 0
        self.total_reps = 0
        self.sessions = 0

    def update(self, reps):
        self.sessions += 1
        self.total_reps += reps
        if reps > self.best_reps:
            self.best_reps = reps

    def summary(self):
        return (
            f"{self.name} → "
            f"Best: {self.best_reps}, "
            f"Total Reps: {self.total_reps}, "
            f"Sessions: {self.sessions}"
        )


def main():
    exercises = {}

    try:
        with open("workout_log.txt", "r") as file:
            for line in file:
                if " - " not in line:
                    continue

                _, data = line.strip().split(" - ", 1)

                if ":" not in data:
                    continue

                name, reps_str = data.split(":", 1)

                try:
                    reps = int(reps_str.strip().split()[0])
                except:
                    continue

                name = name.strip()

                if name not in exercises:
                    exercises[name] = Exercise(name)

                exercises[name].update(reps)

        print("📊 Exercise Summary:\n")
        for ex in exercises.values():
            print(ex.summary())

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")


main()
