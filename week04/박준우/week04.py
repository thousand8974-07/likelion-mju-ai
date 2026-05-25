import torch
import torch.nn as nn

torch.manual_seed(123)

inputs = torch.tensor([
    [0.43, 0.15, 0.89],
    [0.55, 0.87, 0.66],
    [0.57, 0.85, 0.64],
    [0.22, 0.58, 0.33],
    [0.77, 0.25, 0.10],
    [0.05, 0.80, 0.55],
])

tokens = ["Your", "journey", "starts", "with", "one", "step"]
print("inputs.shape:", inputs.shape)


# Part 1. Dot Product Attention
def get_attention_scores(inputs, query_index):
    query = inputs[query_index]
    attn_scores = torch.zeros(inputs.shape[0])
    for i, x_i in enumerate(inputs):
        attn_scores[i] = torch.dot(x_i, query)
    return attn_scores

scores = get_attention_scores(inputs, query_index=1)
print(scores)

expected_scores = torch.tensor([0.9544, 1.4950, 1.4754, 0.8434, 0.7070, 1.0865])
assert scores.shape == torch.Size([6])
assert torch.allclose(scores, expected_scores, atol=1e-4)
print("Part 1 통과")


# Part 2. Attention Weight와 Context Vector
def get_context_vector(inputs, query_index):
    attn_scores = get_attention_scores(inputs, query_index)
    attn_weights = torch.softmax(attn_scores, dim=0)
    context_vec = torch.zeros(inputs.shape[1])
    for i, x_i in enumerate(inputs):
        context_vec += attn_weights[i] * x_i
    return context_vec, attn_weights

context_vec, attn_weights = get_context_vector(inputs, query_index=1)
print("attention weights:", attn_weights)
print("sum:", attn_weights.sum())
print("context vector:", context_vec)

assert attn_weights.shape == torch.Size([6])
assert torch.allclose(attn_weights.sum(), torch.tensor(1.0), atol=1e-6)
assert context_vec.shape == torch.Size([3])
expected_context = torch.tensor([0.4419, 0.6515, 0.5683])
assert torch.allclose(context_vec, expected_context, atol=1e-4)
print("Part 2 통과")


# Part 3. 모든 토큰에 대해 Self-Attention 계산
def self_attention_basic(inputs):
    attn_scores = inputs @ inputs.T
    attn_weights = torch.softmax(attn_scores, dim=-1)
    context_vecs = attn_weights @ inputs
    return attn_weights, context_vecs

attn_weights_basic, context_vecs_basic = self_attention_basic(inputs)
print("attn_weights_basic.shape:", attn_weights_basic.shape)
print("context_vecs_basic.shape:", context_vecs_basic.shape)
print("row sums:", attn_weights_basic.sum(dim=-1))

assert attn_weights_basic.shape == torch.Size([6, 6])
assert context_vecs_basic.shape == torch.Size([6, 3])
assert torch.allclose(attn_weights_basic.sum(dim=-1), torch.ones(6), atol=1e-6)
assert torch.allclose(context_vecs_basic[1], torch.tensor([0.4419, 0.6515, 0.5683]), atol=1e-4)
print("Part 3 통과")


# Part 4. Q, K, V를 사용하는 Self-Attention
def self_attention_qkv_manual(inputs, d_out=2):
    torch.manual_seed(123)
    d_in = inputs.shape[1]

    W_query = nn.Parameter(torch.rand(d_in, d_out), requires_grad=False)
    W_key = nn.Parameter(torch.rand(d_in, d_out), requires_grad=False)
    W_value = nn.Parameter(torch.rand(d_in, d_out), requires_grad=False)

    queries = inputs @ W_query
    keys = inputs @ W_key
    values = inputs @ W_value

    attn_scores = queries @ keys.T

    d_k = keys.shape[-1]
    attn_weights = torch.softmax(attn_scores / d_k**0.5, dim=-1)

    context_vecs = attn_weights @ values

    return context_vecs, attn_weights, queries, keys, values

context_vecs_qkv, attn_weights_qkv, queries, keys, values = self_attention_qkv_manual(inputs)
print("queries.shape:", queries.shape)
print("keys.shape:", keys.shape)
print("values.shape:", values.shape)
print("attn_weights_qkv.shape:", attn_weights_qkv.shape)
print("context_vecs_qkv.shape:", context_vecs_qkv.shape)

assert queries.shape == torch.Size([6, 2])
assert keys.shape == torch.Size([6, 2])
assert values.shape == torch.Size([6, 2])
assert attn_weights_qkv.shape == torch.Size([6, 6])
assert context_vecs_qkv.shape == torch.Size([6, 2])
assert torch.allclose(attn_weights_qkv.sum(dim=-1), torch.ones(6), atol=1e-6)
print("Part 4 통과")


