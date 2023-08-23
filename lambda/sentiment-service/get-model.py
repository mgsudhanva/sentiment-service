from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = AutoModelForSequenceClassification.from_pretrained(model)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)

def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)

get_tokenizer("cambridgeltl/sst_mobilebert-uncased")
get_model("cambridgeltl/sst_mobilebert-uncased")