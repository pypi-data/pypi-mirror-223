from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoModelForCausalLM, DataCollatorForLanguageModeling, \
    LineByLineTextDataset, TrainingArguments, Trainer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification, \
    AutoModelForNextSentencePrediction, AutoModelForTokenClassification, AutoModelForQuestionAnswering
from huggingface_hub import login
from aityz import exceptions
import os
import logging
import torch


class NLP:
    def __init__(self, task, modelName=None):
        super().__init__()
        if task == 'CLM':
            if modelName is None:
                self.model = AutoModelForCausalLM.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForCausalLM.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'MLM':
            if modelName is None:
                self.model = AutoModelForMaskedLM.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForMaskedLM.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'QA':
            if modelName is None:
                self.model = AutoModelForQuestionAnswering.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForQuestionAnswering.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'TokenClassification':
            if modelName is None:
                self.model = AutoModelForTokenClassification.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForTokenClassification.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'SequenceClassification':
            if modelName is None:
                self.model = AutoModelForSequenceClassification.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForSequenceClassification.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'SentencePrediction':
            if modelName is None:
                self.model = AutoModelForNextSentencePrediction.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForNextSentencePrediction.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        elif task == 'S2S':
            if modelName is None:
                self.model = AutoModelForSeq2SeqLM.from_pretrained('distilgpt2')
                self.tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
            else:
                try:
                    self.model = AutoModelForSeq2SeqLM.from_pretrained(modelName)
                    self.tokenizer = AutoTokenizer.from_pretrained(modelName)
                except Exception as e:
                    print('Unknown Model!')
                    raise exceptions.InitialisationError()
        else:
            raise exceptions.InitialisationError()
        self.task = task

    def inference(self, inputs, context=None, maxTokens=100, doSample=True, topK=50, topP=0.95):
        if self.task == 'CLM':
            inputs = self.tokenizer(inputs, return_tensors="pt").input_ids
            outputs = self.model.generate(inputs, max_new_tokens=maxTokens, do_sample=doSample, top_k=topK, top_p=topP)
            output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            return ''.join(output)
        elif self.task == 'MLM':
            text = inputs
            inputs = self.tokenizer(inputs, return_tensors="pt")
            mask_token_index = torch.where(inputs["input_ids"] == self.tokenizer.mask_token_id)[1]
            logits = self.model(**inputs).logits
            mask_token_logits = logits[0, mask_token_index, :]
            top_3_tokens = torch.topk(mask_token_logits, 3, dim=1).indices[0].tolist()
            return text.replace(self.tokenizer.mask_token, self.tokenizer.decode(top_3_tokens[0]))
        elif self.task == 'QA':
            if context is None:
                logging.warning('Question Answering Inference Requires Context!')
                return
            else:
                inputs = self.tokenizer(inputs, context, return_tensors="pt")
                with torch.inference_mode():
                    outputs = self.model(**inputs)
                answer_start_index = outputs.start_logits.argmax()
                answer_end_index = outputs.end_logits.argmax()
                predict_answer_tokens = inputs.input_ids[0, answer_start_index: answer_end_index + 1]
                return self.tokenizer.decode(predict_answer_tokens)
        elif self.task == 'S2S':
            return
        else:
            return


def GPT2LineByLine(token: str, filepath, evalFilePath, blockSize, modelName, epochs=3):
    login(token)
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    model = AutoModelForCausalLM.from_pretrained('gpt2')
    if os.path.exists(filepath):
        dataset = LineByLineTextDataset(
            tokenizer=tokenizer,
            file_path=filepath,
            block_size=blockSize
        )
        if os.path.exists(evalFilePath):
            evalDataset = LineByLineTextDataset(
                tokenizer=tokenizer,
                file_path=evalFilePath,
                block_size=blockSize
            )
        else:
            raise exceptions.InitialisationError()
    else:
        raise exceptions.InitialisationError()

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    tokenizer.pad_token = tokenizer.eos_token
    training_args = TrainingArguments(
        output_dir=modelName,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        push_to_hub=True,
        num_train_epochs=epochs
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=evalDataset,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.push_to_hub()
    return model, tokenizer


def CasualInference(inputs, model, tokenizer, maxTokens=100, doSample=True, topK=50, topP=0.95):
    inputs = tokenizer(inputs, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=maxTokens, do_sample=doSample, top_k=topK, top_p=topP)
    output = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ''.join(output)


def CLM(modelName):
    model = AutoModelForCausalLM.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def MLM(modelName):
    model = AutoModelForMaskedLM.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def S2S(modelName):
    model = AutoModelForSeq2SeqLM.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def SequenceClassification(modelName):
    model = AutoModelForSequenceClassification(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def SentencePrediction(modelName):
    model = AutoModelForNextSentencePrediction.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def TokenClassification(modelName):
    model = AutoModelForTokenClassification.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer


def QA(modelName):
    model = AutoModelForQuestionAnswering.from_pretrained(modelName)
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    return model, tokenizer
