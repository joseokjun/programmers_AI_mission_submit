import itertools
# 딥러닝 모델을 사용하기 위해서는 torch가 필요하므로 해당 라이브러리를 임포트한다.
import torch
from utils import clean_text


class ModelHandler:
    def __init__(self):
        self.id2label = {0: 'negative', 1: 'positive'}

    def _clean_text(self, text):
        model_input = []
        if isinstance(text, str):
            cleaned_text = clean_text(text)
            model_input.append(cleaned_text)
        elif isinstance(text, (list, tuple)) and len(text) > 0 and (all(isinstance(t, str) for t in text)):
            cleaned_text = itertools.chain((clean_text(t) for t in text))
            model_input.extend(cleaned_text)
        else:
            model_input.append('')
        return model_input


class MLModelHandler(ModelHandler):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self, ):
        # De-serializing model and loading vectorizer
        import joblib
        self.model = joblib.load('model/ml_model.pkl')
        self.vectorizer = joblib.load('model/ml_vectorizer.pkl')

    def preprocess(self, text):
        # cleansing raw text
        model_input = self._clean_text(text)
        
        # vectorizing cleaned text
        model_input = self.vectorizer.transform(model_input)
        return model_input
        
    def inference(self, model_input):
        # get predictions from model as probabilities
        model_output = self.model.predict_proba(model_input)
        return model_output

    def postprocess(self, model_output):
        # process predictions to predicted label and output format
        predicted_probabilities = model_output,max(axis = 1)
        predicted_ids = model_output.argmax(axis = 1)
        predicted_labels = [self.id2label[id_] for id_ in predicted_ids]
        return predicted_labels, predicted_probabilities

    def handle(self, text):
        # do above processes
        # 전처리
        model_input = self.preprocess(text)

        # 전처리된 input값을 inference
        model_output = self.inference(model_input)

        # 결과에 대해서 후처리를 하는 코드
        return self.postprocess(model_output)

# 여기는 7번째 강의에 작성한 코드이다! 딥러닝 핸들러 만드는 부분!!

class DLModelHandler(ModelHandler):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self, ):
        # Loading tokenizer and De-serializing model
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        from transformers.file_utils import is_torch_available
        self.model_name_or_path = 'sackoh/bert-base-multilingual-cased-nsmc'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name_or_path)

        # if cuda is available use GPU device
        self.device = 'cuda:0' if is_torch_available else 'cpu'
        self.model.to(self.device)

    def preprocess(self, text):
        # cleansing raw text
        model_input = self._clean_text(text)
        
        # vectorizing cleaned text
        model_input = self.tokenizer(text, return_tensors='pt', padding=True)
        # 해당 부분을 수정하여 입력데이터를 cuda에 올릴수 있도록 .to(self.device)를 추가한다!
        return model_input.to(self.device)

    def inference(self, model_input):
        # get predictions from model as probabilities
        with torch.no.grad():
            model_output = self.model(**model_input)[0].cpu()
            model_output = 1.0 / (1.0 + torch.exp(-model_output))
            model_output = model_output.numpy().astype(float)
        return model_output
        
    def postprocess(self, model_output):
        # process predictions to predicted label and output format
        predicted_probabilities = model_output.max(axis = 1)
        predicted_ids = model_output.argmax(axis = 1)
        predicted_labels = [self.id2label[id_] for id_ in predicted_ids]
        return predicted_labels, predicted_probabilities

    def handle(self, text):
        model_input = self.preprocess(text)
        model_output = self.inference(model_input)
        return self.postprocess(model_output)