# Part 5. SelfAttention 클래스
class SelfAttention(nn.Module):
    def __init__(self, d_in, d_out, qkv_bias=False):
        super().__init__()
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)

    def forward(self, x):
        keys = self.W_key(x)
        queries = self.W_query(x)
        values = self.W_value(x)

        attn_scores = queries @ keys.T

        d_k = keys.shape[-1]
        attn_weights = torch.softmax(attn_scores / d_k**0.5, dim=-1)

        context_vecs = attn_weights @ values
        return context_vecs

torch.manual_seed(789)
sa = SelfAttention(d_in=3, d_out=2)
out_sa = sa(inputs)
print(out_sa)
print(out_sa.shape)

assert out_sa.shape == torch.Size([6, 2])
print("Part 5 통과")


# Part 6. Causal Mask 적용
def apply_causal_mask(attn_scores):
    context_length = attn_scores.shape[0]
    # 대각선 위쪽(미래 위치)을 True로 만드는 마스크
    mask = torch.triu(torch.ones(context_length, context_length), diagonal=1).bool()
    masked_scores = attn_scores.masked_fill(mask, float('-inf'))
    return masked_scores

attn_scores_qkv = queries @ keys.T
masked_scores = apply_causal_mask(attn_scores_qkv)
masked_weights = torch.softmax(masked_scores / keys.shape[-1]**0.5, dim=-1)
print(masked_weights)
print("row sums:", masked_weights.sum(dim=-1))

assert masked_weights.shape == torch.Size([6, 6])
assert torch.allclose(masked_weights.sum(dim=-1), torch.ones(6), atol=1e-6)
assert torch.all(masked_weights[0, 1:] == 0)
assert torch.all(masked_weights[1, 2:] == 0)
assert torch.all(masked_weights[2, 3:] == 0)
print("Part 6 통과")


# Part 7. Attention Dropout
def apply_attention_dropout(attn_weights, dropout_rate=0.5):
    torch.manual_seed(123)
    dropout = nn.Dropout(dropout_rate)
    dropped_weights = dropout(attn_weights)
    return dropped_weights

for p in [0.0, 0.1, 0.5]:
    dropped = apply_attention_dropout(masked_weights, dropout_rate=p)
    print(f"dropout={p}")
    print(dropped)

assert apply_attention_dropout(masked_weights, 0.0).shape == masked_weights.shape
print("Part 7 통과")


# Part 8. CausalAttention 클래스
class CausalAttention(nn.Module):
    def __init__(self, d_in, d_out, context_length, dropout, qkv_bias=False):
        super().__init__()
        self.d_out = d_out
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer("mask", torch.triu(torch.ones(context_length, context_length), diagonal=1))

    def forward(self, x):
        b, num_tokens, d_in = x.shape

        keys = self.W_key(x)
        queries = self.W_query(x)
        values = self.W_value(x)

        attn_scores = queries @ keys.transpose(1, 2)

        # 현재 시퀀스 길이에 맞게 mask 슬라이싱
        attn_scores = attn_scores.masked_fill(
            self.mask.bool()[:num_tokens, :num_tokens], float('-inf')
        )

        attn_weights = torch.softmax(attn_scores / keys.shape[-1]**0.5, dim=-1)

        attn_weights = self.dropout(attn_weights)

        context_vecs = attn_weights @ values
        return context_vecs

batch = torch.stack((inputs, inputs), dim=0)
torch.manual_seed(123)
ca = CausalAttention(d_in=3, d_out=2, context_length=batch.shape[1], dropout=0.0)
context_vecs_ca = ca(batch)
print(context_vecs_ca)
print(context_vecs_ca.shape)

assert context_vecs_ca.shape == torch.Size([2, 6, 2])
print("Part 8 통과")


# Part 9. MultiHeadAttentionWrapper
class MultiHeadAttentionWrapper(nn.Module):
    def __init__(self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False):
        super().__init__()
        self.heads = nn.ModuleList([
            CausalAttention(d_in, d_out, context_length, dropout, qkv_bias)
            for _ in range(num_heads)
        ])

    def forward(self, x):
        return torch.cat([head(x) for head in self.heads], dim=-1)

torch.manual_seed(123)
mha_wrapper = MultiHeadAttentionWrapper(d_in=3, d_out=2, context_length=6, dropout=0.0, num_heads=2)
context_vecs_mha_wrapper = mha_wrapper(batch)
print(context_vecs_mha_wrapper)
print(context_vecs_mha_wrapper.shape)

assert context_vecs_mha_wrapper.shape == torch.Size([2, 6, 4])
print("Part 9 통과")


