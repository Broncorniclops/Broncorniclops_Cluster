class PRNDLDisplay:
    def __init__(self, can_data):
        self.can_data = can_data
        self.gears = ["P", "R", "N", "D", "L"]
        self.current_gear = "P"

    def update_gear(self):
        gear = self.can_data.get("GEAR")
        if gear in self.gears:
            self.current_gear = gear

    def get_display_data(self):
        return {g: (g == self.current_gear) for g in self.gears}