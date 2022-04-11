class ConversationData:
    def __init__(
        self,
        stage: str = "",
        third_stage: str = "",
        numeric_stage: int = 0
    ):
        self.stage = stage
        self.third_stage = third_stage
        self.numeric_stage = numeric_stage
