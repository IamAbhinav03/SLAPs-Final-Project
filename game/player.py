class Player:

    def __init__(self):
        self.progress = 0
        self.inventory = []
        self.decisions = []

    def update_progress(self):
        self.progress += 1
