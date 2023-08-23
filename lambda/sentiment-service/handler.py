from transformers import MobileBertForSequenceClassification, AutoTokenizer, AutoConfig
import torch
import json

predict_map = {
    0: 'negative',
    1: 'neutral',
    2: 'positive'
}

def serverless_pipeline(model_path='./model'):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    config = AutoConfig.from_pretrained(model_path)
    model = MobileBertForSequenceClassification.from_pretrained(model_path, config=config)
    model.eval()
    
    def predict(batch_sentences):
        
        inputs = tokenizer(batch_sentences, max_length=256, truncation=True, padding=True, return_tensors='pt')
        input_ids, attention_mask = inputs.input_ids, inputs.attention_mask

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim = -1)
        
        return predict_map[predictions[0].item()]
    return predict

pipeline = serverless_pipeline()

def handler(event, context):
    try:
        body = json.loads(event['body'])
        
        sentiment = pipeline(batch_sentences=[body['text']])
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True

            },
            "body": json.dumps({'sentiment': sentiment})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }    
    