from transformers import AutoTokenizer, AutoModelForSequenceClassification
from konlpy.tag import Okt
import torch
import pandas as pd
import re

class CitiesExtractor:
    def __init__(self):
        self.cities = ['다낭', '호치민', '하노이', '나트랑', '달랏', '코타키나발루', '쿠알라룸푸르', '시엠립', '프놈펜',
       '싱가포르', '홍콩', '마카오', '발리', '자카르타', '보라카이', '보홀', '세부', '타이페이',
       '가오슝', '타이중', '파타야', '방콕', '치앙마이', '크라비', '푸켓', '코사무이', '도쿄',
       '요코하마', '교토', '오사카', '나라', '고베', '나고야', '후쿠오카', '나가사키', '삿포로',
       '하코다테', '오키나와']
        self.cities_to_labels = {city: idx for idx, city in enumerate(self.cities)}
        self.labels_to_cities = {idx: city for city, idx in self.cities_to_labels.items()}
        self.model_name = "INo0121/travel-cities-extractor_tf-idf128"
        self.device = torch.device('cuda' if torch.cuda.is_available else 'cpu')
        self.clsfier = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.okt = Okt()
    
    # 전처리 함수 선언
    def text_preprocessing(self, text):
        # 한글과 공백을 제외한 나머지를 제거
        text = re.sub("[^0-9ㄱ-ㅎㅏ-ㅣ가-힣 ]"," ", text)
        return text

    # 텍스트로부터 명사와 형용사, 동사만 추출하여 반환하는 함수 선언
    def extract_noun_adj(self, text):
        processed_text = self.okt.pos(text, stem=True)
        word_list = [word[0] for word in processed_text if (word[1] == 'Noun' or word[1] == 'Adjective' or word[1] == 'Verb') and len(word[0]) >= 2]
        word_list = " ".join(word_list)
        return word_list

    # 예측 함수 선언
    def text_predict(self, text):
        # 모델을 평가 모드로 변경
        self.clsfier.eval()

        # 입력된 문장에 대하여 전처리 및 토크나이징
        preprocessed = self.text_preprocessing(text)
        extracted = self.extract_noun_adj(preprocessed)

        tokenized = self.tokenizer(
            extracted,
            return_tensors="pt",
            max_length=256,
            padding=True,
            truncation=True,
            add_special_tokens=True,
        )

        tokenized.to(self.device)

        # 예측
        with torch.no_grad():
            outputs = self.clsfier(
                input_ids = tokenized["input_ids"],
                attention_mask = tokenized["attention_mask"],
                token_type_ids = tokenized["token_type_ids"]
                )

        # 결과 반환
        logits = outputs.logits
        sigmoid = torch.nn.Sigmoid()
        preds = sigmoid(logits.squeeze())
        results = {}

        for id, label in self.labels_to_cities.items():
            prob = preds[id].item()
            results[label] = prob

        results = pd.DataFrame(results, index=[0]).T.sort_values(0, ascending=False)
        results = [i for i in zip(results[0][:3].index, results[0][:3].values)]

        return results