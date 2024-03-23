from modules.info_chat import InformationChatbot
from modules.classifier import CitiesExtractor
from modules.generative_chat import GenerativeChatbot
import gradio as gr
import time

info_chat = InformationChatbot()
clsfier = CitiesExtractor()
informer = GenerativeChatbot()
recommended_city = str()

def chat_response(message, history):
    # 첫 번째 - 인삿말 출력
    if info_chat.count == 0:
        info_chat.count += 1
        return info_chat.chat_greetings()
    # 두 번째 - 여행 시기 질문
    elif info_chat.count == 1:
        info_chat.count += 1
        return info_chat.chat_season()
    # 세 번째 - 여행 기간 질문
    elif info_chat.count == 2:
        if (not message.isdigit()) or ("".join((set(message))) == "0") or (int(message) > 12):
            if not message.isdigit():
                return "죄송해요. 이번엔 숫자만 입력해 주시겠어요?"
            elif ("".join((set(message))) == "0") or (int(message) > 12):
                return "월 단위니까 1~12 사이의 숫자를 입력해 주시겠어요?"
        else:
            info_chat.month = int(message)
            info_chat.count += 1
            return info_chat.chat_periods()
    # 4번째 - 랜덤 질문(1개)
    elif info_chat.count == 3:
        if (not message.isdigit()) or ("".join((set(message))) == "0"):
            if not message.isdigit():
                return "죄송해요. 이번에도 숫자만 입력해 주시겠어요?"
            elif "".join((set(message))) == "0":
                return "0을 제외한 숫자를 입력해 주세요."
        else:
            info_chat.itinerary = int(message)
            info_chat.count += 1
            return info_chat.chat_random_questions()
    # 5~6번째 - 랜덤 질문(2개)
    elif 3 < info_chat.count < 3 + info_chat.num_of_questions:
        info_chat.count += 1
        info_chat.user_inputs += message + " "
        return info_chat.chat_random_questions()
    # 7번째 - 마지막 질문
    elif info_chat.count == 3 + info_chat.num_of_questions:  # 현재 6
        info_chat.count += 1
        info_chat.user_inputs += message + " "
        return info_chat.last_question()
    # 8번째 - 추천 도시 출력
    elif info_chat.count == 4 + info_chat.num_of_questions:
        info_chat.count += 1
        info_chat.user_inputs += message + " "
        # 분류 모델로 추천 도시 추출
        global recommended_city
        recommended_city = clsfier.text_predict(info_chat.user_inputs)[0][0]
        city_information = informer.inform_city(city=recommended_city)
        response = f"""좋아요! 제가 생각한 추천 도시는 {recommended_city}입니다! {recommended_city}에 대해 소개할게요!
        \n\n{city_information}\n\n{recommended_city}행 항공권 정보도 알려드릴게요!"""
        return response
    # 9번째 - 항공권 정보 출력
    elif info_chat.count == 5 + info_chat.num_of_questions:
        info_chat.count += 1
        flight_information = informer.inform_flight(month=info_chat.month, city=recommended_city)
        response = f"{info_chat.month}월 기준 항공권 정보입니다!\n\n{flight_information}\n\n다음으로 숙박 정보도 알려드릴게요!"
        return response
    # 10번째 - 숙박 정보 출력
    elif info_chat.count == 6 + info_chat.num_of_questions:
        info_chat.count += 1
        hotels_information = informer.inform_hotels(month=info_chat.month, itinerary=info_chat.itinerary, city=recommended_city)
        response = f"{info_chat.month}월 {info_chat.itinerary}일 숙박 기준 숙박 정보입니다!\n\n{hotels_information}\n\n마지막으로 관광지도 몇 군데 알려드리고 싶어요!"
        return response
    # 11번째 - 관광지 정보 출력
    elif info_chat.count == 7 + info_chat.num_of_questions:
        info_chat.count += 1
        attractions_information = informer.inform_attractions(month=info_chat.month, city=recommended_city)
        response = f"{attractions_information}\n\n어때요? 여행지 고민이 해결되셨다면 너무 기쁠 것 같아요!"
        return response

gr.ChatInterface(fn=chat_response,
                 title = "MJC Travel Chatbot project",
                 description = "여행지(도시)를 추천해주는 챗봇입니다.",
                 retry_btn=None,
                 undo_btn=None,
                 clear_btn=None,
                 ).launch(share=True)