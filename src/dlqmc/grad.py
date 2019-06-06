import torch


def grad(xs, f, create_graph=False):
    xs = xs if xs.requires_grad else xs.detach().requires_grad_()
    ys = f(xs)
    grad_ys, = torch.autograd.grad(
        ys, xs, torch.ones_like(ys), create_graph=create_graph
    )
    if not create_graph:
        ys.detach_()
    return grad_ys, ys


def laplacian(xs, f, create_graph=False):
    xis = [xi.requires_grad_() for xi in xs.flatten(start_dim=1).t()]
    xs_flat = torch.stack(xis, dim=1)
    ys = f(xs_flat.view_as(xs))
    ones = torch.ones_like(ys)
    dy_dxs, = torch.autograd.grad(ys, xs_flat, ones, create_graph=True)
    lap_ys = sum(
        torch.autograd.grad(
            dy_dxi, xi, ones, retain_graph=True, create_graph=create_graph
        )[0]
        for xi, dy_dxi in zip(xis, (dy_dxs[..., i] for i in range(len(xis))))
    )
    return lap_ys, ys
