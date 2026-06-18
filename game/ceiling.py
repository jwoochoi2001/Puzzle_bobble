from settings import stage_ceiling_settings


class CeilingManager:

    def __init__(self, stage=1):

        self.stage = stage
        self._apply_stage_settings(stage)

        self.drop_count = 0
        self.shots_since_drop = 0

    def _apply_stage_settings(self, stage):

        cfg = stage_ceiling_settings(stage)

        self.fire_count = cfg["fire_count"]
        self.drop_seconds = cfg["drop_seconds"]
        self.warning_shots = cfg["warning_shots"]
        self.warning_seconds = cfg["warning_seconds"]
        self.time_until_drop = float(self.drop_seconds)

    def configure_stage(self, stage):

        self.stage = stage
        self._apply_stage_settings(stage)
        self.shots_since_drop = 0

    def shots_remaining(self):

        return max(0, self.fire_count - self.shots_since_drop)

    def seconds_remaining(self):

        return max(0.0, self.time_until_drop)

    def is_shot_warning(self):

        remaining = self.shots_remaining()
        return 0 < remaining <= self.warning_shots

    def is_timer_warning(self):

        return 0 < self.time_until_drop <= self.warning_seconds

    def is_warning(self):

        return self.is_shot_warning() or self.is_timer_warning()

    def update(self, delta_time):

        if self.time_until_drop > 0:
            self.time_until_drop = max(
                0.0,
                self.time_until_drop - delta_time,
            )

    def record_shot(self):

        self.shots_since_drop += 1

    def should_drop(self):

        return (
            self.shots_since_drop >= self.fire_count
            or self.time_until_drop <= 0
        )

    def drop(self):

        self.drop_count += 1
        self.shots_since_drop = 0
        self.time_until_drop = float(self.drop_seconds)
