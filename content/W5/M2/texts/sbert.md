## Sentence Transformers

Use [`sentence_transformers`](https://www.sbert.net/) specifically for state-of-the-art **embedding** and **reranker** models; used for semantic search, clustering, and classification.

- [NAMAA-Space/AraModernBert-Base-V1.0](https://huggingface.co/NAMAA-Space/AraModernBert-Base-V1.0)
- [GATE-Reranker-V1](https://huggingface.co/NAMAA-Space/GATE-Reranker-V1)

## Semantic Textual Similarity (STS)

**Semantic Textual Similarity (STS)** measures how closely two sentences match in meaning, regardless of the exact words used.
[Semantic Textual Similarity (STS)](https://sbert.net/examples/sentence_transformer/training/sts/README.html) assigns a score between 0 and 1 on the similarity of two texts. Here are exampels from the [STSB Dataset](https://huggingface.co/datasets/sentence-transformers/stsb):

| Sentence A | Sentence B | Score |
| --- | --- | --- |
| A plane is taking off. | An air plane is taking off. | 1 |
| A man is playing a large flute. | A man is playing a flute. | 0.76 |
| A man is spreading shreded cheese on a pizza. | A man is spreading shredded cheese on an uncooked pizza. | 0.76 |
| Three men are playing chess. | Two men are playing chess. | 0.52 |
| A man is playing the cello. | A man seated is playing the cello. | 0.85 |
| Some men are fighting. | Two men are fighting. | 0.85 |
| A man is smoking. | A man is skating. | 0.1 |
| The man is playing the piano. | The man is playing the guitar. | 0.32 |
| A man is playing on a guitar and singing. | A woman is playing an acoustic guitar and singing. | 0.44 |
| A person is throwing a cat on to the ceiling. | A person throws a cat on the ceiling. | 1 |
| The man hit the other man with a stick. | The man spanked the other man with a stick. | 0.84 |


## Natural Language Inference (NLI)

Given two sentence (premise and hypothesis), Natural Language Inference (NLI) is the task of deciding if the premise entails the hypothesis, if they are contradiction or if they are neutral.

- **Entailment**: Hypothesis is definitely true given the premise.
- **Contradiction**: Hypothesis is definitely false given the premise.
- **Neutral**: Hypothesis may or may not be true given the premise.


### NLI: General Knowledge

Commonly used NLI dataset are [SNLI](https://huggingface.co/datasets/stanfordnlp/snli) and [MultiNLI](https://huggingface.co/datasets/nyu-mll/multi_nli) for general knowledge:

| Premise | Hypothesis | Label |
| --- | --- | --- |
| Children smiling and waving at camera | They are smiling at their parents | neutral |
| Children smiling and waving at camera | There are children present | entailment |
| Children smiling and waving at camera | The kids are frowning | contradiction |


### MedNLI: Medical Knowledge

[MedNLI](https://jgc128.github.io/mednli/) dataset for medical knowledge:

| Premise | Hypothesis | Label |
| --- | --- | --- |
| Labs were notable for Cr 1.7 (baseline 0.5 per old records) and lactate 2.4. | Patient has elevated Cr | entailment |
| Labs were notable for Cr 1.7 (baseline 0.5 per old records) and lactate 2.4. | Patient has normal Cr | contradiction |
| Labs were notable for Cr 1.7 (baseline 0.5 per old records) and lactate 2.4. | Patient has elevated BUN | neutral |


### Email Application

[Email Intent Classification Dataset](https://huggingface.co/datasets/aadilsayad/email-intent-classification):

| Premise | Hypothesis | Label |
| --- | --- | --- |
| Can I send an email, please? | send | send |
| I'd like to compose an email. | send | send |
| I need to send an email. | send | send |
| Could you help me write an email? | send | send |
| Is it possible to send an email with you? | send | send |
| Show me all my emails. | list | list |
| Can you list my emails, please? | list | list |
| Open my inbox. | list | list |
| I want to see all my mail. | list | list |
| Display my email messages. | list | list |
| Delete this email, please. | trash | trash |
| Can you get rid of this email? | trash | trash |
| I want to remove this email. | trash | trash |
| Please erase this email. | trash | trash |
| Time to delete this one. | trash | trash |


### Sales Application

| Premise | Hypothesis | Label |
| --- | --- | --- |
| "Hello, I want to get me a Laptop how much does it cost?" | "BUY Laptop" | "BUY Laptop" |
| "I am very frustrated with your service, and I wanna cancel right now!" | "CANCEL Subscription" | "CANCEL Subscription" |
| "Here I bought this Keyboard, but it is not working. I want to get my money back!" | "REFUND Transaction" | "REFUND Transaction" |
