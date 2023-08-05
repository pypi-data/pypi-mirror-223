import numpy as np 
from tensor import Tensor
from graph import draw_dot
from micrograd.engine import Value
import torch


# class Linear:
#     def __init__(self, in_features: int, out_features: int, bias: bool = True):
#         self.weight = Tensor.normal(0, 1, (out_features, in_features))
#         self.bias = Tensor.normal(0, 1, (out_features,)) if bias else None
    
#     def __call__(self, x: Tensor) -> Tensor:
#         out = x @ self.weight.T  # Matrix multiplication
#         if self.bias is not None:
#             out += self.bias
#         return out


# a = Tensor.ones((2,3), requires_grad=True)
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = a @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)

# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = torch.ones((2,3), requires_grad=True)
# b = torch.full((3,2), 3., requires_grad=True)
# c = a @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)


# a = Tensor.ones((3,2), requires_grad=True)
# aa = a.reshape((2,3))
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)
# print(aa.grad)
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = torch.ones((3,2), requires_grad=True)
# aa = a.view((2,3))
# b = torch.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)

# a = Tensor.ones((3,3), requires_grad=True)
# aa = a[0:2]
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)
# print(a.grad)
# print(b.grad)

# a = torch.ones((3,3), requires_grad=True)
# aa = a[0:2]
# b = torch.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)

# a = Tensor.eye(3, requires_grad=True)
# b = Tensor.full((3,3), 3., requires_grad=True)
# c = a @ b
# d = c.mean(axis=0, keepdim=True)
# e = Tensor.full((1,3), 4., requires_grad=True)
# f = d * e
# loss = f.sum()
# loss.backward()
# res_robin_1 = a.grad.tolist()
# print(res_robin_1)
# # torch 
# a = torch.eye(3, requires_grad=True)
# b = torch.full((3,3), 3., requires_grad=True)
# c = a @ b
# d = c.mean(axis=0, keepdim=True)
# e = torch.full((1,3), 4., requires_grad=True)
# f = d * e
# loss = f.sum()
# loss.backward()
# res_torch_1 = a.grad.numpy().tolist()
# print(res_torch_1)

# a = Tensor.full((5,1), 3., requires_grad=True)
# b = Tensor.full((1,1), 2., requires_grad=True)
# c = a + b
# loss = c.mean()
# try:
#     loss.backward()
#     print(loss.grad)
#     print(c.grad)
#     print(a.grad)
#     print(b.grad)
#     draw_dot(loss, filename="img/graph_inspect", inspect=True)
# except Exception as e:
#     print(e)

# print("\n")
# print("- TORCH -")
# a = torch.full((5,1), 3., requires_grad=True)
# b = torch.full((1,1), 2., requires_grad=True)
# c = a + b
# loss = c.mean()
# try:
#     loss.backward()
#     print("torch win")
#     print(a.grad)
#     print(b.grad)
# except Exception as e:
#     print(e)



# a = Tensor.full((5,1), 3., requires_grad=True)
# b = Tensor.ones((1,), requires_grad=True)
# c = b + a
# print(c.shape)
# loss = c.sum()
# try:
#     loss.backward()
# except Exception as e:
#     print(e)
# print(a.grad)
# print(a.shape, a.grad.shape)
# print(b.grad)
# print(b.shape, b.grad.shape)

# print('\nTORCH')
# a = torch.full((5,1), 3., requires_grad=True)
# b = torch.ones((1,), requires_grad=True)
# c = b + a
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(a.shape, a.grad.shape)
# print(b.grad)
# print(b.shape, b.grad.shape)



# a = Tensor.full((5,1), 3., requires_grad=True)
# b = Tensor.ones((1,), requires_grad=True)
# c = a * b
# loss = c.sum()
# try:
#     loss.backward()
# except Exception as e:
#     print(e)
# print(a.grad)
# # print(a.shape, a.grad.shape)
# print(b.grad)
# # print(b.shape, b.grad.shape)

# print('\nTORCH')
# a = torch.full((5,1), 3., requires_grad=True)
# b = torch.ones((1,), requires_grad=True)
# c = a * b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# # print(a.shape, a.grad.shape)
# print(b.grad)
# # print(b.shape, b.grad.shape)


# print("\nREVERSE\n")

# a = Tensor.full((5,1), 3., requires_grad=True)
# b = Tensor.ones((1,), requires_grad=True)
# c = b * a
# loss = c.sum()
# try:
#     loss.backward()
# except Exception as e:
#     print(e)
# print(a.grad)
# # print(a.shape, a.grad.shape)
# print(b.grad)
# # print(b.shape, b.grad.shape)

# print('\nTORCH')
# a = torch.full((5,1), 3., requires_grad=True)
# b = torch.ones((1,), requires_grad=True)
# c = b * a
# loss = c.sum()
# loss.backward()
# print(a.grad)
# # print(a.shape, a.grad.shape)
# print(b.grad)
# # print(b.shape, b.grad.shape)

# a = Value(-4.0)
# b = Value(2.0)
# c = a + b
# d = a * b + b**3
# c += c + 1
# c += 1 + c + (-a)
# d += d * 2 + (b + a).relu()
# d += 3 * d + (b - a).relu()
# e = c - d
# f = e**2
# g = f / 2.0
# g += 10.0 / f
# print(f'{g.data:.4f}') # prints 24.7041, the outcome of this forward pass
# g.backward()
# print(f'{a.grad:.4f}') # prints 138.8338, i.e. the numerical value of dg/da
# print(f'{b.grad:.4f}') # prints 645.5773, i.e. the numerical value of dg/db

# print("\nrobin\n")
# a = Tensor(-4.0, requires_grad=True)
# b = Tensor(2.0, requires_grad=True)
# c = a + b
# d = a * b + b**3
# c += c + 1
# c += 1 + c + (-a)
# d += d * 2 + (b + a).relu()
# d += 3 * d + (b - a).relu()
# e = c - d
# f = e**2
# g = f / 2.0
# g += 10.0 / f
# print(f'{g.data:.4f}') # prints 24.7041, the outcome of this forward pass
# g.backward()
# print(f'{a.grad:.4f}') # prints 138.8338, i.e. the numerical value of dg/da
# print(f'{b.grad:.4f}') # prints 645.5773, i.e. the numerical value of dg/db



a = Tensor.full((5,1), 3., requires_grad=True)
b = Tensor.ones((1,1), requires_grad=True)
c = b * a
loss = c.sum()
try:
    loss.backward()
except Exception as e:
    print(e)
print(a.grad)
print(b.grad)

a = torch.full((5,1), 3., requires_grad=True)
b = torch.ones((1,1), requires_grad=True)
c = b * a
loss = c.sum()
loss.backward()
print(a.grad)
print(b.grad)
print(c.grad)
# res_torch_1 = a.grad.numpy().tolist()
# res_torch_2 = b.grad.numpy().tolist()

# print(res_robin_1)
# print(res_robin_2)
# print('\nTORCH')
# print(res_torch_1)
# print(res_torch_2)
