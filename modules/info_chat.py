from collections import deque
import random
import time

class InformationChatbot:
    def __init__(self):
        self.questions = {"좋아하는 음식": ["어떤 종류의 음식을 가장 선호하시나요? 예를 함께 들어 주시겠어요?",
                                    "당신의 입맛을 자극하는 음식은 어떤 종류인가요? 예를 들어 주시면 더 좋을 것 같아요.",
                                    "자주 먹는 음식 중에서 특히 좋아하는 것은 무엇인가요? 예를 들어 주시면 더 좋을 것 같아요.",
                                    "가장 좋아하는 음식 종류는 무엇인가요? 예를 함께 들어 주시겠어요?",
                                    "특별히 좋아하는 음식 종류는 있으신가요? 예를 들어 주시면 더 좋을 것 같아요.",
                                    "음식점에서 자주 먹는 음식 종류는 무엇인가요? 예를 함께 들어 주시겠어요?",
                                    "좋아하는 음식을 몇 가지 생각해볼까요? 어떤 음식들인가요?",],

                        "좋아하는 날씨": ["선호하는 기후 조건은 있으신가요?",
                                    "편안함을 느끼는 어떤 특정한 날씨가 있나요?",
                                    "여행지의 날씨가 어땠으면 하시나요?",
                                    "특별히 좋아하는 날씨가 있나요?",],

                        "여행지에서 하고 싶은 일": ['여행지에서 어떤 종류의 활동을 즐기고 싶으신가요?',
                                          '여행 중 우선적으로 하고 싶은 활동이 있나요?',
                                          '특별한 명소나 자연 경관을 감상하는 것을 선호하시나요? 아니면 어떤 활동을 선호하시나요?',
                                          '문화와 역사를 경험하는 활동에 관심이 있으신가요? 아니라면 어떤 활동이 좋으신가요?',
                                          '스릴을 느끼거나 모험을 즐길 수 있는 활동을 선호하시나요? 아니라면 어떤 활동을 선호하시나요?',
                                          '여행 중에 해 보고 싶은 활동이 있나요?',
                                          '운동이나 액티비티를 하며 여행을 즐기는 것을 선호하시나요? 아니라면 어떤 활동이 좋으신가요?',
                                          '자연 속에서 즐길 수 있는 야외 활동을 선호하시나요? 아니라면 어떤 활동을 선호하시나요?',
                                          ],
                            }

        self.chats_1 = ["그렇군요. 그러면",
                        "좋아요. 그럼 이번엔",
                        "무슨 말인지 알 것 같아요. 음, 그러면 다음으로는",
                        "아하! 그래요? 저와 비슷하군요! 그럼 이번에는",
                        "오! 알겠어요. 그럼 다음으로",
                        ]
        
        self.chats_2 = ["에 대해 여쭤볼게요.",
                        "에 대해 이야기해 봐요.",
                        "에 관한 건 어떤가요?",
                        "에 관해서도 여쭤볼게요.",
                        "와 관련한 질문을 해 볼게요.",
                        ]
        self.keys = deque(list(self.questions.keys()))
        self.num_of_questions = len(self.keys)
        self.user_inputs = str()
        self.count = 0
        self.month = int()
        self.itinerary = int()
        random.shuffle(self.keys)

    def chat_greetings(self):
        response = "반가워요. 저는 당신의 여행지 고민을 도와줄 Tripy예요. 아직 여행지를 결정하지 못하신 거죠?"
        return response
    
    def chat_season(self):
        response = "좋아요. 그럼 먼저 여행에 대해 이야기를 나눠 봐요. 먼저 여행 시기에 대해 이야기해 볼까요?\n언제 여행을 가려고 생각하고 계신가요? 해당하는 월을 숫자로 입력해 주시겠어요?"
        return response

    def chat_periods(self):
        response = "와, 좋은 때네요! 그럼 혹시 며칠 동안 여행을 하실 생각이신가요? 마찬가지로 숫자로 입력해 주시겠어요?"
        return response

    def chat_random_questions(self):
        key = self.keys.popleft()
        question = random.sample(self.questions[key], 1)
        response = f"{('').join(random.sample(self.chats_1, 1))} {key}{('').join(random.sample(self.chats_2, 1))}\n{('').join(question)}"
        return response

    def last_question(self):
        response = "좋아요. 그럼 마지막으로 그밖에 여행지에 대해 선호하는 조건이나 중요하게 여기는 게 있다면 말씀해 주시겠어요?"
        return response