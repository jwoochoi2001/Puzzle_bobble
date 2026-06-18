from settings import stage_color_count, stage_ceiling_settings


class DifficultyManager:

    def __init__(self, stage=1):

        self.stage = stage

    def set_stage(self, stage):

        self.stage = stage

    def available_colors(self):

        return stage_color_count(self.stage)

    def ceiling_settings(self):

        return stage_ceiling_settings(self.stage)

    def misses_before_drop(self):

        return self.ceiling_settings()["fire_count"]
