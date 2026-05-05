"""
shared.py — Shared utilities for M3.Ex1 RAG pipeline
"""

SAMPLE_CORPUS = """
Neural networks are computational models inspired by the structure and function of biological
neural networks in animal brains. A neural network consists of layers of interconnected nodes
called neurons. Each neuron receives input, applies an activation function, and passes output
to the next layer.

The three main types of layers in a feedforward neural network are: the input layer, which
receives raw data; hidden layers, which learn abstract representations; and the output layer,
which produces the final prediction. Deep learning refers to neural networks with many hidden
layers, enabling them to learn hierarchical features.

Training a neural network involves two phases: forward propagation and backpropagation.
During forward propagation, input data flows through the network layer by layer, producing
a prediction. The loss function then measures how far the prediction is from the true label.

Backpropagation computes gradients of the loss with respect to each weight using the chain
rule of calculus. These gradients flow backward through the network, indicating how much each
weight contributed to the error. Gradient descent then updates the weights to minimize the loss.

The learning rate is a hyperparameter that controls how large each weight update is. A learning
rate that is too high causes the model to diverge; one that is too low causes slow convergence.
Adaptive optimizers like Adam and RMSProp adjust the learning rate per parameter automatically.

Activation functions introduce non-linearity into the network. The ReLU (Rectified Linear Unit)
function outputs zero for negative inputs and the identity for positive inputs. Sigmoid and tanh
are older activation functions that suffer from the vanishing gradient problem in deep networks.

The vanishing gradient problem occurs when gradients become extremely small as they propagate
back through many layers, causing early layers to learn very slowly. ReLU mitigates this problem
because its gradient is 1 for positive inputs. Batch normalization also helps by normalizing
activations within each mini-batch during training.

Convolutional Neural Networks (CNNs) are specialized for processing grid-like data such as
images. They use convolutional layers with learned filters that slide across the input, sharing
weights and drastically reducing the number of parameters compared to fully connected layers.
Pooling layers reduce spatial dimensions by summarizing regions of the feature map.

Recurrent Neural Networks (RNNs) process sequential data by maintaining a hidden state that
is updated at each time step. Long Short-Term Memory (LSTM) networks and Gated Recurrent Units
(GRUs) were introduced to address the vanishing gradient problem in vanilla RNNs, enabling
learning of long-term dependencies.

Transformers revolutionized NLP by replacing recurrence with self-attention mechanisms. Each
token in the input attends to every other token, allowing the model to capture long-range
dependencies in parallel. The original transformer uses multi-head attention, positional
encodings, and feed-forward sublayers within each encoder and decoder block.

Transfer learning allows practitioners to adapt a model pre-trained on a large dataset to a
new task with limited labeled data. Fine-tuning updates all or a subset of the pre-trained
weights on the target dataset. Feature extraction freezes the pre-trained layers and trains
only a new classification head.

Regularization techniques prevent overfitting. Dropout randomly sets a fraction of activations
to zero during training, preventing co-adaptation of neurons. L2 regularization adds a penalty
proportional to the squared magnitude of weights to the loss function. Data augmentation
artificially expands the training set by applying random transformations to input samples.

Batch size affects training dynamics. Larger batches provide more stable gradient estimates
but require more memory. Smaller batches introduce noise that can help escape local minima.
Mini-batch gradient descent strikes a balance and is standard practice.

The universal approximation theorem states that a feedforward neural network with a single
hidden layer containing enough neurons can approximate any continuous function on a compact
subset of Euclidean space to any desired degree of accuracy.

Retrieval-Augmented Generation (RAG) is a technique that enhances language models by retrieving
relevant documents from an external knowledge base before generating a response. The retriever
finds the top-k most relevant chunks using vector similarity search. The retrieved chunks are
then concatenated with the user query and passed to the language model as context.

Vector stores are databases optimized for storing and querying dense embedding vectors. They
support approximate nearest-neighbor (ANN) search algorithms such as HNSW (Hierarchical
Navigable Small World) and IVF (Inverted File Index). ChromaDB is an open-source embedding
database that supports persistent storage on disk. Embeddings are computed once and stored;
subsequent queries use the stored vectors without recomputation.

Sentence transformers produce fixed-length dense vector representations of sentences. The
all-MiniLM-L6-v2 model produces 384-dimensional embeddings and is efficient for semantic
similarity tasks. Cosine similarity is commonly used to measure the relevance between a query
embedding and document embeddings in the vector store.
"""


def get_corpus_from_youtube(video_id: str) -> str:
    """Fetch transcript from YouTube. Requires internet and youtube-transcript-api >= 0.6."""
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    return " ".join(seg.text for seg in transcript)


def get_corpus(source: str = "sample") -> str:
    """
    Returns a text corpus.
    source='sample'      -> uses the bundled SAMPLE_CORPUS (works offline)
    source='<youtube_id>'-> fetches YouTube transcript (requires internet)
    """
    if source == "sample":
        print("  Using bundled sample corpus.")
        return SAMPLE_CORPUS.strip()
    else:
        print(f"  Fetching YouTube transcript for video: {source}")
        return get_corpus_from_youtube(source)


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    """Split text into overlapping character-level chunks."""
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if len(c) > 30]