# Part 10. 효율적인 MultiHeadAttention
class MultiHeadAttention(nn.Module):
    def __init__(self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False):
        super().__init__()
        assert d_out % num_heads == 0, "d_out은 num_heads로 나누어 떨어져야 합니다."
        self.d_out = d_out
        self.num_heads = num_heads
        self.head_dim = d_out // num_heads
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.out_proj = nn.Linear(d_out, d_out)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer("mask", torch.triu(torch.ones(context_length, context_length), diagonal=1))

    def forward(self, x):
        b, num_tokens, d_in = x.shape

        # [b, num_tokens, d_out]
        keys = self.W_key(x)
        queries = self.W_query(x)
        values = self.W_value(x)

        # [b, num_tokens, num_heads, head_dim]
        keys = keys.view(b, num_tokens, self.num_heads, self.head_dim)
        queries = queries.view(b, num_tokens, self.num_heads, self.head_dim)
        values = values.view(b, num_tokens, self.num_heads, self.head_dim)

        # [b, num_heads, num_tokens, head_dim]
        keys = keys.transpose(1, 2)
        queries = queries.transpose(1, 2)
        values = values.transpose(1, 2)

        # [b, num_heads, num_tokens, num_tokens]
        attn_scores = queries @ keys.transpose(2, 3)

        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]
        attn_scores = attn_scores.masked_fill(mask_bool, float('-inf'))

        attn_weights = torch.softmax(attn_scores / self.head_dim**0.5, dim=-1)
        attn_weights = self.dropout(attn_weights)

        # [b, num_heads, num_tokens, head_dim] -> [b, num_tokens, d_out]
        context_vec = (attn_weights @ values).transpose(1, 2)
        context_vec = context_vec.contiguous().view(b, num_tokens, self.d_out)

        context_vec = self.out_proj(context_vec)
        return context_vec

torch.manual_seed(123)
mha = MultiHeadAttention(d_in=3, d_out=4, context_length=6, dropout=0.0, num_heads=2)
context_vecs_mha = mha(batch)
print(context_vecs_mha)
print(context_vecs_mha.shape)

assert context_vecs_mha.shape == torch.Size([2, 6, 4])
print("Part 10 통과")


# 최종 과제: Tiny GPT Attention Block
print("\n=== 최종 과제 ===")

x = torch.randn(4, 8, 16)

model = MultiHeadAttention(
    d_in=16,
    d_out=16,
    context_length=8,
    dropout=0.1,
    num_heads=4
)

out = model(x)
print(out.shape)
assert out.shape == torch.Size([4, 8, 16])
print("최종 과제 기본 실행 통과")

# dropout=0.0 vs dropout=0.1 비교
print("\n--- dropout 비교 ---")
torch.manual_seed(0)
x_test = torch.randn(2, 6, 16)

model_no_drop = MultiHeadAttention(d_in=16, d_out=16, context_length=6, dropout=0.0, num_heads=2)
model_no_drop.eval()
out_no_drop = model_no_drop(x_test)

model_drop = MultiHeadAttention(d_in=16, d_out=16, context_length=6, dropout=0.1, num_heads=2)
model_drop.train()
out_drop = model_drop(x_test)

print(f"dropout=0.0 출력 shape: {out_no_drop.shape}")
print(f"dropout=0.1 출력 shape: {out_drop.shape}")

# num_heads 비교
print("\n--- num_heads 비교 ---")
for num_heads in [1, 2, 4]:
    model_h = MultiHeadAttention(d_in=16, d_out=16, context_length=8, dropout=0.0, num_heads=num_heads)
    out_h = model_h(torch.randn(4, 8, 16))
    print(f"num_heads={num_heads}, 출력 shape: {out_h.shape}")

"""
[Q/K/V, Causal Mask, Multi-Head Attention 설명]

Q(Query), K(Key), V(Value):
  입력 벡터를 세 가지 역할로 분리하는 개념입니다.
  Query는 "지금 내가 무엇을 찾고 있나?", Key는 "나는 어떤 정보를 가지고 있나?",
  Value는 "실제로 전달할 정보"입니다.
  Query와 Key의 내적으로 유사도(attention score)를 계산하고,
  softmax를 거친 weight로 Value를 가중합해 context vector를 만듭니다.

Causal Mask:
  GPT처럼 텍스트를 왼쪽에서 오른쪽으로 생성하는 모델에서,
  현재 토큰이 미래 토큰을 참조하면 안 됩니다.
  상삼각 행렬 마스크로 미래 위치의 attention score를 -inf로 만들면,
  softmax 후 해당 위치의 weight가 0이 되어 미래 정보를 차단할 수 있습니다.

Multi-Head Attention:
  attention을 여러 개의 head로 나눠 병렬로 수행합니다.
  각 head가 서로 다른 관점(위치 관계, 의미 유사도 등)에 집중할 수 있어
  단일 attention보다 풍부한 표현을 학습합니다.
  head별 출력을 concat한 뒤 projection으로 최종 출력을 만듭니다.
"""
