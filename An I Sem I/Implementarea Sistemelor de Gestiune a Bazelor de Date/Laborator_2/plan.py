class ExecutionStep:
    def __init__(self, operation, table, details=None, cost=0):
        self.operation = operation
        self.table = table
        self.details = details or {}
        self.cost = cost

    def __repr__(self):
        return f"{self.operation} on {self.table} (Cost={self.cost}, Details={self.details})"


class ExecutionPlan:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def explain(self):
        print("Execution plan:")
        for step in self.steps:
            line = f"{step.operation} on {step.table}"

            # dacă pasul folosește index, îl afisez
            if "index" in step.details:
                line += f" using {step.details['index']}"

            line += f" (cost={step.cost}"

            # rânduri estimate 
            if "estimated_rows" in step.details:
                line += f", rows={step.details['estimated_rows']}"

            line += ")"
            print(line)
